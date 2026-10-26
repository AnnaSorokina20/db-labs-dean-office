
import click
from scripts import database, operations
from api.engine import DBConn
from models.base import myBase
from queries import common
from pathlib import Path

# IMPORTANT: all models should be imported before the call to
#            myBase.metadata.create_all();
#            otherway no tables will be created
from models import *

@click.group()
def cli():
    # Щоб підключитися до бази, потрібно створити об'єкт engine. Зауважимо, що в цей момент програма
    # ще не підключилася до бази. Воно створило пул з'єднань, і коли бібліотеці SQLAlchemy знадобиться
    # виконати команду, вона запросить з'єднання з цього пулу. Якщо з'єднання ще не існує, воно буде
    # встановлено.
    DBConn()


@cli.command(help='Створити таблиці та тригери в БД')
def create_tables():
    sql_path = Path(__file__).parent / 'scripts' / 'triggers.sql'
    trigger_sql = sql_path.read_text(encoding='utf-8-sig')
    trigger_sql = trigger_sql.replace(
        'CREATE FUNCTION', 'CREATE OR REPLACE FUNCTION'
    )

    with DBConn.engine.begin() as connection:
        myBase.metadata.create_all(connection)

        connection.exec_driver_sql(
            'DROP TRIGGER IF EXISTS check_result_type_trigger '
            'ON session_results'
        )
        connection.exec_driver_sql(
            'DROP TRIGGER IF EXISTS check_result_group_trigger '
            'ON session_results'
        )
        connection.exec_driver_sql(
            'DROP TRIGGER IF EXISTS transfer_student_results_trigger '
            'ON students'
        )

        connection.exec_driver_sql(trigger_sql)

    print('Таблиці та тригери створено.')


@cli.command(help='Видалити таблиці в БД')
def drop_tables():
    myBase.metadata.drop_all(DBConn.engine)





@cli.command(help='Заповнити БД тестовими даними')
def fill_db():
    database.fill_db()

@cli.command(help='Показати нескладені іспити студентів кафедри')
@click.option('--department-id', '-d', type=click.INT, required=True)
def failed_exams(department_id):
    common.list_failed_exams(department_id)

@cli.command(help='Показати середній бал груп факультету')
@click.option('--faculty-id', '-f', type=click.INT, required=True)
def group_averages(faculty_id):
    common.list_group_averages(faculty_id)

@cli.command(help='Показати середній бал із кожного предмета')
def subject_averages():
    common.list_subject_averages()

@cli.command(help='Показати студентів кафедри з правом на стипендію')
@click.option('--department-id', '-d', type=click.INT, required=True)
def scholarship_students(department_id):
    common.list_scholarship_students(department_id)

@cli.command(help='Додати студента')
@click.option('--record-book-number', prompt='Номер залікової книжки')
@click.option('--group-id', type=click.INT, prompt='ID групи')
@click.option('--last-name', prompt='Прізвище')
@click.option('--first-name', prompt="Ім'я")
@click.option('--patronymic', prompt='По батькові (можна пропустити)', default='')
@click.option('--permanent-city', prompt='Місто прописки')
@click.option('--permanent-street', prompt='Вулиця прописки')
@click.option('--permanent-building', prompt='Будинок прописки')
@click.option('--current-city', prompt='Місто проживання')
@click.option('--current-street', prompt='Вулиця проживання')
@click.option('--current-building', prompt='Будинок проживання')
def add_student(
    record_book_number,
    group_id,
    last_name,
    first_name,
    patronymic,
    permanent_city,
    permanent_street,
    permanent_building,
    current_city,
    current_street,
    current_building
):
    try:
        operations.add_student(
            record_book_number=record_book_number,
            group_id=group_id,
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic or None,
            permanent_city=permanent_city,
            permanent_street=permanent_street,
            permanent_building=permanent_building,
            current_city=current_city,
            current_street=current_street,
            current_building=current_building
        )
    except ValueError as error:
        raise click.ClickException(str(error))

@cli.command(help='Видалити студента за ID')
@click.option('--student-id', '-s', type=click.INT, required=True)
def delete_student(student_id):
    try:
        operations.delete_student(student_id)
    except ValueError as error:
        raise click.ClickException(str(error))

@cli.command(help='Змінити номер залікової книжки студента')
@click.option('--student-id', '-s', type=click.INT, required=True)
@click.option('--new-number', '-n', required=True)
def change_record_book(student_id, new_number):
    try:
        operations.change_record_book(student_id, new_number)
    except ValueError as error:
        raise click.ClickException(str(error))

@cli.command(help='Внести або змінити оцінку з іспиту')
@click.option('--student-id', '-s', type=click.INT, required=True)
@click.option('--group-subject-id', '-g', type=click.INT, required=True)
@click.option('--grade', type=click.IntRange(2, 5), required=True)
def set_exam_grade(student_id, group_subject_id, grade):
    try:
        operations.set_exam_grade(student_id, group_subject_id, grade)
    except ValueError as error:
        raise click.ClickException(str(error))

@cli.command(help='Внести або змінити результат заліку')
@click.option('--student-id', '-s', type=click.INT, required=True)
@click.option('--group-subject-id', '-g', type=click.INT, required=True)
@click.option('--passed', type=click.BOOL, required=True)
def set_credit_result(student_id, group_subject_id, passed):
    try:
        operations.set_credit_result(student_id, group_subject_id, passed)
    except ValueError as error:
        raise click.ClickException(str(error))

@cli.command(help='Перевести студента до іншої групи')
@click.option('--student-id', '-s', type=click.INT, required=True)
@click.option('--new-group-id', '-g', type=click.INT, required=True)
def transfer_student(student_id, new_group_id):
    try:
        operations.transfer_student(student_id, new_group_id)
    except ValueError as error:
        raise click.ClickException(str(error))

@cli.command(help='Нарахувати стипендії студентам кафедри')
@click.option('--department-id', '-d', type=click.INT, required=True)
def assign_scholarships(department_id):
    try:
        operations.assign_scholarships(department_id)
    except ValueError as error:
        raise click.ClickException(str(error))
                           
if __name__ == '__main__':
    print("\nБаза даних деканату — лабораторна робота №3")
    cli()
