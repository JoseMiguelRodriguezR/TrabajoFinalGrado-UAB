import requests
import json
import re 
import os
import nltk

from telegram import *
from telegram.ext import *
from requests import *
from nltk.tag.stanford import StanfordNERTagger


""" 
La funcionalitat de detecció del nom de l'usuari requereix "jaxa" per al seu funcionament.
Aquesta funcionalitat correspont a la part del registre de l'usuari i utilitza l'import de "nltk". """
"""
java_path = "C:/Program Files/Java/jdk-17.0.1/bin/java.exe"
os.environ['JAVAHOME'] = java_path
"""

""" Per la detecció de noms de persones """
"""
st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar') 
"""

""" Per la comprovació de noms de persones """
regex_for_name = '^[a-zA-Z\u00C0-\u00FF\' ]*$'

""" Per la comprovació de emails """
regex_for_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def register_user_message(update, context):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = "Aquest procés es pot repetir per diverses assignatures.\n" +
        "Necessitem la següent informació per poder-te registrar en alguna assignatura:"
    )
    context.bot.send_message(
        chat_id = update.effective_chat.id,
         text ="1⃣ Contrasenya de l'assignatura on et vols registrar.\n" +
         "2⃣ El teu nom.\n" +
         "3⃣ Els teus cognoms.\n" +
         "4⃣ El teu email.\n" +
         "5⃣ El teu NIU."
    )
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text ="Escriu 3 guions i seguidament la teva informació:\n" +
        "---contrasenya de l'assignatura\n"+
        "---el meu nom\n"+
        "---el meu cognom\n"+
        "---el meu mail\n"+
        "---el meu niu"
    )
    

