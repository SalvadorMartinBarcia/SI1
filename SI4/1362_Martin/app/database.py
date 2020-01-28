# -*- coding: utf-8 -*-

import os
import sys, traceback, time

from sqlalchemy import create_engine

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()

def getListaCliMes(db_conn, mes, anio, iumbral, iintervalo, use_prepare, break0, niter):

    # implementar la consulta; asignar nombre 'cc' al contador resultante
    
    
    
    # TODO: ejecutar la consulta 
    # - mediante PREPARE, EXECUTE, DEALLOCATE si use_prepare es True
    # - mediante db_conn.execute() si es False

    # Array con resultados de la consulta para cada umbral
    dbr=[]
    if use_prepare:

        consulta = " PREPARE getCliMes (int) AS \
                SELECT COUNT(DISTINCT customerid) as cc\
                FROM orders\
                WHERE EXTRACT(YEAR FROM orderdate) = "+anio+"\
                AND EXTRACT(MONTH FROM orderdate) = "+mes+"\
                AND totalamount >= $1"

        db_result = db_conn.execute(consulta)

        for ii in range(niter):

            db_result = db_conn.execute("EXECUTE getCliMes("+str(iumbral)+")")

            res = db_result.fetchall()[0][0]

            # Guardar resultado de la query
            dbr.append({"umbral":iumbral,"contador":res})#igual quito el cc

            # TODO: si break0 es True, salir si contador resultante es cero
            if break0 and res == 0:
                break
            
            # Actualizacion de umbral
            iumbral = iumbral + iintervalo

        db_result = db_conn.execute("DEALLOCATE getCliMes")
    
    else:

        for ii in range(niter):

            db_result = db_conn.execute("SELECT COUNT(DISTINCT customerid) as cc\
                FROM orders\
                WHERE EXTRACT(YEAR FROM orderdate) = "+anio+"\
                AND EXTRACT(MONTH FROM orderdate) = "+mes+"\
                AND totalamount >= "+str(iumbral)+"")

            res = db_result.fetchall()[0][0]

            # Guardar resultado de la query
            dbr.append({"umbral":iumbral,"contador":res})#igual quito el cc

            # TODO: si break0 es True, salir si contador resultante es cero
            if break0 and res == 0:
                break
            
            # Actualizacion de umbral
            iumbral = iumbral + iintervalo
                
    return dbr

def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy=db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d={}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)
        
    resultproxy.close()  
    
    db_conn.close()  
    
    return a
    
def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select * from customers where username='" + username + "' and password='" + password + "'"
    res=db_conn.execute(query).first()
    
    db_conn.close()  

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}
    
