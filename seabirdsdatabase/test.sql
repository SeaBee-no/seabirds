SELECT * FROM files WHERE filetype = 'image/jpeg' and datetimeoriginal BETWEEN '2022-06-09' AND '2022-06-10';
SELECT st_y(geom) as lat, st_x(geom) as lon FROM files LIMIT 100;
SELECT DISTINCT(mission) FROM files;