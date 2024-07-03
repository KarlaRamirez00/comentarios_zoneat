from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

#Importamos los modelos
from flask_app.models.usuario import Usuario
from flask_app.models.local_comida import Local_comida

#Importar Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Ruta para plantilla de formularios
@app.route("/")
def index():
    return render_template("index.html")

#Ruta que recibe el formulario
@app.route("/register", methods=["POST"])
def register():
    #request.form = {"first_name": "Elena", "last_name": "De Troya"....}

    #Validar la info que recibimos
    if not Usuario.validate_user(request.form):
        #No es valida la info, redirecciono al form
        return redirect("/")


    #Encriptar o Hashear contraseña
    pass_hash = bcrypt.generate_password_hash(request.form["contrasena"])

    #Crear un diccionario que simule el form incluyendo la contraseña hasheada
    form = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"],
        "contrasena": pass_hash
    }

    id = Usuario.save(form) #recibo el id del nuevo usuario 1
    session["usuario_id"] = id
    session["nombre"] = request.form["nombre"]
    return redirect("/dashboard")

#Ruta que recibe el formulario
@app.route("/dashboard")
def dashboard():
    #Verificar que el usuario haya iniciado sesión
    if 'usuario_id' not in session:
        return redirect("/")
    
    dicc = {"id" : session['usuario_id']}
    usuario = Usuario.get_by_id(dicc) #Ontener el objeto User
    
    locales_comida = Local_comida.read_all() 
    
    return render_template("dashboard.html", usuario=usuario, locales_comida=locales_comida)


@app.route("/login", methods=["POST"])
def login():
    #request.form = {"email": "elena@codingdojo.com", "password": "Hola123"}
    #Verifico que el email esté en mi BD
    usuario = Usuario.get_by_email(request.form) #Recibo false si no existe ese usuario en mi BD o recibo un objeto de usuario con la info guardada en la BD

    if not usuario: #Si user es igual a Falso, es decir, que no existe...
        flash("Email not found", "login")
        return redirect("/")
    #Si user SI es objeto User...
    #user = User() .id=1, .first_name="Elena", .last_name="De Troya"... .password=#"g2&r&tfd$657%$7u$3"
    if not bcrypt.check_password_hash(usuario.contrasena, request.form["contrasena"]):  #entre los parentesis pongo el password hasheado, y el password NO hasheado
        flash("Password incorrect", "login")
        return redirect("/")
    
    session["usuario_id"] = usuario.id
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")