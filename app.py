from flask import Flask, render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)

# Creación de base de datos y tabla
def inIt_database():
    conn = sqlite3.connect("almacen.db")

    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS producto(
            id INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio FLOAT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

inIt_database()

@app.route("/")
def index():
    return render_template("index.html")

# Mostrar productos
@app.route("/productos")
def productos():
    conn = sqlite3.connect("almacen.db")
    # Permite manejar los registros como diccionarios
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    return render_template("productos/index.html",productos = productos)

# Agregar producto
@app.route("/productos/create")
def create():
    return render_template("productos/create.html")

@app.route("/productos/create/save",methods=['POST'])
def producto_save():
    descripcion = request.form['descripcion']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])

    conn  = sqlite3.connect("almacen.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO producto (descripcion,cantidad,precio) VALUES(?,?,?)", (descripcion,cantidad,precio))

    conn.commit()
    conn.close()
    return redirect('/productos')

#Editar producto
@app.route("/productos/edit/<int:id>")
def producto_edit(id):
    conn = sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE id = ?",(id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template("productos/edit.html",producto=producto)

@app.route("/productos/update",methods=['POST'])
def producto_update():
    id = request.form['id']
    descripcion = request.form['descripcion']
    cantidad = int(request.form['cantidad'])
    precio = float(request.form['precio'])

    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE producto SET descripcion = ?,cantidad=?,precio=? WHERE id=?",(descripcion,cantidad,precio,id))
    conn.commit()
    conn.close()

    return redirect("/productos")

#Eliminar registro
@app.route("/productos/delete/<int:id>")
def productos_delete(id):
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE id=?",(id,))
    conn.commit()
    conn.close()

    return redirect('/productos')

if __name__ == "__main__":
    app.run(debug=True)