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
    '''Endpoint que obtiene todas las personas'''
    data = Persona.get_all_persona()
    return data

@persona.route('/persona/get_persona_by_id/<int:id>',methods=['GET'])
def get_persona_by_id(id:int):
    '''Endpoint que obtiene datos de la persona a partir del idpersona'''
    #Validaciones (validators.py)
    data = Persona.get_persona_by_id(id)
    return data

@persona.route('/persona/nueva_persona' , methods=['POST'])
def nueva_persona():
    '''Endpoint que que inserta una nueva persona , in:json '''
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
    '''Endpoint que inserta una nueva mascota perteneciente a una persona (idpersona)'''
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

@persona.route('/persona/get_mascotas/<int:id>' , methods=['GET'])
def get_mascotas(id:int):
    '''Endpoint que muestra todas las mascotas de una persona (idpersona)'''
    data = Persona.get_mascotas(id)
    return data
  