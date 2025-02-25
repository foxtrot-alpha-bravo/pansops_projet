from flask import Flask, render_template, redirect, session, request,send_file
from myApp.model import bdd
from myApp.controller import function as f
import random,hashlib,datetime,locale
from datetime import datetime
from fillpdf import fillpdfs
import os
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
    if 'nom_agent' in session:
        agent_connecte=session['nom_agent']+' '+session['prenom_agent']
        id_agent_connecte=session['id_agents']
    else:
        agent_connecte=''
        id_agent_connecte=None
    session['datesouhaite']=0
    f.calcul_FC(listeAgents)
    f.calcul_MAC(listeAgents,listeMaint)
    params={'listeAgents':listeAgents,
            'listeMAC':listeMAC,
            'listeMaint':listeMaint,
            'agent_connecte':agent_connecte,
            'id_agent_connecte':id_agent_connecte}
    params=f.messageInfo(params)
         
    return render_template('index2.html',**params)

@app.route("/backup")
def index_backup():
    listeAgents=bdd.get_data()
    listeMAC=bdd.get_actionsMAC_data()
    listeMaint=bdd.get_dataMAINT()
    if 'nom_agent' in session:
        agent_connecte=session['nom_agent']+' '+session['prenom_agent']
        id_agent_connecte=session['id_agents']
    else:
        agent_connecte=''
        id_agent_connecte=None
    session['datesouhaite']=0
    params={'listeAgents':listeAgents,'listeMAC':listeMAC,'listeMaint':listeMaint,'agent_connecte':agent_connecte,'id_agent_connecte':id_agent_connecte}
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
    for i in range(len(listeMaint)):  #on redefinie une nouvelle couleur, cette fois-ci pour le maintien de compétences
        listeMaint[i]['couleurM'] = 'None' #on set la nouvelle clé 'couleurM' pour Maintien de compétences en 'None' par défaut
        if listeMaint[i]["derniere_formation_3"]=='None' : #on ne check que la 3e dernière formation 
            listeMaint[i]['couleurM'] = 'red' #si il n'y a pas de 3e dernière formation, la couleur sera rouge
        else : 
            date_maint = datetime.strptime(listeMaint[i]["derniere_formation_3"], "%Y-%m-%d").date() 
            ecart_maint = (date_maint - date_ajour).days
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
        
        params=f.messageInfo(params)
         
    return render_template('index2.html',**params)


@app.route('/detail_agent/<id_agents>')
def detailAgent(id_agents=''):
    detail_agent=bdd.get_actionsMAC_one_agent(id_agents)
    name_agent=bdd.get_name_one_agent(id_agents)
    id_agent_connecte=session['id_agents']
    if 'nom_agent' in session:
        agent_connecte=session['nom_agent']+' '+session['prenom_agent']
    else:
        agent_connecte=""
        id_agent_connecte=None
    params={'detail_agent':detail_agent,'name_agent':name_agent,'agent_connecte':agent_connecte,'id_agent_connecte':id_agent_connecte}
    return render_template('agent_data.html',**params)

@app.route("/update_data")
def update_data():
    listeAgents=bdd.get_data()
    listeMAC=bdd.get_actionsMAC_data()
    listeMaint=bdd.get_dataMAINT()
    if 'nom_agent' in session:
        agent_connecte=session['nom_agent']+' '+session['prenom_agent']
        id_agent_connecte=session['id_agents']
    else:
        agent_connecte=''
        id_agent_connecte=None
    
    params={'listeAgents':listeAgents,'listeMAC':listeMAC,'listeMaint':listeMaint,'agent_connecte':agent_connecte,'id_agent_connecte':id_agent_connecte}
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
    id_agent=request.form['id_agent']  #on récupère l'identifiant de l'agent depuis le formulaire html
    id_maintien_competences=request.form['id_maintien_competences'] #on récupère l'identifiant de la participation maintien de compétences depuis le formulaire html
    date_participation_agent=request.form['date_participation_agent'] #on récupère la date de la fin de la participation de l'agent depuis le formulaire html
    date_debut_formation=request.form['date_debut_formation'] #on récupère la date de début de la participation de l'agent depuis le formulaire html
    commentaires=request.form['commentaires']  #on récupère les commentaires depuis le formulaire html
    bdd.add_formation_MAC(id_agent,id_maintien_competences,date_participation_agent,date_debut_formation,commentaires)  #on ajoute toutes ces données à la base de données
    return redirect('/')


@app.route("/form_add_agent")
def form_add_agent():
    listeAgents=bdd.get_data()
    listeMAC=bdd.get_actionsMAC_data()
    if 'nom_agent' in session:
        agent_connecte=session['nom_agent']+' '+session['prenom_agent']
        id_agent_connecte=session['id_agents']
    else:
        agent_connecte=''
        id_agent_connecte=None
    params={'listeAgents':listeAgents,'listeMAC':listeMAC,'agent_connecte':agent_connecte,'id_agent_connecte':id_agent_connecte}
    params=f.messageInfo(params)
    
    return render_template('add_agent.html', **params)