def register_user(update, context):
    register_message = update.message.text
    lines_list = register_message.splitlines()
    
    if len(lines_list)>5 :
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "El missatge enviat té més informació de la demanada. 🧐\n"+
                "Recorda que el format d'enviament de l'informació de registe és el següent:\n"+
                "---contrasenya de l'assignatura\n"+
                "---el meu nom\n"+
                "---el meu cognom\n"+
                "---el meu mail\n"+
                "---el meu niu"
            )
    elif len(lines_list)<4:
        context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = "Falta algun camp del registre per omplir. 🧐\n"+
                "Recorda que el format d'enviament de l'informació de registe és el següent:\n"+
                "---contrasenya de l'assignatura\n"+
                "---el meu nom\n"+
                "---el meu cognom\n"+
                "---el meu mail\n"+
                "---el meu niu"
            )
    else:
        """ Comprovació de que cada linia té --- """
        guions_correcte = True
        for i in range(len(lines_list)):
            if "---" not in lines_list[i]:
                guions_correcte = False
            else:
                lines_list[i] = lines_list[i].replace("---", "")
        
        if guions_correcte == False:
            context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = "Algun dels camps no conté els 3 guions. 🧐\n"+
                "Recorda que el format d'enviament de l'informació de registe és el següent:\n"+
                "---contrasenya de l'assignatura\n"+
                "---el meu nom\n"+
                "---el meu cognom\n"+
                "---el meu mail\n"+
                "---el meu niu"
            )
        else:
            content = True
            for line in lines_list:
                if not line or line.isspace():
                    content = False

            if content == False:
                context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = "En algun dels camps falta informació. 🧐\n"+
                    "Recorda que el format d'enviament de l'informació de registe és el següent:\n"+
                    "---contrasenya de l'assignatura\n"+
                    "---el meu nom\n"+
                    "---el meu cognom\n"+
                    "---el meu mail\n"+
                    "---el meu niu"
                )

            else:
                """ ### Comprovació contrasenya. ### """
                password_test = {"password": lines_list[0], "chat_id": update.effective_chat.id}
                header = {"content-type": "application/json"}
                response = requests.post("http://127.0.0.1:5000/password", data=json.dumps(password_test), headers=header)
                if not response.json()["password_return"] == "Success" and response.json()["chat_id"] == update.effective_chat.id:
                    context.bot.send_message(
                        chat_id = update.effective_chat.id,
                        text = "No existeix cap contrasenya igual en la base de dades. 🧐\n" +
                        "La contrasenya no és correcta."
                    )
                    return

                """ ### Comprovació niu. ### """
                if re.match("^[0-9]{7}$", lines_list[4]) is None:
                    context.bot.send_message(
                        chat_id = update.effective_chat.id,
                        text = "El NIU és un identificador que es compon de 7 números.\n" +
                        "Revisa si hi ha algun espai o caràcter invàlid en el camp del NIU. 🧐"
                    )
                    return

                """ ### Comprovació email. ### """
                if re.fullmatch(regex_for_email, lines_list[3]) is None:
                    context.bot.send_message(
                        chat_id = update.effective_chat.id,
                        text = "El seu email no es considera de format correcte. 🧐 \n" +
                        "Si us plau, utilitza un altre email o el que la teva universitat t'ha assignat.\n"+
                        "Assegura't que el mail no tingui un espai al final."
                    )
                    return

                """ ### Comprovació de nom i cognom. ### """
                result = None
                for i in range(len(lines_list)-3):
                        result = re.match(regex_for_name, lines_list[i+1])
                        if (i+1)==1 and result is None:
                            context.bot.send_message(
                                chat_id = update.effective_chat.id,
                                text = "És possible que existeixi algún caràcterinvàlid en el seu nom. 🧐\n" +
                                "Contacta amb el professor via mail per sol·lucionar el problema."
                            )
                            return
                        elif (i+1)==2 and result is None:
                            context.bot.send_message(
                                chat_id = update.effective_chat.id,
                                text = "És possible que existeixi algun caràcter invàlid en el seu nom.\n" +
                                "Contacta amb el professor via mail per solucionar el problema. 🧐"
                            )
                            return
                

                """ Insertar user en BD. """
                user_data = {"nom": lines_list[1], "cognoms": lines_list[2], "email": lines_list[3], "niu": lines_list[4], "chat_id": str(update.effective_chat.id), "password": lines_list[0]}
                response = requests.post("http://127.0.0.1:5000/users", data=json.dumps(user_data), headers=header)
                if response.json()["registration"] == "Success" and response.json()["chat_id"] == str(update.effective_chat.id):
                    context.bot.send_message(
                        chat_id = update.effective_chat.id,
                        text = "Ja estàs registrat a @TFG_Xatbot !\n🤩🎉\n\n" +
                        "<i>Pots accedir a les</i> /options .",
                        parse_mode=ParseMode.HTML,
                    )

                    """ Comprovació de nom i cognoms - EXTRA --------------------
                    Funció que utilitza el pakage de Stanford NER, fet per Stanford Natural Language Processing Group.
                    """
                    """
                    person_count = 0
                    for i in range(len(lines_list)-3):
                        for sent in nltk.sent_tokenize(lines_list[i+1]):
                            tokens = nltk.tokenize.word_tokenize(sent)
                            tags = st.tag(tokens)
                            for tag in tags:
                                if tag[1] in ["PERSON"]:
                                    person_count += 1
                    
                    if person_count < 3:    # Normalment: Nom Cognom1 Cognom2.
                                            # Si l'algoritme NO detecta els 3 correctament, envia alerta al professor,
                                            # però l'usuari es registra de totes formes.
                                            # L'algoritme no detecta el nom "Ona" (nom femení).
                        chat_professor = requests.get("http://127.0.0.1:5000/get_professors/" + str(response.json()["assignatura"]))
                        for chat in chat_professor.json()["chat_id"]:
                            try:
                                context.bot.send_message(
                                    chat_id = str(chat),
                                    text = "⚠ <b>Un usuari de nom singular s'acaba de registrar.</b>\n\n" +
                                    "Nom: " + str(lines_list[1]) + "\n" + "Cognom: " + str(lines_list[2]) + "\n" + "Email: " + str(lines_list[3]) + "\n" +
                                    "Niu: " + str(lines_list[4]) + "\n" + "Chat_id: " + str(update.effective_chat.id),
                                    parse_mode=ParseMode.HTML,
                                )
                            except:
                                print("Chat_id:"+ str(chat)+" NOT FOUND. Msg_Alert:Irregular Name and Surname. To:Teacher")
                    """    
                    """ ------------------------------------------------------------ """
                else:
                    context.bot.send_message(
                        chat_id = update.effective_chat.id,
                        text = "Ho sentim molt, hi ha hagut un error al introduïr les dades en la base de dades. 😓\n" +
                        "Torna a intentar registrar-te, si segueix sense funcionar contacta amb el professor encarregat."
                    )