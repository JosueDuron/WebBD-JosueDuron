# Sistema de Gestión Académica

Aplicación web con conexión a base de datos que permite administrar cursos y estudiantes mediante operaciones CRUD completas (Crear, Leer, Actualizar, Eliminar).

## Datos del estudiante

- Nombre: Josue Elias Duron Miguel
- Número de cuenta: 202410010782

## Descripcion del proyecto

El sistema permite gestionar dos entidades relacionadas entre si:

- Cursos: registro de los cursos disponibles, con nombre y descripcion.
- Estudiantes: registro de estudiantes, cada uno asociado a un curso mediante una relacion de clave foranea.

La aplicacion cuenta con una interfaz web funcional, formularios de creacion y edicion, listados con tablas, confirmacion antes de eliminar registros, y mensajes de retroalimentacion para el usuario.

## Tecnologias utilizadas

- Backend: Python 3, Flask
- ORM: Flask-SQLAlchemy
- Base de datos: PostgreSQL (en la nube, mediante Render)
- Frontend: HTML5, Bootstrap 5, Font Awesome
- Servidor de produccion: Gunicorn
- Despliegue: Render

## Estructura del proyecto

```
app_web_bd/
├── app.py                     Backend: modelos, rutas y logica CRUD
├── seed.py                    Script para insertar datos de prueba
├── requirements.txt           Dependencias del proyecto
├── Procfile                   Comando de arranque para Render
├── .gitignore
├── templates/
│   ├── base.html               Plantilla base con navegacion
│   ├── index.html              Panel principal
│   ├── cursos.html             Listado de cursos
│   ├── curso_form.html         Formulario de curso (crear/editar)
│   ├── estudiantes.html        Listado de estudiantes
│   └── estudiante_form.html    Formulario de estudiante (crear/editar)
└── static/
```

## Modelo de datos

### Curso
| Campo       | Tipo    | Descripcion                          |
|-------------|---------|---------------------------------------|
| id          | Integer | Llave primaria                        |
| nombre      | String  | Nombre del curso                      |
| descripcion | String  | Descripcion breve del curso           |

### Estudiante
| Campo           | Tipo     | Descripcion                                  |
|------------------|----------|-----------------------------------------------|
| id               | Integer  | Llave primaria                                |
| nombre           | String   | Nombre completo del estudiante                |
| correo           | String   | Correo electronico                            |
| fecha_registro   | DateTime | Fecha en que se registro (automatica)         |
| curso_id         | Integer  | Llave foranea que referencia a Curso.id       |

Relacion: un curso puede tener varios estudiantes (1 a muchos).

## Funcionalidades (CRUD)

### Cursos
- Listar todos los cursos registrados
- Crear un nuevo curso
- Editar un curso existente
- Eliminar un curso (elimina en cascada a sus estudiantes asociados)

### Estudiantes
- Listar todos los estudiantes registrados
- Crear un nuevo estudiante, asignandolo a un curso
- Editar los datos de un estudiante
- Eliminar un estudiante

## Instalacion y ejecucion en local

### Requisitos previos
- Python 3.10 o superior
- pip

### Pasos

1. Clonar o descomprimir el proyecto y entrar a la carpeta:
```
cd app_web_bd
```

2. Crear un entorno virtual e instalar dependencias:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
En Windows, activar el entorno con:
```
venv\Scripts\activate
```

3. Ejecutar la aplicacion:
```
python3 app.py
```

4. Abrir en el navegador:
```
http://127.0.0.1:5000
```

Si no se configura la variable de entorno `DATABASE_URL`, la aplicacion usa automaticamente una base de datos SQLite local (`local.db`), util para pruebas rapidas sin necesidad de configurar PostgreSQL.

### Cargar datos de prueba

Para poblar la base de datos con cursos y estudiantes de ejemplo:
```
python3 seed.py
```
El script puede ejecutarse varias veces sin duplicar los registros existentes.

## Despliegue en Render

1. Subir el proyecto a un repositorio de GitHub.

2. Crear una base de datos PostgreSQL en Render (New -> PostgreSQL) y copiar el Internal Database URL.

3. Crear un Web Service en Render conectado al repositorio, con la siguiente configuracion:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. Agregar las variables de entorno en la seccion Environment del Web Service:
   - `DATABASE_URL`: el Internal Database URL copiado en el paso 2
   - `SECRET_KEY`: una cadena de texto aleatoria

5. Desplegar. Al iniciar, la aplicacion crea automaticamente las tablas necesarias en la base de datos si no existen.

6. Para cargar datos de prueba en la base de datos de produccion, abrir la pestana Shell del Web Service en Render y ejecutar:
```
python3 seed.py
```

## Notas tecnicas

- La creacion de tablas se realiza automaticamente mediante `db.create_all()` al iniciar la aplicacion, por lo que no es necesario ejecutar sentencias SQL manuales para crear las entidades.
- `db.create_all()` no modifica tablas ya existentes; si se realizan cambios en los modelos despues del primer despliegue, estos no se reflejaran automaticamente en una base de datos ya creada.
- Las validaciones de formularios se realizan tanto en el frontend (atributos `required` de HTML) como en el backend (verificacion de campos vacios antes de guardar).
