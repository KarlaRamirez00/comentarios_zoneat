from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash #flash es el encargado de mostrar los mensajes

from datetime import datetime #me permite manipular fechas -- ya no lo usaré pero no lo borraré por si me sirve en el futuro

# Importo Comment
from flask_app.models.comentario import Comentario

class Local_comida:
    def __init__(self, data):

        self.id = data["id"]
        self.nombre = data["nombre"]
        self.direccion = data["direccion"]
        self.telefono = data["telefono"]
        self.email = data["email"]
        self.sitio_web = data["sitio_web"]
        self.categoria = data["categoria"]       
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuario_id = data["usuario_id"]

        self.user_name = data["user_name"] # Columna extra al hacer una consulta JOIN
        self.comentarios = []


    # Metodo que crea un nuevo objeto de local de comida
    @classmethod
    def create(cls, form):
        query = """
        INSERT INTO locales_comida (nombre, direccion, telefono, email, sitio_web, categoria, usuario_id) 
        VALUES (%(nombre)s, %(direccion)s, %(telefono)s, %(email)s, %(sitio_web)s, %(categoria)s, %(usuario_id)s);
        """
        result = connectToMySQL('esquema_zoneat').query_db(query, form)
        print("Resultado de la creación:", result)
        return result     

    # Metodo que muestra un objeto de local de comida
    @classmethod
    def read_one(cls, data):
        #data ={"id": 1}
        query = "SELECT locales_comida.*, usuarios.nombre as user_name FROM locales_comida JOIN usuarios ON locales_comida.usuario_id = usuarios.id WHERE locales_comida.id = %(id)s;"
        # Lista con 1 diccionario
        result = connectToMySQL('esquema_zoneat').query_db(query, data) 
        local_comida = cls(result[0]) # Objeto local de comida
        # Genero una consulta en la cual vaya específicamente por los comentarios del local de comida mostrado
        query_comentarios = "SELECT comentarios.*, usuarios.nombre as user_name FROM comentarios JOIN usuarios ON comentarios.usuario_id = usuarios.id WHERE local_comida_id = %(local_comida_id)s;"
        data_comment = {"local_comida_id": local_comida.id}
        results_comentarios = connectToMySQL("esquema_zoneat").query_db(query_comentarios, data_comment)
        comentarios = [] # Lista de comentarios vacía
        for c in results_comentarios:
            local_comida.comentarios.append(Comentario(c)) # Creo objeto de Comentario y lo agrego a la lista

        return local_comida
    
    # Metodo que muestra un objeto de local de comida
    @classmethod
    def read_all(cls):
        query = "SELECT locales_comida.*, usuarios.nombre as user_name FROM locales_comida JOIN usuarios ON locales_comida.usuario_id = usuarios.id;" 
        # Lista con 1 diccionario
        results = connectToMySQL('esquema_zoneat').query_db(query) 
        locales_comida = [] # Objetos de local de comida
        for local in results:
            locales_comida.append(cls(local)) # local = {diccionario con la ifo de BD}, cls(local) : Crear el objeto localcula, locales_comida.append(): el objeto localcula lo agrego a la lista
        return locales_comida
    
    @staticmethod
    def validate_local_comida(form):
        is_valid = True

        if len(form["nombre"]) < 3:
            flash("El nombre del local debe tener al menos 3 caracteres", "local")
            is_valid = False

        if len(form["direccion"]) < 5:
            flash("La direccion del local debe tener al menos 5 caracteres", "local")
            is_valid = False

        if len(form["telefono"]) < 3:
            flash("El teléfono del local debe tener al menos 3 caracteres", "local")
            is_valid = False

        if len(form["email"]) < 5:
            flash("El e-mail del local debe tener al menos 5 caracteres", "local")
            is_valid = False

        if len(form["sitio_web"]) < 8:
            flash("El Sitio Web del local debe tener al menos 8 caracteres", "local")
            is_valid = False
    
            
        return is_valid #Regresa True o False
    
    # update
    @classmethod
    def update(cls, form):
        query = "UPDATE locales_comida SET nombre=%(nombre)s, direccion=%(direccion)s, telefono=%(telefono)s, email=%(email)s, sitio_web=%(sitio_web)s, usuario_id=%(usuario_id)s WHERE id=%(id)s;"
        return connectToMySQL('esquema_zoneat').query_db(query, form) 

    # delete
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM locales_comida WHERE id = %(id)s;"
        return connectToMySQL('esquema_zoneat').query_db(query, data) 