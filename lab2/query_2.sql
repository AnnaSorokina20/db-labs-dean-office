SELECT
    sg.group_number,
    ROUND(AVG(sr.grade), 2) AS average_grade
FROM student_groups sg
JOIN specialties sp
    ON sp.specialty_id = sg.specialty_id
JOIN departments d
    ON d.department_id = sp.department_id
JOIN faculties f
    ON f.faculty_id = d.faculty_id
JOIN students s
    ON s.group_id = sg.group_id
JOIN session_results sr
    ON sr.student_id = s.student_id
JOIN group_subjects gs
    ON gs.group_subject_id = sr.group_subject_id
WHERE f.name = 'Факультет комп''ютерних наук'
  AND gs.assessment_type = 'exam'
  AND sr.grade IS NOT NULL
GROUP BY sg.group_number
ORDER BY sg.group_number;