CREATE OR REPLACE FUNCTION getTopMonths (numeric, numeric)
RETURNS TABLE(
    anyo INTEGER,
    mes INTEGER,
    importe numeric,
    productos BIGINT
) AS $$
DECLARE
productos ALIAS FOR $1;
importe ALIAS FOR $2;
BEGIN
    RETURN QUERY 
    SELECT CAST(EXTRACT(YEAR FROM orderdate) AS INTEGER), CAST(EXTRACT(MONTHS FROM orderdate) AS INTEGER), SUM(totalamount) AS precio, SUM(quantity) AS cantidad
    FROM orders NATURAL JOIN orderdetail
    GROUP BY EXTRACT(YEAR FROM orderdate), EXTRACT(MONTHS FROM orderdate)
    HAVING SUM(totalamount) > importe or SUM(quantity) > productos
    ORDER BY EXTRACT(YEAR FROM orderdate), EXTRACT(MONTHS FROM orderdate);
END;
$$ LANGUAGE plpgsql;