# app.py
from flask import Flask, render_template, redirect, url_for, session, flash, jsonify
from flask_principal import Principal, Permission, RoleNeed, Identity, AnonymousIdentity, identity_loaded, UserNeed
from flask_principal import identity_changed, current_app
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_muy_segura_aqui'

# Configuración de Flask-Principal
Principal(app)

# Definición de permisos
# Necesidades (Needs) para roles
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))
viewer_permission = Permission(RoleNeed('viewer'))

# Base de datos de usuarios simulada
users_db = {
    'admin': {
        'password': generate_password_hash('adminpass'),
        'roles': ['admin', 'editor', 'viewer']
    },
    'editor1': {
        'password': generate_password_hash('editorpass'),
        'roles': ['editor']
    },
    'viewer1': {
        'password': generate_password_hash('viewerpass'),
        'roles': ['viewer']
    },
    'multirole': {
        'password': generate_password_hash('multipass'),
        'roles': ['editor', 'viewer']
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login/<username>/<password>')
def login(username, password):
    user = users_db.get(username)
    
    if user and check_password_hash(user['password'], password):
        # Establecer sesión de usuario
        session['username'] = username
        
        # Configurar identidad para Flask-Principal
        identity = Identity(username)
        identity_changed.send(current_app._get_current_object(), identity=identity)
        
        flash('Login exitoso', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Usuario o contraseña incorrectos', 'danger')
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    # Limpiar sesión
    session.pop('username', None)
    
    # Limpiar identidad
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Por favor inicia sesión primero', 'warning')
        return redirect(url_for('home'))
    
    return render_template('dashboard.html', username=session['username'])

@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin_panel():
    return render_template('admin_panel.html')

@app.route('/edit')
@editor_permission.require(http_exception=403)
def editor_panel():
    return render_template('editor_panel.html')

@app.route('/view')
@viewer_permission.require(http_exception=403)
def viewer_panel():
    return render_template('viewer_panel.html')

@app.route('/api/data')
@viewer_permission.require(http_exception=403)
def api_data():
    return jsonify({'data': 'Informacion confidencial'})

# Callback para cargar necesidades cuando la identidad está establecida
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Establecer la identidad del usuario
    username = session.get('username')
    if username:
        identity.provides.add(UserNeed(username))
        
        # Añadir roles del usuario
        user_roles = users_db.get(username, {}).get('roles', [])
        for role in user_roles:
            identity.provides.add(RoleNeed(role))

if __name__ == '__main__':
    app.run(debug=True)