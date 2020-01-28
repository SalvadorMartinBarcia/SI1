# -*- coding: utf-8 -*-

import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select
from random import randint

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# cargar una tabla
db_table_movies = Table('imdb_movies', db_meta, autoload=True, autoload_with=db_engine)

def db_pelisIndex():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "select * FROM imdb_movies JOIN getTopVentas(2013) ON imdb_movies.movieid=getTopVentas.id"
        db_result = db_conn.execute(db_Index)
        
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_pelisTotal():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "select movieid id, movietitle titulo, genero, year anyo FROM imdb_movies NATURAL JOIN imdb_moviegenres NATURAL JOIN generos"
        db_result = db_conn.execute(db_Index)
        
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_getGeneros():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_genero = "select genero from generos"
        db_result = db_conn.execute(db_genero)
        
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_product(id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "select prod_id id, price precio, description FROM products where movieid=" + str(id)
        db_result = db_conn.execute(db_Index)
        
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_login(correo, password):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "select email correo, password FROM customers where email='" + str(correo) + "' AND password ='" + str(password) + "'"
        db_result = db_conn.execute(db_Index)
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_check_Reg(correo):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "select email correo FROM customers where email='" + str(correo) + "'"
        db_result = db_conn.execute(db_Index)
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_registrarse(correo, usuario, password, tarjeta):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        id=db_maxID()
        max_id=id[0][0]
        max_id+=1
        
        db_Index = "INSERT INTO customers (customerid, email, username, password, creditcard, income)\
            VALUES ("+str(max_id)+", '"+correo+"', '"+usuario+"', '"+password+"', '"+tarjeta+"', "+str(randint(0, 100))+") "
        db_conn.execute(db_Index)
        
        db_conn.close()
        return
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_maxID():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "SELECT MAX(customerid) AS max_id FROM customers"
        db_result = db_conn.execute(db_Index)
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_carro(correo):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "SELECT prod_id, movietitle titulo, description tipo, orderdetail.price precio, quantity cantidad, totalamount preciototal\
        from customers NATURAL JOIN orders NATURAL JOIN orderdetail NATURAL JOIN products NATURAL JOIN imdb_movies\
        WHERE customers.email='"+correo+"' AND\
        orders.status is NULL"
        db_result = db_conn.execute(db_Index)
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_ancarro(product, movieid, correo):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        orderid=db_haycarro(correo)
        customerid=db_getcustomerid(correo)
        customerid=customerid[0][0]
        if len(orderid)>0:
            orderid=orderid[0][0]
        else:
            orderid=db_maxID_order()
            orderid=orderid[0][0]
            orderid+=1
            db_Index = "INSERT INTO orders (orderid, orderdate, customerid, tax)\
            VALUES ("+str(orderid)+", CURRENT_DATE, "+str(customerid)+", 21) "
            db_conn.execute(db_Index)

        prod=db_getprodid(movieid, product)
        prod_id=prod[0][0]
        price=prod[0][1]

        quantity=db_hayproducto_order(orderid, prod_id)
        if len(quantity)>0:
            quantity=quantity[0][0]
            quantity+=1
            db_Index = "UPDATE orderdetail SET quantity="+str(quantity)+" WHERE orderid="+str(orderid)+" AND prod_id="+str(prod_id)
            db_conn.execute(db_Index)
            print("SADKFMKAS")

        else:
            db_Index = "INSERT INTO orderdetail (orderid, prod_id, price, quantity)\
                VALUES ("+str(orderid)+", "+str(prod_id)+", "+str(price)+", 1) "
            db_conn.execute(db_Index)
        
        db_conn.close()
        return
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_elimcarro(prod_id, correo):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        orderid=db_haycarro(correo)
        orderid=orderid[0][0]
        
        quantity=db_hayproducto_order(orderid, prod_id)
        quantity=quantity[0][0]
        if quantity == 1:
            db_Index = "DELETE FROM orderdetail where orderid="+str(orderid)+" AND prod_id="+str(prod_id)
            db_conn.execute(db_Index)
        else:
            quantity-=1
            db_Index = "UPDATE orderdetail SET quantity="+str(quantity)+" WHERE orderid="+str(orderid)+" AND prod_id="+str(prod_id)
            db_conn.execute(db_Index)
        
        db_conn.close()
        
        return
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_haycarro(correo):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "select orderid from orders NATURAL JOIN customers where email='"+correo+"' AND orders.status is NULL"
        db_result = db_conn.execute(db_Index)
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_hayproducto_order(orderid, prod_id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "select quantity from orderdetail where orderid='"+str(orderid)+"' AND prod_id='"+str(prod_id)+"'"
        db_result = db_conn.execute(db_Index)
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_getcustomerid(correo):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "select customerid from customers where email='"+correo+"'"
        db_result = db_conn.execute(db_Index)
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_getprodid(movieid, prodtype):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "select prod_id, price from products where movieid='"+movieid+"' AND description='"+prodtype+"'"
        db_result = db_conn.execute(db_Index)
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_maxID_order():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        
        db_Index = "SELECT MAX(orderid) AS max_id FROM orders"
        db_result = db_conn.execute(db_Index)
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

#desist.bevy@kran.com erase