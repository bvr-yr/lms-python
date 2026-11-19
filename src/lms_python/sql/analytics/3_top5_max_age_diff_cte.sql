WITH
    students_age AS (
        SELECT
            room_id,
            EXTRACT(
                YEAR FROM AGE(birthday)
            )::INT AS age
        FROM
            students
    )

SELECT
    r.id                    AS room_id,
    r.room_name,
    MAX(s.age) - MIN(s.age) AS age_diff
FROM
    rooms AS r
    INNER JOIN
        students_age AS s
        ON r.id = s.room_id
GROUP BY
    r.id, r.room_name
ORDER BY
    age_diff DESC,
    r.id ASC
LIMIT 5;
