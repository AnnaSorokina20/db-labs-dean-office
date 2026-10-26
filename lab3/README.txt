Лабораторна робота №3
Варіант 15 — Деканат

Програма працює з базою даних деканату через ORM SQLAlchemy. Результати виконання команд виводяться в консоль.

ВИМОГИ

- Потрібні встановлені Docker Desktop і Docker Compose.
- Docker Desktop має бути запущений.

Використані технології:
- Python 3.12;
- PostgreSQL 14;
- SQLAlchemy;
- psycopg2-binary;
- Click.

Python-залежності з requirements.txt встановлюються автоматично під час збирання Docker-образу.

ПЕРШИЙ ЗАПУСК

Відкрити термінал у зовнішній папці lab3, де розташований docker-compose.yml.

1. Зібрати образ і запустити контейнери:
docker compose up -d --build

2. Перевірити готовність PostgreSQL:
docker compose exec postgres_db pg_isready -U testuser -d lab3

Якщо сервер ще не готовий, повторити перевірку.
Продовжити після повідомлення "accepting connections".

3. Створити таблиці та тригери:
docker compose exec python_app python cli.py create-tables

4. Заповнити порожні таблиці тестовими даними:
docker compose exec python_app python cli.py fill-db

fill-db виконувати один раз для порожньої бази. Повторний виклик для заповненої бази спричинить помилку унікальності тестових даних.

ПЕРЕГЛЯД КОМАНД

docker compose exec python_app python cli.py --help

Довідка для конкретної команди, наприклад:
docker compose exec python_app python cli.py add-student --help

ЗАПИТИ

Нескладені іспити студентів кафедри:
docker compose exec python_app python cli.py failed-exams -d 1

Середній бал груп факультету:
docker compose exec python_app python cli.py group-averages -f 1

Середній бал із кожного предмета:
docker compose exec python_app python cli.py subject-averages

Студенти кафедри, які мають право на стипендію:
docker compose exec python_app python cli.py scholarship-students -d 1

ЗМІНА ДАНИХ

Додавання студента з послідовним введенням його даних:
docker compose exec python_app python cli.py add-student

Видалення студента:
docker compose exec python_app python cli.py delete-student -s STUDENT_ID

Зміна номера залікової книжки:
docker compose exec python_app python cli.py change-record-book -s STUDENT_ID -n NEW_NUMBER

Внесення або зміна екзаменаційної оцінки від 2 до 5:
docker compose exec python_app python cli.py set-exam-grade -s STUDENT_ID -g GROUP_SUBJECT_ID --grade 5

Внесення або зміна результату заліку: true — складено, false — не складено.
docker compose exec python_app python cli.py set-credit-result -s STUDENT_ID -g GROUP_SUBJECT_ID --passed true

Переведення студента до іншої групи:
docker compose exec python_app python cli.py transfer-student -s STUDENT_ID -g NEW_GROUP_ID

Нарахування стипендій студентам кафедри:
docker compose exec python_app python cli.py assign-scholarships -d 1

-- STUDENT_ID, GROUP_SUBJECT_ID, NEW_GROUP_ID і NEW_NUMBER потрібно замінити фактичними значеннями.
GROUP_SUBJECT_ID — ідентифікатор запису в group_subjects, а не ідентифікатор предмета в subjects.

Під час переведення наявні результати переносяться на відповідні предмети нової групи з тим самим видом контролю.
Якщо відповідності немає, переведення відхиляється.
Спеціальність і кафедра студента визначаються через його групу.

ТРИГЕРИ

Команда create-tables створює таблиці ORM та встановлює тригери
з файла lab3/scripts/triggers.sql (шлях від зовнішньої папки lab3).

Тригери PostgreSQL перевіряють відповідність результату виду
контролю та групі студента. Під час зміни групи тригер переносить
результати на відповідні предмети нової групи або відхиляє
переведення, якщо відповідності немає.

Ці перевірки діють також під час прямої зміни даних через SQL.

СТИПЕНДІЯ

Команда scholarship-students показує студентів, які мають право на стипендію, та її ПІДВИЩЕННЯ:
0% — базова стипендія без підвищення;
50% — підвищення на половину базової стипендії;
100% — підвищення на розмір базової стипендії.

Студенти без права на стипендію до цього списку не входять.
Команда перегляду не змінює дані.

Команда assign-scholarships зберігає нарахування в БД.
Поле scholarship_percent містить ЗАГАЛЬНИЙ РОЗМІР стипендії у відсотках від базової:
0 — не призначено;
100 — призначено без підвищення;
150 — призначено з підвищенням на 50%;
200 — призначено з підвищенням на 100%.

Після зміни оцінок, заліків або групи попереднє нарахування скидається. Потрібно повторно виконати assign-scholarships для поточної кафедри студента.

ПЕРЕГЛЯД БАЗИ ЧЕРЕЗ ADMINER

Адреса: http://localhost:8080

Система: PostgreSQL
Сервер: postgres_db
Користувач: testuser
Пароль: password
База даних: lab3

Для підключення з програми на комп'ютері: сервер localhost, порт 8432.

ЗУПИНКА ТА ПОВТОРНИЙ ЗАПУСК

Зупинити контейнери:
docker compose stop

Запустити раніше створені контейнери:
docker compose start

Після звичайної зупинки та запуску повторно створювати таблиці й заповнювати їх тестовими даними не потрібно.

ВИДАЛЕННЯ ТАБЛИЦЬ

Наступна команда видаляє всі таблиці моделей разом із даними:
docker compose exec python_app python cli.py drop-tables