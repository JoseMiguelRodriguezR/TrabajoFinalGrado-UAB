
import requests
import json
import ast
import Constants as keys
import logging
import re 

from functions_linking import *
from functions_register import *
from functions_faqs import *
from functions_notification import *
from greet_new_member import *
from requests import *
from telegram import *
from telegram.ext import *


print("\nXatBot started...\n")


""" El txt que carreguem al sistema, té la informació del usuaris que es troben en un xat amb Xatbot. """
users_inchat = {}
a_file = open("users_inchat.txt", "r")
contents = a_file.read()
users_inchat = ast.literal_eval(contents)
if users_inchat == {}:
    users_inchat = {'chat_ids': set()}
a_file.close()
print(users_inchat)


""" Filter personalitzat per la funció "register_user". """
class FilterRegister(MessageFilter):
    def filter(self, message):
        return '---' in message.text
 

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


""" Rastrea los chats en los que está el bot. """
def track_chats(update: Update, context: CallbackContext, ) -> None:
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    # Let's check who is responsible for the change
    cause_name = update.effective_user.full_name
    
    # Handle chat types differently:
    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if is_member:
            context.bot_data.setdefault("chat_ids", set()).add(chat.id)
            update.effective_chat.send_message( 
                f"Benvingut a Xatbot {cause_name}! ✨\n" 
            )
            if not was_member:
                logger.info("%s started the bot", cause_name)

        elif was_member and not is_member:
            logger.info("%s blocked the bot", cause_name)
            context.bot_data.setdefault("chat_ids", set()).discard(chat.id)

    users_inchat["chat_ids"] = context.bot_data["chat_ids"]
    with open('users_inchat.txt','w') as data: 
        data.write(str(users_inchat))
    print(users_inchat)


def start_command(update, context):                   
    # BUSCAR SI L'USUARI EXISTEIX A LA BD.
    response = requests.get("http://127.0.0.1:5000/users/" + str(update.effective_chat.id))
    if response.json()[str(update.effective_chat.id)] == False:
        update.effective_chat.send_message( 
                "/register - Sóc nou, registrar-me a Xatbot. 🤩 \n\n" +
                "<i>Quan et registris podràs accedir a les</i>\n/options <i>de Xatbot.</i>",
                parse_mode=ParseMode.HTML,
            )
    else: 
        update.effective_chat.send_message(  
                "Ja ets membre de Xatbot. 👍\n\n"+ 
                "/options - Començar amb els serveis de Xatbot.\n"+ 
                "/register - Registrar-se a una altra assignatura.",
                parse_mode=ParseMode.HTML,
            )
         

"""
InlineKeyboardMarkup --> permite definir el teclado.
InlineKeyboardButton --> permite definir los botones.
Los botones de tipo "callback_data" retornan información de vuelta al bot.
"""
def options_command(update, context):
    query=update.callback_query
    buttons = []
    response = requests.get("http://127.0.0.1:5000/users/" + str(update.effective_chat.id))
    if response.json()[str(update.effective_chat.id)] == True:
        buttons.append([InlineKeyboardButton(text = "Sobre @TFG_Xatbot. "+"🤖", callback_data="about")])
        buttons.append([InlineKeyboardButton(text = "Accedir a les meves assignatures. "+"🎓", callback_data="faqs")])

        header = {"content-type": "application/json"}
        user_data = {"assignatura":"0", "chat_id":str(update.effective_chat.id)}
        response = requests.post("http://127.0.0.1:5000/professor", data=json.dumps(user_data), headers=header)
        if response.json()[str(update.effective_chat.id)] == True:
            buttons.append([InlineKeyboardButton(text = "Enviar notificació. "+"💫", callback_data="global")])

        if query:
            query.answer()
            query.edit_message_text(
                text = 'Què necessites?',
                reply_markup = InlineKeyboardMarkup(buttons)
            )
        else:
            update.message.reply_text(
                text = 'Què necessites?',
                reply_markup = InlineKeyboardMarkup(buttons)
            )


def show_about(update, context):
    query= update.callback_query
    query.answer()

    context.bot.send_sticker(update.effective_chat.id, 'CAACAgIAAxkBAAIGsGHz77DtMJZPVpranuP6qS56FVH8AAJvAAPb234AAZlbUKh7k4B0IwQ')

    inlineboard_buttons=[]     # Creación de botones del teclado personalizado.
    inlineboard_buttons.append([InlineKeyboardButton(text="🔙", callback_data="options")])
    query.edit_message_text(
        text="Hola, sóc @TFG_Xatbot.\n"+
        "Un Bot de Telegram creat amb el propòsit de solucionar els dubtes dels estudiants amb la major brevetat possible.\n\n"+
        "Espero que puguis gaudir dels meus serveis.",
        reply_markup=InlineKeyboardMarkup(inlineboard_buttons)
    )


