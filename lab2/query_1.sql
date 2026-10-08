SELECT
    s.student_id,
    s.last_name,
    s.first_name,
    sg.group_number,
    sub.name AS subject_name,
    sr.grade
FROM students s
JOIN student_groups sg
    ON sg.group_id = s.group_id
JOIN specialties sp
    ON sp.specialty_id = sg.specialty_id
JOIN departments d
    ON d.department_id = sp.department_id
JOIN group_subjects gs
    ON gs.group_id = sg.group_id
JOIN subjects sub
    ON sub.subject_id = gs.subject_id
LEFT JOIN session_results sr
    ON sr.student_id = s.student_id
    AND sr.group_subject_id = gs.group_subject_id
WHERE d.name = 'Кафедра програмної інженерії'
  AND gs.assessment_type = 'exam'
  AND (sr.grade = 2 OR sr.grade IS NULL)
ORDER BY
    s.last_name,
    sub.name;
    