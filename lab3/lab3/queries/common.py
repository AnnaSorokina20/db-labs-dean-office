
from api.engine import DBConn
from models import Student, StudentGroup, Specialty, Department, Subject, GroupSubject, SessionResult
from sqlalchemy import select, and_, or_, func

def list_failed_exams(department_id):
    # Щоб запросити дані з бази та отримати екземпляри певного класу в програмі, ми повинні
    # створити об'єкт класу Session.
    #
    # Цей клас реалізує сеанс – діалог з базою даних, що належить до поточної виконуваної
    # операції предметної області. Якщо програма звертається до кількох об'єктів при виконанні
    # однієї операції, то для всіх використовується той самий сеанс.
    #
    # У багатьох випадках сеанс пов'язаний із однією транзакцією.
    with DBConn.get_session() as session:
        statement = (
            select(
                Student.last_name,
                Student.first_name,
                StudentGroup.group_number,
                Subject.name.label('subject_name'),
                SessionResult.grade
            )
            .select_from(Student)
            .join(StudentGroup, Student.group_id == StudentGroup.group_id)
            .join(Specialty, StudentGroup.specialty_id == Specialty.specialty_id)
            .join(GroupSubject, GroupSubject.group_id == StudentGroup.group_id)
            .join(Subject, GroupSubject.subject_id == Subject.subject_id)
            .outerjoin(
                SessionResult,
                and_(
                    SessionResult.student_id == Student.student_id,
                    SessionResult.group_subject_id == GroupSubject.group_subject_id
                )
            )
            .where(
                Specialty.department_id == department_id,
                GroupSubject.assessment_type == 'exam',
                or_(
                    SessionResult.grade.is_(None),
                    SessionResult.grade == 2
                )
            )
        
            .order_by(
                Student.last_name,
                Student.first_name,
                StudentGroup.group_number,
                Subject.name
            )
        )
    

        rows = session.execute(statement).all()

        if not rows:
            print('Нескладених іспитів для цієї кафедри не знайдено.')

        for row in rows:
            grade = 'відсутня' if row.grade is None else row.grade
            print(
                f'{row.last_name} {row.first_name} | '
                f'{row.group_number} | {row.subject_name} | '
                f'Оцінка: {grade}'
            )

def list_group_averages(faculty_id):
    with DBConn.get_session() as session:
        statement = (
            select(
                StudentGroup.group_number,
                func.avg(SessionResult.grade).label('average_grade')
            )
            .select_from(StudentGroup)
            .join(
                Specialty,
                StudentGroup.specialty_id == Specialty.specialty_id
            )
            .join(
                Department,
                Specialty.department_id == Department.department_id
            )
            .outerjoin(Student, Student.group_id == StudentGroup.group_id)
            .outerjoin(
                SessionResult,
                SessionResult.student_id == Student.student_id
            )
            .where(Department.faculty_id == faculty_id)
            .group_by(StudentGroup.group_id, StudentGroup.group_number)
            .order_by(StudentGroup.group_number)
        )

        rows = session.execute(statement).all()

        if not rows:
            print('Груп для цього факультету не знайдено.')

        for row in rows:
            average = (
                f'{row.average_grade:.2f}'
                if row.average_grade is not None
                else 'немає оцінок'
            )
            print(f'{row.group_number} | Середній бал: {average}')


def list_subject_averages():
    with DBConn.get_session() as session:
        statement = (
            select(
                Subject.name,
                func.avg(SessionResult.grade).label('average_grade')
            )
            .select_from(Subject)
            .outerjoin(
                GroupSubject,
                GroupSubject.subject_id == Subject.subject_id
            )
            .outerjoin(
                SessionResult,
                SessionResult.group_subject_id == GroupSubject.group_subject_id
            )
            .group_by(Subject.subject_id, Subject.name)
            .order_by(Subject.name)
        )

        rows = session.execute(statement).all()

        if not rows:
            print('Предметів не знайдено.')

        for row in rows:
            average = (
                f'{row.average_grade:.2f}'
                if row.average_grade is not None
                else 'немає екзаменаційних оцінок'
            )
            print(f'{row.name} | Середній бал: {average}')


def get_scholarship_students(department_id):
    with DBConn.get_session() as session:
        statement = (
            select(
                Student.student_id,
                Student.last_name,
                Student.first_name,
                Student.permanent_city,
                StudentGroup.group_number,
                func.min(SessionResult.grade).label('min_grade'),
                func.count().filter(
                    SessionResult.grade == 3
                ).label('threes'),
                func.count().filter(
                    SessionResult.grade == 4
                ).label('fours')
            )
            .select_from(Student)
            .join(StudentGroup, Student.group_id == StudentGroup.group_id)
            .join(
                Specialty,
                StudentGroup.specialty_id == Specialty.specialty_id
            )
            .join(GroupSubject, GroupSubject.group_id == StudentGroup.group_id)
            .outerjoin(
                SessionResult,
                and_(
                    SessionResult.student_id == Student.student_id,
                    SessionResult.group_subject_id == GroupSubject.group_subject_id
                )
            )
            .where(Specialty.department_id == department_id)
            .group_by(
                Student.student_id,
                Student.last_name,
                Student.first_name,
                Student.permanent_city,
                StudentGroup.group_number
            )
            .having(
                func.count(SessionResult.result_id)
                == func.count(GroupSubject.group_subject_id),
                func.count().filter(
                    and_(
                        GroupSubject.assessment_type == 'credit',
                        SessionResult.credit_passed.is_distinct_from(True)
                    )
                ) == 0,
                func.min(SessionResult.grade) >= 3,
                or_(
                    func.count().filter(SessionResult.grade == 3) == 0,
                    and_(
                        Student.permanent_city != 'Харків',
                        func.count().filter(SessionResult.grade == 3) <= 1
                    )
                )
            )
            .order_by(Student.last_name, Student.first_name)
        )

        rows = session.execute(statement).all()
        return rows


def list_scholarship_students(department_id):
    rows = get_scholarship_students(department_id)

    if not rows:
        print('Студентів із правом на стипендію не знайдено.')

    for row in rows:
        if row.min_grade == 5:
            percent = 100
        elif row.threes == 0 and row.fours <= 2:
            percent = 50
        else:
            percent = 0

        print(
            f'{row.last_name} {row.first_name} | '
            f'{row.group_number} | '
            f'Підвищення стипендії: {percent}%'
        )