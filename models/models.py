'''
Models.py 
Edicion : 02/08/2021
'''
from flask import json , make_response
from flask.json import jsonify
from sqlalchemy import Column
from datetime import datetime
from config.database import db
from config.database import ma

'''
Seccion : Modelos
'''
class Persona(db.Model):
    idpersona = db.Column(db.Integer , primary_key = True)
    nombre = db.Column(db.String(20))
    def __init__(self,nombre):
        self.nombre=nombre
    def __repr__(self):
        return f"<Persona : {self.nombre}> , ID : {self.idpersona}"
    def get_persona_by_id(idpersona:int)->jsonify:
        '''
        Obtiene Los Datos de una Persona a Partir del ID Ingresado
        '''
        persona = Persona.query.filter_by(idpersona=idpersona).first()
        persona_schema = PersonaSchema(many=False)
        datos = persona_schema.dump(persona)
        return jsonify({'persona' : datos})
    
    def get_all_persona()->jsonify:
        '''
        Obtiene los datos de las Personas
        '''
        personas = Persona.query.all()
        personas_schema = PersonaSchema(many=True)
        datos = personas_schema.dump(personas)
        return jsonify({'personas' : datos})
    
    def insert_persona(data:json)->jsonify:
        nombre = data['nombre']
        nueva_persona = Persona(nombre)
        db.session.add(nueva_persona)
        db.session.commit()
        response = make_response('OK!',200)
        response.headers["Content-Type"] = "application/json"
        #return jsonify({'response' : '200'})
        return response 

'''
Seccion : Schemas
'''
class PersonaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Persona
        load_instance = True
