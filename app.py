from flask import Flask, request, render_template
import pymongo as mongo


#crear objeto de tipo flask
app = Flask(__name__)

#configura carpeta para subir las fotos de los productos
app.config['UPLOAD_FOLDER']='./static/images'

#conexión al servidor mongodb
miConexion = mongo.MongoClient("mongodb://localhost:27017/") 

#acceso a la base de datos
baseDatos = miConexion["miTienda"] 

#objetos para referencias a la colecciones de la base de datos
productos = baseDatos["productos"]
categorias = baseDatos["categorias"]

#validar que la base de datos exista
def existeBaseDatos():
    listaBaseDatos = miConexion.list_database_names()
    if "miTienda" in listaBaseDatos:
        return True
    return False

#raiz del sitio
@app.route("/")
def inicio():
    return render_template("inicio.html")

#controladores
from controlador.controllerCategoria import *
from controlador.controllerProducto import *

#iniciar el servidor web
if __name__=='__main__':
    app.run(port=3000,debug=True)