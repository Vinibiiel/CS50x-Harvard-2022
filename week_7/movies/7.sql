SELECT m.title,r.rating
 FROM movies AS m, ratings AS r
 WHERE year = 2010 AND m.id = r.movie_id ORDER BY r.rating DESC, m.title ASC;