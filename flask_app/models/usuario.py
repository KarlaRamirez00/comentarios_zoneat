from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash #flash es el encargado de mostrar los mensajes

import re  # Expresiones Regulares -> Empatar con un patrón de texto
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class Usuario:
    def __init__(self, data):
        #data = diccionario que tiene toda la info para el objeto
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.tipo_usuario = data["tipo_usuario"]
        self.email = data["email"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

#OJO AQUI! las @classmethod siembre deben ir indentadas dentro de la clase!!!
    # Metodo que crea un nuevo objeto de Usuario
    @classmethod
    def save(cls, form):
        query = "INSERT INTO usuarios (nombre, apellido, tipo_usuario, email, contrasena) VALUES (%(nombre)s, %(apellido)s, %(tipo_usuario)s, %(email)s, %(contrasena)s)"
        return connectToMySQL('esquema_zoneat').query_db(query, form)
    
    # Metodo que regresa objeto de Usuario en base a email
    @classmethod
    def get_by_email(cls, form):
        #form = {"email":"elena@cd.com", "password":"hola123"}
        query = "SELECT * FROM usuarios WHERE email = %(email)s"
        result = connectToMySQL('esquema_zoneat').query_db(query, form) #Regresa Lista de Diccionario

        if len(result) < 1: # Revisa si mi lista esté vacía
            return False
        else:
            #M e regresa 1 registro
            # result = [{"id":1, "nombre":"Elena"....}]
            usuario = cls(result[0]) #User ({"id":1, "nombre":"Elena"....})
            return usuario
        
    #M etodo que regresa objeto de Usuario en base a email
    @classmethod
    def get_by_id(cls, data):
        #form = {"id": 1}
        query = "SELECT * FROM usuarios WHERE id = %(id)s"
        result = connectToMySQL('esquema_zoneat').query_db(query, data) #Regresa Lista de Diccionario
        usuario = cls(result[0])
        return usuario

    @staticmethod  # es static porque es un metodo que ayuda a hacer una validacion
    def validate_user(form):
        # form = {diccionario con toda la info del formulario}
        is_valid = True    

        # Validamos que el nombre tenga al menos dos caracteres
        if len(form["nombre"]) < 2:
            flash("Nombre must have at least 2 chars", "register")
            is_valid = False

        # Validamos que el apellido tenga al menos dos caracteres
        if len(form["apellido"]) < 2:
            flash("Apellido must have at least 2 chars", "register")
            is_valid = False

        # Validamos que el largo de la contraseña tenga al menos 6 caracteres
        if len(form["contrasena"]) < 6:
            flash("Contrasena must have at least 6 chars", "register")
            is_valid = False

        # Validamos que el email sea único
        query = "SELECT * FROM usuarios WHERE email = %(email)s"
        result = connectToMySQL('esquema_zoneat').query_db(query, form) #Regresa Lista de Diccionario
        # Aqui podría ocurrir que me regrese una lista vacía o una lista con 1 diccionario
        if len(result) >=1:
            # Si existe ese email en mi Base de datos
            flash("Email already registered", "register")
            is_valid = False

        # Validamos que las contraseñas coinsidan (porque tengo el campo password y el campo confirm password)
        if form["contrasena"] != form["confirm"]:
            flash("Contrasena do not match", "register")
            is_valid = False

        # Validamos que el email cumpla con la expresion regular
        if not EMAIL_REGEX.match(form["email"]):
            flash("Email not valid", "register")
            is_valid = False
        
        # Validar tipo de usuario
        if form['tipo_usuario'] not in ['1', '2']:
            flash("Tipo de usuario inválido. Debes seleccionar 'Propietario' o 'Cliente'.", "register")
            is_valid = False
        
        return is_valid
    
    @classmethod
    def update(cls, data):
        query = """
            UPDATE usuarios 
            SET nombre=%(nombre)s, apellido=%(apellido)s, email=%(email)s, 
                contrasena=IF(%(contrasena)s != '', %(contrasena)s, contrasena), 
                tipo_usuario=%(tipo_usuario)s 
            WHERE id=%(id)s;
        """
        return connectToMySQL('esquema_zoneat').query_db(query, data)

    @staticmethod
    def validate_user_edit(form):
        is_valid = True

        if not EMAIL_REGEX.match(form["email"]):
            flash("Email no válido.", "edit")
            is_valid = False

        if form["contrasena"] != form["confirm"]:
            flash("Las contraseñas no coinciden.", "edit")
            is_valid = False

        # Validar tipo de usuario
        if form['tipo_usuario'] not in ['1', '2']:
            flash("Tipo de usuario inválido. Debes seleccionar 'Propietario' o 'Cliente'.", "edit")
            is_valid = False

        return is_valid