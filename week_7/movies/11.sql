SELECT title FROM movies AS m
    INNER JOIN ratings AS r ON r.movie_id = m.id
    INNER JOIN stars AS s ON m.id = s.movie_id
    INNER JOIN people AS p ON p.id = s.person_id
    AND p.name LIKE 'Chadwick Boseman'
    ORDER BY r.rating DESC
    LIMIT 0,5;
