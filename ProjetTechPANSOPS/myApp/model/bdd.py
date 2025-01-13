from . import bddGen

def get_data():
    cnx=bddGen.connexion()
    if cnx is None: return None
    sql='SELECT * from agents'
    param=None
    msg={
        "success":"OKagents",
        "error" : "Failed get agents data"
}
    listeAgents=bddGen.selectData(cnx,sql,param,msg)
    cnx.close()
    return listeAgents

def get_data():
    cnx=bddGen.connexion()
    if cnx is None: return None
    sql='SELECT * from agents'
    param=None
    msg={
        "success":"OKagents",
        "error" : "Failed get agents data"
}
    listeAgents=bddGen.selectData(cnx,sql,param,msg)
    cnx.close()
    return listeAgents

def add_agent(nom,prenom,date_naissance,tel,date_fin_formation):
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = "INSERT INTO `agents` (`nom_agent`, `prenom_agent`, `date_naissance_agent`, `tel_agent`, `fin_formation_theorique_agent`) VALUES (%s, %s, %s,%s,%s);"
    param = (nom,prenom,date_naissance,tel,date_fin_formation)
    msg = {
    "success":"addAgentOK",
    "error" : "Failed add agent data"
    }
    lastId = bddGen.addData(cnx, sql, param, msg)
    cnx.close()
    return lastId

def add_competence(nom,prenom,date_naissance,tel,date_fin_formation):
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = "INSERT INTO `agents` (`nom_agent`, `prenom_agent`, `date_naissance_agent`, `tel_agent`, `fin_formation_theorique_agent`) VALUES (%s, %s, %s,%s,%s);"
    param = (nom,prenom,date_naissance,tel,date_fin_formation)
    msg = {
    "success":"addAgentOK",
    "error" : "Failed add agent data"
    }
    lastId = bddGen.addData(cnx, sql, param, msg)
    cnx.close()
    return lastId