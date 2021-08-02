from flask import Blueprint , request
from config.database import db
from models.models import Persona 
from sqlalchemy import exc
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
    data = Persona.insert_persona(persona)
    return data
    
