from app import app,mongo,categorias
from flask import Flask, render_template, request

@app.route("/vistaCategoria")
def vistaCategoria():
    return render_template("frmCategoria.html")


def listarCategorias():
    mensaje = ""
    try:
        listarCategorias = categorias.find()
        return listarCategorias
    except mongo.errors as error:
        mensaje = error

@app.route("/agregarCategoria",methods=["POST"])
def agregarCategoria():
    mensaje = ""
    estado = False
    try:
        nombre = request.form["txtNombre"]
        categoria = {
            "nombre":nombre
        }
        existe = categorias.find_one(categoria)
        if (existe is not None):
            resulado = categorias.insert_one(categoria)
            if (resulado.acknowledged):
                idCategoria = resulado.inserted_id
                mensaje = f"Categoria agregada correctamente"
                estado = True
            else:
                mensaje = f"Problemaas al agregar la categoria"
        else:
            mensaje = f"Ya existe la categoria {nombre}"
    except mongo.errors as error:
        mensaje = f"Error al agregar categoria{error}"
        
    return render_template("frmCategoria.html",estado=estado,mensaje=mensaje)