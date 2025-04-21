from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Servidor Flask de la actividad 1 del módulo 1 lección 2"

# Ruta GET /info
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        'app': 'Servidor Flask de ejemplo',
        'version': '2.0',
        'autora': 'Krystal S. Perez Rosado'
    })

# Ruta POST /mensaje
@app.route('/mensaje', methods=['POST'])
def mensaje():
    data = request.get_json()
    nombre = data.get('nombre', 'Usuario')
    respuesta = f"Hola, {nombre}. Tu mensaje ha sido recibido correctamente."
    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    app.run(debug=True)
