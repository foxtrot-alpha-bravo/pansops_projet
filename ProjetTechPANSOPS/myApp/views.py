from flask import Flask, render_template, redirect, session, request
from myApp.model import bdd
from myApp.controller import function as f
import random,hashlib,datetime,locale
from dateutil.relativedelta import relativedelta
locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

app=Flask(__name__)
app.template_folder='template'
app.static_folder='static'
app.config.from_object('myApp.config')

@app.route("/")
def index():
    listeAgents=bdd.get_data()
    listeMAC=bdd.get_actionsMAC_data()
    params={'listeAgents':listeAgents,'listeMAC':listeMAC}
    params=f.messageInfo(params)
    
    return render_template('index.html', **params)

@app.route("/add_formation_MAC",methods=['POST'])
def add_formation_MAC():
    id_agent=request.form['id_agent']
    id_maintien_competences=request.form['id_maintien_competences']
    date_participation_agent=request.form['date_participation_agent']
    bdd.add_formation_MAC(id_agent,id_maintien_competences,date_participation_agent)
    return redirect('/')
    

@app.route('/add_agent',methods=['POST'])
def ajoutagent():
    nom=request.form['nom']
    prenom=request.form['prenom']
    date_naissance=request.form['date_naissance']
    tel=request.form['tel']
    date_fin_formation=request.form['date_fin_formation']
    bdd.add_agent(nom,prenom,date_naissance,tel,date_fin_formation)
    return redirect('/')