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
comidavalidator = { 'idpersona' : {'type' : 'integer','required':True} , 
                     'nombre_comida' : {'type':'string' , 'required':True} , 
                     'fecha_caducidad' : {'type' : 'string' , 'required':True}
                  }
comervalidator = {'idpersona': {'type':'integer', 'required':True},
                  'idcomida' : {'type':'integer', 'required':True}
                  }
idpersonaval = {'idpersona' : {'type':'integer','required':True}
               }
idmascotaval = {'idmascota' : {'type':'integer','required':True}
               }      
idcomidaval = {'idcomida' : {'type':'integer','required':True}
               }                               
darcomerval = {'idmascota': {'type':'integer','required':True},
               'idcomida': {'type':'integer','required':True}
               }
comermascotavalidator = {'idmascota': {'type':'integer', 'required':True},
                  'idcomida' : {'type':'integer', 'required':True}
                  }
gustovalidador = {'idmascota': {'type':'integer', 'required':True},
                  'idcomida' : {'type':'integer', 'required':True},
                  'comestible' : {'type':'string', 'required':True ,'maxlength': 2},
                  'favorito' : {'type':'string', 'required':True ,'maxlength': 2}
                  }

personav = Validator(personavalidator)
mascotav = Validator(mascotavalidator)
comidav = Validator(comidavalidator)
comerv = Validator(comervalidator)
idpv = Validator(idpersonaval)
darcomerv = Validator(darcomerval)
comermascotav = Validator(comermascotavalidator)
idmascotav = Validator(idmascotaval)
idcomidav = Validator(idcomidaval)
gustov = Validator(gustovalidador)

