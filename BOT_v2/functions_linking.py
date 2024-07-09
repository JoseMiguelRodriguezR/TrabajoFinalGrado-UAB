
import requests
import json

from requests import *
from telegram import *
from telegram.ext import *

def get_assignatures(update, context):
    #Obtencion de FAQs de la API.
    response = requests.get("http://127.0.0.1:5000/assignatures_user/" + str(update.effective_chat.id))
    
    query= update.callback_query
    query.answer()

    inlineboard_buttons=[]     # Creación de botones del teclado personalizado.
    for i in range(len(response.json()["assignatures_user"])):
        callback_string = "a1_" + str(response.json()["codi"][i]) # + response.json()["assignatures_user"][i]
        inlineboard_buttons.append([InlineKeyboardButton(text=response.json()["assignatures_user"][i], callback_data=callback_string)])
    
    inlineboard_buttons.append([InlineKeyboardButton(text="🔙", callback_data="options")])
     
    query.edit_message_text(
        text="Estàs enregistrat en aquestes <b>assignatures</b>:\n\n"+
        "<i>Si vols accedir a una altra assignatura t'hi has d'enregistrar amb</i> /register .",
        reply_markup=InlineKeyboardMarkup(inlineboard_buttons),
        parse_mode=ParseMode.HTML
    )


def get_decision(update, context):
    query=update.callback_query
    query.answer()
    str_aux = update.callback_query['data']
    str_aux = str_aux.split('_')
    header = {"content-type": "application/json"}
    user_data = {"assignatura":str_aux[1], "chat_id":str(update.effective_chat.id)}
    buttons = []
    
    buttons.append([InlineKeyboardButton(text = "Info. general de l'assignatura. ℹ", callback_data="a2_"+str_aux[1]+"_0")])
    buttons.append([InlineKeyboardButton(text = "Temari de l'assignatura. 📚", callback_data="d_temari_"+str_aux[1])])
    buttons.append([InlineKeyboardButton(text = "El grau. 👨‍🎓", callback_data="a2_"+str_aux[1]+"_None")])
    
    response = requests.post("http://127.0.0.1:5000/professor", data=json.dumps(user_data), headers=header)
    if response.json()[str(update.effective_chat.id)] == False: #si no es professor es dona l'opció de contactar amb professor.
        buttons.append([InlineKeyboardButton(text = "Contactar amb professor/a. "+"🆘", callback_data="contact_"+str_aux[1])])
    
    buttons.append([InlineKeyboardButton(text="🔙", callback_data="faqs")])

    nom_assignatura = requests.get("http://127.0.0.1:5000/nom_assignatura/" + str_aux[1])

    query.edit_message_text(
        text = "Et trobes en l'assignatura <b>\""+ nom_assignatura.json()["nom_assignatura"] +"\"</b>.\n"+
        "Escull l'opció que t'interessi.",
        reply_markup = InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.HTML
    )
    

def get_temari(update, context):
    query= update.callback_query
    query.answer()
    
    str_aux = update.callback_query['data']
    str_aux = str_aux.split('d_temari_')
    response = requests.get("http://127.0.0.1:5000/temari/" + str_aux[1])

    inlineboard_buttons=[]     # Creación de botones del teclado personalizado.
    count = 0                  # Identifica el tema, ja que es mostren en ordre.
    for row in response.json()["temes_assignatura"]:
        ### El últim 1 que afegim al "callback_string" serveix per indicar que les faqs que es busquen pertanyen al TEMARI de l'assiguatura.
        callback_string = "a2_" + str_aux[1] + "_" + str(response.json()["ordre"][count])
        show_string = "T." + str(response.json()["ordre"][count]) + " " + row
        inlineboard_buttons.append([InlineKeyboardButton(text=show_string, callback_data=callback_string)])
        count+=1

    nom_assignatura = requests.get("http://127.0.0.1:5000/nom_assignatura/" + str_aux[1])
    callback_string = "a1_" + str_aux[1]
    inlineboard_buttons.append([InlineKeyboardButton(text="🔙", callback_data=callback_string)])


    if response.json()["temes_assignatura"] != []:
        query.edit_message_text(
            text="Sobre quin tema de <b>\""+ nom_assignatura.json()["nom_assignatura"] +"\"</b> estàs interessat:",
            reply_markup=InlineKeyboardMarkup(inlineboard_buttons),
            parse_mode=ParseMode.HTML

        )
    else:
        query.edit_message_text(
            text= "L'assignatura \"" + nom_assignatura.json()["nom_assignatura"] +"\" NO està organitzada per temes.",
            reply_markup=InlineKeyboardMarkup(inlineboard_buttons)
        )