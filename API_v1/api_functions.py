
import re
import mysql.connector
import json
from datetime import datetime



def get_faqs_function(request):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    try:
    ### OBTAIN MOST COMMON QÜESTIOSNS FROM DB  ###
        records = []
        if request.json["tema"] != "None" and request.json["tema"] != "0":  ### preguntes del temari d'alguna assignatura
            selectquery = "SELECT titol, id FROM faqs WHERE titol_tema IN (SELECT titol_tema FROM `seqüencia temari` WHERE ordre = \"" + request.json["tema"] + "\" AND codi_assignatura = \"" + request.json["assignatura"] + "\")"
            cursor.execute(selectquery)
            records = cursor.fetchall() # It returns all the rows as a list of tuples."""

        elif request.json["tema"] == "None":    ### preguntes sobre el grau
            selectquery = "SELECT titol,id FROM faqs WHERE codi_assignatura IS NULL AND nom_grau IN (SELECT nom_grau FROM assignatura WHERE codi = \"" + request.json["assignatura"] + "\")"
            cursor.execute(selectquery)
            records = cursor.fetchall()

        elif request.json["tema"] == "0":   ### preguntes del generals d'alguna assignatura
            selectquery = "SELECT titol,id FROM faqs WHERE titol_tema IS NULL AND codi_assignatura = \"" + request.json["assignatura"] + "\""
            cursor.execute(selectquery)
            records = cursor.fetchall()
            

        preguntes_freq_str ="" # Creation of string to show.
        dictionary = {}
        dictionary["faqs"]=[]
        dictionary["faqs_id"]=[]
        aux=0
        for row in records:
            preguntes_freq_str = str(aux+1) + " . " + row[0]
            dictionary["faqs"].append(preguntes_freq_str)
            dictionary["faqs_id"].append(row[1])
            aux+=1
        return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    finally:
        conn.close()


def get_nom_assignatura_function(id):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    try:
    ### OBTAIN AN ANSWER FROM DB  ###
        
        selectquery = "SELECT nom, nom_grau FROM assignatura WHERE codi= " + id
        cursor.execute(selectquery)
        records = cursor.fetchall() # It returns all the rows as a list of tuples."""
        
        dictionary = {}
        dictionary["nom_assignatura"]=""
        dictionary["nom_grau"]=""
        for row in records:
            dictionary["nom_assignatura"]=row[0]
            dictionary["nom_grau"]=row[1]
        return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    finally:
        conn.close()


def get_faq_id_function(request):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    try:
    ### OBTAIN AN ANSWER FROM DB  ###
        
        selectquery = "SELECT resposta, titol, codi_assignatura, nom_grau FROM faqs WHERE id= \"" + request.json["faq_id"] + "\""
        cursor.execute(selectquery)
        records = cursor.fetchall() # It returns all the rows as a list of tuples."""

        selectquery = "SELECT niu FROM usuari WHERE chat_id= \"" + request.json["chat_id"] + "\""
        cursor.execute(selectquery)
        user_niu = cursor.fetchall() # It returns all the rows as a list of tuples."""

        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime('%Y-%m-%d %H:%M:%S')

        titol = records[0][1].replace("'","\\"+"'")
        
        if  records[0][2] == None:
            selectquery = "INSERT INTO consulta (titol_faq,niu_estudiant,data,valoracio,nom_grau) VALUES (" + \
                "\'" + str(titol) + "\'" + "," + "\'" + str(user_niu[0][0]) + "\'" + "," + "\'" + dt_string + "\'" + "," + "\'" + "0" + "\'" + "," + \
                "\'" + str(records[0][3]) + "\'" + ")"
            cursor.execute(selectquery)
            conn.commit()
        else:
            codi = records[0][2]
            selectquery = "INSERT INTO consulta (titol_faq,niu_estudiant,data,valoracio,codi_assignatura,nom_grau) VALUES (" + \
                "\'" + str(titol) + "\'" + "," + "\'" + str(user_niu[0][0]) + "\'" + "," + "\'" + dt_string + "\'" + "," + "\'" + "0" + "\'" + "," + \
                "\'" + str(codi) + "\'" + "," + "\'" + str(records[0][3]) + "\'" + ")"
            cursor.execute(selectquery)
            conn.commit()
        

        dictionary = {}
        dictionary["resposta"]=[]
        for row in records:
            dictionary["resposta"].append(row[0])
        return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    finally:
        conn.close()


