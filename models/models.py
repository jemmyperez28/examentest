'''
Models.py 
Proposito : Configuracion de Modelos de la BD. 
Ejecutar flask db migrate , flask db upgrade en cada modificacion 
'''
from flask import json , make_response
from flask.json import jsonify
from sqlalchemy import exc
from datetime import datetime
from config.database import db
from config.database import ma

'''
Seccion : Modelos
'''
class Persona(db.Model):
    idpersona = db.Column(db.Integer , primary_key = True)
    nombre = db.Column(db.String(20))
    salud = db.Column(db.Integer , default = 100)
    estado_sueno = db.Column(db.Integer, default = 100 )
    relacion_mascota = db.relationship('Mascota',backref='persona',lazy=True)
    relacion_comida = db.relationship('Comida',backref='comida',lazy=True)
    def __init__(self,nombre,salud,estado_sueno):
        self.nombre = nombre
        self.salud = salud
        self.estado_sueno = estado_sueno
    def __repr__(self):
        return f"<Persona : {self.nombre}> , ID : {self.idpersona}"
    def get_persona_by_id(idpersona:int)->jsonify:
        '''
        Obtiene Los Datos de una Persona a Partir del ID Ingresado
        '''
        persona = Persona.query.filter_by(idpersona=idpersona).first()
        persona_schema = PersonaSchema(many=False)
        datos = persona_schema.dump(persona)
        return make_response(jsonify({'persona' : datos}),200)
    
    def get_mascotas(idpersona:int)->jsonify:
        '''Obtiene las mascotas de la Persona in:(idpersona). Output:Json type'''
        mascotas = Mascota.query.with_entities(Mascota.idmascota,Mascota.nombre_mascota).filter_by(idpersona=idpersona).all()
        mascotas_schema = MascotaSchema(many=True)
        datos = mascotas_schema.dump(mascotas)
        return make_response(jsonify({'mascotas' : datos}),200) 

    def get_all_persona()->jsonify:
        '''
        Obtiene los datos de las Personas
        '''
        personas = Persona.query.all()
        personas_schema = PersonaSchema(many=True)
        datos = personas_schema.dump(personas)
        return jsonify({'personas' : datos})
    
    def insert_persona(data:json)->jsonify:
        '''
        Inserta una Nueva Persona
        '''
        nombre = data['nombre']
        salud = None 
        estado_sueno = None
        try:
            nueva_persona = Persona(nombre,salud,estado_sueno)
            db.session.add(nueva_persona)
            db.session.commit()
            response = make_response(jsonify({'nombre' : nueva_persona.nombre , 'mensaje' : 'OK'}),200)
            response.headers["Content-Type"] = "application/json"
        except exc.SQLAlchemyError as e:
            response = make_response(jsonify({'Error' : str(e._sql_message)}),500)
        return response 
    
    def insert_mascota(data:json)->jsonify:
        '''
        Inserta una nueva mascota , ingresada un idpersona
        '''
        idpersona = data['idpersona']
        nombre_mascota = data['nombre_mascota']
        tipo = data['tipo']
        try: 
            nueva_mascota = Mascota(nombre_mascota,None,None,tipo,None,idpersona)
            db.session.add(nueva_mascota)
            db.session.commit()
            response = make_response(jsonify({'nombre_mascota' : nueva_mascota.nombre_mascota , 'mensaje':'OK'}),200)
            response.headers["Content-Type"] = "application/json"
        except exc.SQLAlchemyError as e:
            response = make_response(jsonify({'Error' : str(e._sql_message)}),500)
        return response  
 


class Mascota(db.Model):
    idmascota = db.Column(db.Integer , primary_key = True)
    nombre_mascota = db.Column(db.String(20))
    estado_sueno = db.Column(db.Integer , default = 100 )
    salud = db.Column(db.Integer , default = 100 )
    tipo = db.Column(db.String(10))
    vivo = db.Column(db.String(2), default = "si")
    idpersona = db.Column(db.Integer,db.ForeignKey('persona.idpersona'))
    relacion_gustosmascota = db.relationship('GustosMascota',backref='mascota',lazy=True)
    def __init__(self,nombre_mascota,estado_sueno,salud,tipo,vivo,idpersona):
        self.nombre_mascota = nombre_mascota
        self.estado_sueno = estado_sueno
        self.salud = salud
        self.tipo = tipo
        self.vivo = vivo 
        self.idpersona = idpersona

class Comida(db.Model):
    idcomida = db.Column(db.Integer , primary_key = True)
    nombre_comida = db.Column(db.String(20))
    estado_podrido = db.Column(db.String(2), default = "no")
    fecha_caducidad = db.Column(db.Date)
    comido = db.Column(db.String(2), default = "no")
    idpersona = db.Column(db.Integer,db.ForeignKey('persona.idpersona'))
    relacion_gustosmascota = db.relationship('GustosMascota',backref='comida',lazy=True)
    def __init__(self,idcomida,nombre_comida,estado_podrido,fecha_caducidad,comido,idpersona):
        self.idcomida = idcomida 
        self.nombre_comida = nombre_comida 
        self.estado_podrido = estado_podrido 
        self.fecha_caducidad = fecha_caducidad 
        self.comido = comido 

class GustosMascota(db.Model):
    idgustosmascota = db.Column(db.Integer , primary_key = True)
    idmascota = db.Column(db.Integer,db.ForeignKey('mascota.idmascota'))
    idcomida = db.Column(db.Integer,db.ForeignKey('comida.idcomida'))
    comestible = db.Column(db.String(2))
    favorito = db.Column(db.String(2))
    def __init__(self,idmascota,idcomida,comestible,favorito):
        self.idmascota = idmascota  
        self.idcomida = idcomida   
        self.comestible = comestible  
        self.favorito = favorito 
    

'''
Seccion : Schemas
'''
class PersonaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Persona
        load_instance = True

class MascotaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mascota
        load_instance = True

class ComidaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comida
        load_instance = True

class GustosMascotaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GustosMascota
        load_instance = True

