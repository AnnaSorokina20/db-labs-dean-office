SELECT
    s.student_id,
    s.last_name,
    s.first_name,
    sg.group_number,
    CASE
        WHEN MIN(sr.grade) = 5 THEN 200

        WHEN COUNT(*) FILTER (WHERE sr.grade = 3) = 0
             AND COUNT(*) FILTER (WHERE sr.grade = 4) <= 2
            THEN 150

        ELSE 100
    END AS scholarship_percent
FROM students s
JOIN student_groups sg
    ON sg.group_id = s.group_id
JOIN specialties sp
    ON sp.specialty_id = sg.specialty_id
JOIN departments d
    ON d.department_id = sp.department_id
JOIN group_subjects gs
    ON gs.group_id = sg.group_id
    AND gs.assessment_type = 'exam'
LEFT JOIN session_results sr
    ON sr.student_id = s.student_id
    AND sr.group_subject_id = gs.group_subject_id
WHERE d.name = 'Кафедра програмної інженерії'
GROUP BY
    s.student_id,
    s.last_name,
    s.first_name,
    sg.group_number,
    s.permanent_city
HAVING
    COUNT(sr.grade) = COUNT(gs.group_subject_id)

    AND MIN(sr.grade) >= 3

    AND (
        COUNT(*) FILTER (WHERE sr.grade = 3) = 0

        OR (
            s.permanent_city <> 'Харків'
            AND COUNT(*) FILTER (WHERE sr.grade = 3) <= 1
        )
    )
ORDER BY s.last_name;