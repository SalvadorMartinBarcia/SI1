UPDATE orderdetail
SET price = (
    SELECT ROUND( product.price/1.02^(EXTRACT (YEAR FROM NOW()) - EXTRACT (YEAR FROM orderdate)) :: numeric, 2)
    FROM products product, orders o
    WHERE o.orderid=orderdetail.orderid and product.prod_id=orderdetail.prod_id
);