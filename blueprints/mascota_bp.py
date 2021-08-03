from flask import Blueprint , request
from flask.helpers import make_response
from flask.json import jsonify
from config.database import db
from models.models import Mascota 
from sqlalchemy import exc
from models.validators import * 
from variables import *
import json 

#Inicializar BP
mascota = Blueprint('mascota',__name__)


@mascota.route('/mascota/comer' , methods=['POST'])
def comer():
    '''Metodo : Mascota comer'''
    datos = request.json
    #validacion
    if comermascotav.validate(datos):
        data = Mascota.comer(datos)
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

@mascota.route('/mascota/saludar/<int:id>' , methods=['GET'])
def saludar(id:int):
    '''Endpoint que muestra el saludo de la mascota '''
    data = Mascota.saludar(id)
    return data

@mascota.route('/mascota/dormir/<int:id>' , methods=['GET'])
def dormir(id:int):
    '''Endpoint que aumenta los puntos de sueno de la mascota '''
    data = Mascota.dormir(id)
    return data


@mascota.route('/mascota/morir' , methods=['POST'])
def morir():
    '''Metodo : Mascota morir'''
    datos = request.json
    #validacion
    if idmascotav.validate(datos):
        data = Mascota.morir(datos)
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
