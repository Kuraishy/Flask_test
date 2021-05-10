from flask import Flask, redirect, url_for, render_template, request, session, flash
import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
#se crea una secrt key para las sesiones
#app.secret_key = "sjfdsjalfjlksdj"
app.secret_key = str(os.urandom(16))
app.permanent_session_lifetime = timedelta(days=1)


#crear un database de la app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

###########SQALCHEMYT################
class users(db.Model):
	_id = db.Column("id",db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))


	#incluir los campos importtantes
	def __init__(self, name, email):
		self.name  =name
		self.email =email
################################################

@app.route("/")
def home():
	return render_template("index.html",content = "Test")

@app.route("/login", methods =["POST","GET"])
def login():
	#recive datos atraves del back end (POST)
	# atravez del url (GET)
	if request.method == "POST":
		session.permanente = True #hacer una sesion "permanente"
		user = request.form["nombre_input"] #crea una sesion para recordar el usuario
		print(user)
		session["user"] = user

		#si usuario ya existe 
		# obtener informacion del database
		found_user = users.query.filter_by(name=user).first() #filter_buy es en donde buscamos
		if found_user:#si encontramos a un usuario
			session["email"]= found_user.email
		else:
			# crea una clase y asa usuario y none
			usr = users(user, None)
			db.session.add(usr)#agrega al usuario al databas
			db.session.commit()        #acepta cambios


		flash(f"conexion exitosa: {user}","info")
		return redirect(url_for("user"))
	else:
		#si el usuario ya esta dentro
		if "user" in session:
			user = session["user"]
			flash(f"Ya estas conectado: {user}","info")
			return redirect(url_for("user"))
		return render_template("login.html")


@app.route("/view")
#nos muestra todas las informacione
def view():
	return render_template("view.html", values=users.query.all())



@app.route("/user",methods=["POST","GET"])
def user():
	email = None
	#si hay una sesion creada redirecciona a la pagina
	if  "user" in session:
		user = session["user"]
		if request.method=="POST": # si el usuario ingresado envia post
			email = request.form["email"] #obtener el email y guardarlo
			session["email"] = email
			found_user = users.query.filter_by(name=user ).first() #filter_buy es en donde buscamos
			found_user.email = email
			db.session.commit()
			flash("Correo Guardado")

		# si no envia nada, entonces ver si existe un email
		else:
			#en la sesion
			if "email" in session:
				email = session["email"]
		return render_template("user.html", user=user, email=email)

	# si no hay sesiones redirecciona al login
	else:
		flash(f"No has ingresado","info")
		return redirect(url_for("login"))



@app.route("/logout")
def logout():
	#remueve el data de la sesion, el none dice que se 
	# remueva la data
	
	#muestra una imagen (txt, categorioa) la categoria sirve para
	# mostrar iconos
	if "user" in session:
		user = session["user"]
		flash(f"Haz sido desconectado: {user}","info")
	session.pop("user", None)
	session.pop("email", None)
	#redirectiona a pagina
	return redirect(url_for("login"))

if __name__=="__main__":
	db.create_all()
	#debug = true nos permite ver los cambios sin tener que reiniciar
	app.run(debug=True)#, host='192.168.1.72')










"""@app.route("/login", methods=["POST","GET"])
def login():
	if request.method == "POST":
		user = request.form["nombre_input"]
		return redirect(url_for("user", usr=user))
	else:
		return render_template("login.html")

@app.route("/<usr>")
def user(usr):
	return f"<h1>{usr}</h1>"""