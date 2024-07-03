# Terminal: pipenv install flask pymysql flask-bcrypt

#Importar la app
from flask_app import app


#Importar  controladores (puede ser más de uno)
from flask_app.controllers import usuarios_controller, locales_comida_controller, comentarios_controller

#Ejecución app
if __name__ == "__main__":
    app.run(debug=True)