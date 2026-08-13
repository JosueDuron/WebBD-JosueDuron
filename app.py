import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-desarrollo')

# --- Configuración de la base de datos ---
# En producción (Render) esta variable la inyecta el proveedor automáticamente.
# En local, si no existe, usa SQLite para que puedas probar sin configurar nada.
db_url = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
# Render entrega postgres:// pero SQLAlchemy 1.4+ requiere postgresql://
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------------------------------------------------
# MODELOS (2 entidades relacionadas: Curso -> Estudiante)
# ---------------------------------------------------------

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300))
    estudiantes = db.relationship('Estudiante', backref='curso', cascade='all, delete-orphan')


class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)


with app.app_context():
    db.create_all()


# ---------------------------------------------------------
# RUTAS - PÁGINA PRINCIPAL
# ---------------------------------------------------------

@app.route('/')
def index():
    total_estudiantes = Estudiante.query.count()
    total_cursos = Curso.query.count()
    return render_template('index.html',
                            total_estudiantes=total_estudiantes,
                            total_cursos=total_cursos)


# ---------------------------------------------------------
# CRUD DE CURSOS
# ---------------------------------------------------------

@app.route('/cursos')
def listar_cursos():
    cursos = Curso.query.all()
    return render_template('cursos.html', cursos=cursos)


@app.route('/cursos/nuevo', methods=['GET', 'POST'])
def crear_curso():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        if not nombre:
            flash('El nombre del curso es obligatorio.', 'danger')
            return redirect(url_for('crear_curso'))
        curso = Curso(nombre=nombre, descripcion=descripcion)
        db.session.add(curso)
        db.session.commit()
        flash('Curso creado correctamente.', 'success')
        return redirect(url_for('listar_cursos'))
    return render_template('curso_form.html', curso=None)


@app.route('/cursos/<int:curso_id>/editar', methods=['GET', 'POST'])
def editar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    if request.method == 'POST':
        curso.nombre = request.form.get('nombre', '').strip()
        curso.descripcion = request.form.get('descripcion', '').strip()
        db.session.commit()
        flash('Curso actualizado correctamente.', 'success')
        return redirect(url_for('listar_cursos'))
    return render_template('curso_form.html', curso=curso)


@app.route('/cursos/<int:curso_id>/eliminar', methods=['POST'])
def eliminar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    db.session.delete(curso)
    db.session.commit()
    flash('Curso eliminado.', 'info')
    return redirect(url_for('listar_cursos'))


# ---------------------------------------------------------
# CRUD DE ESTUDIANTES
# ---------------------------------------------------------

@app.route('/estudiantes')
def listar_estudiantes():
    estudiantes = Estudiante.query.all()
    return render_template('estudiantes.html', estudiantes=estudiantes)


@app.route('/estudiantes/nuevo', methods=['GET', 'POST'])
def crear_estudiante():
    cursos = Curso.query.all()
    if not cursos:
        flash('Primero debes crear al menos un curso.', 'warning')
        return redirect(url_for('crear_curso'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        curso_id = request.form.get('curso_id')

        if not nombre or not correo or not curso_id:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('crear_estudiante'))

        estudiante = Estudiante(nombre=nombre, correo=correo, curso_id=curso_id)
        db.session.add(estudiante)
        db.session.commit()
        flash('Estudiante registrado correctamente.', 'success')
        return redirect(url_for('listar_estudiantes'))

    return render_template('estudiante_form.html', estudiante=None, cursos=cursos)


@app.route('/estudiantes/<int:estudiante_id>/editar', methods=['GET', 'POST'])
def editar_estudiante(estudiante_id):
    estudiante = Estudiante.query.get_or_404(estudiante_id)
    cursos = Curso.query.all()
    if request.method == 'POST':
        estudiante.nombre = request.form.get('nombre', '').strip()
        estudiante.correo = request.form.get('correo', '').strip()
        estudiante.curso_id = request.form.get('curso_id')
        db.session.commit()
        flash('Estudiante actualizado correctamente.', 'success')
        return redirect(url_for('listar_estudiantes'))
    return render_template('estudiante_form.html', estudiante=estudiante, cursos=cursos)


@app.route('/estudiantes/<int:estudiante_id>/eliminar', methods=['POST'])
def eliminar_estudiante(estudiante_id):
    estudiante = Estudiante.query.get_or_404(estudiante_id)
    db.session.delete(estudiante)
    db.session.commit()
    flash('Estudiante eliminado.', 'info')
    return redirect(url_for('listar_estudiantes'))


if __name__ == '__main__':
    app.run(debug=True)
