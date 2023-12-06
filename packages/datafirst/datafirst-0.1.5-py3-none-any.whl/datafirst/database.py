import sqlite3
from pathlib import Path

from datafirst.models.database import (
    Advisor,
    Award,
    Project,
    School,
    SkillOrSoftware,
    Student,
    Topic,
)


class Database:
    def __init__(self, database_file: Path):
        self.database_file = database_file
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    # Advisor Queries
    def get_advisor_by_id(self, advisor_id: str) -> Advisor:
        self.cursor.execute(
            """SELECT advisor.id, advisor.name, email, organization, is_formerly_primary_school, school.id, school.name, school.url  FROM advisor
            LEFT JOIN school ON advisor.primary_school_id = school.id
            WHERE advisor.id = ?;""",
            (advisor_id,),
        )
        row = self.cursor.fetchone()
        if row is None:
            raise Exception(f"Advisor with id {advisor_id} not found")
        semester_participated = self.get_semesters_participed_by_advisor(advisor_id)
        semester_participated_as_chair = (
            self.get_semesters_participed_by_advisor_as_chair(advisor_id)
        )
        if row[5] is None:
            school = None
        else:
            school = School(
                id=row[5],
                name=row[6],
                url=row[7],
            )
        advisor = Advisor(
            id=row[0],
            name=row[1],
            email=row[2],
            organization=row[3],
            is_formerly_primary_school=row[4],
            primary_school=school,
            semesters_participated=semester_participated,
            semesters_participated_as_chair=semester_participated_as_chair,
        )
        return advisor

    def get_advisors_by_project_id(self, project_id: str) -> list[Advisor]:
        advisors: list[Advisor] = []
        self.cursor.execute(
            "SELECT advisor.id FROM advisor WHERE advisor.id IN (SELECT advisor_id FROM project_has_advisor WHERE project_id = ?)",
            (project_id,),
        )
        for row in self.cursor.fetchall():
            advisor = self.get_advisor_by_id(row[0])
            advisors.append(advisor)
        return advisors

    def get_advisors(self) -> list[Advisor]:
        advisors: list[Advisor] = []
        self.cursor.execute("SELECT id FROM advisor")
        for row in self.cursor.fetchall():
            advisor = self.get_advisor_by_id(row[0])
            advisors.append(advisor)
        return advisors

    # Project Queries
    def get_project_by_id(self, project_id: str) -> Project:
        self.cursor.execute("SELECT * FROM project WHERE project.id = ?", (project_id,))
        row = self.cursor.fetchone()
        project = Project(
            id=row[0],
            name=row[1],
            semester=row[2],
            year=row[3],
            project_overview=row[4],
            final_presentation=row[5],
            student_learning=row[6],
            website=row[7],
            advisors=self.get_advisors_by_project_id(project_id),
            awards=self.get_awards_by_project_id(project_id),
            skill_required=self.get_skills_by_project_id(project_id),
            students=self.get_students_by_project_id(project_id),
            topics=self.get_topics_by_project_id(project_id),
        )
        return project

    def get_projects_by_student_id(self, student_id: int) -> list[Project]:
        projects: list[Project] = []
        self.cursor.execute(
            "SELECT project.id FROM project WHERE project.id IN (SELECT project_id FROM project_has_student WHERE student_id = ?)",
            (student_id,),
        )

        for row in self.cursor.fetchall():
            project = self.get_project_by_id(row[0])
            projects.append(project)
        return projects

    def get_projects_by_advisor_id(self, advisor_id: str) -> list[Project]:
        projects: list[Project] = []
        self.cursor.execute(
            "SELECT project.id FROM project WHERE project.id IN (SELECT project_id FROM project_has_advisor WHERE advisor_id = ?)",
            (advisor_id,),
        )

        for row in self.cursor.fetchall():
            project = self.get_project_by_id(row[0])
            projects.append(project)
        return projects

    def get_projects(self) -> list[Project]:
        projects: list[Project] = []
        self.cursor.execute("SELECT project.id FROM project")
        for row in self.cursor.fetchall():
            project = self.get_project_by_id(row[0])
            projects.append(project)
        return projects

    # Students Queries
    def get_student_by_id(self, student_id: str) -> Student:
        self.cursor.execute("SELECT * FROM student WHERE student.id = ?", (student_id,))
        row = self.cursor.fetchone()
        semesters_participated = self.get_semesters_participed_by_student(student_id)
        student = Student(
            id=row[0],
            name=row[1],
            email=row[2],
            degree_program=row[3],
            school=row[4],
            github_username=row[5],
            last_participation=row[6],
            semesters_participated=semesters_participated,
        )
        return student

    def get_students(self) -> list[Student]:
        students: list[Student] = []
        self.cursor.execute("SELECT student.id FROM student")
        for row in self.cursor.fetchall():
            student = self.get_student_by_id(row[0])
            students.append(student)
        return students

    def get_students_by_project_id(self, project_id: str) -> list[Student]:
        students: list[Student] = []
        self.cursor.execute(
            "SELECT * FROM student WHERE student.id IN (SELECT student_id FROM project_has_student WHERE project_id = ?)",
            (project_id,),
        )
        for row in self.cursor.fetchall():
            student = self.get_student_by_id(row[0])
            students.append(student)
        return students

    # Skills Queries
    def get_skills_by_project_id(self, project_id: str) -> list[SkillOrSoftware]:
        skills: list[SkillOrSoftware] = []
        self.cursor.execute(
            "SELECT name, type FROM skill_or_software WHERE project_id = ?",
            (project_id,),
        )
        for row in self.cursor.fetchall():
            skill = SkillOrSoftware(name=row[0], type=row[1])
            skills.append(skill)
        return skills

    # Topics Queries
    def get_topics_by_project_id(self, project_id: str) -> list[Topic]:
        topics: list[Topic] = []
        self.cursor.execute(
            "SELECT name FROM project_has_topic INNER JOIN topic ON topic.id = project_has_topic.topic_id WHERE project_id = ? ",
            (project_id,),
        )
        for row in self.cursor.fetchall():
            topic = Topic(name=row[0])
            topics.append(topic)
        return topics

    # Awards
    def get_awards_by_project_id(self, project_id: str) -> list[Award]:
        awards: list[Award] = []
        self.cursor.execute(
            "SELECT project_id, award FROM project_has_award WHERE project_id = ?",
            (project_id,),
        )
        for row in self.cursor.fetchall():
            award = Award(name=row[1])
            awards.append(award)
        return awards

    def get_semesters_participed_by_advisor(self, advisor_id: str) -> list[str]:
        semester_participated: list[str] = []
        self.cursor.execute(
            """
                SELECT project.semester, project.year  FROM advisor
                            INNER JOIN project_has_advisor ON project_has_advisor.advisor_id = advisor.id
                            INNER JOIN project ON project.id = project_has_advisor.project_id
                    WHERE advisor.id = ?;""",
            (advisor_id,),
        )

        rows = self.cursor.fetchall()
        for row in rows:
            semester = row[0]
            year = row[1]
            edition = f"{semester} {year}"
            if edition not in semester_participated:
                semester_participated.append(edition)
        return semester_participated

    def get_semesters_participed_by_advisor_as_chair(
        self, advisor_id: str
    ) -> list[str]:
        semester_participated: list[str] = []
        self.cursor.execute(
            """
            SELECT semester.semester, semester.year  FROM advisor
            INNER JOIN semester_has_co_chair ON semester_has_co_chair.co_chair_id = advisor.id
            INNER JOIN semester ON semester.id = semester_has_co_chair.semester_id
            WHERE advisor.id = ?;""",
            (advisor_id,),
        )

        rows = self.cursor.fetchall()
        for row in rows:
            semester = row[0]
            year = row[1]
            edition = f"{semester} {year}"
            if edition not in semester_participated:
                semester_participated.append(edition)
        return semester_participated

    def get_semesters_participed_by_student(self, student_id: str) -> list[str]:
        semester_participated: list[str] = []
        self.cursor.execute(
            """
                SELECT project.semester, project.year  FROM student
                            INNER JOIN project_has_student ON project_has_student.student_id = student.id
                            INNER JOIN project ON project.id = project_has_student.project_id
                    WHERE student.id = ?;""",
            (student_id,),
        )

        rows = self.cursor.fetchall()
        for row in rows:
            semester = row[0]
            year = row[1]
            edition = f"{semester} {year}"
            if edition not in semester_participated:
                semester_participated.append(edition)
        return semester_participated
