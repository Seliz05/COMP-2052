from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

# Formulario para login de usuario
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Formulario para registrar un nuevo usuario
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    
    role = SelectField(
        'Role',
        choices=[('Lector', 'Lector'), ('Bibliotecario', 'Bibliotecario'), ('Admin', 'Admin')],
        validators=[DataRequired()]
    )

    submit = SubmitField('Register')

# Formulario para cambiar la contraseña del usuario
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

# Formulario para crear o editar un libro
class LibroForm(FlaskForm):
    titulo = StringField('Título del libro', validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    autor = StringField('Autor', validators=[DataRequired(), Length(max=100)])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(max=20)])
    categoria = StringField('Categoría', validators=[DataRequired(), Length(max=50)])
    anio_publicacion = IntegerField('Año de publicación', validators=[DataRequired(), NumberRange(min=1000, max=2100)])
    estado = SelectField(
        'Estado',
        choices=[('Disponible', 'Disponible'), ('Prestado', 'Prestado')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Guardar')