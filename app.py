'''
| app.py : Archivo de aplicacion principal 
'''
from flask import Flask
from flask.helpers import send_from_directory
from flask_migrate import Migrate
from config.database import db , ma
from blueprints.persona_bp import persona
from blueprints.mascota_bp import mascota
from blueprints.comida_bp import comida
from blueprints.swagger_bp import swaggerui_blueprint , SWAGGER_URL

#Inicializacion de Objetos principales
app = Flask(__name__)
app.config.from_object('config.settings')
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

#Registro de Blueprints
app.register_blueprint(persona)
app.register_blueprint(mascota)
app.register_blueprint(comida)
app.register_blueprint(swaggerui_blueprint, url_prefix = SWAGGER_URL)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)



if __name__ == "__main__":
    app.run(debug=True)
