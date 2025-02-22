from flask import request, jsonify
from config import app, db
from models import usuarios  

@app.route("/buscar_usuarios", methods=["GET"])
def buscar_usuarios():
    query = request.args.get('query', '')  # Obtener el query desde la URL
    usuarios_lista = [
        {"id": 1, "nombre": "toji", "lastname": "fushiguro", "email": "toji@example.com"},
        {"id": 2, "nombre": "gojo", "lastname": "satoru", "email": "gojo@example.com"},
        {"id": 3, "nombre": "sukuna", "lastname": "riomen", "email": "sukuna@example.com"},
        {"id": 4, "nombre": "batman", "lastname": "bruce", "email": "batman@example.com"},
    ]
    
    # Filtrar usuarios si hay un query
    if query:
        usuarios_filtrados = [
            usuario for usuario in usuarios_lista
            if query.lower() in usuario["nombre"].lower() or
               query.lower() in usuario["email"].lower() or
               query.lower() in usuario["lastname"].lower()
        ]
    else:
        usuarios_filtrados = usuarios_lista  # Si no hay query, devolver todos los usuarios
    
    return jsonify({"usuarios": usuarios_filtrados})

@app.route("/usuarioslista", methods=["GET"])
def obtener_usuarios():
    # Arreglo de ejemplo de usuarios
    usuarios_lista = [
        {"id": 1, "nombre": "toji", "lastname": "fushiguro", "email": "toji@example.com"},
        {"id": 2, "nombre": "gojo", "lastname": "satoru", "email": "gojo@example.com"},
        {"id": 3, "nombre": "sukuna", "lastname": "riomen", "email": "sukuna@example.com"},
        {"id": 4, "nombre": "batman", "lastname": "bruce", "email": "batman@example.com"},
    ]
    
    # Convertimos el arreglo a formato JSON (aunque ya está en formato dict)
    return jsonify({"usuarios": usuarios_lista})

@app.route("/agregarusuario", methods=["POST"])
def crear():
    nombre = request.json.get("nombre")
    email = request.json.get("email")
    lastname = request.json.get("lastname")

    if not nombre or not email or not lastname:
        return (
            jsonify({"message": "Debes agregar un nombre, email y lastname"}),
            400,
        )

    nuevo_usuario = usuarios(nombre=nombre, email=email, lastname=lastname)  
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Usuario creado!"}), 201

@app.route("/modificarusuario/<int:usuario_id>", methods=["PATCH"])
def actualizar(usuario_id):
    usuario = usuarios.query.get(usuario_id)  

    if not usuario:
        return jsonify({"message": "Usuario no encontrado"}), 404

    data = request.json
    usuario.nombre = data.get("nombre", usuario.nombre)
    usuario.email = data.get("email", usuario.email)
    usuario.lastname = data.get("lastname", usuario.lastname)

    db.session.commit()

    return jsonify({"message": "Actualizado"}), 200

@app.route("/eliminarusuario/<int:usuario_id>", methods=["DELETE"])
def borrar(usuario_id):
    usuario = usuarios.query.get(usuario_id)  

    if not usuario:
        return jsonify({"message": "No encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Eliminado!"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
