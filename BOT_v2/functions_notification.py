import requests
import json
import re 

from requests import *
from telegram import *
from telegram.ext import *

def global_message(update, context):
    query=update.callback_query
    query.answer()
    
    response = requests.get("http://127.0.0.1:5000/assignatures_professor/" + str(update.effective_chat.id))

    inlineboard_buttons=[]     # Creación de botones del teclado personalizado.
    for i in range(len(response.json()["assignatures_professor"])):
        callback_string = "g_" + str(response.json()["codi"][i]) 
        inlineboard_buttons.append([InlineKeyboardButton(text=response.json()["assignatures_professor"][i], callback_data=callback_string)])
    inlineboard_buttons.append([InlineKeyboardButton(text="Enviar a totes. "+"🧙‍♂", callback_data="g_ALL")])
    inlineboard_buttons.append([InlineKeyboardButton(text="🔙", callback_data="options")])

    query.edit_message_text(
        text="Tens aquestes assignatures assignades en la base de dades...\n\n"+
        "A qui vols enviar el missatge?",
        reply_markup=InlineKeyboardMarkup(inlineboard_buttons)
    )


def prepare_global_message(update, context):
    query=update.callback_query
    query.answer()
    str_aux =update.callback_query['data'].split("g_")
    
    aux = ""
    if str_aux[1] == "ALL":
        aux = "TOTES les assignatures assignades"
    else:
        nom_assignatura = requests.get("http://127.0.0.1:5000/nom_assignatura/" + str_aux[1])
        aux = nom_assignatura.json()["nom_assignatura"]

    context.bot.send_message(   #query.edit_message_text
        chat_id=update.effective_chat.id,
        text="⚠ Còpia i enganxa el text següent al començament del missatge per difondre una notificació a <b>" + aux + "</b>.\n\n"+
        "⬇  ⬇  ⬇",
        parse_mode=ParseMode.HTML
    )
    
    context.bot.send_message(   #query.edit_message_text
        chat_id=update.effective_chat.id,
        text="GLOBAL:" + str_aux[1] + ":"
    )


def process_global(update, context):
    text = update.message.text
    global_to = re.split(":", text)

    header = {"content-type": "application/json"}
    user_data = {"assignatura":str(global_to[1]), "chat_id":str(update.effective_chat.id)}
    professor = requests.post("http://127.0.0.1:5000/professor", data=json.dumps(user_data), headers=header)
    
    if professor.json()[str(update.effective_chat.id)] == True:
        text_split = re.split("^GLOBAL:[_a-zA-Z0-9\u00C0-\u00FF\' ]*:", text)

        header = {"content-type": "application/json"}
        user_data = {"chat_id":str(update.effective_chat.id), "global_to":global_to[1], "text": text_split[1], "titol":"--something--"}
        response = requests.post("http://127.0.0.1:5000/notificacio_global", data=json.dumps(user_data), headers=header)
        
        """
        nom_assignatura = requests.get("http://127.0.0.1:5000/nom_assignatura/" + global_to[1])
        aux = nom_assignatura.json()["nom_assignatura"]
        """

        for user_chat_id in response.json()["to"]:
            context.bot.send_message(  
                chat_id=user_chat_id,
                text="<b>Norificació enviada per " + professor.json()["nom_professor"] + ": 📩</b>\n\n" + text_split[1], #text="<b>Norificació enviada a "+ aux + ". 📩</b>\n\n" + text_split[1],
                parse_mode=ParseMode.HTML
            )