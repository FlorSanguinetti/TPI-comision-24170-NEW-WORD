import mysql.connector
from mysql.connector import Error

from flask import Flask, request, jsonify

from flask_cors import CORS

from werkzeug.utils import secure_filename

import os
import time
#--------------------------------------------------------------------
app = Flask(__name__)
CORS(app) 

class Alumnos:
    def __init__(self, host, user, password, database):

        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f'USE {database}')
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err
            
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS newwordalumnos(
            dni INT NOT NULL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            nivel INT NOT NULL,
            imagen_url VARCHAR(255))''')
        self.conn.commit()
        self.cursor.close()

        self.cursor = self.conn.cursor(dictionary=True)

    def agregar_alumno(self, dni, nombre, apellido, email, nivel, imagen_url):
        sql = "INSERT INTO newwordalumnos (dni, nombre, apellido, email, nivel, imagen_url) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (dni, nombre, apellido, email, nivel, imagen_url)
        try:
            self.cursor.execute(sql,valores)
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.IntegrityError as e:
            if "1062" in str(e):
                print(f"Error: Ya existe un alumno con el DNI {dni}.")
            else:
                print(f"Error al agregar alumno: {e}")
            return None
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        
    def consultar_alumno(self, dni):
        self.cursor.execute(f"SELECT * FROM newwordalumnos WHERE dni = {dni}")
        return self.cursor.fetchone()
    
    def modificar_alumno(self, dni, nuevo_nombre, nuevo_apellido, nuevo_email, nuevo_nivel, nueva_imagen):
        sql = "UPDATE newwordalumnos SET nombre = %s, apellido = %s, email = %s, nivel = %s, imagen_url = %s WHERE dni = %s"
        valores = (nuevo_nombre, nuevo_apellido, nuevo_email, nuevo_nivel, nueva_imagen, dni)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0 
    
    def mostrar_alumnos(self, dni):
        alumnos = self.consultar_alumno(dni)
        if alumnos:
            print("-" * 40)
            print(f"DNI.....: {alumnos['dni']}")
            print(f"Nombre..: {alumnos['nombre']}")
            print(f"Apellido: {alumnos['apellido']}")
            print(f"Email...: {alumnos['email']}")
            print(f"Nivel...: {alumnos['nivel']}")
            print(f"Imagen..: {alumnos['imagen_url']}")
            print("-" * 40)
        else:
            print("Alumno no encontrado.")

    def listar_alumnos(self):
        self.cursor.execute("SELECT * FROM newwordalumnos")
        newword = self.cursor.fetchall()
        return newword
    
    def eliminar_alumno(self, dni):
        self.cursor.execute(f"DELETE FROM newwordalumnos WHERE dni = {dni}")
        self.conn.commit()
        return self.cursor.rowcount > 0
    
#Programa principal

newword = Alumnos(host='frsanguinetti.mysql.pythonanywhere-services.com', user='frsanguinetti', password='PALMAnova123*', database='frsanguinetti$newwordalumnos')

ruta_destino = '/home/frsanguinetti/mysite/static/imagenes/'

@app.route("/newwordalumnos", methods=["GET"])
def listar_alumnos():
    alumnos = newword.listar_alumnos()
    return jsonify(alumnos)

@app.route("/newwordalumnos/<int:dni>", methods=["GET"])
def mostrar_alumnos(dni):
    alumnos = newword.consultar_alumno(dni)
    if alumnos:
        return jsonify(alumnos)
    else:
        return "Producto no encontrado", 404
    
@app.route("/newwordalumnos", methods=["POST"])
def agregar_alumno(): 

    #Recojo los datos del form 
    dni = request.form['dni'] 
    nombre = request.form['nombre'] 
    apellido = request.form['apellido'] 
    email = request.form['email']   
    nivel = request.form['nivel']   
    imagen = request.files['imagen'] 
    nombre_imagen = "" 

    # Genero el nombre de la imagen 
    nombre_imagen = secure_filename(imagen.filename)  
    nombre_base, extension = os.path.splitext(nombre_imagen)  
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"  
    
    nuevo_dni = newword.agregar_alumno( dni, nombre, apellido, email, nivel, nombre_imagen) 

    if nuevo_dni is not None:     
        imagen.save(os.path.join(ruta_destino, nombre_imagen)) 
        return jsonify({"mensaje": "Alumno agregado correctamente.", "dni": nuevo_dni, "imagen": nombre_imagen}), 201 
    else: 
        return jsonify({"mensaje": "Error al agregar el producto."}), 500

@app.route("/newwordalumnos/<int:dni>", methods=["PUT"]) 
def modificar_alumno(dni): 
    #Se recuperan los nuevos datos del formulario 
    nuevo_nombre = request.form.get("nombre")
    nuevo_apellido = request.form.get("apellido") 
    nuevo_email = request.form.get("email") 
    nuevo_nivel = request.form.get("nivel")  
     
    # Verifica si se proporcionó una nueva imagen 
    if 'imagen' in request.files: 
        imagen = request.files['imagen'] 
        # Procesamiento de la imagen 
        nombre_imagen = secure_filename(imagen.filename)  
        nombre_base, extension = os.path.splitext(nombre_imagen)  
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
        # Guardar la imagen en el servidor 
        imagen.save(os.path.join(ruta_destino, nombre_imagen)) 
         
        # Busco el producto guardado
        alumno = newword.consultar_alumno(dni) 
        if alumno:
            imagen_vieja = alumno["imagen_url"] 
            # Armo la ruta a la imagen 
            ruta_imagen = os.path.join(ruta_destino, imagen_vieja) 
 
            # Y si existe la borro. 
            if os.path.exists(ruta_imagen): 
                os.remove(ruta_imagen) 
    else:      
        alumno = newword.consultar_alumno(dni) 
        if alumno: 
            nombre_imagen = alumno["imagen_url"] 
 
   # Se llama al método modificar_producto pasando el codigo del producto y los nuevos datos. 
    if newword.modificar_alumno(dni, nuevo_nombre, nuevo_apellido, nuevo_email, nuevo_nivel, nombre_imagen): 
        return jsonify({"mensaje": "Alumno modificado"}), 200 
    else: 
        return jsonify({"mensaje": "Alumno no encontrado"}), 403 
    
@app.route("/newwordalumnos/<int:dni>", methods=["DELETE"]) 
def eliminar_alumno(dni): 
# Primero, obtiene la información del producto para encontrar la imagen 
    alumno = newword.consultar_alumno(dni) 
    if alumno: 
    # Eliminar la imagen asociada si existe 
        ruta_imagen = os.path.join(ruta_destino, alumno['imagen_url']) 
        if os.path.exists(ruta_imagen): 
            os.remove(ruta_imagen) 
        # Luego, elimina el producto del catálogo 
        if newword.eliminar_alumno(dni): 
            return jsonify({"mensaje": "Producto eliminado"}), 200 
        else: 
            return jsonify({"mensaje": "Error al eliminar el producto"}), 500 
    else: 
        return jsonify({"mensaje": "Producto no encontrado"}), 404 

if __name__ == "__main__":
    app.run(debug=True)