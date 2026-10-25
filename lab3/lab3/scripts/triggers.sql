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
