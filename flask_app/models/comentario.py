from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash #flash es el encargado de mostrar los mensajes

class Comentario:
    def __init__(self, data):
        #data = {diccionario con la info de mi BD}
        self.id = data["id"]
        self.comentario = data["comentario"]
        self.cant_estrellas = data["cant_estrellas"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]        
        self.usuario_id = data["usuario_id"]
        self.local_comida_id = data["local_comida_id"]

        self.user_name = data["user_name"]

    @classmethod
    def save(cls, form):
        #form = {"comentario" : "contenido de la reseña", "usuario_id" : 1}
        query = "INSERT INTO comentarios (comentario, cant_estrellas, usuario_id, local_comida_id) VALUES (%(comentario)s, %(cant_estrellas)s, %(usuario_id)s, %(local_comida_id)s)"
        return connectToMySQL("esquema_zoneat").query_db(query, form)
    
    @staticmethod
    def validate_comment(form):
        is_valid = True

        if len(form["comentario"]) < 1:
            flash("Comentario is required", "comment")
            is_valid = False
        return is_valid    

    # Metodo para obtener los comentarios de un  local de comida (Los comentarios se despliegan en orden de más reciente a más antiguo)
    @classmethod
    def get_by_local_comida_id(cls, local_comida_id):
        query = """
                SELECT comentarios.*, usuarios.nombre as user_name 
                FROM comentarios 
                JOIN usuarios ON comentarios.usuario_id = usuarios.id 
                WHERE comentarios.local_comida_id = %(local_comida_id)s ORDER BY comentarios.created_at DESC; 
                """
        data = {'local_comida_id': local_comida_id}
        results = connectToMySQL("esquema_zoneat").query_db(query, data)
        comentarios = []
        for c in results:
            comentarios.append(cls(c))
        return comentarios
    
    # Este metodo lo agregué para poder hacer el que un usuario puede borrar sus propios comentarios
    @classmethod
    def get_comment_by_id(cls, comentario_id):
        query = """
                SELECT comentarios.*, usuarios.nombre as user_name
                FROM comentarios
                JOIN usuarios ON comentarios.usuario_id = usuarios.id
                WHERE comentarios.id = %(id)s;
                """
        result = connectToMySQL("esquema_zoneat").query_db(query, {"id": comentario_id})
        if result:
            return cls(result[0])
        else:
            return None
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM comentarios WHERE id = %(id)s AND usuario_id = %(usuario_id)s;" # Aqui me aseguro de que el usuario que va a borrar, sea el mismo que creó el comentario
        return connectToMySQL("esquema_zoneat").query_db(query, data)
