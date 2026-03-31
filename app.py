from flask import Flask, flash, redirect, render_template, request, jsonify, url_for, session
from flask_jwt_extended import (
    JWTManager, create_access_token, decode_token, jwt_required, get_jwt_identity
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mysqldb import MySQL
import pickle
import joblib
import json 

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)
limiter = Limiter(get_remote_address, app=app)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'bd_proyecto'

mysql = MySQL(app)

modelo_cargado = joblib.load("Modelo/pipeline_sentimientos.pkl")


@app.route("/")
def home():
    return redirect(url_for("login_proyecto"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")

        if not usuario or not clave:
            flash("Por favor, ingrese un nombre de usuario y contraseña", "error")
            return redirect(url_for("login"))
        
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "SELECT id_usuario, nombre, usuario, clave FROM usuarios WHERE usuario = %s AND clave = %s",
                (usuario, clave)
            )
            user = cursor.fetchone()
            cursor.close()

            if user:
                session["token"] = create_access_token(identity=user[0])
                session["usuario"] = user[2]
                session["nombre"] = user[1]

                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for("predict"))

            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for("login"))

        except Exception as e:
            flash(f"Error al conectar con la base de datos: {str(e)}", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")

        if not nombre or not usuario or not clave:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("register"))

        try:
            cursor = mysql.connection.cursor()

            cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", (usuario,))
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                cursor.close()
                flash("Ese nombre de usuario ya está en uso", "error")
                return redirect(url_for("register"))

            cursor.execute(
                "INSERT INTO usuarios (nombre, usuario, clave) VALUES (%s, %s, %s)",
                (nombre, usuario, clave)
            )
            mysql.connection.commit()
            cursor.close()

            flash("Usuario registrado correctamente", "success")
            return redirect(url_for("login"))

        except Exception as e:
            flash(f"Error al registrar usuario: {str(e)}", "error")
            return redirect(url_for("register"))

    return render_template("register.html")
@app.route("/logout")
def logout():
    session.pop("token", None),
    session.pop("username", None),
    session.pop("nombre", None)

    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("login_proyecto"))

if __name__ == "__main__":
    app.run(debug=True)