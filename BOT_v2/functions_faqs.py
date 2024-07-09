import requests
import json

from telegram import *
from telegram.ext import *
from requests import *

""" 
Poden arribar 3 tipus de callback_data:
    - codi assignatura_Nom de l'assignatura_3 : l'ultim nombre int indica que es vol obtindre info. sobre preguntes del Tema 3.
    - codi assignatura_Nom de l'assignatura_0 : es volen obtenir les prequntes freqüents de l'assignatura (que no pretanyen al temari, 
                                                és a dir, preguntes generals).
    - codi assignatura_Nom de l'assignatura_None : no hi ha cap identificador final d'int, per tant, indica que es vol la info. corresponent
                                                    del GRAU al qual l'assignatura pertany.
"""
def get_faqs(update, context):
    str_aux =update.callback_query['data'].split("_")
    header = {"content-type": "application/json"}
    query= update.callback_query
    query.answer()

    # Inicialització de variables que necessitem per construir el missatge del bot.
    preguntes_freq_str =""  # Creation of string to show.
    aux=0
    new_line = 0
    keyboard_buttons=[[]]     # Creación de botones del teclado personalizado.
    user_data = {"assignatura":str_aux[1], "tema":str_aux[2], "chat_id":update.effective_chat.id}

    response = requests.post("http://127.0.0.1:5000/faqs", data=json.dumps(user_data), headers=header)
    nom_assign_grau = requests.get("http://127.0.0.1:5000/nom_assignatura/" + str_aux[1])

    for row in response.json()["faqs"]:
        preguntes_freq_str += row + "\n"
        callback_string = "faq_id_" + str(response.json()["faqs_id"][aux])
        keyboard_buttons[new_line].append(InlineKeyboardButton(text=str(aux+1), callback_data=callback_string)) # KeyboardButton(str(aux+1))
        aux+=1
        if (aux) % 5 == 0:
            keyboard_buttons.append([])
            new_line += 1
    keyboard_buttons.append([])

    if str_aux[2] != 'None' and str_aux[2] != '0':  ### Si hem demanat preguntes d'algun tema.
        callback_string = "d_temari_" + str_aux[1]
        keyboard_buttons[new_line+1].append(InlineKeyboardButton(text="🔙", callback_data=callback_string))
        if response.json()["faqs"] != []:
                query.edit_message_text(
                    text="Aquestes són les preguntes més freqüents sobre el <b>\"T."+ str_aux[2] + "\"</b> de l'assignatura " + nom_assign_grau.json()["nom_assignatura"] +":\n\n" + preguntes_freq_str + "\n\n",
                    reply_markup=InlineKeyboardMarkup(keyboard_buttons),
                    parse_mode=ParseMode.HTML
                )
        else:
            query.edit_message_text(   #query.edit_message_text
                text="No hi han preguntes per aquest TEMA (T."+ str_aux[2] +").\n"+
                "Si tens alguna pregunta, si us plau, envia un missatge al professor encarregat. 😓",
                reply_markup=InlineKeyboardMarkup(keyboard_buttons)
            )
    
    elif str_aux[2] == '0': 
        callback_string = "a1_" + str_aux[1]
        keyboard_buttons[new_line+1].append(InlineKeyboardButton(text="🔙", callback_data=callback_string))
        if response.json()["faqs"] != []:
                query.edit_message_text(
                    text="Aquestes són les preguntes més freqüents sobre el la <b>\"Info. general\"</b> de l'assignatura <b>" + nom_assign_grau.json()["nom_assignatura"] +"</b>:\n\n" + preguntes_freq_str + "\n\n",
                    reply_markup=InlineKeyboardMarkup(keyboard_buttons),  #, resize_keyboard=True,one_time_keyboard=True
                    parse_mode=ParseMode.HTML
                )
        else:
            query.edit_message_text(   #query.edit_message_text
                text="\""+ nom_assign_grau.json()["nom_assignatura"] +"\" NO té preguntes generals en aquest moment. \n"+
                "Si tens alguna pregunta, si us plau, envia un missatge al professor encarregat. 😓",
                reply_markup=InlineKeyboardMarkup(keyboard_buttons)
            )
    
    elif str_aux[2] == 'None': ### GRAU.
        callback_string = "a1_" + str_aux[1]
        keyboard_buttons[new_line+1].append(InlineKeyboardButton(text="🔙", callback_data=callback_string))
        if response.json()["faqs"] != []:
                query.edit_message_text(
                    text="Aquestes són les preguntes més freqüents sobre el GRAU <b>\""+ nom_assign_grau.json()["nom_grau"] +"\"</b>:\n\n" + preguntes_freq_str + "\n\n",
                    reply_markup=InlineKeyboardMarkup(keyboard_buttons),
                    parse_mode=ParseMode.HTML
                )
        else:
            query.edit_message_text(   #query.edit_message_text
                text="El grau \""+ nom_assign_grau.json()["nom_grau"] +"\" NO té preguntes en aquest moment.\n" +
                "Si tens alguna pregunta, si us plau, envia un missatge al professor encarregat. 😓",
                reply_markup=InlineKeyboardMarkup(keyboard_buttons)
            )


def get_faqs_response(update, context):
    str_aux =update.callback_query['data'].split("faq_id_")
    header = {"content-type": "application/json"}
    user_data = {"faq_id":str_aux[1], "chat_id":str(update.effective_chat.id)}
    response = requests.post("http://127.0.0.1:5000/faqs_id", data=json.dumps(user_data), headers=header)
    
    query= update.callback_query
    query.answer()

    if response.json()["resposta"] != []:
        update.effective_chat.send_message(
            text=str(response.json()["resposta"][0]),
            parse_mode=ParseMode.HTML
        )