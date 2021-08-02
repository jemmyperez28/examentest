'''
| app.py : Archivo de aplicacion principal 
'''
from flask import Flask
from flask_migrate import Migrate
from config.database import db , ma
from blueprints.persona_bp import persona

#Inicializacion de Objetos principales
app = Flask(__name__)
app.config.from_object('config.settings')
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

#Registro de Blueprints
app.register_blueprint(persona)

if __name__ == "__main__":
    app.run(debug=True)
