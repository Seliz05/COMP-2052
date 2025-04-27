from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Datos almacenados en memoria
usuarios = [{
  "usuarios": [
    {
      "id": 1,
      "nombre": "Spencer Reid",
      "correo": "Sreid@example.com"
    },
    {
      "id": 2,
      "nombre": "Penelope García",
      "correo": "Pgarcia@example.com"
    }
  ]
}
]


# Ruta GET /info
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "nombre_sistema": "Administrador de Productos y Usuarios",
        "version": "2.0",
        "descripcion": "Este sistema permite crear y visualizar usuarios colocandolos en una lista de usuarios."
    })

# Ruta POST /crear_usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    
    id = datos.get('id')
    nombre = datos.get('nombre')
    correo = datos.get('correo')

    if not nombre or not correo:
        return jsonify({"error": "Faltan datos: nombre y correo son obligatorios."}), 400

    nuevo_usuario = {"nombre": nombre, "correo": correo, "id": id}
    usuarios.append(nuevo_usuario)
    
    return jsonify({"mensaje": "Usuarios creados con exito.", "usuario": nuevo_usuario}), 201

# Ruta GET /usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({"usuarios": usuarios})

if __name__ == '__main__':
    app.run(debug=True)
