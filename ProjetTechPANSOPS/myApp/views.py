from flask import Flask, render_template, redirect, session, request
from myApp.model import bdd
from myApp.controller import function as f
import random,hashlib,datetime,locale
from datetime import datetime
"""from dateutil.relativedelta import relativedelta"""
locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

app=Flask(__name__)
app.template_folder='template'
app.static_folder='static'
app.config.from_object('myApp.config')

@app.route("/")
def index():
    listeAgents=bdd.get_data()
    listeMAC=bdd.get_actionsMAC_data()
    listeMaint=bdd.get_dataMAINT()
    params={'listeAgents':listeAgents,'listeMAC':listeMAC,'listeMaint':listeMaint}
    
    params=f.messageInfo(params)
    for k in range(len(listeAgents)): #La fonction sera exécutée pour chaque agent 
        if listeAgents[k]["derniere_formation"]=='None' : #Si l'agent n'a aucune formation enregistrée
            listeAgents[k]['couleur'] = 'red' #La couleur revenant dans le dictionnaire est rouge, et sera affichée en conséquence
        else :
            date_ajour = datetime.today().date() #La variable est initialisée avec la date du jour
            date_form = datetime.strptime(listeAgents[k]["derniere_formation"], "%Y-%m-%d").date() #La date présente dans le dictionnaire est appellée par cette variable
            jours_ecart = (date_form - date_ajour).days #On recherche le nombre de jours entre la date de la dernière formation et la date du jour en faisant une soustraction entre les deux dates
            listeAgents[k]['jours_ecart'] = jours_ecart #La variable jours_ecart correspondant aux nombres de jours est incluse au dictionnaire
            
            #Une couleur est renvoyée en fonction du nombre de jours, qui reflétera l'urgence de la situation de l'agent
            if jours_ecart >= 365 :
                listeAgents[k]['couleur'] = 'vert'
            elif jours_ecart >= 180 :
                listeAgents[k]['couleur'] = 'jaune'
            elif jours_ecart >=0 :
                listeAgents[k]['couleur'] = 'orange'
            else :
                listeAgents[k]['couleur'] = 'rouge'
    for i in range(len(listeMaint)):
        listeMaint[i]['couleurM'] = 'None'
        if listeMaint[i]["derniere_formation_3"]=='None' :
            listeMaint[i]['couleurM'] = 'red'
        else : 
            date_maint = datetime.strptime(listeMaint[i]["derniere_formation_3"], "%Y-%m-%d").date()
            ecart_maint = (date_maint - date_ajour).days
            ecart_maint=ecart_maint + 730
            listeAgents[i]["jours_ecartM"]=ecart_maint
            if ecart_maint >= 365 :
                listeMaint[i]['couleurM'] = 'vert'
            elif ecart_maint >= 180 :
                listeMaint[i]['couleurM'] = 'jaune'
            elif ecart_maint >=0 :
                listeMaint[i]['couleurM'] = 'orange'
            else :
                listeMaint[i]['couleurM'] = 'rouge'
        listeAgents[i]['couleurM'] = listeMaint[i]['couleurM']
        print(listeMaint[i])

    return render_template('index2.html', **params)


@app.route('/detail_agent/<id_agents>')
def detailAgent(id_agents=''):
    detail_agent=bdd.get_actionsMAC_one_agent(id_agents)
    name_agent=bdd.get_name_one_agent(id_agents)
    params={'detail_agent':detail_agent,'name_agent':name_agent}
    return render_template('agent_data.html',**params)

@app.route("/update_data")
def update_data():
    listeAgents=bdd.get_data()
    listeMAC=bdd.get_actionsMAC_data()
    listeMaint=bdd.get_dataMAINT()
    params={'listeAgents':listeAgents,'listeMAC':listeMAC,'listeMaint':listeMaint}
    params=f.messageInfo(params)
    return render_template('update_data.html',**params)

@app.route('/updateData/<champ>',methods=['POST'])
def updateData(champ=None):
    idAgent=request.form['pk']
    newvalue=request.form['value']
    if champ=='Nom':
        bdd.update_AgentData('nom_agent',idAgent,newvalue)
    if champ=='Prenom':
        bdd.update_AgentData('prenom_agent',idAgent,newvalue)
    if champ=='DateNaissance':
        bdd.update_AgentData('date_naissance_agent',idAgent,newvalue)
    if champ=='Tel':
        bdd.update_AgentData('tel_agent',idAgent,newvalue)
    if champ=='FinFormationTH':
        bdd.update_AgentData('fin_formation_theorique_agent',idAgent,newvalue)
    if champ=='Statut':
        bdd.update_AgentData('statut_agent',idAgent,newvalue)
    return "Data succesfully updated"


@app.route("/add_formation_MAC",methods=['POST'])
def add_formation_MAC():
    id_agent=request.form['id_agent']
    id_maintien_competences=request.form['id_maintien_competences']
    date_participation_agent=request.form['date_participation_agent']
    commentaires=request.form['commentaires']
    bdd.add_formation_MAC(id_agent,id_maintien_competences,date_participation_agent,commentaires)
    return redirect('/')


@app.route("/form_add_agent")
def form_add_agent():
    listeAgents=bdd.get_data()
    listeMAC=bdd.get_actionsMAC_data()
    params={'listeAgents':listeAgents,'listeMAC':listeMAC}
    params=f.messageInfo(params)
    
    return render_template('login.html', **params)

@app.route('/add_agent',methods=['POST'])
def ajoutagent():
    nom=request.form['nom']
    prenom=request.form['prenom']
    date_naissance=request.form['date_naissance']
    tel=request.form['tel']
    date_fin_formation=request.form['date_fin_formation']
    debut_activite_enac=request.form['debut_activite_enac']
    s="abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    mdp = "".join(random.sample( s , 6 )) #6 = longueur du mot de passe
    mdpClair=mdp
    mdp=hashlib.sha256(mdp.encode())
    mdpC=mdp.hexdigest()
    bdd.add_agent(nom,prenom,date_naissance,tel,date_fin_formation,debut_activite_enac,mdpC)
    if "errorDB" not in session:
        session["infoVert"] = "Nouveau membre inséré. Votre mot de passe est " + mdpClair
    else:
        session["infoRouge"] = "Problème ajout membre"
    return redirect('/')

