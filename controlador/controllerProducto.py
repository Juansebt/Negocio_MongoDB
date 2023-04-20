from app import app,mongo,miConexion, productos, categorias
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import os


@app.route("/vistaProducto")
def vistaProducto():
    import controlador.controllerCategoria as cat
    listaCategorias = cat.listarCategorias()
    # listaCategorias = obtenerCategorias()
    producto = []
    print(listaCategorias)
    return render_template("frmProducto.html",listaCategorias=listaCategorias,producto=producto)


@app.route("/agregarProducto",methods=["POST"])
def agregarProducto():
    mensaje=""
    estado=False
    try:
        codigo = int(request.form["txtCodigo"])
        nombre = request.form["txtNombreP"]
        precio = int(request.form["txtPrecio"])
        categoria = request.form["cbCategoria"]
        import controlador.controllerCategoria as cat
        categoriaProducto = cat.categorias.find({"_id":categoria})
        producto = {
            "codigo":codigo,
            "nombre":nombre,
            "precio":precio,
            "categoria":ObjectId(categoria)
        }
        if (consultarProductoPorCodigo(codigo)):
            mensaje = f"Ya existe producto con ese código"
        else:        
            resultado = productos.insert_one(producto)
            if(resultado.acknowledged):
                idProducto = resultado.inserted_id
                archivo = request.files['fileFoto']
                nombreArchivo = secure_filename(archivo.filename)
                listaNombreArchivo = nombreArchivo.rsplit(".",1)
                extension = listaNombreArchivo[1].lower()
                nombreArchivoImagen = str(idProducto) + "." + str(extension)
                archivo.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreArchivoImagen))
                mensaje = f"Producto agregado correctamente"
                estado = True
                # return redirect("/listarProductos")
                estado2,listaProductos = obtenerProductos()
                return render_template("listarProductos.html",listaProductos=listaProductos,estado=estado,mensaje=mensaje)
    except mongo.errors as error:
        mensaje= f"Error al agregar producto{error}"
    import controlador.controllerCategoria as cat
    listaCategorias = cat.listarCategorias()
    return render_template("frmProducto.html",estado=estado,mensaje=mensaje,listaCategorias=listaCategorias,producto=producto)
    
    
def obtenerProductos():
    try:
        products = productos.find()
        return True,products
    except mongo.errors as error:
        return False,error
    

@app.route("/listarProductos")
def listarProductos():
    estado,listaProductos = obtenerProductos()
    return render_template("listarProductos.html",listaProductos=listaProductos,estado=estado)

@app.route("/eliminar/<string:idProducto>")
def eliminar(idProducto):
    estado = False
    mensaje = ""
    try:
        consulta = {"_id":ObjectId(idProducto)}
        resultado = productos.delete_one(consulta)
        if(resultado.acknowledged):
            nombreArchivo = str(idProducto)+".jpg"
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"]+"/"+nombreArchivo))
            estado =  True
            mensaje = f"Producto eliminado correctamente"
    except mongo.errors as error:
        mensaje = error
    estado2,listaProductos = obtenerProductos()
    return render_template("listarProductos.html",mensaje=mensaje,listaProductos=listaProductos,estado=estado)

@app.route("/consultarProducto/<string:idProducto>")
def consultarProducto(idProducto):
    try:
        consulta = {"_id":ObjectId(idProducto)}
        producto = productos.find_one(consulta)
        import controlador.controllerCategoria as cat
        listaCategorias = cat.listarCategorias()
        return render_template("frmEditarProducto.html",producto=producto,listaCategorias=listaCategorias)
    except mongo.errors as error:
        mensaje = error
        return render_template("listarProductos")
    
@app.route("/actualizarProducto",methods=["POST"])
def actualizarProducto():
    mensaje = ""
    estado = False
    try:
        idProducto = ObjectId(request.form["idProducto"])
        #nuevos parametros
        nuevoCodigo = int(request.form["txtCodigo"])
        nuevoNombre = request.form["txtNombreP"]
        nuevoPrecio = int(request.form["txtPrecio"])
        nuevoCategoria = request.form["cbCategoria"]
        
        producto = {
            "_id":idProducto,
            "codigo":nuevoCodigo,
            "nombre":nuevoNombre,
            "precio":nuevoPrecio,
            "categoria":ObjectId(nuevoCategoria)
        }
        
        consulta = {"$and" :[ {"_id": {"$ne": idProducto}},{"codigo":nuevoCodigo}]}
        resultado = productos.find_one(consulta)
        
        if(resultado):
            mensaje = f"Ya existe producto con ese código"
        else:
            criterio = {"_id":idProducto}
            consulta = {"$set":producto}
            resultado = productos.update_one(criterio,consulta)
            if(resultado.acknowledged):
                archivo = request.files['fileFoto']
                if(archivo.filename != ""):
                    nombreArchivo = secure_filename(archivo.filename)
                    listaNombreArchivo = nombreArchivo.rsplit(".",1)
                    extension = listaNombreArchivo[1].lower()
                    nombreArchivoImagen = str(idProducto) + "." + str(extension)
                    archivo.save(os.path.join(app.config["UPLOAD_FOLDER"],nombreArchivoImagen))
                mensaje = f"Producto actualizado"
                estado = True
                # return redirect("/listarProductos")
                estado2,listaProductos = obtenerProductos()
                return render_template("listarProductos.html",listaProductos=listaProductos,estado=estado,mensaje=mensaje)
            else:
                mensaje = f"¡NO es posible actualizar el producto, por favor revisar...!"
    except mongo.errors as error:
        mensaje=error
    import controlador.controllerCategoria as cat
    listaCategorias = cat.listarCategorias()
    return render_template("frmEditarProducto.html",estado=estado,mensaje=mensaje,listaCategorias=listaCategorias,producto=producto)
        
    
def consultarProductoPorCodigo(codigo):
    try:
        consulta = {"codigo":codigo}
        producto = productos.find_one(consulta)
        if(producto is not None):
            return True
        else:
            return False
    except mongo.errors as error:
        mensaje = error
        return False