SELECT
    r.id             AS room_id,
    r.room_name,
    COUNT(s.room_id) AS students_count
FROM
    rooms AS r
    LEFT JOIN
        students AS s
        ON r.id = s.room_id
GROUP BY
    r.id, r.room_name
ORDER BY
    r.id ASC;
