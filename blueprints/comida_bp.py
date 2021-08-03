from flask import Blueprint , request
from flask.helpers import make_response
from flask.json import jsonify
from config.database import db
from models.models import Comida , GustosMascota 
from sqlalchemy import exc
from models.validators import * 
from variables import *
import json 

#Inicializar BP
comida = Blueprint('comida',__name__)


@comida.route('/comida/pudrir' , methods=['POST'])
def pudrir():
    '''Metodo : Comida podrir'''
    datos = request.json
    #validacion
    if idcomidav.validate(datos):
        data = Comida.podrirse(datos)
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

@comida.route('/comida/nuevo_gusto' , methods=['POST'])
def nuevo_gusto():
    '''Metodo : Agregar una Comida a la mascota para decidir si es su favorito o si lo puede comer'''
    datos = request.json
    #validacion
    if gustov.validate(datos):
        data = GustosMascota.nuevo_gusto_mascota(datos)
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
