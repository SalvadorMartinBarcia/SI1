CREATE OR REPLACE FUNCTION getTopVentas (numeric)
RETURNS TABLE(
    id integer,
    titulo character varying(255),
    ventas double precision,
    vendidas bigint
) AS $$
DECLARE
dato ALIAS FOR $1;
BEGIN
    RETURN QUERY with movie_number_year AS
(SELECT year, movieid, movietitle, SUM(quantity) AS cantidad, EXTRACT(YEAR FROM orderdate) AS anyo_venta
    FROM imdb_movies NATURAL JOIN (products INNER JOIN orderdetail ON products.prod_id = orderdetail.prod_id) NATURAL JOIN orders
    GROUP BY (movieid, anyo_venta)
),
most_vendidas AS
(SELECT anyo_venta, MAX(cantidad) AS times
	FROM movie_number_year
	group by anyo_venta
)
select im.movieid, im.movietitle, most.anyo_venta, times
FROM most_vendidas most, movie_number_year numb, imdb_movies im
WHERE most.times = numb.cantidad AND most.anyo_venta = numb.anyo_venta AND
numb.movieid= im.movieid AND most.anyo_venta>=dato
order by most.anyo_venta;
END;
$$ LANGUAGE plpgsql;