def get_user_function(chat_id):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    try:
        ### OBTAIN ANSW FROM DB  ###
        selectquery = "SELECT chat_id FROM usuari WHERE chat_id = " + chat_id
        cursor.execute(selectquery)
        records = cursor.fetchall() # It returns all the rows as a list of tuples."""

        dictionary = {}
        if records:
            dictionary[chat_id]=True
        else:
            dictionary[chat_id]=False
        return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)
    
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    finally:
        conn.close()


def get_professor_function(request):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    dictionary = {}
    selectquery = "SELECT nom, cognoms, niu FROM usuari WHERE chat_id = \"" + request.json["chat_id"] + "\""
    cursor.execute(selectquery)
    records = cursor.fetchall()
    dictionary["nom_professor"]=records[0][0]+" "+records[0][1]

    try:
        if request.json["assignatura"] == "0" or request.json["assignatura"] == "ALL": # Pregunta si és professor d'alguna assignatura. (sense concretar)
            selectquery = "SELECT niu_usuari FROM professor WHERE niu_usuari = \"" + str(records[0][2]) + "\""
            cursor.execute(selectquery)
            niu_professor = cursor.fetchall() # It returns all the rows as a list of tuples."""
            
            if niu_professor:
                dictionary[str(request.json["chat_id"])]=True
            else:
                dictionary[str(request.json["chat_id"])]=False
            return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            selectquery = "SELECT niu_usuari FROM professor WHERE niu_usuari = \"" + str(records[0][2]) + "\"" + \
                "AND codi_assignatura = \"" + request.json["assignatura"] + "\""
            cursor.execute(selectquery)
            records = cursor.fetchall() # It returns all the rows as a list of tuples."""
            
            if records:
                dictionary[str(request.json["chat_id"])]=True
            else:
                dictionary[str(request.json["chat_id"])]=False
            return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)
    
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    finally:
        conn.close()


def add_user_function(request):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")
    try:
        selectquery = "SELECT codi FROM assignatura WHERE password = \"" + request.json["password"] + "\""
        cursor.execute(selectquery)
        records = cursor.fetchall()

        selectquery = "SELECT niu FROM usuari WHERE chat_id = \"" + request.json["chat_id"] + "\""
        cursor.execute(selectquery)
        user_exist = cursor.fetchall()
        
        ### if user NOT exists
        if not user_exist:
            newuser = "INSERT INTO usuari (niu,nom,cognoms,email,idioma,chat_id) VALUES (" + \
                "\'" + str(request.json["niu"]) + "\'" + "," + "\'" + str(request.json["nom"]) + "\'" + "," + "\'" + str(request.json["cognoms"]) + "\'" + "," + \
                "\'" + str(request.json["email"]) + "\'" + "," + "\'" + "Català" + "\'" + "," + "\'" + str(request.json["chat_id"]) + "\'" + ")"
            cursor.execute(newuser)
            conn.commit()

        for row in records:
            newstudent = "INSERT INTO estudiant (niu_usuari,codi_assignatura) VALUES (" + \
            "\'" + str(request.json["niu"]) + "\'" + "," + "\'" + str(row[0]) + "\'" + ")"
            cursor.execute(newstudent)
            conn.commit()
            break       # NOMES ENREGISTREM A UN ESTIRUDANT(chat_usuari) EN UNA ASSIGNRATURA(codi_assignatura).

        return json.dumps({"registration": "Success", "chat_id":request.json["chat_id"], "assignatura": str(row[0])}, indent=4, sort_keys=True, ensure_ascii=False)
    
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return json.dumps({"registration": "Error", "chat_id":request.json["chat_id"]}, indent=4, sort_keys=True, ensure_ascii=False)
    finally:
        conn.close()


