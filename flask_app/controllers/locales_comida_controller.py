from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

#Importamos los modelos
from flask_app.models.local_comida import Local_comida
from flask_app.models.usuario import Usuario
from flask_app.models.comentario import Comentario

@app.route("/nuevo")
def nuevo():
    # Verificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect("/")
    
    # Verificar si el usuario es propietario (tipo_usuario = '1')
    if session.get('tipo_usuario') != '1':
        return redirect('/dashboard')

    # Crear una instancia vacía de Local_comida
    local_comida = Local_comida({
        "id": None,
        "nombre": "",
        "direccion": "",
        "telefono": "",
        "email": "",
        "sitio_web": "",
        "categoria": "",
        "created_at": None,
        "updated_at": None,
        "usuario_id": session['usuario_id'],  # Pasar el ID del usuario en sesión
        "user_name": None,  # Puedo dejar esto como None si no lo necesito en la plantilla
        "comentarios": []
    })

    return render_template("new.html", local_comida=local_comida)

@app.route("/create", methods=["POST"])
def create():
    # Va a recibir el formulario... request.form = diccionario con toda la info del Formulario
    # Verificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect("/")
        
    # Validamos
    if not Local_comida.validate_local_comida(request.form):
        return redirect("/nuevo")    
    # Crear el nuevo local de comida
    nuevo_local_id = Local_comida.create(request.form)
    
    if nuevo_local_id:
        print(f"Nuevo local creado con ID: {nuevo_local_id}")
    else:
        print("Error al crear el nuevo local")
    
    return redirect("/dashboard")

@app.route("/ver/<int:id>") #ver/1
def read(id):
    # Verificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect("/")
    
    dicc = {"id" : id} #{"id" = 1}
    local_comida = Local_comida.read_one(dicc) #Invoco de la clase Local_comida al método read_one(), enviamos el diccionario y recibimos un objeto Local_comida
    return render_template("view.html", local_comida=local_comida)

@app.route("/borrar/<int:id>")  #/borrar/2
def delete(id):
    # Verificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect("/")
    
    # Metodo que borra un local de comida en base a su ID
    dicc = {"id" : id}
    Local_comida.delete(dicc)
    return redirect("/dashboard")

@app.route("/editar/<int:id>") #/editar/3
def edit(id):
    #V erificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect("/")
    
    dicc = {"id" : id} #{"id" = 1}
    local_comida = Local_comida.read_one(dicc) #Invoco de la clase Local_comida al método read_one(), enviamos el diccionario y recibimos un objeto Local_comida.
    # Revisar que sí sea el usuario en sesión el mismo que creó el local, para que la pueda editar
    if session['usuario_id'] != local_comida.usuario_id:
        return redirect("/dashboard")
    
    return render_template("edit.html", local_comida=local_comida)

@app.route("/update", methods=["POST"])
def update():
    # Verificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect("/")
    
    # Recibir request.form = diccionario con la info del formulario
    # Validamos
    if not Local_comida.validate_local_comida(request.form):
        return redirect("/editar"+request.form["id"])
    
    Local_comida.update(request.form)
    return redirect("/dashboard")

@app.route("/comentarios/borrar/<int:id>", methods=["POST"])
def delete_comment(id):
    # Verificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect("/")
    data = {"id" : id, "usuario_id" : session['usuario_id']}

    Comentario.delete(data)
    return redirect(request.referrer) # referrer redirige a la página anteriormente visitada por el usuario.
