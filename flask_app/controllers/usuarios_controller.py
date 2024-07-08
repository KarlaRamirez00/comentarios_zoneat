from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

# Importamos los modelos
from flask_app.models.usuario import Usuario
from flask_app.models.local_comida import Local_comida

# Importar Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Ruta para plantilla de formularios
@app.route("/")
def index():
    return render_template("index.html")

# Ruta que recibe el formulario
@app.route("/register", methods=["POST"])
def register():
    #request.form = {"first_name": "Elena", "last_name": "De Troya"....}

    # Validar la info que recibimos
    if not Usuario.validate_user(request.form):
        # No es valida la info, redirecciono al form
        return redirect("/")


    # Encriptar o Hashear contraseña
    pass_hash = bcrypt.generate_password_hash(request.form["contrasena"])

    # Crear un diccionario que simule el form incluyendo la contraseña hasheada y el tipo de usuario
    form = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"],
        "contrasena": pass_hash,
        "tipo_usuario": request.form["tipo_usuario"]
    }

    id = Usuario.save(form) # recibo el id del nuevo usuario 1
    session["usuario_id"] = id
    session["nombre"] = request.form["nombre"]
    session['tipo_usuario'] = request.form["tipo_usuario"]
    return redirect("/dashboard")

# Ruta que recibe el formulario
@app.route("/dashboard")
def dashboard():
    # Verificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect("/")
    
    dicc = {"id" : session['usuario_id']}
    usuario = Usuario.get_by_id(dicc) # Obtener el objeto Usuario
    
    locales_comida = Local_comida.read_all() 
    
    return render_template("dashboard.html", usuario=usuario, locales_comida=locales_comida)


@app.route("/login", methods=["POST"])
def login():
    # request.form = {"email": "elena@codingdojo.com", "password": "Hola123"}
    # Verifico que el email esté en mi BD
    usuario = Usuario.get_by_email(request.form) # Recibo false si no existe ese usuario en mi BD o recibo un objeto de usuario con la info guardada en la BD

    if not usuario: # Si usuario es igual a Falso, es decir, que no existe...
        flash("Email not found", "login")
        return redirect("/")
    #Si usuario SI es objeto Usuario...
    if not bcrypt.check_password_hash(usuario.contrasena, request.form["contrasena"]):  # entre los parentesis pongo el password hasheado, y el password NO hasheado
        flash("Password incorrect", "login")
        return redirect("/")
    
    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    session['tipo_usuario'] = usuario.tipo_usuario  # Guardar el tipo de usuario en la sesión
    return redirect('/dashboard')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/edit_user/<int:usuario_id>')
def edit_user(usuario_id):
    if 'usuario_id' not in session or session['usuario_id'] != usuario_id:
        return redirect('/')

    data = {'id': usuario_id}
    usuario = Usuario.get_by_id(data)  # Obtiene los datos del usuario a editar

    # Prellenar los datos en la sesión para que se muestren en el formulario
    session['editando_usuario'] = True
    session['nombre_edit'] = usuario.nombre
    session['apellido_edit'] = usuario.apellido
    session['email_edit'] = usuario.email
    session['tipo_usuario_edit'] = usuario.tipo_usuario
    
    return render_template("edit_user.html", usuario=usuario)  # Pasar el objeto 'usuario' a la plantilla

from flask import flash

@app.route('/actualizar_usuario/<int:usuario_id>', methods=['POST'])
def actualizar_usuario(usuario_id):
    if 'usuario_id' not in session or session['usuario_id'] != usuario_id:
        return redirect('/')

    # Convertir request.form a un diccionario mutable
    form_data = request.form.to_dict()

    # Añadir el id del usuario al diccionario
    form_data['id'] = usuario_id

    # Validación de datos (similar a la del registro, pero adaptada para la edición)
    if not Usuario.validate_user_edit(form_data):
        return redirect(f'/edit_user/{usuario_id}')

    # Encriptar la nueva contraseña (si se proporcionó)
    if form_data['contrasena']:
        pass_hash = bcrypt.generate_password_hash(form_data["contrasena"])
        form_data['contrasena'] = pass_hash
    else:
        form_data['contrasena'] = ''  # Mantener la contraseña actual si no se proporciona una nueva

    # Actualizar los datos del usuario en la base de datos
    Usuario.update(form_data)

    # Limpiar variables de sesión
    session.pop('editando_usuario', None)
    session.pop('nombre_edit', None)
    session.pop('apellido_edit', None)
    session.pop('email_edit', None)
    session.pop('tipo_usuario_edit', None)
    
    return redirect('/dashboard')