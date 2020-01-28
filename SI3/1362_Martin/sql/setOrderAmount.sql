CREATE OR REPLACE FUNCTION setOrderAmount ()
RETURNS void AS $$
BEGIN
    UPDATE orders AS o
    SET netamount = CASE WHEN netamount IS NULL THEN
    (SELECT ROUND( SUM(price * quantity) :: numeric, 2) FROM orderdetail WHERE orderid=o.orderid)
    ELSE netamount END;
    UPDATE orders AS o
    SET totalamount = CASE WHEN totalamount IS NULL THEN
    (SELECT ROUND(netamount * (1+(tax/100)) :: numeric, 2) FROM orders WHERE orderid=o.orderid)
    ELSE totalamount END;
END;
$$ LANGUAGE plpgsql;


