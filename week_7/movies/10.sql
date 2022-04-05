SELECT name FROM people AS p
    INNER JOIN directors AS d ON d.person_id = p.id
    INNER JOIN ratings AS r ON d.movie_id = r.movie_id AND r.rating >= 9;