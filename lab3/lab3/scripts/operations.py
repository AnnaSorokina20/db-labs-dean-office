from api.engine import DBConn
from models import Student, StudentGroup, Specialty, GroupSubject, SessionResult
from queries import common
from sqlalchemy import select


def add_student(
    record_book_number,
    group_id,
    last_name,
    first_name,
    permanent_city,
    permanent_street,
    permanent_building,
    current_city,
    current_street,
    current_building,
    patronymic=None
):
    with DBConn.get_session() as session:
        group = session.get(StudentGroup, group_id)

        if group is None:
            raise ValueError('Групу із зазначеним ID не знайдено.')

        student = Student(
            record_book_number=record_book_number,
            group_id=group_id,
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            permanent_city=permanent_city,
            permanent_street=permanent_street,
            permanent_building=permanent_building,
            current_city=current_city,
            current_street=current_street,
            current_building=current_building,
            scholarship_percent=0
        )

        session.add(student)
        session.flush()
        student_id = student.student_id
        session.commit()

        print(f'Студента додано. ID: {student_id}')

def delete_student(student_id):
    with DBConn.get_session() as session:
        student = session.get(Student, student_id)

        if student is None:
            raise ValueError('Студента із зазначеним ID не знайдено.')

        session.delete(student)
        session.commit()

        print(f'Студента з ID {student_id} видалено.')        

def change_record_book(student_id, new_number):
    with DBConn.get_session() as session:
        student = session.get(Student, student_id)

        if student is None:
            raise ValueError('Студента із зазначеним ID не знайдено.')

        student.record_book_number = new_number
        session.commit()

        print(
            f'Номер залікової книжки студента з ID {student_id} '
            f'змінено на {new_number}.'
        )        

def set_exam_grade(student_id, group_subject_id, grade):
    with DBConn.get_session() as session:
        student = session.get(Student, student_id)
        group_subject = session.get(GroupSubject, group_subject_id)

        if student is None:
            raise ValueError('Студента не знайдено.')

        if group_subject is None:
            raise ValueError('Предмет сесії не знайдено.')

        if student.group_id != group_subject.group_id:
            raise ValueError('Предмет не належить до групи студента.')

        if group_subject.assessment_type != 'exam':
            raise ValueError('Для цього предмета передбачено залік.')

        if grade not in (2, 3, 4, 5):
            raise ValueError('Оцінка має бути від 2 до 5.')

        result = session.scalar(
            select(SessionResult).where(
                SessionResult.student_id == student_id,
                SessionResult.group_subject_id == group_subject_id
            )
        )

        if result is None:
            result = SessionResult(
                student_id=student_id,
                group_subject_id=group_subject_id
            )
            session.add(result)

        result.grade = grade
        result.credit_passed = None
        student.scholarship_percent = 0

        session.commit()
        print('Оцінку збережено. Стипендія потребує перерахунку.')        

def set_credit_result(student_id, group_subject_id, passed):
    with DBConn.get_session() as session:
        student = session.get(Student, student_id)
        group_subject = session.get(GroupSubject, group_subject_id)

        if student is None:
            raise ValueError('Студента не знайдено.')

        if group_subject is None:
            raise ValueError('Предмет сесії не знайдено.')

        if student.group_id != group_subject.group_id:
            raise ValueError('Предмет не належить до групи студента.')

        if group_subject.assessment_type != 'credit':
            raise ValueError('Для цього предмета передбачено іспит.')

        if not isinstance(passed, bool):
            raise ValueError('Результат заліку має бути True або False.')

        result = session.scalar(
            select(SessionResult).where(
                SessionResult.student_id == student_id,
                SessionResult.group_subject_id == group_subject_id
            )
        )

        if result is None:
            result = SessionResult(
                student_id=student_id,
                group_subject_id=group_subject_id
            )
            session.add(result)

        result.grade = None
        result.credit_passed = passed
        student.scholarship_percent = 0

        session.commit()
        print('Результат заліку збережено. Стипендія потребує перерахунку.')        

def transfer_student(student_id, new_group_id):
    with DBConn.get_session() as session:
        student = session.get(Student, student_id)
        new_group = session.get(StudentGroup, new_group_id)

        if student is None:
            raise ValueError('Студента із зазначеним ID не знайдено.')

        if new_group is None:
            raise ValueError('Нову групу із зазначеним ID не знайдено.')

        if student.group_id == new_group_id:
            raise ValueError('Студент уже навчається в цій групі.')

        results = session.execute(
            select(SessionResult, GroupSubject)
            .join(
                GroupSubject,
                SessionResult.group_subject_id
                == GroupSubject.group_subject_id
            )
            .where(SessionResult.student_id == student_id)
        ).all()

        new_subjects = session.scalars(
            select(GroupSubject)
            .where(GroupSubject.group_id == new_group_id)
        ).all()

        subject_map = {
            (subject.subject_id, subject.assessment_type):
                subject.group_subject_id
            for subject in new_subjects
        }

        transfers = []

        for result, old_subject in results:
            key = (old_subject.subject_id, old_subject.assessment_type)

            if key not in subject_map:
                raise ValueError(
                    'Переведення неможливе: у новій групі немає '
                    'відповідного предмета з таким самим видом контролю '
                    'для збереження результату.'
                )

            transfers.append((result, subject_map[key]))



        student.group_id = new_group_id
        student.scholarship_percent = 0
        session.commit()

        print(
            'Студента переведено. Результати збережено. '
            'Стипендія потребує перерахунку.'
        )        

def assign_scholarships(department_id):
    eligible = common.get_scholarship_students(department_id)

    amounts = {}

    for row in eligible:
        if row.min_grade == 5:
            amounts[row.student_id] = 200
        elif row.threes == 0 and row.fours <= 2:
            amounts[row.student_id] = 150
        else:
            amounts[row.student_id] = 100

    with DBConn.get_session() as session:
        students = session.scalars(
            select(Student)
            .join(StudentGroup, Student.group_id == StudentGroup.group_id)
            .join(
                Specialty,
                StudentGroup.specialty_id == Specialty.specialty_id
            )
            .where(Specialty.department_id == department_id)
        ).all()

        if not students:
            raise ValueError('Студентів цієї кафедри не знайдено.')

        for student in students:
            student.scholarship_percent = amounts.get(
                student.student_id, 0
            )

        session.commit()

        print(
            f'Нарахування збережено. '
            f'Стипендію призначено {len(eligible)} студентам.'
        )        