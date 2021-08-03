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
from variables import *
import pytz

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
 
    def preparar_comida(data:json)->jsonify:
        '''Inserta una nueva Comida'''
        idpersona = data['idpersona']
        nombre_comida = data['nombre_comida']
        fecha_caducidad = data['fecha_caducidad']
        try:
            nueva_comida = Comida(nombre_comida,None,fecha_caducidad,None,idpersona)
            db.session.add(nueva_comida)
            db.session.commit()
            response = make_response(jsonify({'nombre_comida' : nueva_comida.nombre_comida , 'mensaje':'Comida Registrada'}),200)
            response.headers["Content-Type"] = "application/json"
        except exc.SQLAlchemyError as e:
            response = make_response(jsonify({'Error' : str(e._sql_message)}),500)
        return response
    
    def comer(data:json)->jsonify:
        '''Metodo Comer, Aumenta salud y no puede comer alimentos podridos'''
        idcomida = data['idcomida']
        idpersona = data['idpersona']
        try:
            #Validar si la Comida esta podrida.
            comida = Comida.query.filter_by(idcomida=idcomida).first()
            if comida.estado_podrido == "si":
                response = make_response(jsonify({'mensaje':ERROR_COMIDA_PODRIDA}),200)
                return response 
            elif comida.comido =="si":
                response = make_response(jsonify({'mensaje':ERROR_COMIDA_CONSUMIDA}),200)
                return response 
            elif comida.estado_podrido == "no":
                #Actualiza puntos de Persona
                persona = Persona.query.filter_by(idpersona=idpersona).first()
                persona.salud = persona.salud + PUNTOS_PERSONA
                db.session.flush()
                #Actualiza Comida (Ya se comio)
                comida.comido = SI
                db.session.commit()
                #Registra en tabla historial de comidas
                RegistroComidas.nuevo_registro(persona.idpersona,persona.nombre,comida.nombre_comida,comida.estado_podrido,PUNTOS_PERSONA,None)
                db.session.commit()
                response = make_response(jsonify({'mensaje' : SUCCESFULL , 'info': str('persona ' + persona.nombre + 'comio ' + comida.nombre_comida)  }),200)
                response.headers["Content-Type"] = "application/json"
        except exc.SQLAlchemyError as e:
            response = make_response(jsonify({'Error' : str(e._sql_message)}),500)
        return response

    def dormir(data:json)->jsonify:
        '''Metodo Dormir , Aumenta los puntos de estado_sueno'''
        idpersona=data['idpersona']
        try:
            persona = Persona.query.filter_by(idpersona=idpersona).first()
            persona.estado_sueno = persona.estado_sueno + PUNTOS_SUENO
            db.session.commit()
            response = make_response(jsonify({'mensaje' : SUCCESFULL , 'info': str('se aumento ' + str(PUNTOS_SUENO) + ' puntos de sueno a la persona '  + str(persona.nombre) )  }),200)
            response.headers["Content-Type"] = "application/json"
        except exc.SQLAlchemyError as e:
            response = make_response(jsonify({'Error' : str(e._sql_message)}),500)
        return response   

    def presentarse(id:int)->jsonify:
        '''Metodo de presentacion de la persona'''
        idpersona = id 
        try : 
            persona = Persona.query.filter_by(idpersona=idpersona).first()
            response = make_response(jsonify({'mensaje': 'OK','presentacion': str('Hola me llamo ') + str(persona.nombre) +
                                                                  str(' Mis puntos de Salud son : ') + str(persona.salud) +  
                                                                  str(' Mis puntos de Sueno son : ') + str(persona.estado_sueno)
                                              }),200)
            return response
        except exc.SQLAlchemyError as e:
            response = make_response(jsonify({'Error' : str(e._sql_message)}),500)
        return response   
    
    def dar_comida(data:json)->jsonify:
        '''Metodo para dar comida a una mascota '''
        idmascota=data['idmascota']
        idcomida=data['idcomida']
        try: 
            #Validar si la mascota tiene Registrado Gustos en tabla gustos_mascota.
            gustos = GustosMascota.query.filter_by(idmascota=idmascota).filter_by(comestible="si").all()
            if not gustos:
                response = make_response(jsonify({'Mensaje' : 'La Mascota No tiene Comidas Aceptadas, porfavor registre sus comidas aceptables antes'}),200)
                return response 
            #Validar si aceptara la Comida
            comida = Comida.query.filter_by(idcomida=idcomida).first()
            resultado = GustosMascota.query.filter_by(idmascota=idmascota).filter_by(comestible="si").filter_by(idcomida=comida.idcomida).first()
            if resultado is None:
                response = make_response(jsonify({'Mensaje' : 'La Mascota No le gusta la comida : ' + str(comida.nombre_comida)}),200)
                return response 
            else:
                #Validar si comida esta podrida.
                if comida.estado_podrido == "si":
                    response = make_response(jsonify({'Mensaje' : 'No se le puede dar comida podrida : ' + str(comida.nombre_comida)}),200)
                    return response 
                #Validar si la comida ya fue consumida.
                elif comida.comido == "si":
                    response = make_response(jsonify({'Mensaje' : 'La comida ya fue consumida : ' + str(comida.nombre_comida)}),200)
                    return response 
                else:
                    mascota = Mascota.query.filter_by(idmascota=idmascota).first()
                    mascota.salud = mascota.salud + PUNTOS_MASCOTA_COMER
                    db.session.flush()
                    #Registro historial comidas
                    RegistroComidas.nuevo_registro(mascota.idmascota,mascota.nombre_mascota,comida.nombre_comida,comida.estado_podrido,PUNTOS_MASCOTA_COMER,None)
                    db.session.commit()
                    response = make_response(jsonify({'mensaje' : SUCCESFULL , 'info': str('se aumento ' + str(PUNTOS_MASCOTA_COMER) + ' puntos de salud a la mascota '  + str(mascota.nombre_mascota) ) }),200)
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
    
    def comer(data:json)->jsonify:
        idmascota=data['idmascota']
        idcomida=data['idcomida']
        #Obtener datos de la comida que comera.
        comida = Comida.query.filter_by(idcomida=idcomida).first()
        if comida.estado_podrido == "si":
            PNTOS = -40
        elif comida.estado_podrido == "no":
            PNTOS = 70
        #Actualizar puntos de Salud de mascota.
        mascota = Mascota.query.filter_by(idmascota=idmascota).first()
        mascota.salud = mascota.salud + PNTOS
        db.session.commit()
        response = make_response(jsonify({'mensaje' : 'OK' , 'info': str('se agrego ' + str(PNTOS) + ' puntos de salud a la mascota '  + str(mascota.nombre_mascota) ) }),200)
        response.headers["Content-Type"] = "application/json"
        return response
    
    def saludar(id:int)->jsonify:
        idmascota = id 
        #Obtener comida favorita y nombre del dueño de la mascota.
        dueno = Mascota.query.filter_by(idmascota=idmascota).join(Persona, Mascota.idpersona ==Persona.idpersona).add_columns(Persona.nombre).first()
        comida = Mascota.query.filter_by(idmascota=idmascota).join(GustosMascota, GustosMascota.idmascota==Mascota.idmascota).filter_by(favorito="si").join(Comida, Comida.idcomida==GustosMascota.idcomida).add_columns(Comida.nombre_comida).first()
        if not comida: 
            response = make_response(jsonify({'mensaje' : 'Error','info' : 'La Mascota no tiene asignado una comida Favorita porfavor asignela , tabla gustos_mascota'}),200)    
            return response
        response = make_response(jsonify({'mensaje' : 'OK','Saludo' : str('Hola , Mi Dueno es : ' + str(dueno.nombre) + 'y mi Comida Favorita es : ' + str(comida.nombre_comida))}),200)
        return response
    
    def dormir(id:int)->jsonify:
        idmascota = id
        #obtener info de la mascota.
        mascota = Mascota.query.filter_by(idmascota=idmascota).first()
        mascota.estado_sueno = mascota.estado_sueno + PUNTOS_MASCOTA_SUENO
        db.session.commit()
        response = make_response(jsonify({'mensaje': 'OK', 'info' : 'Se agrego ' + str(PUNTOS_MASCOTA_SUENO) + ' puntos de sueno a la mascota ' + str(mascota.nombre_mascota)}),200)
        return response 
    
    def morir(data:json)->jsonify:
        idmascota = data['idmascota']
        #obtener info de la mascota
        mascota = Mascota.query.filter_by(idmascota=idmascota).first()
        mascota.vivo = "no"
        db.session.commit()
        response = make_response(jsonify({'mensaje': 'OK', 'info' : 'La mascota ' + str(mascota.nombre_mascota) + ' ha muerto †††'}),200)
        return response 


