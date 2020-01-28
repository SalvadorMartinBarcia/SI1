#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, make_response
from hashlib import md5
import json
import os
import sys
from random import randint
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    categoria = []
    peliculasaux = []
    peliculas = []
    for elemento in catalogue['peliculas']:
        if elemento['categoria'] not in categoria:
            categoria.append(elemento['categoria'])

    if request.method == 'POST' and (request.form['barraBusq'] != "" or request.form['genero'] != "0"):
        for element in catalogue['peliculas']:
            if request.form['barraBusq'].lower() in element['titulo'].lower():
                peliculasaux.append(element)
        if request.form['genero'] == "0":
                peliculas=peliculasaux
        else:
            for element in peliculasaux:
                if request.form['genero'] == element['categoria']:
                    peliculas.append(element)

        return render_template('index.html', title = "Inicio", movies=peliculas, generos=categoria)
        
    else:
        return render_template('index.html', title = "Inicio", movies=catalogue['peliculas'], generos=categoria)
    

@app.route('/carro')
def carro():
    carro=[]
    total = 0
    if 'carro' in session:
        carro=session['carro']
        for elemento in carro:
            total+=elemento['precio']
    return render_template('carro.html', title = "Carro", movies=carro, precio=total)

@app.route('/ancarro')
def ancarro():
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

@app.route('/elimcarro')
def elimcarro():
    carro=session['carro']
    id = int(request.args.get('id'))
    for elemento in carro:
        if str(elemento['id']) == str(id):
            carro.remove(elemento)
            session['carro']=carro
            session.modified=True
            return redirect(url_for('carro'))
    return redirect(url_for('carro'))

@app.route('/confcarro')
def confcarro():
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

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    historial = {}
    historial['peliculas'] = []
    if request.method == 'POST':
        userdir = "usuarios/" + request.form['NombUsInname']
        if os.path.exists(os.path.join(app.root_path,userdir)) == False:
            os.mkdir(os.path.join(app.root_path,userdir))

            userdir = os.path.join(app.root_path,userdir)
            userdat = os.path.join(userdir,"data.dat")

            historialJason = open(os.path.join(userdir,'historial.json'), "w",encoding="utf-8")
            json.dump(historial, historialJason, indent=4)
            historialJason.close()

            file = open(userdat, "w")
            file.write(request.form['NombUsInname'] + os.linesep)
            file.write(md5(request.form['ContInname'].encode("utf-8")).hexdigest() + os.linesep)
            file.write(request.form['EmaiIlnname'] + os.linesep)
            file.write(request.form['TarInname'] + os.linesep)
            file.write(str(randint(0, 100)))
            file.close()
            return redirect(url_for('index'))
        else:
            return render_template('registrarse.html', title = "Registrarse", errormsg ="El usuario ya existe")
    return render_template('registrarse.html', title = "Registrarse")

@app.route('/detalle')
def detalle():
    id = int(request.args.get('id'))
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    for elemento in catalogue['peliculas']:
        if elemento["id"] == id:
            return render_template('detalle.html', title = "Detalle", peli=elemento)
    return redirect(url_for('index'))

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
        userdir = "usuarios/" + request.form['username']
        userdir = os.path.join(app.root_path,userdir)
        if os.path.exists(userdir):
            userdat = os.path.join(userdir,"data.dat")
            file = open(userdat, "r")
            lineas = file.readlines()
            if lineas[1] == (md5(request.form['password'].encode("utf-8")).hexdigest() + "\n"):
                session['usuario'] = request.form['username']
                session.modified=True
                file.close()
                return redirect(url_for('index'))
            file.close()

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
    return str(randint(1, 420))