DROP DATABASE IF EXISTS lab2;

CREATE ROLE testuser LOGIN;

--For linux
CREATE DATABASE lab2 ENCODING 'UTF-8' LC_COLLATE 'en_US.UTF-8' LC_CTYPE 'en_US.UTF-8' TEMPLATE template0 OWNER testuser;

\c lab2

SET ROLE testuser;

CREATE TABLE faculties (
    faculty_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE departments (
    department_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    faculty_id INTEGER NOT NULL REFERENCES faculties(faculty_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    UNIQUE (faculty_id, name)
);

CREATE TABLE specialties (
    specialty_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_id INTEGER NOT NULL REFERENCES departments(department_id) ON DELETE CASCADE,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);

CREATE TABLE student_groups (
    group_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    specialty_id INTEGER NOT NULL REFERENCES specialties(specialty_id) ON DELETE CASCADE,
    group_number TEXT NOT NULL UNIQUE,
    formation_year INTEGER NOT NULL CHECK (formation_year > 2000)
);
CREATE TABLE students (
    student_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    record_book_number TEXT NOT NULL UNIQUE,
    group_id INTEGER NOT NULL REFERENCES student_groups(group_id) ON DELETE CASCADE,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    patronymic TEXT,
    permanent_address TEXT NOT NULL,
    current_address TEXT NOT NULL,
    is_nonresident BOOLEAN NOT NULL DEFAULT FALSE,
    scholarship_percent INTEGER NOT NULL DEFAULT 0 CHECK (scholarship_percent IN (0, 100, 150, 200))
);

CREATE TABLE subjects (
    subject_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE group_subjects (
    group_subject_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES student_groups(group_id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    assessment_type TEXT NOT NULL CHECK (assessment_type IN ('exam', 'credit')),
    UNIQUE (group_id, subject_id)
);

CREATE TABLE session_results (
    result_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    group_subject_id INTEGER NOT NULL REFERENCES group_subjects(group_subject_id) ON DELETE CASCADE,
    grade INTEGER CHECK (grade BETWEEN 2 AND 5),
    credit_passed BOOLEAN,
    UNIQUE (student_id, group_subject_id),
    CHECK (
        (grade IS NOT NULL AND credit_passed IS NULL)
        OR
        (grade IS NULL AND credit_passed IS NOT NULL)
    )
);
