from . import bddGen

def get_data():
    cnx=bddGen.connexion()
    if cnx is None: return None
    sql="SELECT agents.*, COALESCE(DATE_ADD(latest_training.date_participation_agent, INTERVAL 2 YEAR), 'None') AS derniere_formation FROM agents LEFT JOIN (SELECT id_agent, MAX(date_participation_agent) AS date_participation_agent FROM participation_agent WHERE id_maintien_competences = 6 GROUP BY id_agent) AS latest_training ON agents.id_agents = latest_training.id_agent;"

    param=None
    msg={
        "success":"OKagents",
        "error" : "Failed get agents data"
}
    listeAgents=bddGen.selectData(cnx,sql,param,msg)
    
    cnx.close()
    
    return listeAgents

def getAll_data():
    cnx=bddGen.connexion()
    if cnx is None: return None
    sql="SELECT * from agents"

    param=None
    msg={
        "success":"OKagents",
        "error" : "Failed get agents data"
}
    listeAgents=bddGen.selectData(cnx,sql,param,msg)
    
    cnx.close()
    
    return listeAgents

def get_dataMAINT():
    cnx=bddGen.connexion()
    if cnx is None: return None
    sql="WITH ranked_trainings AS ( SELECT pa.id_agent, pa.date_participation_agent, ROW_NUMBER() OVER (PARTITION BY pa.id_agent ORDER BY pa.date_participation_agent DESC) AS row_num FROM participation_agent pa WHERE pa.id_maintien_competences BETWEEN 1 AND 5 ) SELECT a.*, COALESCE(t1.date_participation_agent, 'None') AS derniere_formation_1, COALESCE(t2.date_participation_agent, 'None') AS derniere_formation_2, COALESCE(t3.date_participation_agent, 'None') AS derniere_formation_3 FROM agents a LEFT JOIN ranked_trainings t1 ON a.id_agents = t1.id_agent AND t1.row_num = 1 LEFT JOIN ranked_trainings t2 ON a.id_agents = t2.id_agent AND t2.row_num = 2 LEFT JOIN ranked_trainings t3 ON a.id_agents = t3.id_agent AND t3.row_num = 3;"

    param=None
    msg={
        "success":"OKmaint",
        "error" : "Failed get maint data"
}
    listeMaint=bddGen.selectData(cnx,sql,param,msg)
    print(listeMaint)
    cnx.close()
    
    return listeMaint


def get_dateFC():
    cnx=bddGen.connexion()
    if cnx is None: return None
    sql='SELECT agents.id_agents,id_maintien_competences,date_participation_agent FROM agents LEFT JOIN participation_agent ON agents.id_agents = participation_agent.id_agent AND id_maintien_competences=6'
    param=None
    msg={
        "success":"OKdateFC",
        "error" : "Failed get dateFC data"
}
    dateFC=bddGen.selectData(cnx,sql,param,msg)
    cnx.close()
    print(dateFC)
    return dateFC


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

def get_actionsMAC_one_agent(idAgent):
    cnx=bddGen.connexion()
    if cnx is None: return None
    sql='''SELECT * FROM participation_agent 
    JOIN agents ON participation_agent.id_agent=agents.id_agents
    JOIN maintien_competences on maintien_competences.id_maintien_competences=participation_agent.id_maintien_competences
    WHERE id_agent=%s'''
    param=(idAgent,)
    msg={
        "success":"OKdetail_agent",
        "error" : "Failed get detail_agent data"
}
    listeMAC_one_agent=bddGen.selectData(cnx,sql,param,msg)
    cnx.close()
    return listeMAC_one_agent

def get_name_one_agent(idAgent):
    cnx=bddGen.connexion()
    if cnx is None: return None
    sql='''SELECT nom_agent, prenom_agent from agents where id_agents=%s'''
    param=(idAgent,)
    msg={
        "success":"OKname_agent",
        "error" : "Failed get name_agent data"
}
    name_one_agent=bddGen.selectData(cnx,sql,param,msg)
    

    cnx.close()
    print(name_one_agent)
    return name_one_agent



def add_agent(nom,prenom,date_naissance,tel,date_fin_formation,debut_activite_enac,mdpC):
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = "INSERT INTO `agents` (`nom_agent`, `prenom_agent`, `date_naissance_agent`, `tel_agent`, `fin_formation_theorique_agent`,`debut_activite_enac`,motPasse) VALUES (%s, %s, %s,%s,%s,%s,%s);"
    param = (nom,prenom,date_naissance,tel,date_fin_formation,debut_activite_enac,mdpC)
    msg = {
    "success":"addAgentOK",
    "error" : "Failed add agent data"
    }
    lastId = bddGen.addData(cnx, sql, param, msg)
    cnx.close()
    return lastId

def add_formation_MAC(id_agent,id_maintien_competences,date_participation_agent,commentaires):
    cnx = bddGen.connexion()
    if cnx is None: return None
    sql = "INSERT INTO `participation_agent` (`id_agent`,`id_maintien_competences`, `date_participation_agent`,`commentaires`) VALUES (%s, %s, %s,%s);"
    param = (id_agent,id_maintien_competences,date_participation_agent,commentaires)
    msg = {
    "success":"addFormationOK",
    "error" : "Failed add formations data"
    }
    lastId = bddGen.addData(cnx, sql, param, msg)
    cnx.close()
    return lastId


def update_AgentData(champ,idAgent,newvalue):
    cnx=bddGen.connexion()
    if cnx is None: return None
    sql= 'UPDATE agents SET '+champ+' =%s WHERE id_agents =%s;'
    param=(newvalue,idAgent)
    msg = {
    "success":"updateAgentDataOK",
    "error" : "Failed update agents data"
    }
    bddGen.updateData(cnx,sql,param,msg)
    cnx.close()