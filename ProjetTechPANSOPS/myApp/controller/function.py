from flask import session
from datetime import datetime
import email.utils

#Permet de récupérer une date présente en session, puis de la convertir au format approprié au fichier PDF
def format_date(date_str):
    try:
        date_obj = email.utils.parsedate_to_datetime(date_str)
        return date_obj.strftime("%d/%m/%Y")
    except Exception:
        return " "
    
def calcul_FC(listeAgents):
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
    return listeAgents

def calcul_MAC(listeAgents,listeMaint):
    date_ajour = datetime.today().date() #La variable est initialisée avec la date du jour
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
    return listeAgents
    
    
# passe les messages d'info en paramètres
def messageInfo(params = None):
    if params is None:
        params = {}
#messages d'infos du views.py
    if "infoVert" in session:
        params["infoVert"] = session['infoVert']
        session.pop("infoVert", None)
        
    if "infoRouge" in session:
        params["infoRouge"] = session['infoRouge']
        session.pop("infoRouge", None)
        
    if "infoBleu" in session:
        params["infoBleu"] = session['infoBleu']
        session.pop("infoBleu", None)
        
#messages d'info du bdd.py
    if "errorDB" in session:
        params["errorDB"] = session['errorDB']
        session.pop("errorDB", None)
        
    if "successDB" in session:
        params["successDB"] = session['successDB']
        session.pop("successDB", None)
        
    return params