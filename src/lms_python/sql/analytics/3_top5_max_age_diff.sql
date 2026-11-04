SELECT
    r.id   AS room_id,
    r.room_name,
    (
        MAX(EXTRACT(YEAR FROM AGE(s.birthday)))
        - MIN(EXTRACT(YEAR FROM AGE(s.birthday)))
    )::INT AS age_diff
FROM
    rooms AS r
    INNER JOIN
        students AS s
        ON r.id = s.room_id
GROUP BY
    r.id, r.room_name
ORDER BY
    age_diff DESC,
    r.id ASC
LIMIT 5;
