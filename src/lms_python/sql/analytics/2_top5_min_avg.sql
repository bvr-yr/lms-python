SELECT
    r.id     AS room_id,
    r.room_name,
    ROUND(
        AVG(
            EXTRACT(
                YEAR FROM AGE(s.birthday)
            )
        ), 2
    )::FLOAT AS avg_student_age
FROM
    rooms AS r
    INNER JOIN
        students AS s
        ON r.id = s.room_id
GROUP BY
    r.id, r.room_name
ORDER BY
    avg_student_age ASC,
    r.id ASC
LIMIT 5;
