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

def get_actionsMAC_data():
    cnx=bddGen.connexion()
    if cnx is None: return None
    sql='SELECT * from maintien_competences'
    param=None
    msg={
        "success":"OKmaintien_competences",
        "error" : "Failed get maintien_competences data"
}
    listeMAC=bddGen.selectData(cnx,sql,param,msg)
    cnx.close()
    return listeMAC

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

def add_formation_MAC(id_agent,id_maintien_competences,date_participation_agent):
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = "INSERT INTO `participation_agent` (`id_agent`,`id_maintien_competences`, `date_participation_agent`) VALUES (%s, %s, %s);"
    param = (id_agent,id_maintien_competences,date_participation_agent)
    msg = {
    "success":"addFormationOK",
    "error" : "Failed add formations data"
    }
    lastId = bddGen.addData(cnx, sql, param, msg)
    cnx.close()
    return lastId