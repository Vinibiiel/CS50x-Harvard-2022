SELECT name
FROM people AS p,movies AS m,stars AS s
WHERE m.id = s.movie_id AND s.person_id = p.id AND m.title LIKE "%Toy Story%";