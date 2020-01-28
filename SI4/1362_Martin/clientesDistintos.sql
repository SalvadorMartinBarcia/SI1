CREATE INDEX indice_orders
ON orders(EXTRACT(YEAR FROM orderdate), EXTRACT(MONTH FROM orderdate))

EXPLAIN SELECT COUNT(DISTINCT customerid)
FROM orders
WHERE EXTRACT(YEAR FROM orderdate) = 2015
    AND EXTRACT(MONTH FROM orderdate) = 04
    AND totalamount >= 100

