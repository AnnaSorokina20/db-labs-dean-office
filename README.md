[Lab1_Sorokina.docx](https://github.com/user-attachments/files/33079395/Lab1_Sorokina.docx)

[Lab2_Sorokina.docx](https://github.com/user-attachments/files/33874025/Lab2_Sorokina.docx)

[Lab3_Sorokina.docx](https://github.com/user-attachments/files/33928099/Lab3_Sorokina.docx)


# db-labs-dean-office
Дисципліна: «Програмування баз даних та знань».
Варіант 15: інформаційна система деканату (групи, студенти, результати сесії).
Виконала: Сорокіна А. В., група КН-М526.

## Лабораторна робота 2. Логічне проєктування бази даних

Дисципліна: «Програмування баз даних та знань».
Варіант 15: інформаційна система деканату (групи, студенти, результати сесії).
Виконала: Сорокіна А. В., група КН-М526.

### Склад

| Файл | Призначення |
|---|---|
| `schema.sql` | Створення бази `lab2`, таблиць і обмежень цілісності |
| `data.sql` | Тестові дані (5–10 рядків у кожній таблиці) |
| `query_1.sql` | Студенти кафедри, які не склали хоча б один іспит (група, предмет) |
| `query_2.sql` | Середній бал кожної групи вказаного факультету |
| `query_3.sql` | Середній бал з кожного предмета |
| `query_4.sql` | Студенти кафедри, які можуть отримувати стипендію (із розміром) |
| `Lab2_Sorokina.docx` | Звіт для Лаб2 |
| `Lab1_Sorokina.docx` | Звіт для Лаб1 |

Таблиці: `faculties`, `departments`, `specialties`, `student_groups`, `students`,
`subjects`, `group_subjects`, `session_results` (3НФ).

### Запуск

СУБД PostgreSQL 14 працює в Docker-контейнері.

1. Створити та запустити контейнер (схема створюється автоматично):

   ```
   ./_create.sh
   ```

   Windows: `_create.bat`, Git Bash: `_create_under_gitbash.sh`.

2. У новому терміналі відкрити консоль `psql`:

   ```
   ./_psql.sh
   ```

   Windows: `_psql.bat`.

3. Перейти до бази, завантажити дані та виконати запити:

   ```
   \c lab2
   \i /repo/data.sql
   \i /repo/query_1.sql
   \i /repo/query_2.sql
   \i /repo/query_3.sql
   \i /repo/query_4.sql
   ```

Перегляд таблиць: `\dt`. Вихід: `\q`.

## Лабораторна робота 3. Взаємодія з базою даних через ORM

У папці `lab3/` реалізовано програму на Python із використанням SQLAlchemy ORM та Click: моделі восьми таблиць, тестові дані, запити, операції зміни даних і тригери PostgreSQL.

Запуск із папки `lab3/`:

```bash
docker compose up -d --build
docker compose exec postgres_db pg_isready -U testuser -d lab3
```

Після повідомлення `accepting connections`:

```bash
docker compose exec python_app python cli.py create-tables
docker compose exec python_app python cli.py fill-db
docker compose exec python_app python cli.py --help
```

`fill-db` виконується один раз для порожньої бази.
Повна інструкція та перелік команд: [lab3/README.txt](lab3/README.txt).
Підключення з хоста (pgAdmin тощо): порт `5434`, користувач `postgres`, пароль `foo`.
