from flask import Blueprint , request
from flask.helpers import make_response
from flask.json import jsonify
from config.database import db
from models.models import Persona 
from sqlalchemy import exc
from models.validators import * 
from variables import *
import json 

#Inicializar BP
persona = Blueprint('persona',__name__)

@persona.route('/persona/get_all_persona',methods=['GET'])
def get_all_persona():
    data = Persona.get_all_persona()
    return data

@persona.route('/persona/get_persona_by_id/<int:id>',methods=['GET'])
def get_persona_by_id(id:int):
    data = Persona.get_persona_by_id(id)
    return data

@persona.route('/persona/nueva_persona' , methods=['POST'])
def nueva_persona():
    persona = request.json
    #Validaciones (validators.py)
    if personav.validate(persona):
        data = Persona.insert_persona(persona)
        return data
    else:
        response = make_response(
                jsonify(
                    {"message": str(ERROR_TIPO), "severity": "danger"}
                ),
                400,
            )
        response.headers["Content-Type"] = "application/json"
        return response

@persona.route('/persona/nueva_mascota' , methods=['POST'])
def nueva_mascota():
    mascota = request.json 
    #validaciones (validators.py)
    if mascotav.validate(mascota):
        data = Persona.insert_mascota(mascota)
        return data 
    else : 
        response = make_response(
                jsonify(
                    {"message": str(ERROR_TIPO), "severity": "danger"}
                ),
                400,
            )
        response.headers["Content-Type"] = "application/json"
        return response
    
