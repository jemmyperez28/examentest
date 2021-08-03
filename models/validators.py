'''
Inicializacion de Validadores de esquemas Controlados Por Cerberus
'''
from cerberus import Validator
personavalidator = {'nombre':  {'type': 'string' , 'required':True}
                     }
mascotavalidator = {'nombre_mascota': {'type':'string' , 'required':True},
                     'tipo' :{'type':'string','required':True},
                     'idpersona' : {'type' : 'integer','required':True}
                     }


personav = Validator(personavalidator)
mascotav = Validator(mascotavalidator)

