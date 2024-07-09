from flask import Flask, request

app = Flask(__name__)

from api_functions import *

"Obtenció de preguntes freqüents"
@app.route("/faqs", methods=["POST"]) 
def get_faqs():
    faq = get_faqs_function(request)
    return faq


@app.route("/faqs_id", methods=["POST"])
def get_faq_id():
    faq = get_faq_id_function(request)
    return faq


@app.route("/nom_assignatura/<id>")
def get_nom_assignatura(id):
    answ = get_nom_assignatura_function(id)
    return answ


@app.route("/get_professors/<id>")
def get_professorsbycodi(id):
    answ = get_professorsbycodi_function(id)
    return answ


@app.route("/answ/<id>")
def get_answ(id):
    answ = get_answ_function(id)
    return answ


@app.route("/users")
def get_all_users():
    bool_exist = get_all_users_function()
    return bool_exist


@app.route("/users/<id>")
def get_user(id):
    bool_exist = get_user_function(id)
    return bool_exist


@app.route("/professor", methods=["POST"])
def get_professor():
    bool_exist = get_professor_function(request)
    return bool_exist


@app.route("/users", methods=["POST"])
def add_user(): 
    user = add_user_function(request)
    return user


@app.route("/notificacio_global", methods=["POST"])
def global_notification(): 
    user = global_notification_function(request)
    return user
    

@app.route("/assignatures_user/<id>")
def get_assignatures_user(id):
    bool_exist = get_assignatures_user_function(id)
    return bool_exist


@app.route("/assignatures_professor/<id>")      ### Per veure on té permis d'enviar una notificació golbal.
def get_assignatures_professor(id):
    bool_exist = get_assignatures_professor_function(id)
    return bool_exist


@app.route("/password", methods=["POST"])
def compare_password():
    password_test = compare_password_function(request)
    return password_test


@app.route("/temari/<id>")
def get_temari_assignatura(id):
    temari = get_temari_assignatura_function(id)
    return temari


@app.route("/")
def index():
    return "Hello!"