class Comida(db.Model):
    idcomida = db.Column(db.Integer , primary_key = True)
    nombre_comida = db.Column(db.String(20))
    estado_podrido = db.Column(db.String(2), default = "no")
    fecha_caducidad = db.Column(db.Date)
    comido = db.Column(db.String(2), default = "no")
    idpersona = db.Column(db.Integer,db.ForeignKey('persona.idpersona'))
    relacion_gustosmascota = db.relationship('GustosMascota',backref='comida',lazy=True)
    def __init__(self,nombre_comida,estado_podrido,fecha_caducidad,comido,idpersona):
        self.nombre_comida = nombre_comida 
        self.estado_podrido = estado_podrido 
        self.fecha_caducidad = fecha_caducidad 
        self.comido = comido 
        self.idpersona = idpersona

    def podrirse(data:json)->jsonify:
        idcomida = data['idcomida']
        #obtener datos comida.
        comida = Comida.query.filter_by(idcomida=idcomida).first()
        comida.estado_podrido = "si"
        db.session.commit()
        response = make_response(jsonify({'mensaje': 'OK', 'info' : 'La comida ' + str(comida.nombre_comida) + ' se pudrio'}),200)
        return response 

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
    
    def nuevo_gusto_mascota(data:json)->jsonify:
        '''Inserta nueva comida que le gusta a la mascota o favorito'''
        idmascota = data['idmascota']
        idcomida = data['idcomida']
        comestible = data['comestible']
        favorito = data['favorito']
        try:
            nuevo_g_mascota=GustosMascota(idmascota,idcomida,comestible,favorito)
            db.session.add(nuevo_g_mascota)
            db.session.commit()
            response = make_response(jsonify({'mensaje' : SUCCESFULL , 'info': 'Se registro la comida'}))
        except exc.SQLAlchemyError as e:
            response = make_response(jsonify({'Error' : str(e._sql_message)}),500)
        return response 