@app.route("/form_add_action")
def form_add_action():
    listeAgents=bdd.get_data()
    listeMAC=bdd.get_actionsMAC_data()
    if 'nom_agent' in session:
        agent_connecte=session['nom_agent']+' '+session['prenom_agent']
        id_agent_connecte=session['id_agents']
    else:
        agent_connecte=' '
        id_agent_connecte=None
    params={'listeAgents':listeAgents,'listeMAC':listeMAC,'agent_connecte':agent_connecte,'id_agent_connecte':id_agent_connecte}
    params=f.messageInfo(params)
    
    return render_template('add_action.html', **params)

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




@app.route('/check_date',methods=['POST'])
def checkdate(): 
    session['datesouhaite']=1  
    date_formcheck=request.form['date_formcheck']
    print(date_formcheck)
    session['newdate']=date_formcheck
    listeMaint=bdd.get_datacheck(date_formcheck)   #récupère les trois dernières actions de maintien de compétences avent la date du formulaire(voir requête sql via  fichier bdd fonction:get_datacheck(date_formcheck)
    listeAgents=bdd.get_datacheckFC(date_formcheck) 
    listeMAC=bdd.get_actionsMAC_data()
    
    
    for k in range(len(listeAgents)): #La fonction sera exécutée pour chaque agent 
        if listeAgents[k]["derniere_formation"]=='None' : #Si l'agent n'a aucune formation enregistrée
                listeAgents[k]['couleur'] = 'red' #La couleur revenant dans le dictionnaire est rouge, et sera affichée en conséquence
        else :
            date_ajour=datetime.strptime(session['newdate'], "%Y-%m-%d").date() #La variable est initialisée avec la date du formulaire
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
            date_ajour=datetime.strptime(session['newdate'], "%Y-%m-%d").date()
            ecart_maint = (date_maint - date_ajour).days
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
        
        params={'listeAgents':listeAgents,'listeMAC':listeMAC,'listeMaint':listeMaint,'date_ajour':date_ajour}
        params=f.messageInfo(params)
    return render_template('index2.html',**params)

@app.route('/update_password',methods=['POST'])
def update_password():
    tel_agent=request.form['tel_agent']
    old_pwd=request.form['old_pwd']
    new_pwd=request.form['new_pwd']
    user=bdd.verifAuthData(tel_agent,old_pwd)
    id_agents=user['id_agents']
    new_pwd=hashlib.sha256(new_pwd.encode())
    new_pwd=new_pwd.hexdigest()
    bdd.updateAuthData(new_pwd,id_agents)
    session['infoBleu']='Votre mot de passe a bien été modifié'
    return redirect('/')

@app.route('/form_update_password')
def form_update_password():
    listeAgents=bdd.get_data()
    listeMAC=bdd.get_actionsMAC_data()
    if 'nom_agent' in session:
        agent_connecte=session['nom_agent']+' '+session['prenom_agent']
        id_agent_connecte=session['id_agents']
    else:
        agent_connecte=' '
        id_agent_connecte=None

    params={'listeAgents':listeAgents,'listeMAC':listeMAC,'agent_connecte':agent_connecte,'id_agent_connecte':id_agent_connecte}
    params=f.messageInfo(params)
    return render_template('update_pwd.html',**params)

@app.route("/connecter", methods=["POST"])
def connecter():
    login = request.form['tel']
    password = request.form['mdp']
    #vérification de paramètres en BDD
    user = bdd.verifAuthData(login, password)
    print(user)
    try:
        # Authentification réussie
        session["id_agents"] = user["id_agents"]
        session["nom_agent"] = user["nom_agent"]
        session["prenom_agent"] = user["prenom_agent"]
        session['date_naissance_agent']=user["date_naissance_agent"]
        session["statut_admin_agent"] = user["statut_admin_agent"]
        session["infoVert"] = "Authentification réussie"
        print(session)
        return redirect('/')
    except TypeError as err:
        # Authentification refusée
        session["infoRouge"] = "Authentification refusée"
        return redirect("/")
    
@app.route("/logout")
def logout():
    session.clear() # suppression de la session
    session["infoBleu"] = "Vous êtes bien déconnecté"
    
    return redirect("/")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
@app.route('/generate_pdf',methods=['GET']) #La fonction permet de générer un fichier PDF en remplissant un modèle existant, avec les informations qu'on lui donnera
def generate_pdf():
    template_pdf = os.path.join(BASE_DIR, "static", "livret_pansops_intro.pdf") #On déclare cette variable pour indiquer le chemin vers le modèle de PDF à utiliser
    filled_pdf = os.path.join(BASE_DIR, "static", "filled_pdf.pdf") #On déclare le chemin où sera enregistré le PDF rempli
    
    
    field_values={ #On crée un dictionnaire contenant les valeurs à insérer dans le PDF
        'nom_titulaire':session['nom_agent'],
        'prenom_titulaire':session['prenom_agent'],
        'ddn_titulaire':f.format_date(session['date_naissance_agent'])
    }
    
    fillpdfs.write_fillable_pdf(template_pdf,filled_pdf,field_values) #Le PDF est rempli par cette fonction
    
    return send_file(filled_pdf, as_attachment=True) #Le fichier créé est envoyé au client pour être téléchargé


@app.route('/debug_path', methods=['GET'])
def debug_path():
    template_pdf = os.path.join(os.getcwd(), 'static', 'livret_pansops_intro.pdf')
    
    return {
        "Chemin absolu attendu": template_pdf,
        "Fichier trouvé": os.path.exists(template_pdf)
    }
