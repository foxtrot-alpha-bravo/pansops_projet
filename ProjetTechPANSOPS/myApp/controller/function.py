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