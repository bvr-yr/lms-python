SELECT
    r.id AS room_id,
    r.room_name
FROM
    rooms AS r
    INNER JOIN
        students AS s
        ON r.id = s.room_id
GROUP BY
    r.id, r.room_name
HAVING COUNT(DISTINCT s.gender) = 2
ORDER BY
    r.id ASC;
