from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum  # Para el campo estado

# Carga el usuario desde su ID (para Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Modelo de rol (Admin, Bibliotecario, Lector)
class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    # Relación con usuarios
    users = db.relationship('User', backref='role', lazy=True)

# Modelo de usuario
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # Relación con libros que administra este usuario (si es bibliotecario)
    libros = db.relationship('Libro', backref='bibliotecario', lazy=True)

    def set_password(self, password: str):
        """Genera el hash de la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica la contraseña contra el hash almacenado."""
        return check_password_hash(self.password_hash, password)

# Modelo de libros
class Libro(db.Model):
    __tablename__ = 'libro'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)  # Campo añadido
    autor = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    anio_publicacion = db.Column(db.Integer, nullable=False)
    estado = db.Column(
        Enum('Disponible', 'Prestado', 'Dañado', name='estado_enum'),
        nullable=False,
        server_default='Disponible'
    )
    # Foreign key para relacionar libro con bibliotecario (usuario)
    bibliotecario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)