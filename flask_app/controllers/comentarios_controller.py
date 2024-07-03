from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

# Importamos los modelos
from flask_app.models.comentario import Comentario
from flask_app.models.local_comida import Local_comida

@app.route('/locales/<int:local_comida_id>/comentarios', methods=['POST'])
def create_comment(local_comida_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    # Ojo El usuario creador del local de comida no puede comentar
    # Obtener el local de comida para luego saber quién es el usuario creador
    local_comida = Local_comida.read_one({"id": local_comida_id})
    # Verificar si el usuario actual es el creador del local de comida
    if session['usuario_id'] == local_comida.usuario_id:
        flash("No puedes comentar tu propio local_comida.", "comment")
        return redirect(f'/locales/{local_comida_id}')

    if not Comentario.validate_comment(request.form):
        return redirect(f'/locales/{local_comida_id}')

    data = {
        'comentario': request.form['comentario'],
        'cant_estrellas': int(request.form['estrellas']),  # Obtener y convertir a entero
        'local_comida_id': local_comida_id,
        'usuario_id': session['usuario_id']
    }

    Comentario.save(data)
    return redirect(f'/locales/{local_comida_id}')

# Ruta para ver la info y comentarios de un local de comida específico
@app.route('/locales/<int:id>')
def view_movie(id):
    data = {"id": id}
    local_comida = Local_comida.read_one(data)

    # Obtener los comentarios ordenados como se indica en la query del método get_by_local_comida_id
    local_comida.comentarios = Comentario.get_by_local_comida_id(local_comida.id)

    if not local_comida:
        return redirect('/dashboard')
    return render_template('view.html', local_comida=local_comida)

# Ruta para Borrar un comentario
@app.route("/comentarios/<int:local_comida_id>/borrar/<int:comentario_id>", methods=['POST'])
def delete_local_comment(local_comida_id, comentario_id):
    # Verificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect("/")
    
    # Obtener el comentario a eliminar
    comentario = Comentario.get_comment_by_id(comentario_id)
    
    if comentario and comentario.usuario_id == session['usuario_id']:
        Comentario.delete({"id": comentario_id, "usuario_id": session['usuario_id']})
    
    return redirect(f"/locales/{local_comida_id}")
