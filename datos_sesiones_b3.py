"""
Contenido enriquecido del Bloque 3 (sesiones 21 a 30).
Persistencia relacional, ORM y seguridad OWASP.
"""

BLOQUE_3 = {
    21: {
        "pregunta": "¿Qué pasa con tus datos cuando el servidor se reinicia?",
        "prerrequisitos": [
            "Sesión 20: API segura del Hito 2",
            "Saber qué es una tabla y una fila",
        ],
        "objetivos": [
            "Persistir datos en una base SQLite.",
            "Escribir consultas SQL parametrizadas.",
            "Verificar que los datos sobreviven al reinicio del proceso.",
        ],
        "conceptos": [
            {
                "termino": "Base de datos",
                "definicion": "Sistema que organiza y conserva datos fuera de la memoria del programa.",
                "analogia": "Como un archivero: los expedientes siguen ahí aunque cierres la oficina.",
            },
            {
                "termino": "Tabla",
                "definicion": "Conjunto de filas con la misma estructura de columnas.",
                "analogia": "Como una hoja de cálculo con encabezados fijos.",
            },
            {
                "termino": "SQL",
                "definicion": "Lenguaje para crear, consultar y modificar datos relacionales.",
                "analogia": "Como el idioma común entre la aplicación y el archivero.",
            },
            {
                "termino": "Persistencia",
                "definicion": "Capacidad de que un dato siga existiendo después de terminar el proceso.",
                "analogia": "Como escribir en un cuaderno en vez de memorizar.",
            },
        ],
        "resultado": {
            "titulo": "Tus libros sobrevivirán al reinicio",
            "lenguaje": "text",
            "codigo": """POST /api/libros  {"titulo":"Rayuela","anio":1963}
HTTP/1.1 201 Created
{"id":1,"titulo":"Rayuela","anio":1963}

GET /api/libros
HTTP/1.1 200 OK
{"libros":[{"id":1,"titulo":"Rayuela","anio":1963}]}

$ sqlite3 biblioteca.db "SELECT id, titulo FROM libros;"
1|Rayuela

El proceso puede reiniciarse: la fila sigue en biblioteca.db.""",
            "nota": "La memoria se pierde al reiniciar; el archivo de la base de datos no.",
        },
        "reto": {
            "enunciado": "Implementa un CRUD mínimo que guarde los libros en una base SQLite real, no en una lista de Python.",
            "archivo": "app.py",
            "requisitos": [
                "La aplicación crea la tabla libros si no existe.",
                "POST /api/libros inserta una fila y responde 201 con el id.",
                "GET /api/libros lee las filas de la base y responde 200.",
                "Los datos quedan en el archivo biblioteca.db.",
                "La base se crea al iniciar la aplicación, sin pasos manuales.",
            ],
            "pista": "`sqlite3` viene incluido en Python. Crea la conexión, ejecuta el `CREATE TABLE IF NOT EXISTS` y usa `commit()` después de insertar.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "limpiar": ["biblioteca.db"],
                "casos": [
                    {
                        "descripcion": "La base inicia sin libros",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": []},
                    },
                    {
                        "descripcion": "El libro se inserta en SQLite",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Rayuela", "anio": 1963},
                    },
                    {
                        "descripcion": "El listado lee la base",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1, "titulo": "Rayuela"}]},
                    },
                ],
            },
            {
                "tipo": "python",
                "checks": [
                    {
                        "descripcion": "La fila existe en el archivo SQLite",
                        "codigo": "import sqlite3\ncon = sqlite3.connect('biblioteca.db')\nfilas = con.execute('SELECT titulo FROM libros').fetchall()\nassert filas, 'la tabla libros está vacía'\nassert filas[0][0] == 'Rayuela', filas",
                    }
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion21.md` con el esquema de la tabla.",
    },
    22: {
        "pregunta": "¿Cómo modelas relaciones sin escribir JOIN a mano?",
        "prerrequisitos": [
            "Sesión 21: SQLite y persistencia",
            "Saber qué es una llave primaria y una llave foránea",
        ],
        "objetivos": [
            "Definir modelos ORM con relaciones 1:N.",
            "Crear un libro asociado a un autor.",
            "Verificar la integridad referencial en la respuesta.",
        ],
        "conceptos": [
            {
                "termino": "ORM",
                "definicion": "Capa que traduce objetos de Python a filas de una base relacional.",
                "analogia": "Como un traductor simultáneo entre dos idiomas.",
            },
            {
                "termino": "Modelo",
                "definicion": "Clase que representa una tabla y sus columnas.",
                "analogia": "Como el plano de una tabla: define qué campos tendrá.",
            },
            {
                "termino": "Llave foránea",
                "definicion": "Columna que apunta a la llave primaria de otra tabla.",
                "analogia": "Como el número de expediente que conecta dos carpetas.",
            },
            {
                "termino": "Relación 1:N",
                "definicion": "Un autor tiene muchos libros; cada libro pertenece a un autor.",
                "analogia": "Como una persona con varias cuentas bancarias.",
            },
        ],
        "resultado": {
            "titulo": "Tu relación autor → libros se verá así",
            "lenguaje": "http",
            "codigo": """POST /api/autores  {"nombre":"Gabriel García Márquez"}
HTTP/1.1 201 Created
{"id":1,"nombre":"Gabriel García Márquez"}

POST /api/autores/1/libros  {"titulo":"Cien años de soledad","anio":1967}
HTTP/1.1 201 Created
{"id":1,"titulo":"Cien años de soledad","anio":1967,"autor_id":1}

GET /api/autores/1
HTTP/1.1 200 OK
{"id":1,"nombre":"Gabriel García Márquez",
 "libros":[{"id":1,"titulo":"Cien años de soledad"}]}""",
            "nota": "El ORM mantiene la relación: tú trabajas con objetos, él escribe el JOIN.",
        },
        "reto": {
            "enunciado": "Modela autores y libros con SQLAlchemy, una relación 1:N y endpoints que respeten la integridad referencial.",
            "archivo": "app.py",
            "requisitos": [
                "El modelo Autor tiene id y nombre.",
                "El modelo Libro tiene id, titulo, anio y una llave foránea autor_id.",
                "La relación Autor.libros está declarada con relationship.",
                "POST /api/autores y POST /api/autores/{id}/libros responden 201.",
                "GET /api/autores/{id} devuelve el autor con sus libros anidados.",
            ],
            "pista": "En SQLAlchemy, `ForeignKey('autores.id')` y `relationship('Libro', back_populates='autor')` describen la relación. La base se crea con `Base.metadata.create_all(engine)`.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "limpiar": ["biblioteca.db"],
                "casos": [
                    {
                        "descripcion": "Se crea el autor",
                        "metodo": "POST",
                        "ruta": "/api/autores",
                        "json": {"nombre": "Gabriel García Márquez"},
                        "estado": 201,
                        "json_contiene": {"id": 1, "nombre": "Gabriel García Márquez"},
                    },
                    {
                        "descripcion": "Se crea el libro asociado",
                        "metodo": "POST",
                        "ruta": "/api/autores/1/libros",
                        "json": {"titulo": "Cien años de soledad", "anio": 1967},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Cien años de soledad", "autor_id": 1},
                    },
                    {
                        "descripcion": "El autor devuelve sus libros",
                        "metodo": "GET",
                        "ruta": "/api/autores/1",
                        "estado": 200,
                        "json_contiene": {
                            "id": 1,
                            "nombre": "Gabriel García Márquez",
                            "libros": [{"id": 1, "titulo": "Cien años de soledad"}],
                        },
                    },
                    {
                        "descripcion": "El listado de libros funciona",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1, "titulo": "Cien años de soledad"}]},
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "app.py",
                        "regex": ["relationship\\(|ForeignKey\\("],
                        "descripcion": "La relación ORM está declarada",
                    },
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion22.md` con el diagrama entidad-relación.",
    },
    23: {
        "pregunta": "¿Por qué esperar a la base de datos no debe bloquear el servidor?",
        "prerrequisitos": [
            "Sesión 22: modelos ORM y relaciones",
            "Saber qué es async/await",
        ],
        "objetivos": [
            "Implementar un CRUD con SQLAlchemy asíncrono.",
            "Usar AsyncSession y aiosqlite.",
            "Verificar 201, 200, 404 y 204 en el mismo flujo.",
        ],
        "conceptos": [
            {
                "termino": "Asincronía",
                "definicion": "Capacidad de seguir atendiendo otras tareas mientras se espera una operación lenta.",
                "analogia": "Como un mesero que toma otro pedido mientras la cocina prepara el primero.",
            },
            {
                "termino": "AsyncSession",
                "definicion": "Sesión de SQLAlchemy que no bloquea el bucle de eventos.",
                "analogia": "Como una ventanilla que atiende varias filas a la vez.",
            },
            {
                "termino": "Event loop",
                "definicion": "Bucle que coordina las tareas asíncronas de la aplicación.",
                "analogia": "Como el director de una orquesta: indica cuándo entra cada instrumento.",
            },
            {
                "termino": "Commit y rollback",
                "definicion": "Confirmar o deshacer una transacción en la base de datos.",
                "analogia": "Como firmar un contrato o romperlo antes de que sea válido.",
            },
        ],
        "resultado": {
            "titulo": "Tu CRUD asíncrono se verá así",
            "lenguaje": "http",
            "codigo": """POST /api/libros  {"titulo":"Rayuela","anio":1963}  -> 201
GET  /api/libros                                  -> 200
GET  /api/libros/1                                -> 200
PUT  /api/libros/1  {"titulo":"Rayuela (edición)"} -> 200
DELETE /api/libros/1                              -> 204
GET  /api/libros/1                                -> 404""",
            "nota": "La base de datos sigue siendo SQLite; lo que cambia es cómo la aplicación espera sus respuestas.",
        },
        "reto": {
            "enunciado": "Implementa un CRUD completo con SQLAlchemy asíncrono y aiosqlite. El servidor no debe bloquearse mientras espera la base.",
            "archivo": "app.py",
            "requisitos": [
                "Usa create_async_engine con sqlite+aiosqlite.",
                "Cada endpoint usa AsyncSession y await.",
                "POST responde 201; GET 200; PUT 200; DELETE 204.",
                "Un id inexistente responde 404.",
                "La tabla se crea al iniciar la aplicación.",
            ],
            "pista": "Si tu endpoint es `def` y usas una sesión síncrona, estás bloqueando el event loop. La regla es: motor async, sesión async, endpoint async.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "limpiar": ["biblioteca.db"],
                "casos": [
                    {
                        "descripcion": "Crear un libro",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Rayuela"},
                    },
                    {
                        "descripcion": "Listar los libros",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1}]},
                    },
                    {
                        "descripcion": "Actualizar el libro",
                        "metodo": "PUT",
                        "ruta": "/api/libros/1",
                        "json": {"titulo": "Rayuela (edición crítica)", "anio": 1963},
                        "estado": 200,
                        "json_contiene": {"id": 1, "titulo": "Rayuela (edición crítica)"},
                    },
                    {
                        "descripcion": "Eliminar el libro",
                        "metodo": "DELETE",
                        "ruta": "/api/libros/1",
                        "estado": 204,
                    },
                    {
                        "descripcion": "El libro eliminado ya no existe",
                        "metodo": "GET",
                        "ruta": "/api/libros/1",
                        "estado": 404,
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "app.py",
                        "regex": ["AsyncSession|async_sessionmaker|aiosqlite"],
                        "descripcion": "La persistencia es asíncrona",
                    },
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion23.md` con la diferencia entre def y async def.",
    },
    24: {
        "pregunta": "¿Cómo cambias el esquema sin borrar los datos?",
        "prerrequisitos": [
            "Sesión 23: CRUD asíncrono",
            "Saber qué es una migración de base de datos",
        ],
        "objetivos": [
            "Escribir una migración versionada con upgrade y downgrade.",
            "Separar el modelo ORM de la migración.",
            "Verificar que la migración crea y elimina la tabla libros.",
        ],
        "conceptos": [
            {
                "termino": "Migración",
                "definicion": "Script versionado que transforma un esquema de base de datos de un estado a otro.",
                "analogia": "Como el historial de cambios de un documento, con fecha y autor.",
            },
            {
                "termino": "Upgrade / downgrade",
                "definicion": "Aplicar o revertir una migración.",
                "analogia": "Como subir o bajar una versión de una aplicación.",
            },
            {
                "termino": "Alembic",
                "definicion": "Herramienta de migraciones para SQLAlchemy.",
                "analogia": "Como el control de versiones, pero para el esquema de la base de datos.",
            },
            {
                "termino": "Revisión (revision)",
                "definicion": "Identificador único de una migración y su relación con la anterior.",
                "analogia": "Como el número de folio de cada cambio.",
            },
        ],
        "resultado": {
            "titulo": "Tu migración se verá así",
            "lenguaje": "text",
            "codigo": """$ alembic upgrade head
INFO  [alembic.runtime.migration] Running upgrade  -> 0001, crear tabla libros
$ sqlite3 biblioteca.db ".schema libros"
CREATE TABLE libros (
  id INTEGER NOT NULL PRIMARY KEY,
  titulo VARCHAR(80) NOT NULL,
  anio INTEGER NOT NULL
);

$ alembic downgrade base
$ sqlite3 biblioteca.db ".tables"
(la tabla libros ya no existe)""",
            "nota": "Una migración no es un `create_all`: es un cambio versionado que se puede aplicar y revertir.",
        },
        "reto": {
            "enunciado": "Crea la migración que lleva una base vacía al esquema de libros y que puede revertirse sin dejar residuos.",
            "archivo": "modelos.py",
            "requisitos": [
                "modelos.py define Base y el modelo Libro con id, titulo y anio.",
                "La migración 0001 crea la tabla libros con op.create_table.",
                "down_revision es None y downgrade elimina la tabla con op.drop_table.",
                "alembic.ini apunta a la base SQLite y a la carpeta migrations.",
                "Env.py usa target_metadata de modelos.Base.",
            ],
            "pista": "La migración describe el cambio, no el estado final. `upgrade` construye; `downgrade` deshace exactamente lo construido.",
            "preparacion": "!mkdir -p migrations/versions\nprint('Carpetas de Alembic listas')\n",
            "archivos": [
                {
                    "ruta": "modelos.py",
                    "esqueleto": "%%writefile modelos.py\nfrom sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column\n\nclass Base(DeclarativeBase):\n    pass\n\n# Define aquí el modelo Libro.\n",
                    "descripcion": "Modelo ORM que describe la tabla.",
                },
                {
                    "ruta": "alembic.ini",
                    "esqueleto": "%%writefile alembic.ini\n[alembic]\nscript_location = migrations\nsqlalchemy.url = sqlite:///biblioteca.db\n",
                    "descripcion": "Configuración de Alembic.",
                },
                {
                    "ruta": "migrations/env.py",
                    "esqueleto": "%%writefile migrations/env.py\nfrom logging.config import fileConfig\nfrom alembic import context\nfrom sqlalchemy import engine_from_config, pool\nfrom modelos import Base\n\nconfig = context.config\ntarget_metadata = Base.metadata\n\n# Completa la configuración de conexión y ejecución.\n",
                    "descripcion": "Puente entre Alembic y los modelos.",
                },
                {
                    "ruta": "migrations/versions/0001_crear_libros.py",
                    "esqueleto": "%%writefile migrations/versions/0001_crear_libros.py\nfrom alembic import op\nimport sqlalchemy as sa\n\nrevision = \"0001\"\ndown_revision = None\nbranch_labels = None\ndepends_on = None\n\ndef upgrade():\n    # Crea la tabla libros.\n    pass\n\ndef downgrade():\n    # Revierte exactamente lo que hiciste.\n    pass\n",
                    "descripcion": "Migración versionada.",
                },
            ],
        },
        "verificacion": [
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "modelos.py",
                        "exigir": ["class Libro", "Base"],
                        "descripcion": "El modelo Libro existe",
                    },
                    {
                        "ruta": "alembic.ini",
                        "exigir": ["script_location", "sqlalchemy.url"],
                        "descripcion": "Alembic está configurado",
                    },
                    {
                        "ruta": "migrations/env.py",
                        "exigir": ["target_metadata"],
                        "descripcion": "Env.py conoce los metadatos",
                    },
                ],
            },
            {
                "tipo": "python",
                "checks": [
                    {
                        "descripcion": "La migración crea y revierte la tabla libros",
                        "codigo": """import importlib.util
from pathlib import Path

ruta = Path("migrations/versions/0001_crear_libros.py")
assert ruta.exists(), "no existe la migración 0001"
spec = importlib.util.spec_from_file_location("migracion", ruta)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Op:
    def __init__(self):
        self.llamadas = []
    def create_table(self, nombre, *args, **kwargs):
        self.llamadas.append(("create", nombre))
    def drop_table(self, nombre, *args, **kwargs):
        self.llamadas.append(("drop", nombre))

op = Op()
mod.op = op
mod.upgrade()
assert ("create", "libros") in op.llamadas, op.llamadas
mod.downgrade()
assert ("drop", "libros") in op.llamadas, op.llamadas
""",
                    }
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion24.md` con la salida de upgrade y downgrade.",
    },
    25: {
        "pregunta": "¿Por qué una lista de 100 autores dispara 101 consultas?",
        "prerrequisitos": [
            "Sesión 24: migraciones",
            "Saber qué es un JOIN",
        ],
        "objetivos": [
            "Cargar relaciones con selectinload.",
            "Evitar el problema N+1.",
            "Verificar que la respuesta anida los libros del autor.",
        ],
        "conceptos": [
            {
                "termino": "JOIN",
                "definicion": "Operación que combina filas de dos tablas relacionadas.",
                "analogia": "Como cruzar dos listas por un campo común.",
            },
            {
                "termino": "Problema N+1",
                "definicion": "Una consulta para la lista y una consulta extra por cada elemento.",
                "analogia": "Como ir al almacén una vez por cada ingrediente en vez de una sola vez.",
            },
            {
                "termino": "Carga ansiosa (eager loading)",
                "definicion": "Traer las relaciones en la misma consulta o en una consulta adicional controlada.",
                "analogia": "Como pedir el paquete completo en una sola entrega.",
            },
            {
                "termino": "selectinload",
                "definicion": "Estrategia de SQLAlchemy que carga la relación con una consulta eficiente.",
                "analogia": "Como un camión que recoge todos los paquetes de una ruta.",
            },
        ],
        "resultado": {
            "titulo": "Tu consulta ansiosa se verá así",
            "lenguaje": "http",
            "codigo": """GET /api/autores
HTTP/1.1 200 OK
{"autores":[
  {"id":1,"nombre":"Gabriel García Márquez",
   "libros":[{"id":1,"titulo":"Cien años de soledad"}]},
  {"id":2,"nombre":"Julio Cortázar",
   "libros":[{"id":2,"titulo":"Rayuela"}]}
]}

GET /api/autores/1
HTTP/1.1 200 OK
{"id":1,"nombre":"Gabriel García Márquez",
 "libros":[{"id":1,"titulo":"Cien años de soledad"}]}""",
            "nota": "El resultado es el mismo; la diferencia es cuántas consultas hiciste para lograrlo.",
        },
        "reto": {
            "enunciado": "Implementa una consulta de autores con sus libros usando carga ansiosa para evitar el problema N+1.",
            "archivo": "app.py",
            "requisitos": [
                "Siembra exactamente: Gabriel García Márquez → «Cien años de soledad»; Julio Cortázar → «Rayuela».",
                "GET /api/autores devuelve todos los autores con sus libros anidados.",
                "GET /api/autores/{id} devuelve un autor con sus libros.",
                "La consulta usa selectinload o joinedload.",
                "La respuesta no incluye autores sin sus libros cuando existen.",
                "El listado de libros sigue disponible en /api/libros.",
            ],
            "pista": "Sin carga ansiosa, cada autor dispara una consulta para sus libros. `selectinload(Autor.libros)` resuelve la relación en una sola consulta adicional.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "limpiar": ["biblioteca.db"],
                "casos": [
                    {
                        "descripcion": "Los autores llegan con sus libros",
                        "metodo": "GET",
                        "ruta": "/api/autores",
                        "estado": 200,
                        "json_contiene": {
                            "autores": [
                                {
                                    "id": 1,
                                    "nombre": "Gabriel García Márquez",
                                    "libros": [{"id": 1, "titulo": "Cien años de soledad"}],
                                },
                                {
                                    "id": 2,
                                    "nombre": "Julio Cortázar",
                                    "libros": [{"id": 2, "titulo": "Rayuela"}],
                                },
                            ]
                        },
                    },
                    {
                        "descripcion": "Un autor concreto trae sus libros",
                        "metodo": "GET",
                        "ruta": "/api/autores/1",
                        "estado": 200,
                        "json_contiene": {
                            "id": 1,
                            "libros": [{"id": 1, "titulo": "Cien años de soledad"}],
                        },
                    },
                    {
                        "descripcion": "El listado de libros sigue disponible",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1}, {"id": 2}]},
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "app.py",
                        "regex": ["selectinload|joinedload"],
                        "descripcion": "Se usa carga ansiosa",
                    },
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion25.md` explicando el problema N+1.",
    },
    26: {
        "pregunta": "¿Qué pasa si falla la segunda mitad de una operación?",
        "prerrequisitos": [
            "Sesión 25: joins y carga ansiosa",
            "Saber qué es una transacción",
        ],
        "objetivos": [
            "Agrupar varias escrituras en una transacción.",
            "Hacer rollback cuando una condición de negocio falla.",
            "Verificar que el stock no queda inconsistente.",
        ],
        "conceptos": [
            {
                "termino": "Transacción",
                "definicion": "Conjunto de operaciones que se confirman o se deshacen como una sola unidad.",
                "analogia": "Como una transferencia bancaria: salen y entran en el mismo movimiento.",
            },
            {
                "termino": "Atomicidad",
                "definicion": "Todo o nada: si una parte falla, no queda ninguna parte aplicada.",
                "analogia": "Como una cirugía: no se puede completar a medias.",
            },
            {
                "termino": "Rollback",
                "definicion": "Deshacer los cambios de una transacción no confirmada.",
                "analogia": "Como deshacer un movimiento antes de firmarlo.",
            },
            {
                "termino": "Consistencia",
                "definicion": "Los datos cumplen las reglas del negocio antes y después de la operación.",
                "analogia": "Como un inventario que cuadra después de cada venta.",
            },
        ],
        "resultado": {
            "titulo": "Tu préstamo transaccional se verá así",
            "lenguaje": "http",
            "codigo": """GET /api/libros/1                 -> 200 {"ejemplares":1}
POST /api/prestamos {"libro_id":1,"usuario":"ana"}
                                   -> 201 {"prestamo_id":1,"quedan":0}
GET /api/libros/1                 -> 200 {"ejemplares":0}
POST /api/prestamos {"libro_id":1,"usuario":"luis"}
                                   -> 409 {"error":"sin ejemplares"}
GET /api/libros/1                 -> 200 {"ejemplares":0}  # no bajó a -1""",
            "nota": "Si el segundo préstamo descontara antes de validar, el stock quedaría en -1. La transacción lo impide.",
        },
        "reto": {
            "enunciado": "Implementa un préstamo de libros que descuente stock y registre el préstamo en una sola transacción.",
            "archivo": "app.py",
            "requisitos": [
                "La base inicia con el libro 1, «Rayuela», con un ejemplar disponible.",
                "POST /api/prestamos descuenta un ejemplar y registra el préstamo.",
                "Si no hay ejemplares, responde 409 y no modifica el stock.",
                "GET /api/libros/{id} muestra los ejemplares restantes.",
                "No puede quedar stock negativo ni un préstamo sin descuento.",
            ],
            "pista": "Valida y escribe dentro de la misma transacción. Si haces `commit` antes de comprobar la condición, ya no puedes deshacer el descuento.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "limpiar": ["biblioteca.db"],
                "casos": [
                    {
                        "descripcion": "El libro inicia con un ejemplar",
                        "metodo": "GET",
                        "ruta": "/api/libros/1",
                        "estado": 200,
                        "json_contiene": {"id": 1, "ejemplares": 1},
                    },
                    {
                        "descripcion": "El primer préstamo se completa",
                        "metodo": "POST",
                        "ruta": "/api/prestamos",
                        "json": {"libro_id": 1, "usuario": "ana"},
                        "estado": 201,
                        "json_contiene": {"libro_id": 1, "quedan": 0},
                    },
                    {
                        "descripcion": "El stock quedó en cero",
                        "metodo": "GET",
                        "ruta": "/api/libros/1",
                        "estado": 200,
                        "json_contiene": {"ejemplares": 0},
                    },
                    {
                        "descripcion": "El segundo préstamo falla con 409",
                        "metodo": "POST",
                        "ruta": "/api/prestamos",
                        "json": {"libro_id": 1, "usuario": "luis"},
                        "estado": 409,
                    },
                    {
                        "descripcion": "El stock no quedó negativo",
                        "metodo": "GET",
                        "ruta": "/api/libros/1",
                        "estado": 200,
                        "json_contiene": {"ejemplares": 0},
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "app.py",
                        "regex": ["commit|rollback"],
                        "descripcion": "La operación usa una transacción",
                    },
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion26.md` con el caso de rollback.",
    },
    27: {
        "pregunta": "¿Qué puede hacer un apóstrofo en tu consulta?",
        "prerrequisitos": [
            "Sesión 26: transacciones ACID",
            "Saber qué es una consulta SQL",
        ],
        "objetivos": [
            "Reconocer una consulta vulnerable a SQL Injection.",
            "Escribir consultas parametrizadas.",
            "Verificar que un payload malicioso no devuelve datos ajenos.",
        ],
        "conceptos": [
            {
                "termino": "Inyección SQL",
                "definicion": "Insertar SQL dentro de un dato para alterar la consulta original.",
                "analogia": "Como colar una instrucción extra en un formulario de pedido.",
            },
            {
                "termino": "Concatenación",
                "definicion": "Unir texto de la consulta con datos del usuario; es la puerta de entrada del ataque.",
                "analogia": "Como mezclar la firma de un cheque con el monto escrito por otra persona.",
            },
            {
                "termino": "Consulta parametrizada",
                "definicion": "Consultar con marcadores y pasar los valores por separado.",
                "analogia": "Como un formulario con casillas: el dato no cambia la estructura.",
            },
            {
                "termino": "Menor privilegio",
                "definicion": "La cuenta de la base solo puede hacer lo estrictamente necesario.",
                "analogia": "Como dar una llave que abre una puerta, no todo el edificio.",
            },
        ],
        "resultado": {
            "titulo": "Tu búsqueda segura se verá así",
            "lenguaje": "http",
            "codigo": """GET /api/libros/buscar?titulo=Cien
HTTP/1.1 200 OK
{"libros":[{"id":1,"titulo":"Cien años de soledad"}]}

GET /api/libros/buscar?titulo=%27%20OR%20%271%27%3D%271
HTTP/1.1 200 OK
{"libros":[]}          # no devuelve toda la tabla

GET /api/libros/1
HTTP/1.1 200 OK
{"id":1,"titulo":"Cien años de soledad"}""",
            "nota": "El payload se trata como texto, no como instrucción. La consulta mantiene su forma.",
        },
        "reto": {
            "enunciado": "Implementa una búsqueda de libros a prueba de SQL Injection y demuéstralo con el payload clásico.",
            "archivo": "app.py",
            "requisitos": [
                "Siembra «Cien años de soledad» (id 1) y «Rayuela» (id 2) como datos de prueba.",
                "GET /api/libros/buscar?titulo=... busca por coincidencia.",
                "La consulta usa parámetros, nunca concatenación de cadenas.",
                "El payload ' OR '1'='1 no devuelve toda la tabla.",
                "GET /api/libros/{id} sigue funcionando.",
            ],
            "pista": "En SQLite: `cursor.execute(\"SELECT ... WHERE titulo LIKE ?\", (f\"%{texto}%\",))`. El marcador `?` separa la estructura de los datos.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "limpiar": ["biblioteca.db"],
                "casos": [
                    {
                        "descripcion": "Una búsqueda normal encuentra un libro",
                        "metodo": "GET",
                        "ruta": "/api/libros/buscar?titulo=Cien",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1, "titulo": "Cien años de soledad"}]},
                    },
                    {
                        "descripcion": "El payload de inyección no devuelve toda la tabla",
                        "metodo": "GET",
                        "ruta": "/api/libros/buscar?titulo=%27%20OR%20%271%27%3D%271",
                        "estado": 200,
                        "json_contiene": {"libros": []},
                    },
                    {
                        "descripcion": "El acceso por id sigue funcionando",
                        "metodo": "GET",
                        "ruta": "/api/libros/1",
                        "estado": 200,
                        "json_contiene": {"id": 1, "titulo": "Cien años de soledad"},
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "app.py",
                        "regex": ["\\?|:titulo|text\\(|like\\(|where\\(|select\\("],
                        "descripcion": "La consulta usa parámetros",
                    },
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion27.md` comparando la consulta vulnerable y la segura.",
    },
    28: {
        "pregunta": "¿Por qué el navegador bloquea tu API aunque funcione en curl?",
        "prerrequisitos": [
            "Sesión 27: SQL Injection y consultas seguras",
            "Saber qué es un origen (protocolo + dominio + puerto)",
        ],
        "objetivos": [
            "Configurar CORS con una lista blanca de orígenes.",
            "Responder correctamente al preflight OPTIONS.",
            "Verificar que un origen no autorizado no recibe permiso.",
        ],
        "conceptos": [
            {
                "termino": "Origen",
                "definicion": "Combinación de protocolo, dominio y puerto.",
                "analogia": "Como la dirección completa de una casa: calle, número y colonia.",
            },
            {
                "termino": "Política de mismo origen",
                "definicion": "Regla del navegador que impide leer respuestas de otro origen sin permiso.",
                "analogia": "Como no poder abrir la puerta de otra casa aunque esté en la misma calle.",
            },
            {
                "termino": "CORS",
                "definicion": "Mecanismo de encabezados con el que el servidor autoriza otros orígenes.",
                "analogia": "Como una lista de invitados en la entrada.",
            },
            {
                "termino": "Preflight",
                "definicion": "Petición OPTIONS previa que pregunta si la operación está permitida.",
                "analogia": "Como llamar antes de llegar para confirmar que te esperan.",
            },
        ],
        "resultado": {
            "titulo": "Tu CORS se verá así",
            "lenguaje": "http",
            "codigo": """GET /api/libros
Origin: https://app.ejemplo.com
HTTP/1.1 200 OK
access-control-allow-origin: https://app.ejemplo.com
{"libros":[]}

OPTIONS /api/libros
Origin: https://app.ejemplo.com
Access-Control-Request-Method: POST
HTTP/1.1 200 OK
access-control-allow-methods: GET, POST, OPTIONS
access-control-allow-headers: Content-Type, Authorization

GET /api/libros   Origin: https://sitio-malicioso.com
HTTP/1.1 200 OK
(sin access-control-allow-origin)""",
            "nota": "El navegador decide si muestra la respuesta; el servidor solo declara a quién autoriza.",
        },
        "reto": {
            "enunciado": "Configura CORS con una lista blanca, métodos y encabezados permitidos, y demuestra que un origen no autorizado no recibe permiso.",
            "archivo": "app.py",
            "requisitos": [
                "El origen https://app.ejemplo.com está autorizado.",
                "Se permiten GET, POST y OPTIONS.",
                "Se permiten los encabezados Content-Type y Authorization.",
                "El preflight OPTIONS responde 200 con los encabezados CORS.",
                "Un origen no autorizado no recibe access-control-allow-origin.",
            ],
            "pista": "`CORSMiddleware` con `allow_origins=[...]` es una lista blanca. Un `*` en producción equivale a invitar a cualquiera.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "El origen autorizado recibe permiso",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "headers": {"Origin": "https://app.ejemplo.com"},
                        "estado": 200,
                        "headers_contiene": {"access-control-allow-origin": "https://app.ejemplo.com"},
                        "headers_no_contiene": {"access-control-allow-origin": "*"},
                    },
                    {
                        "descripcion": "El preflight autoriza el método",
                        "metodo": "OPTIONS",
                        "ruta": "/api/libros",
                        "headers": {
                            "Origin": "https://app.ejemplo.com",
                            "Access-Control-Request-Method": "POST",
                        },
                        "estado": 200,
                        "headers_contiene": {"access-control-allow-methods": "post"},
                    },
                    {
                        "descripcion": "Un origen desconocido no recibe permiso",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "headers": {"Origin": "https://sitio-malicioso.com"},
                        "estado": 200,
                        "headers_no_contiene": {"access-control-allow-origin": "sitio-malicioso"},
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "app.py",
                        "exigir": ["CORSMiddleware"],
                        "descripcion": "Se usa el middleware CORS",
                    },
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion28.md` con la lista blanca de orígenes.",
    },
    29: {
        "pregunta": "¿Por qué una cookie sola no basta para proteger una acción?",
        "prerrequisitos": [
            "Sesión 28: CORS",
            "Saber qué es una petición entre sitios",
        ],
        "objetivos": [
            "Configurar cookies HttpOnly y SameSite.",
            "Implementar un token anti-CSRF.",
            "Verificar que una acción sensible falla sin el token.",
        ],
        "conceptos": [
            {
                "termino": "CSRF",
                "definicion": "Ataque que aprovecha la cookie del usuario para enviar una acción no deseada.",
                "analogia": "Como usar la firma de alguien en un documento que no leyó.",
            },
            {
                "termino": "SameSite",
                "definicion": "Atributo que limita el envío de la cookie en peticiones entre sitios.",
                "analogia": "Como un pase que solo sirve dentro del edificio.",
            },
            {
                "termino": "HttpOnly",
                "definicion": "Atributo que impide que JavaScript lea la cookie.",
                "analogia": "Como una caja fuerte que solo abre el servidor.",
            },
            {
                "termino": "Token anti-CSRF",
                "definicion": "Valor impredecible que el cliente debe enviar además de la cookie.",
                "analogia": "Como un código de confirmación para una operación sensible.",
            },
        ],
        "resultado": {
            "titulo": "Tu protección CSRF se verá así",
            "lenguaje": "http",
            "codigo": """POST /api/login
HTTP/1.1 200 OK
Set-Cookie: session=...; HttpOnly; SameSite=Lax

GET /api/csrf
HTTP/1.1 200 OK
{"csrf_token":"a1b2c3..."}

POST /api/logout   (sin X-CSRF-Token)
HTTP/1.1 403 Forbidden

POST /api/logout   X-CSRF-Token: a1b2c3...
HTTP/1.1 204 No Content""",
            "nota": "La cookie demuestra quién eres; el token demuestra que la acción la pediste tú.",
        },
        "reto": {
            "enunciado": "Implementa una acción sensible protegida por cookie y token anti-CSRF.",
            "archivo": "app.py",
            "requisitos": [
                "El usuario de prueba es ana con contraseña secreta.",
                "POST /api/login emite una cookie HttpOnly y SameSite=Lax.",
                "GET /api/csrf devuelve un token para la sesión actual.",
                "POST /api/logout exige el token en X-CSRF-Token.",
                "Sin token o con token incorrecto responde 403.",
                "Con el token correcto responde 204.",
            ],
            "pista": "El token no se guarda en una cookie legible por JavaScript; se entrega en el cuerpo y el cliente lo reenvía en un encabezado. Así un sitio externo no puede leerlo.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "El login emite una cookie HttpOnly y SameSite",
                        "metodo": "POST",
                        "ruta": "/api/login",
                        "json": {"usuario": "ana", "password": "secreta"},
                        "estado": 200,
                        "headers_contiene": {"set-cookie": ["httponly", "samesite"]},
                    },
                    {
                        "descripcion": "El logout sin token se rechaza",
                        "metodo": "POST",
                        "ruta": "/api/logout",
                        "estado": 403,
                    },
                    {
                        "descripcion": "El token CSRF se obtiene",
                        "metodo": "GET",
                        "ruta": "/api/csrf",
                        "estado": 200,
                        "guardar": {"csrf": "csrf_token"},
                    },
                    {
                        "descripcion": "El logout con token funciona",
                        "metodo": "POST",
                        "ruta": "/api/logout",
                        "headers": {"X-CSRF-Token": "{csrf}"},
                        "estado": 204,
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion29.md` con la diferencia entre autenticación y CSRF.",
    },
    30: {
        "pregunta": "¿Tu API ya soporta datos reales sin sacrificar seguridad?",
        "prerrequisitos": [
            "Sesiones 21 a 29: persistencia, ORM, transacciones, SQLi, CORS y CSRF",
            "Tu API del Hito 2 como base",
        ],
        "objetivos": [
            "Integrar persistencia, búsqueda segura y CORS.",
            "Verificar el contrato completo del Hito 3.",
            "Demostrar que la API resiste un payload de inyección.",
        ],
        "conceptos": [
            {
                "termino": "Persistencia",
                "definicion": "Los datos sobreviven al reinicio del proceso.",
                "analogia": "Como un cuaderno, no una pizarra.",
            },
            {
                "termino": "Blindaje OWASP",
                "definicion": "Conjunto de controles contra las vulnerabilidades más comunes.",
                "analogia": "Como las cerraduras y alarmas de una casa.",
            },
            {
                "termino": "Integración",
                "definicion": "Hacer que piezas desarrolladas por separado funcionen como un sistema.",
                "analogia": "Como ensamblar un motor: cada pieza funciona, pero el conjunto es lo que se prueba.",
            },
            {
                "termino": "Hito",
                "definicion": "Entrega evaluable que demuestra un bloque completo.",
                "analogia": "Como un examen integrador.",
            },
        ],
        "resultado": {
            "titulo": "Tu Hito 3 completo se verá así",
            "lenguaje": "http",
            "codigo": """POST /api/libros              -> 201
GET  /api/libros              -> 200
GET  /api/libros/buscar?titulo=' OR '1'='1 -> 200 {"libros":[]}
OPTIONS /api/libros (origen permitido)      -> 200 + CORS
GET  /health                  -> 200 {"status":"ok"}

RESUMEN: 5/5 casos correctos. ¡Hito 3 listo!""",
            "nota": "La base de datos y la seguridad no son módulos opcionales: son parte del contrato del hito.",
        },
        "reto": {
            "enunciado": "Integra una API persistente de libros con búsqueda segura, CORS y healthcheck para cerrar el Hito 3.",
            "archivo": "app.py",
            "requisitos": [
                "Los libros se guardan en SQLite y sobreviven al reinicio.",
                "La búsqueda usa consultas parametrizadas.",
                "CORS permite https://app.ejemplo.com.",
                "GET /health responde 200 con status ok.",
                "Los cinco casos del hito deben quedar en verde.",
            ],
            "pista": "No agregues una capa nueva sin volver a ejecutar los casos anteriores. Un hito se prueba completo, no por partes.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "limpiar": ["biblioteca.db"],
                "casos": [
                    {
                        "descripcion": "Crear un libro persistente",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Rayuela"},
                    },
                    {
                        "descripcion": "Listar los libros persistidos",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1, "titulo": "Rayuela"}]},
                    },
                    {
                        "descripcion": "La búsqueda resiste inyección",
                        "metodo": "GET",
                        "ruta": "/api/libros/buscar?titulo=%27%20OR%20%271%27%3D%271",
                        "estado": 200,
                        "json_contiene": {"libros": []},
                    },
                    {
                        "descripcion": "CORS autoriza el origen permitido",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "headers": {"Origin": "https://app.ejemplo.com"},
                        "estado": 200,
                        "headers_contiene": {"access-control-allow-origin": "https://app.ejemplo.com"},
                    },
                    {
                        "descripcion": "El healthcheck responde",
                        "metodo": "GET",
                        "ruta": "/health",
                        "estado": 200,
                        "json_contiene": {"status": "ok"},
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {"ruta": "app.py", "regex": ["sqlite3|SQLAlchemy|create_engine"], "descripcion": "Hay persistencia real"},
                    {"ruta": "app.py", "exigir": ["CORSMiddleware"], "descripcion": "CORS está configurado"},
                ],
            },
        ],
        "entrega": "Cuaderno en verde, bitácora `auditorias/auditoria_sesion30.md` y tag `v0.3-hito3` en tu repositorio.",
    },
}
