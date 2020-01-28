#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from app import database
from flask import render_template, request, url_for, redirect, session, make_response
import json
import os
import sys
from random import randint
from datetime import datetime
catalogue = database.db_pelisIndex()
pelis = database.db_pelisTotal()



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    categoria = []
    peliculasaux = []
    peliculas = []
    categoria_aux = database.db_getGeneros()
    for elemento in categoria_aux:
        categoria.append(elemento[0])

    if request.method == 'POST' and (request.form['barraBusq'] != "" or request.form['genero'] != "0"):
        for element in pelis:
            flag=0
            if request.form['barraBusq'].lower() in element['titulo'].lower():
                for elemento2 in peliculasaux:
                    if element['titulo']==elemento2['titulo']:
                        flag=1
                if flag==0:
                    peliculasaux.append(element)
        if request.form['genero'] == "0":
                peliculas=peliculasaux
        else:
            for element in peliculasaux:
                if request.form['genero'] == element['genero']:
                    peliculas.append(element)

        return render_template('index.html', title = "Inicio", movies=peliculas, generos=categoria)
        
    else:
        return render_template('index.html', title = "Inicio", movies=catalogue, generos=categoria)

@app.route('/detalle', methods=['GET', 'POST'])
def detalle():
    id = int(request.args.get('id'))
    generos = []
    productos = []
    productos = database.db_product(id)

    if request.method == "POST":
        ancarro(request.form['product'])

    for elemento in pelis:
        if elemento["id"]==id:
            generos.append(elemento["genero"])
    for elemento in pelis:
        if elemento["id"] == id:
            return render_template('detalle.html', title = "Detalle", peli=elemento, generos=generos, productos=productos)
    return redirect(url_for('index'))
    

@app.route('/carro')
def carro():
    if 'usuario' not in session:
        carro=[]
        total = 0
        if 'carro' in session:
            carro=session['carro']
            for elemento in carro:
                total+=elemento['precio']
        return render_template('carro.html', title = "Carro", movies=carro, precio=total)
    else:
        carro=[]
        carro = database.db_carro(session['usuario'])
        if len(carro)>0:
            total = carro[0][5]
        else:
            total = 0
        return render_template('carro.html', title = "Carro", movies=carro, precio=total)

@app.route('/ancarro')
def ancarro(product):
    if 'usuario' not in session:
        catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
        catalogue = json.loads(catalogue_data)
        if 'carro' not in session:
            session['carro'] = []
        carro=session['carro']
        id = int(request.args.get('id'))
        for elemento in catalogue['peliculas']:
            if str(elemento['id']) == str(id):
                carro.append(elemento)
                session['carro']=carro
                session.modified=True
        return redirect(url_for('index'))
    else:
        movieid=request.args.get('id')
        database.db_ancarro(product, movieid, session['usuario'])
        return redirect(url_for('index'))

@app.route('/elimcarro')
def elimcarro():
    if 'usuario' not in session:
        carro=session['carro']
        id = int(request.args.get('id'))
        for elemento in carro:
            if str(elemento['id']) == str(id):
                carro.remove(elemento)
                session['carro']=carro
                session.modified=True
                return redirect(url_for('carro'))
        return redirect(url_for('carro'))
    else:
        prod_id=request.args.get('id')
        database.db_elimcarro(prod_id,  session['usuario'])
        return redirect(url_for('carro'))


@app.route('/confcarro')
def confcarro():
    if 'usuario' not in session:
        if 'usuario' not in session:
            return redirect(url_for('login'))
        if 'carro' not in session:
            return redirect(url_for('carro'))

        carro=session['carro']
        userdir = "usuarios/" + session['usuario']
        userdir = os.path.join(app.root_path,userdir)

        catalogue_data = open(os.path.join(userdir,'historial.json'), encoding="utf-8").read()
        historial = json.loads(catalogue_data)

        file = open(os.path.join(userdir,'data.dat'), "r")
        lineas = file.readlines()
        dineroU = int(lineas[4])
        file.close()

        dineroTo=0
        for elemento in carro:
            dineroTo+=elemento['precio']
        if dineroU < dineroTo:
            return redirect(url_for('carro'))

        now=datetime.now()
        for elemento in carro:
            elemento['fecha'] = now.strftime('%d/%m/%Y %H:%M:%S')
            historial['peliculas'].append(elemento)
        session.pop('carro', None)

        historialJason = open(os.path.join(userdir,'historial.json'), "w",encoding="utf-8")
        json.dump(historial, historialJason, indent=4)
        historialJason.close()

        dineroU-=dineroTo
        lineas[4]=str(dineroU)

        file = open(os.path.join(userdir,'data.dat'), "w")
        file.writelines(lineas)
        file.close()

        return redirect(url_for('index'))
    else:
        return redirect(url_for('carro'))

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    historial = {}
    historial['peliculas'] = []
    if request.method == 'POST':
        usuario = request.form['NombUsInname']
        correo = request.form['EmaiIlnname']
        password = request.form['ContInname']
        tarjeta = request.form['TarInname']
        if len(database.db_check_Reg(correo)) <= 0:
            database.db_registrarse(correo, usuario, password, tarjeta)

            return redirect(url_for('index'))
        else:
            return render_template('registrarse.html', title = "Registrarse", errormsg ="El usuario ya existe")
    return render_template('registrarse.html', title = "Registrarse")

@app.route('/historial', methods=['GET', 'POST'])
def historial():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    userdir = "usuarios/" + session['usuario']
    userdir = os.path.join(app.root_path,userdir)
    userdat = os.path.join(userdir,"data.dat")
    file = open(userdat, "r")
    lineas = file.readlines()
    dineroU = int(lineas[4])
    file.close()
    if request.method == 'POST':

        dineroU+=int(request.form['saldo'])
        lineas[4]=str(dineroU)

        file = open(os.path.join(userdir,'data.dat'), "w")
        file.writelines(lineas)
        file.close()

    catalogue_data = open(os.path.join(userdir,'historial.json'), encoding="utf-8").read()
    historial = json.loads(catalogue_data)
    return render_template('historial.html', title = "Historial", historial=historial['peliculas'], dinero=dineroU)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        correo = request.form['username']
        password = request.form['password']
        query=database.db_login(correo, password)
        if len(query)<=0:
            return render_template('login.html', title = "Inicio de sesion", nombre = request.cookies.get('userID'))
        else:
            session['usuario'] = correo
            session.modified=True
            return redirect(url_for('index'))
    return render_template('login.html', title = "Inicio de sesion", nombre = request.cookies.get('userID'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('userID', session['usuario'])
    session.pop('usuario', None)
    session.pop('carro', None)
    return resp

@app.route('/genRand', methods=['GET', 'POST'])
def genRand():
    return str(randint(69, 420))