def compare_password_function(request):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    try:
        selectquery = "SELECT password FROM assignatura WHERE password = \"" + request.json["password"] + "\""
        cursor.execute(selectquery)
        records = cursor.fetchall()
        if records:
            return json.dumps({"password_return": "Success", "chat_id":request.json["chat_id"]}, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            return json.dumps({"password_return": "Not found", "chat_id":request.json["chat_id"]}, indent=4, sort_keys=True, ensure_ascii=False)

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return json.dumps({"password_return": "Error", "chat_id":request.json["chat_id"]}, indent=4, sort_keys=True, ensure_ascii=False)
    finally:
        conn.close()


def get_all_users_function():
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    try:
    ### OBTAIN MOST COMMON QÜESTIOSNS FROM DB  ###
        selectquery = "SELECT chat_id FROM usuari"
        cursor.execute(selectquery)
        records = cursor.fetchall() # It returns all the rows as a list of tuples."""
        if records:
            dictionary = {}
            dictionary["users"]=[]
            aux=0
            for row in records:
                dictionary["users"].append(row[0])
                aux+=1
            return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            return json.dumps({"users":[]}, indent=4, sort_keys=True, ensure_ascii=False)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    finally:
        conn.close()


def get_assignatures_user_function(chat_id):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    try:
        
        selectquery = "SELECT niu FROM usuari WHERE chat_id = \"" + chat_id + "\""
        cursor.execute(selectquery)
        records = cursor.fetchall()
        

        ### OBTAIN ANSW FROM DB  ###
        selectquery = "SELECT nom, codi FROM assignatura WHERE codi IN (SELECT codi_assignatura FROM estudiant WHERE niu_usuari = " + str(records[0][0]) + \
            " UNION SELECT codi_assignatura FROM professor WHERE niu_usuari = " + str(records[0][0]) + ")"
        cursor.execute(selectquery)
        info = cursor.fetchall() # It returns all the rows as a list of tuples."""

        dictionary = {}
        if info:
            dictionary = {}
            dictionary["assignatures_user"]=[]
            dictionary["codi"]=[]
            aux=0
            for row in info:
                dictionary["assignatures_user"].append(row[0])
                dictionary["codi"].append(row[1])
                aux+=1
            return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            return json.dumps({"assignatures_user":[], "codi":[]}, indent=4, sort_keys=True, ensure_ascii=False)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    finally:
        conn.close()


def get_assignatures_professor_function(chat_id):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    try:
        selectquery = "SELECT niu FROM usuari WHERE chat_id = \"" + chat_id + "\""
        cursor.execute(selectquery)
        records = cursor.fetchall()

        selectquery = "SELECT nom, codi FROM assignatura WHERE codi IN (SELECT codi_assignatura FROM professor WHERE niu_usuari = " + str(records[0][0]) + ")"
        cursor.execute(selectquery)
        info = cursor.fetchall() # It returns all the rows as a list of tuples."""

        dictionary = {}
        if info:
            dictionary = {}
            dictionary["assignatures_professor"]=[]
            dictionary["codi"]=[]
            aux=0
            for row in info:
                dictionary["assignatures_professor"].append(row[0])
                dictionary["codi"].append(row[1])
                aux+=1
            return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            return json.dumps({"assignatures_professor":[]}, indent=4, sort_keys=True, ensure_ascii=False)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    finally:
        conn.close()

def get_temari_assignatura_function(codi_assignatura):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    try:
        #selectquery = "SELECT titol FROM tema WHERE codi_assignatura IN (SELECT codi FROM assignatura WHERE nom = \"" + nom_assignatura + "\")" + \
        #    "ORDER BY ordre"
        selectquery ="SELECT ordre, titol_tema FROM `seqüencia temari` WHERE codi_assignatura = \"" + codi_assignatura + "\"" + \
            "ORDER BY ordre"
        cursor.execute(selectquery)          
        records = cursor.fetchall() # It returns all the rows as a list of tuples."""

        dictionary = {}
        dictionary["temes_assignatura"]=[]
        dictionary["ordre"]=[]
        if records:
            aux=0
            for row in records:
                dictionary["ordre"].append(row[0])
                dictionary["temes_assignatura"].append(row[1])
                aux+=1
            return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    finally:
        conn.close()


def global_notification_function(request):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    descripcio = request.json["text"].replace("'","\\"+"'")

    try:
        # Varifica l'existència del professor.
        selectquery = "SELECT niu_usuari FROM professor WHERE niu_usuari IN (SELECT niu FROM usuari WHERE chat_id = \"" + request.json["chat_id"] + "\")"
        cursor.execute(selectquery)
        records = cursor.fetchall()

        dictionary = {}
        dictionary["to"]=[]
        if records:
            if request.json["global_to"] == "ALL":
                ### Primer obtenim TOTES les assignatures a les quals està assignat el professor a la BD.
                selectquery = "SELECT codi_assignatura FROM professor WHERE niu_usuari = \"" + str(records[0][0]) + "\""
                cursor.execute(selectquery)
                assignatures = cursor.fetchall()
                
                string_codis = ""
                for i in range(len(assignatures)):
                    ### Preparació de la llista de codis en format string ###
                    if i != len(assignatures)-1:
                        string_codis += ("'"+ str(assignatures[i][0]) + "',")
                    else:
                        string_codis += ("'"+ str(assignatures[i][0]) + "'")
                   
                    ### INSERT NOTIFICACIO per cada assignatura ###
                    selectquery = "INSERT INTO notificacio (codi_assignatura,descripcio,titol,data,niu_professor) VALUES (" + \
                        "\'" + str(assignatures[i][0]) + "\'" + "," + "\'" + str(descripcio) + "\'" + "," + "\'" + "NULL" + "\'" + "," + \
                        "\'" + dt_string + "\'" + "," + "\'" + str(records[0][0]) + "\')"
                    cursor.execute(selectquery)
                    conn.commit()
                
                ### Retorna els chat_id dels alumnes i professors que tenen accés a les assignatures esmentades.
                selectquery = "SELECT chat_id FROM usuari WHERE niu IN (SELECT E.niu_usuari FROM estudiant E WHERE E.codi_assignatura IN (" + string_codis + ") " + \
                    "UNION " + \
                    "SELECT P.niu_usuari FROM professor P WHERE P.codi_assignatura IN (" + string_codis + "))"
                cursor.execute(selectquery)
                records = cursor.fetchall()

                for row in records:
                    dictionary["to"].append(row[0])
                return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)

            else:
                ### INSERT NOTIFICACIO per assignatura única ###
                selectquery = "INSERT INTO notificacio (codi_assignatura,descripcio,titol,data,niu_professor) VALUES (" + \
                        "\'" + str(request.json["global_to"]) + "\'" + "," + "\'" + str(descripcio) + "\'" + "," + "\'" + "NULL" + "\'" + "," + \
                        "\'" + dt_string + "\'" + "," + "\'" + str(records[0][0]) + "\')"
                cursor.execute(selectquery)
                conn.commit()

                selectquery = "SELECT chat_id FROM usuari WHERE niu IN (SELECT E.niu_usuari FROM estudiant E WHERE E.codi_assignatura = \"" + request.json["global_to"] + "\" " + \
                    "UNION " + \
                    "SELECT P.niu_usuari FROM professor P WHERE P.codi_assignatura = \"" + request.json["global_to"] + "\")"
                cursor.execute(selectquery)
                records = cursor.fetchall()
                
                for row in records:
                    dictionary["to"].append(row[0])
                return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            return json.dumps({"to": "Sense permís."}, indent=4, sort_keys=True, ensure_ascii=False)
        
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return json.dumps({"to": "Error."}, indent=4, sort_keys=True, ensure_ascii=False)
    finally:
        conn.close()


def get_professorsbycodi_function(id):
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="tfg_xatbot_v5", port="3306")
    cursor = conn.cursor()
    print("Connected successfully to BD...\n\n")

    try:
        selectquery = "SELECT U.nom, U.cognoms, P.usuari_telegram, U.email, P.codi_assignatura, U.chat_id FROM professor P " + \
            "JOIN usuari U ON P.niu_usuari=U.niu AND P.codi_assignatura= " + id
        cursor.execute(selectquery)
        records = cursor.fetchall() # It returns all the rows as a list of tuples."""

        dictionary = {}
        if records:
            dictionary = {}
            dictionary["noms_professors"]=[]
            dictionary["cognoms_professors"]=[]
            dictionary["user_professors"]=[]
            dictionary["chat_id"]=[]
            for row in records:
                dictionary["noms_professors"].append(row[0])
                dictionary["cognoms_professors"].append(row[1])
                dictionary["user_professors"].append(row[2])
                dictionary["chat_id"].append(row[5])
            return json.dumps(dictionary, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            return json.dumps({"noms_professors":[], "cognoms_professors":[], "user_professors":[], "chat_id":[]}, indent=4, sort_keys=True, ensure_ascii=False)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    finally:
        conn.close()