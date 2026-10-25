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
    permanent_city TEXT NOT NULL,
    permanent_street TEXT NOT NULL,
    permanent_building TEXT NOT NULL,
    current_city TEXT NOT NULL,
    current_street TEXT NOT NULL,
    current_building TEXT NOT NULL,
    scholarship_percent INTEGER NOT NULL DEFAULT 0
        CHECK (scholarship_percent IN (0, 100, 150, 200))
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

CREATE FUNCTION check_result_type() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
    control_type TEXT;
BEGIN
    SELECT assessment_type INTO control_type
    FROM group_subjects
    WHERE group_subject_id = NEW.group_subject_id;

    IF (control_type = 'exam' AND NEW.grade IS NULL)
       OR (control_type = 'credit' AND NEW.credit_passed IS NULL) THEN
        RAISE EXCEPTION 'Result does not match assessment type';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER check_result_type_trigger
BEFORE INSERT OR UPDATE ON session_results
FOR EACH ROW EXECUTE FUNCTION check_result_type();

CREATE FUNCTION check_result_group() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM students s
        JOIN group_subjects gs ON gs.group_id = s.group_id
        WHERE s.student_id = NEW.student_id
          AND gs.group_subject_id = NEW.group_subject_id
    ) THEN
        RAISE EXCEPTION 'Student and subject must belong to the same group';
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER check_result_group_trigger
BEFORE INSERT OR UPDATE ON session_results
FOR EACH ROW EXECUTE FUNCTION check_result_group();


CREATE FUNCTION transfer_student_results() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.group_id = OLD.group_id THEN
        RETURN NEW;
    END IF;

    IF EXISTS (
        SELECT 1
        FROM session_results sr
        JOIN group_subjects old_gs
            ON old_gs.group_subject_id = sr.group_subject_id
        WHERE sr.student_id = NEW.student_id
          AND NOT EXISTS (
              SELECT 1
              FROM group_subjects new_gs
              WHERE new_gs.group_id = NEW.group_id
                AND new_gs.subject_id = old_gs.subject_id
                AND new_gs.assessment_type = old_gs.assessment_type
          )
    ) THEN
        RAISE EXCEPTION 'Resolve unmatched subjects before transfer';
    END IF;

    UPDATE session_results sr
    SET group_subject_id = new_gs.group_subject_id
    FROM group_subjects old_gs
    JOIN group_subjects new_gs
        ON new_gs.subject_id = old_gs.subject_id
       AND new_gs.assessment_type = old_gs.assessment_type
       AND new_gs.group_id = NEW.group_id
    WHERE sr.student_id = NEW.student_id
      AND sr.group_subject_id = old_gs.group_subject_id;

    RETURN NEW;
END;
$$;

CREATE TRIGGER transfer_student_results_trigger
AFTER UPDATE OF group_id ON students
FOR EACH ROW EXECUTE FUNCTION transfer_student_results();