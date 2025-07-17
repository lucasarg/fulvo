from flask import Flask, render_template, request, redirect, flash, url_for, session
import sqlite3
from init_db import init_db
#texto agregado para practicar una educion a github

app = Flask(__name__)
app.secret_key = "clave-secreta-muy-segura"  # usá una string difícil en producción

#ruta principal
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")

        if usuario == "admin" and clave == "1234":
            session["usuario"] = usuario
            flash("Sesión iniciada correctamente", "success")
            return redirect(url_for("inicio"))
        else:
            flash("Credenciales incorrectas", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Sesión cerrada", "success")
    return redirect(url_for("login"))

#formulario
@app.route("/form")
def formulario():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("form.html")

# Procesar formulario y guardar en base de datos
@app.route("/procesar", methods=["POST"])
def procesar():
    if "usuario" not in session:
        return redirect(url_for("login"))
        
    nombre = request.form.get("nombre")
    posicion = request.form.get("posicion")
    numero = request.form.get("numero")
    equipo = request.form.get("equipo")

    if not nombre.strip() or not posicion.strip() or not numero.strip():
        flash("Todos los campos obligatorios deben completarse.")
        return redirect(url_for("formulario"))

    conn = sqlite3.connect('basedatos.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO jugadores (nombre, posicion, numero, equipo)
        VALUES (?, ?, ?, ?)
    """, (nombre, posicion, numero, equipo))
    conn.commit()
    conn.close()

    flash(f"{nombre} agregado correctamente.")
    return redirect(url_for("formulario"))

    
    
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conn = sqlite3.connect('basedatos.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jugadores WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Registro eliminado correctamente.")
    return redirect(url_for("listado"))
    


# Ver todos los nombres guardados
@app.route("/listado")
def listado():
    if "usuario" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect('basedatos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, posicion, numero, equipo FROM jugadores")
    jugadores = cursor.fetchall()
    conn.close()
    return render_template("listado.html", jugadores=jugadores)

@app.route("/editar/<int:id>")
def editar(id):
    conn = sqlite3.connect('basedatos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, posicion, numero, equipo FROM jugadores WHERE id = ?", (id,))
    jugador = cursor.fetchone()
    conn.close()

    if jugador:
        return render_template("editar.html", id=id, nombre=jugador[0], posicion=jugador[1], numero=jugador[2], equipo=jugador[3])
    else:
        flash("Jugador no encontrado.")
        return redirect(url_for("listado"))


@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    nombre = request.form.get("nombre")
    posicion = request.form.get("posicion")
    numero = request.form.get("numero")
    equipo = request.form.get("equipo")

    if not nombre.strip() or not posicion.strip() or not numero.strip():
        flash("Todos los campos obligatorios deben completarse.")
        return redirect(url_for("editar", id=id))

    conn = sqlite3.connect('basedatos.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE jugadores SET nombre = ?, posicion = ?, numero = ?, equipo = ?
        WHERE id = ?
    """, (nombre, posicion, numero, equipo, id))
    conn.commit()
    conn.close()

    flash("Jugador actualizado correctamente.")
    return redirect(url_for("listado"))

    



if __name__ == "__main__":
    init_db()
    app.run(debug=True)
