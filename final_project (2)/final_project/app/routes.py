from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.forms import LibroForm, ChangePasswordForm
from app.models import db, Libro, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Página pública de inicio.
    """
    return render_template('index.html')

@main.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario cambiar su contraseña.
    """
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('La contraseña actual es incorrecta.')
            return render_template('cambiar_password.html', form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('✅ Contraseña actualizada correctamente.')
        return redirect(url_for('main.dashboard'))

    return render_template('cambiar_password.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    """
    Panel principal del usuario. Muestra libros.
    """
    # Los lectores ven todos los libros, bibliotecarios solo los que agregaron, admins todos.
    if current_user.role.name == 'Lector':
        libros = Libro.query.all()
    elif current_user.role.name == 'Bibliotecario':
        libros = Libro.query.filter_by(bibliotecario_id=current_user.id).all()
    else:  # Admin
        libros = Libro.query.all()

    return render_template('dashboard.html', libros=libros)

@main.route('/libros', methods=['GET', 'POST'])
@login_required
def libros():
    """
    Crear nuevo libro. Solo para Bibliotecarios o Admins.
    """
    if current_user.role.name not in ['Bibliotecario', 'Admin']:
        flash('No tienes permiso para crear libros.')
        return redirect(url_for('main.dashboard'))

    form = LibroForm()
    if form.validate_on_submit():
        libro = Libro(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            autor=form.autor.data,
            isbn=form.isbn.data,
            categoria=form.categoria.data,
            anio_publicacion=form.anio_publicacion.data,
            estado=form.estado.data,
            bibliotecario_id=current_user.id
        )
        db.session.add(libro)
        db.session.commit()
        flash("Libro creado correctamente.")
        return redirect(url_for('main.dashboard'))

    return render_template('libros_form.html', form=form)

@main.route('/libros/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_libro(id):
    """
    Editar libro existente. Solo Admin o bibliotecario dueño.
    """
    libro = Libro.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Bibliotecario'] or (
        libro.bibliotecario_id != current_user.id and current_user.role.name != 'Admin'):
        flash('No tienes permiso para editar este libro.')
        return redirect(url_for('main.dashboard'))

    form = LibroForm(obj=libro)
    if form.validate_on_submit():
        libro.titulo = form.titulo.data
        libro.descripcion = form.descripcion.data
        libro.autor = form.autor.data
        libro.isbn = form.isbn.data
        libro.categoria = form.categoria.data
        libro.anio_publicacion = form.anio_publicacion.data
        libro.estado = form.estado.data
        db.session.commit()
        flash("Libro actualizado correctamente.")
        return redirect(url_for('main.dashboard'))

    return render_template('libros_form.html', form=form, editar=True)

@main.route('/libros/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_libro(id):
    """
    Eliminar libro. Solo Admin o bibliotecario dueño.
    """
    libro = Libro.query.get_or_404(id)

    if current_user.role.name not in ['Admin', 'Bibliotecario'] or (
        libro.bibliotecario_id != current_user.id and current_user.role.name != 'Admin'):
        flash('No tienes permiso para eliminar este libro.')
        return redirect(url_for('main.dashboard'))

    db.session.delete(libro)
    db.session.commit()
    flash("Libro eliminado correctamente.")
    return redirect(url_for('main.dashboard'))

@main.route('/usuarios')
@login_required
def listar_usuarios():
    """
    Lista usuarios solo para Admin.
    """
    if current_user.role.name != 'Admin':
        flash("No tienes permiso para ver esta página.")
        return redirect(url_for('main.dashboard'))

    usuarios = User.query.join(User.role).all()
    return render_template('usuarios.html', usuarios=usuarios)