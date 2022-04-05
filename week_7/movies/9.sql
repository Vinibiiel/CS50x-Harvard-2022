SELECT name FROM people AS p
    INNER JOIN stars AS s ON s.person_id = p.id
    INNER JOIN movies AS m ON m.id = s.movie_id AND m.year = 2004 ORDER BY p.birth ASC;