def contact_teacher(update, context):
    query=update.callback_query
    query.answer()
    str_aux=update.callback_query['data'].split("contact_")

    inlineboard_buttons=[]     # Creación de botones del teclado personalizado.
    callback_string = "a1_" + str(str_aux[1]) # + response.json()["assignatures_user"][i]
    inlineboard_buttons.append([InlineKeyboardButton(text="🔙", callback_data=callback_string)])
    
    nom_assignatura = requests.get("http://127.0.0.1:5000/nom_assignatura/" + str(str_aux[1]))
    response = requests.get("http://127.0.0.1:5000/get_professors/" + str(str_aux[1]))
    if response.json()["noms_professors"] != []:
        show_string = ""
        for i in range(len(response.json()["noms_professors"])):
            show_string += str(response.json()["noms_professors"][i]) + " " + str(response.json()["cognoms_professors"][i]) + \
                "\n" + "https://t.me/" + str(response.json()["user_professors"][i]) + "\n\n"

        query.edit_message_text(
            text="Els professors de l'assignatura <b>\""+ str(nom_assignatura.json()["nom_assignatura"]) +"\"</b> són:\n\n"+
            show_string +
            "<i>Accedint als links, obriràs un xat privat amb ells.</i>",
            reply_markup=InlineKeyboardMarkup(inlineboard_buttons),
            parse_mode=ParseMode.HTML
        )
    else:
        query.edit_message_text(
            text="No hi han professors per aquesta assignatura (<b>"+ str(nom_assignatura.json()["nom_assignatura"]) +"</b>)",
            reply_markup=InlineKeyboardMarkup(inlineboard_buttons),
            parse_mode=ParseMode.HTML
        )


""" Implementacions futures:
def exit_message(update, context):
"""    


def error(update, context):
    print("ERROR Update from : " + str(update["message"]["chat"]))


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    print("\n------------\n")
    print(update.message)


def main():
    """
    La finalitat de "Updater" és rebre les actualitzacions de Telegram 
    i lliurar-les al "Dispatcher".
    El Despatcher admet controladors per a diferents tipus de dades. 
    """
    updater=Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    """ Detecta quan l'usuari es vol registrar al escriure al xat "---" i més informació. """
    filter_register = FilterRegister()

    """
    Utilitzem el diccionar de bot_data com a auxiliar. 
    Aquest identifica els usuaris que tenen un chat obert amb el Xatbot (no tenen perquè estar registrats). 
    """
    dp.bot_data["chat_ids"] = users_inchat["chat_ids"]

    # dp.add_error_handler(error)

    """
    ConversationHandler --> capta el flux d'info. que l'usuari envia al bot per determinats "entry_points". 
    CommandHandler --> per tractar los comandos! "/start".
    CallbackQueryHandler --> per tractar la info. de "callback_data"  # (que transporta "pattern").
    MessageHandler --> per tractar el text que l'usuari introdueix.
    ... 
    """
    dp.add_handler(ConversationHandler(
        entry_points = [
            CommandHandler("start" , start_command, run_async=True),
            ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER),                                                                     
            CommandHandler("register" , register_user_message),
            MessageHandler(filter_register, register_user),
            MessageHandler(Filters.regex('^GLOBAL:[_a-zA-Z0-9\u00C0-\u00FF\' ]*:'), process_global),
            CommandHandler("options" , options_command),    # , Filters.chat(chat_id=users_list)
            CallbackQueryHandler(pattern='options', callback=options_command),
            CallbackQueryHandler(pattern='about', callback=show_about),
            CallbackQueryHandler(pattern='faqs', callback=get_assignatures),
            CallbackQueryHandler(pattern='^a1[_a-zA-Z0-9\u00C0-\u00FF\' ]*$', callback=get_decision), ### a - assignatura, 1 - primer pas.
            CallbackQueryHandler(pattern='^d_temari[_a-zA-Z0-9\u00C0-\u00FF\' ]*$', callback=get_temari),
            CallbackQueryHandler(pattern='^a2[_a-zA-Z0-9\u00C0-\u00FF\' ]*$', callback=get_faqs),   ### a - assignatura, 2 - continua l'arbre de passos.
            CallbackQueryHandler(pattern='^faq_id_[0-9]*$', callback=get_faqs_response),
            CallbackQueryHandler(pattern='^global$', callback=global_message),
            CallbackQueryHandler(pattern='^g_[_a-zA-Z0-9\u00C0-\u00FF\' ]*$', callback=prepare_global_message),
            CallbackQueryHandler(pattern='^contact_[0-9]*$', callback=contact_teacher), 
            # CallbackQueryHandler(pattern='exit', callback=exit_message) # Implementacions futures
            # MessageHandler(Filters.all, echo), #---TEST---
            ],
        states = {},
        fallbacks=[],
    ))

    """ les dues línies de codi següents fan que el bot es mantingui a l'espera de l'entrada de l'usuari. """
    updater.start_polling()
    updater.idle() 

main()
