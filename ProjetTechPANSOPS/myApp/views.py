from flask import Flask, render_template, redirect, session, request
from myApp.model import bdd
from myApp.controller import function as f
import random,hashlib,datetime,locale
locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

app=Flask(__name__)
app.template_folder='template'
app.static_folder='static'
app.config.from_object('myApp.config')

@app.route("/")
def index():
    listeAgents=bdd.get_data()
    params={'listeAgents':listeAgents}
    params=f.messageInfo(params)
    return render_template('index.html', **params)

@app.route('/add_agent',methods=['POST'])
def ajoutanomalie():
    nom=request.form['nom']
    prenom=request.form['prenom']
    date_naissance=request.form['date_naissance']
    tel=request.form['tel']
    date_fin_formation=request.form['date_fin_formation']
    bdd.add_agent(nom,prenom,date_naissance,tel,date_fin_formation)
    return redirect('/')

