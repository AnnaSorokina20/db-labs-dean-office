SELECT
    sub.name AS subject_name,
    ROUND(AVG(sr.grade), 2) AS average_grade
FROM subjects sub
JOIN group_subjects gs
    ON gs.subject_id = sub.subject_id
JOIN session_results sr
    ON sr.group_subject_id = gs.group_subject_id
WHERE gs.assessment_type = 'exam'
  AND sr.grade IS NOT NULL
GROUP BY sub.name
ORDER BY sub.name;