def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):
    
    # Array de trazas a mostrar en la página
    dbr=[]
    db_conn = dbConnect()

    # TODO: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()
    db_result = db_conn.execute("SELECT * FROM customers WHERE customerid="+customerid)
    if len(db_result.fetchall()) == 0:
        dbr.append("No hay un usuario con el id: "+customerid)
        dbCloseConnect(db_conn)
        return dbr

    if bFallo is True and bCommit is True and bSQL is True: # Hecho
        try:
            # drop de customers
            db_result = db_conn.execute("begin; delete from orderdetail using orders where orders.orderid = orderdetail.orderid and orders.customerid = "+customerid+";commit;")
            dbr.append("BEGIN->DELETE ORDERDETAIL->COMMIT")

            db_result = db_conn.execute("begin; delete from customers where customerid = "+customerid+";commit;")
            dbr.append("BEGIN->DELETE CUSTOMERS->COMMIT")

        except Exception as e:
            db_result = db_conn.execute("rollback;")
            dbr.append("ROLLBACK")
        else:
            print("Error con bFallo==true, bCommit==true, bSQL==true")

    elif bFallo is True and bCommit is False and bSQL is True: # Hecho
        try:
            db_result = db_conn.execute("begin; delete from customers where customerid = "+customerid)
            dbr.append("BEGIN->DELETE CUSTOMERS")

        except Exception as e:
            db_result = db_conn.execute("rollback;")
            dbr.append("ROLLBACK")

        else:
            db_result = db_conn.execute("commit;")
            print("Error con bFallo==true, bCommit==false, bSQL==true")

    elif bFallo is False and bCommit is True and bSQL is True: # Hecho
        try:
            db_result = db_conn.execute("begin;delete from orderdetail using orders where orders.orderid = orderdetail.orderid and orders.customerid = "+customerid+";commit;")
            dbr.append("BEGIN->DELETE ORDERDETAIL->COMMIT")
            db_result = db_conn.execute("begin;delete from orders where customerid = "+customerid+";commit;")
            dbr.append("BEGIN->DELETE ORDERS->COMMIT")
            
            db_result = db_conn.execute("begin;delete from customers where customerid = "+customerid+";commit;")
            dbr.append("BEGIN->DELETE CUSTOMERS->COMMIT")
        except Exception as e:
            db_result = db_conn.execute("ROLLBACK;")
            dbr.append("ROLLBACK")
        else:
            print("Bien")

    elif bFallo is False and bCommit is False and bSQL is True: # Hecho
        try:
            db_result = db_conn.execute("begin;delete from orderdetail using orders where orders.orderid = orderdetail.orderid and orders.customerid = "+customerid+";")
            dbr.append("BEGIN->DELETE ORDERDETAIL")
            db_result = db_conn.execute("delete from orders where customerid = "+customerid+";")
            dbr.append("DELETE ORDERS")

            db_result = db_conn.execute("delete from customers where customerid = "+customerid+";")
            dbr.append("DELETE CUSTOMERS")

        except Exception as e:
            db_result = db_conn.execute("rollback;")
            dbr.append("ROLLBACK")

        else:
            db_result = db_conn.execute("commit;")
            dbr.append("COMMIT")

    
    elif bFallo is True and bCommit is True and bSQL is False: # Hecho
        try:
            db = db_conn.begin()
            db_result = db_conn.execute("delete from orderdetail using orders where orders.orderid = orderdetail.orderid and orders.customerid = "+customerid)
            db.commit()
            dbr.append("BEGIN->DELETE ORDERDETAIL->COMMIT")

            db = db_conn.begin()
            db_result = db_conn.execute("delete from customers where customerid = "+customerid)
            db.commit()

        except Exception as e:
            db.rollback()
            dbr.append("ROLLBACK")

        else:
           print("Error con bFallo==true, bCommit==false, bSQL==true")

    elif bFallo is True and bCommit is False and bSQL is False: # Hecho
        try:
            db = db_conn.begin()
            db_result = db_conn.execute("begin; delete from customers where customerid = "+customerid)
            dbr.append("BEGIN->DELETE CUSTOMERS")

        except Exception as e:
            db.rollback()
            dbr.append("ROLLBACK")

        else:
            db.commit()
            print("Error con bFallo==true, bCommit==false, bSQL==false")

    elif bFallo is False and bCommit is True and bSQL is False: # Hecho
        try:
            db = db_conn.begin()
            db_result = db_conn.execute("delete from orderdetail using orders where orders.orderid = orderdetail.orderid and orders.customerid = "+customerid+";")
            db.commit()
            dbr.append("BEGIN->DELETE ORDERDETAIL->COMMIT")
            
            db = db_conn.begin()
            db_result = db_conn.execute("delete from orders where customerid = "+customerid+";")
            db.commit()
            dbr.append("BEGIN->DELETE ORDERS->COMMIT")
            
            db = db_conn.begin()
            db_result = db_conn.execute("delete from customers where customerid = "+customerid+";")
            db.commit()
            dbr.append("BEGIN->DELETE CUSTOMERS->COMMIT")

        except Exception as e:
            db.rollback()
            dbr.append("ROLLBACK")

        else:
            print("Error con bFallo==false, bCommit==true, bSQL==false")

    elif bFallo is False and bCommit is False and bSQL is False: # Hecho
        try:
            db = db_conn.begin()
            db_result = db_conn.execute("delete from orderdetail using orders where orders.orderid = orderdetail.orderid and orders.customerid = "+customerid+";")
            dbr.append("BEGIN->DELETE ORDERDETAIL")
            db_result = db_conn.execute("delete from orders where customerid = "+customerid+";")
            dbr.append("DELETE ORDERS")

            db_result = db_conn.execute("delete from customers where customerid = "+customerid+";")
            dbr.append("DELETE CUSTOMERS")

        except Exception as e:
            db.rollback()
            dbr.append("ROLLBACK")

        else:
            db.commit()
            dbr.append("COMMIT")

    #orderdetail using orders WHERE orderid =orderid and customerid="+customerid+"
    dbCloseConnect(db_conn)

    return dbr

