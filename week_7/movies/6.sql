SELECT avg(r.rating)
FROM ratings AS r,movies AS m
WHERE m.year = 2012 AND r.movie_id = m.id;