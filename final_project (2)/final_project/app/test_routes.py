from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Libro

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def index():
    """
    Página pública simple.
    """
    return '<h1>API de Libros corriendo en modo prueba.</h1>'

@main.route('/libros', methods=['GET'])
@login_required
def listar_libros():
    """
    Retorna lista de libros (JSON). Visible para todos los roles.
    """
    libros = Libro.query.all()
    data = [
        {
            'id': libro.id,
            'titulo': libro.titulo,
            'descripcion': libro.descripcion,
            'autor': libro.autor,
            'bibliotecario_id': libro.bibliotecario_id
        }
        for libro in libros
    ]
    return jsonify(data), 200

@main.route('/libros/<int:id>', methods=['GET'])
@login_required
def obtener_libro(id):
    """
    Retorna un solo libro por ID.
    """
    libro = Libro.query.get_or_404(id)
    data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'descripcion': libro.descripcion,
        'autor': libro.autor,
        'bibliotecario_id': libro.bibliotecario_id
    }
    return jsonify(data), 200

@main.route('/libros', methods=['POST'])
@login_required
def crear_libro():
    """
    Crea un libro (solo Bibliotecario o Admin).
    """
    if current_user.role.name not in ['Bibliotecario', 'Admin']:
        return jsonify({'error': 'No tienes permiso para crear libros.'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se proporcionaron datos'}), 400

    libro = Libro(
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        autor=data.get('autor'),
        bibliotecario_id=current_user.id
    )

    db.session.add(libro)
    db.session.commit()
    return jsonify({'message': 'Libro creado', 'id': libro.id}), 201

@main.route('/libros/<int:id>', methods=['PUT'])
@login_required
def actualizar_libro(id):
    """
    Actualiza libro (solo Admin o bibliotecario dueño).
    """
    libro = Libro.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Bibliotecario'] or \
       (libro.bibliotecario_id != current_user.id and current_user.role.name != 'Admin'):
        return jsonify({'error': 'No tienes permiso para actualizar este libro.'}), 403

    data = request.get_json()
    libro.titulo = data.get('titulo', libro.titulo)
    libro.descripcion = data.get('descripcion', libro.descripcion)
    libro.autor = data.get('autor', libro.autor)

    db.session.commit()
    return jsonify({'message': 'Libro actualizado', 'id': libro.id}), 200

@main.route('/libros/<int:id>', methods=['DELETE'])
@login_required
def eliminar_libro(id):
    """
    Elimina libro (solo Admin o bibliotecario dueño).
    """
    libro = Libro.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Bibliotecario'] or \
       (libro.bibliotecario_id != current_user.id and current_user.role.name != 'Admin'):
        return jsonify({'error': 'No tienes permiso para eliminar este libro.'}), 403

    db.session.delete(libro)
    db.session.commit()
    return jsonify({'message': 'Libro eliminado', 'id': libro.id}), 200