class RegistroComidas(db.Model):
    '''Tabla de Registro de Consumo de Comidas'''
    idregistrocomidas =  db.Column(db.Integer , primary_key = True)
    idconsumidor = db.Column(db.Integer)
    consumidor = db.Column(db.String(20))
    comida = db.Column(db.String(20))
    estado_podrido = db.Column(db.String(2))
    puntos_sumados = db.Column(db.Integer)
    fecha_consumo = db.Column(db.DateTime,default=datetime.now(pytz.timezone('America/Lima')))
    def __init__(self,idconsumidor,consumidor,comida,estado_podrido,puntos_sumados,fecha_consumo):
        self.idconsumidor = idconsumidor
        self.consumidor = consumidor
        self.comida = comida
        self.estado_podrido = estado_podrido
        self.puntos_sumados = puntos_sumados
        self.fecha_consumo = fecha_consumo
    
    def nuevo_registro(idconsumidor:int,consumidor:str,comida:str,estado_podrido:str,puntos_sumados:int,fecha_consumo:datetime):
        '''Nuevo Registro de Comida'''
        idconsumidor = idconsumidor
        consumidor = consumidor
        comida = comida 
        estado_podrido = estado_podrido
        puntos_sumados = puntos_sumados
        fecha_consumo = fecha_consumo
        try:
            nuevo_regis = RegistroComidas(idconsumidor,consumidor,comida,estado_podrido,puntos_sumados,fecha_consumo)
            db.session.add(nuevo_regis)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            mensaje = ('Error'+ str(e._sql_message))
            return mensaje


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

