SELECT DISTINCT m.title FROM stars AS s
    INNER JOIN movies AS m ON m.id = s.movie_id
    INNER JOIN people AS p ON p.id = s.person_id
    WHERE p.name = "Johnny Depp"

INTERSECT

SELECT DISTINCT m.title FROM stars AS s
    INNER JOIN movies AS m ON m.id = s.movie_id
    INNER JOIN people AS p ON p.id = s.person_id
    WHERE p.name = "Helena Bonham Carter"