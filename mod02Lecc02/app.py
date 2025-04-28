from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'una_clave_secreta_segura'

# Formulario de registro
class RegistrationForm(FlaskForm):
    name = StringField('Nombre', validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(min=3, message="El nombre debe tener al menos 3 caracteres.")
    ])
    email = StringField('Correo', validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="Ingrese un correo válido.")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
    ])

# Ruta principal
@app.route('/')
def home():
    return render_template('home.html')

# Ruta de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Aquí se manejaría el registro del usuario
        # Por ejemplo, guardar datos en la base de datos
        return redirect(url_for('registro_exitoso'))
    return render_template('index.html.jinja2', form=form)

@app.route('/registro_exitoso')
def registro_exitoso():
    return "<h2>¡Registro exitoso!</h2><p>Gracias por registrarte.</p><a href='/'>Volver al inicio</a>"

if __name__ == '__main__':
    app.run(debug=True)
