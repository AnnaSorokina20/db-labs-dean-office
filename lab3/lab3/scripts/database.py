
from models import (
    Faculty, Department, Specialty, StudentGroup,
    Student, Subject, GroupSubject, SessionResult
)
from api.engine import DBConn


def fill_db():
    with DBConn.get_session() as session:
        faculties = [
            Faculty(name="Факультет комп'ютерних наук"),
            Faculty(name="Факультет інформаційних технологій"),
            Faculty(name="Економічний факультет"),
            Faculty(name="Факультет механічної інженерії"),
            Faculty(name="Факультет енергетики"),
        ]

        session.add_all(faculties)
        session.flush()

        departments = [
            Department(
                name='Кафедра програмної інженерії',
                faculty_id=faculties[0].faculty_id
            ),
            Department(
                name="Кафедра комп'ютерних наук",
                faculty_id=faculties[0].faculty_id
            ),
            Department(
                name="Кафедра комп'ютерної інженерії",
                faculty_id=faculties[1].faculty_id
            ),
            Department(
                name='Кафедра менеджменту',
                faculty_id=faculties[2].faculty_id
            ),
            Department(
                name='Кафедра прикладної механіки',
                faculty_id=faculties[3].faculty_id
            ),
            Department(
                name='Кафедра електроенергетики',
                faculty_id=faculties[4].faculty_id
            ),
        ]

        session.add_all(departments)
        session.flush()

        specialties = [
            Specialty(
                department_id=departments[0].department_id,
                code='121',
                name='Інженерія програмного забезпечення'
            ),
            Specialty(
                department_id=departments[1].department_id,
                code='122',
                name="Комп'ютерні науки"
            ),
            Specialty(
                department_id=departments[2].department_id,
                code='123',
                name="Комп'ютерна інженерія"
            ),
            Specialty(
                department_id=departments[3].department_id,
                code='073',
                name='Менеджмент'
            ),
            Specialty(
                department_id=departments[4].department_id,
                code='131',
                name='Прикладна механіка'
            ),
            Specialty(
                department_id=departments[5].department_id,
                code='141',
                name='Електроенергетика, електротехніка та електромеханіка'
            ),
        ]

        session.add_all(specialties)
        session.flush()

        groups = [
            StudentGroup(
                specialty_id=specialties[0].specialty_id,
                group_number='ПЗ-М126',
                formation_year=2026
            ),
            StudentGroup(
                specialty_id=specialties[1].specialty_id,
                group_number='КН-М126',
                formation_year=2026
            ),
            StudentGroup(
                specialty_id=specialties[2].specialty_id,
                group_number='КІ-М126',
                formation_year=2026
            ),
            StudentGroup(
                specialty_id=specialties[3].specialty_id,
                group_number='МН-М125',
                formation_year=2025
            ),
            StudentGroup(
                specialty_id=specialties[5].specialty_id,
                group_number='ЕЕ-М126',
                formation_year=2026
            ),
        ]

        session.add_all(groups)
        session.flush()

        students = [
            Student(
                record_book_number='RB001',
                group_id=groups[0].group_id,
                last_name='Іваненко',
                first_name='Олена',
                patronymic='Сергіївна',
                permanent_city='Харків',
                permanent_street='Сумська',
                permanent_building='10',
                current_city='Харків',
                current_street='Сумська',
                current_building='10',
                scholarship_percent=0
            ),
            Student(
                record_book_number='RB002',
                group_id=groups[0].group_id,
                last_name='Петренко',
                first_name='Максим',
                patronymic='Олегович',
                permanent_city='Полтава',
                permanent_street='Європейська',
                permanent_building='22',
                current_city='Харків',
                current_street='Студентська',
                current_building='15',
                scholarship_percent=0
            ),
            Student(
                record_book_number='RB003',
                group_id=groups[1].group_id,
                last_name='Коваленко',
                first_name='Анна',
                patronymic='Ігорівна',
                permanent_city='Дніпро',
                permanent_street='Воскресенська',
                permanent_building='7',
                current_city='Харків',
                current_street='Студентська',
                current_building='8',
                scholarship_percent=0
            ),
            Student(
                record_book_number='RB004',
                group_id=groups[2].group_id,
                last_name='Шевченко',
                first_name='Дмитро',
                patronymic='Андрійович',
                permanent_city='Харків',
                permanent_street='Науки',
                permanent_building='15',
                current_city='Харків',
                current_street='Науки',
                current_building='15',
                scholarship_percent=0
            ),
            Student(
                record_book_number='RB005',
                group_id=groups[3].group_id,
                last_name='Бондаренко',
                first_name='Марія',
                patronymic='Вікторівна',
                permanent_city='Суми',
                permanent_street='Харківська',
                permanent_building='18',
                current_city='Харків',
                current_street='Студентська',
                current_building='12',
                scholarship_percent=0
            ),
            Student(
                record_book_number='RB006',
                group_id=groups[4].group_id,
                last_name='Мельник',
                first_name='Олексій',
                patronymic='Петрович',
                permanent_city='Харків',
                permanent_street='Мироносицька',
                permanent_building='31',
                current_city='Харків',
                current_street='Мироносицька',
                current_building='31',
                scholarship_percent=0
            ),
        ]

        session.add_all(students)
        session.flush()

        subjects = [
            Subject(name='Бази даних'),
            Subject(name='Програмування'),
            Subject(name='Управління ІТ-проєктами'),
            Subject(name='Математичні методи'),
            Subject(name='Англійська мова'),
            Subject(name="Комп'ютерні мережі"),
        ]

        session.add_all(subjects)
        session.flush()

        group_subjects = [
            GroupSubject(
                group_id=groups[0].group_id,
                subject_id=subjects[0].subject_id,
                assessment_type='exam'
            ),
            GroupSubject(
                group_id=groups[0].group_id,
                subject_id=subjects[1].subject_id,
                assessment_type='exam'
            ),
            GroupSubject(
                group_id=groups[0].group_id,
                subject_id=subjects[4].subject_id,
                assessment_type='credit'
            ),
            GroupSubject(
                group_id=groups[1].group_id,
                subject_id=subjects[0].subject_id,
                assessment_type='exam'
            ),
            GroupSubject(
                group_id=groups[1].group_id,
                subject_id=subjects[3].subject_id,
                assessment_type='exam'
            ),
            GroupSubject(
                group_id=groups[2].group_id,
                subject_id=subjects[1].subject_id,
                assessment_type='exam'
            ),
            GroupSubject(
                group_id=groups[2].group_id,
                subject_id=subjects[5].subject_id,
                assessment_type='exam'
            ),
            GroupSubject(
                group_id=groups[3].group_id,
                subject_id=subjects[2].subject_id,
                assessment_type='exam'
            ),
            GroupSubject(
                group_id=groups[4].group_id,
                subject_id=subjects[3].subject_id,
                assessment_type='exam'
            ),
            GroupSubject(
                group_id=groups[4].group_id,
                subject_id=subjects[4].subject_id,
                assessment_type='credit'
            ),
        ]

        session.add_all(group_subjects)
        session.flush()

        results = [
            SessionResult(
                student_id=students[0].student_id,
                group_subject_id=group_subjects[0].group_subject_id,
                grade=5
            ),
            SessionResult(
                student_id=students[0].student_id,
                group_subject_id=group_subjects[1].group_subject_id,
                grade=5
            ),
            SessionResult(
                student_id=students[0].student_id,
                group_subject_id=group_subjects[2].group_subject_id,
                credit_passed=True
            ),
            SessionResult(
                student_id=students[1].student_id,
                group_subject_id=group_subjects[0].group_subject_id,
                grade=2
            ),
            SessionResult(
                student_id=students[1].student_id,
                group_subject_id=group_subjects[2].group_subject_id,
                credit_passed=True
            ),
            SessionResult(
                student_id=students[2].student_id,
                group_subject_id=group_subjects[3].group_subject_id,
                grade=4
            ),
            SessionResult(
                student_id=students[2].student_id,
                group_subject_id=group_subjects[4].group_subject_id,
                grade=5
            ),
            SessionResult(
                student_id=students[3].student_id,
                group_subject_id=group_subjects[5].group_subject_id,
                grade=4
            ),
            SessionResult(
                student_id=students[4].student_id,
                group_subject_id=group_subjects[7].group_subject_id,
                grade=3
            ),
            SessionResult(
                student_id=students[5].student_id,
                group_subject_id=group_subjects[8].group_subject_id,
                grade=5
            ),
        ]

        session.add_all(results)
        session.commit()
