from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Simulación de base de datos
users = {
    "admin": User(1, "admin", "secreto", "admin"),
    "user1": User(2, "user1", "clave123", "usuario")
}
