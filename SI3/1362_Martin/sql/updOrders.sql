CREATE OR REPLACE FUNCTION updOrders() RETURNS TRIGGER AS $$
  BEGIN
    IF (TG_OP = 'INSERT') THEN
      UPDATE orders set netamount = 
      (SELECT ROUND(SUM(price * quantity) :: numeric, 2) 
      FROM orderdetail
      WHERE orderid=orders.orderid AND orderid=NEW.orderid);
      
      UPDATE orders set totalamount = 
      (SELECT ROUND(netamount * (1+(tax/100)) :: numeric, 2) 
      FROM orders 
      WHERE orderid=orders.orderid AND orderid=NEW.orderid);

      
    ELSIF (TG_OP = 'DELETE') THEN 
      UPDATE orders set netamount = 
      (SELECT ROUND(SUM(price * quantity) :: numeric, 2) 
      FROM orderdetail 
      WHERE orderid=orders.orderid AND orderid=OLD.orderid);
      
      UPDATE orders set totalamount = 
      (SELECT ROUND(netamount * (1+(tax/100)) :: numeric, 2) 
      FROM orders 
      WHERE orderid=orders.orderid AND orderid=OLD.orderid);

      
    ELSIF (TG_OP = 'UPDATE') THEN 
      UPDATE orders set netamount = 
      (SELECT ROUND(SUM(price * quantity) :: numeric, 2) 
      FROM orderdetail 
      WHERE orderid=orders.orderid AND orderid=OLD.orderid AND orderid=NEW.orderid);
      
      UPDATE orders set totalamount = 
      (SELECT ROUND(netamount * (1+(tax/100)) :: numeric, 2)
      FROM orders 
      WHERE orderid=orders.orderid AND orderid=NEW.orderid AND orderid=OLD.orderid);
    END IF;
  RETURN NEW;
  END;
  $$ LANGUAGE plpgsql;

CREATE TRIGGER updOrders AFTER INSERT OR DELETE OR UPDATE ON orderdetail
FOR EACH ROW EXECUTE PROCEDURE updOrders();