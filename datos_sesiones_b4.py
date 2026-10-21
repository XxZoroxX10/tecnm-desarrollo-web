"""
Contenido enriquecido del Bloque 4 (sesiones 31 a 40).
Despliegue, frontend SPA, pruebas E2E e hito final.
"""

BLOQUE_4 = {
    31: {
        "pregunta": "¿Cómo empaquetas tu API para que corra igual en cualquier lado?",
        "prerrequisitos": [
            "Sesión 30: API persistente del Hito 3",
            "Saber qué es una imagen y un contenedor",
        ],
        "objetivos": [
            "Escribir un Dockerfile reproducible.",
            "Separar dependencias del código para aprovechar la caché.",
            "Verificar que la imagen no corre como root ni filtra secretos.",
        ],
        "conceptos": [
            {
                "termino": "Imagen",
                "definicion": "Plantilla inmutable con el sistema base, dependencias y código de la aplicación.",
                "analogia": "Como el molde de un pastel: de ahí salen copias idénticas.",
            },
            {
                "termino": "Contenedor",
                "definicion": "Instancia en ejecución de una imagen.",
                "analogia": "Como el pastel ya horneado a partir del molde.",
            },
            {
                "termino": "Capa",
                "definicion": "Cada instrucción del Dockerfile genera una capa reutilizable.",
                "analogia": "Como las capas de una cebolla: si no cambia la de abajo, se reutiliza.",
            },
            {
                "termino": "Multi-stage build",
                "definicion": "Usar una etapa para compilar y otra más ligera para ejecutar.",
                "analogia": "Como construir un mueble en el taller y llevarlo armado a casa.",
            },
        ],
        "resultado": {
            "titulo": "Tu imagen se construirá y ejecutará así",
            "lenguaje": "text",
            "codigo": """$ docker build -t biblioteca-api .
[+] Building 12.4s (9/9) FINISHED
 => [1/5] FROM python:3.11-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . .

$ docker run --rm -p 8000:8000 biblioteca-api
$ curl http://127.0.0.1:8000/api/libros
HTTP/1.1 200 OK
{"libros":[]}

$ docker image inspect biblioteca-api --format '{{.Config.User}}'
appuser""",
            "nota": "La imagen no debe contener el archivo .env ni ejecutarse como root.",
        },
        "reto": {
            "enunciado": "Escribe el Dockerfile y el .dockerignore de la API de libros para que la imagen sea pequeña, reproducible y segura.",
            "archivo": "Dockerfile",
            "requisitos": [
                "La imagen parte de una versión fija de Python slim.",
                "Las dependencias se copian e instalan antes de copiar el código.",
                "El contenedor se ejecuta con un usuario sin privilegios.",
                "El comando de arranque usa uvicorn y expone el puerto 8000.",
                ".dockerignore excluye .git, __pycache__ y .env.",
                "El Dockerfile no copia el archivo .env ni define secretos.",
            ],
            "pista": "El orden importa: `COPY requirements.txt` antes de `COPY . .` permite que Docker reutilice la capa de dependencias cuando solo cambia el código.",
            "archivos": [
                {
                    "ruta": "requirements.txt",
                    "esqueleto": "%%writefile requirements.txt\nfastapi\nuvicorn[standard]\n",
                    "descripcion": "Dependencias de la aplicación.",
                },
                {
                    "ruta": "Dockerfile",
                    "esqueleto": "%%writefile Dockerfile\n# Define la imagen base, el usuario, las dependencias y el comando de arranque.\n",
                    "descripcion": "Receta de la imagen.",
                },
                {
                    "ruta": ".dockerignore",
                    "esqueleto": "%%writefile .dockerignore\n# Excluye lo que no debe entrar a la imagen.\n",
                    "descripcion": "Archivos excluidos del contexto de construcción.",
                },
            ],
        },
        "verificacion": [
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "Dockerfile",
                        "regex": ["FROM\\s+python:3\\.1[12]-slim", "WORKDIR\\s+/app", "COPY\\s+requirements\\.txt", "RUN\\s+pip\\s+install", "COPY\\s+\\.\\s+\\."],
                        "prohibir": ["COPY .env", "USER root", "ENV SECRET"],
                        "descripcion": "Dockerfile reproducible y sin secretos",
                    },
                    {
                        "ruta": "Dockerfile",
                        "regex": ["USER\\s+appuser", "adduser|useradd", "CMD.*uvicorn|ENTRYPOINT.*uvicorn"],
                        "descripcion": "Usuario sin privilegios y arranque con uvicorn",
                    },
                    {
                        "ruta": ".dockerignore",
                        "exigir": [".git", "__pycache__", ".env"],
                        "descripcion": "Contexto de construcción limpio",
                    },
                    {
                        "ruta": "requirements.txt",
                        "regex": ["fastapi", "uvicorn"],
                        "descripcion": "Dependencias declaradas",
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion31.md` con el tamaño de la imagen y el usuario de ejecución.",
    },
    32: {
        "pregunta": "¿Dónde guardas la contraseña de la base de datos?",
        "prerrequisitos": [
            "Sesión 31: Dockerfile",
            "Saber qué es una variable de entorno",
        ],
        "objetivos": [
            "Leer configuración desde variables de entorno.",
            "Fallar rápido si falta un secreto crítico.",
            "Verificar que los secretos nunca se exponen en la respuesta.",
        ],
        "conceptos": [
            {
                "termino": "Variable de entorno",
                "definicion": "Valor que el sistema operativo entrega al proceso al iniciar.",
                "analogia": "Como la configuración del tablero de un coche antes de arrancar.",
            },
            {
                "termino": "Secreto",
                "definicion": "Credencial que no debe estar en el repositorio ni en la imagen.",
                "analogia": "Como la llave de la caja fuerte: no se pega en la puerta.",
            },
            {
                "termino": "12-Factor App",
                "definicion": "Metodología que separa la configuración del código.",
                "analogia": "Como el mismo aparato que funciona con distinto voltaje según el país.",
            },
            {
                "termino": "Fail-fast",
                "definicion": "Detener el arranque si falta una configuración crítica.",
                "analogia": "Como no encender un avión si falta el combustible.",
            },
        ],
        "resultado": {
            "titulo": "Tu configuración se verá así",
            "lenguaje": "text",
            "codigo": """$ DATABASE_URL=sqlite:///biblioteca.db SECRET_KEY=clave uvicorn app:app
GET /api/config
HTTP/1.1 200 OK
{"entorno":"dev","debug":false}

$ uvicorn app:app   (sin SECRET_KEY)
RuntimeError: Falta la variable SECRET_KEY
[el servidor no arranca]

La respuesta de /api/config NUNCA incluye SECRET_KEY.""",
            "nota": "Si el servidor arranca sin secreto, el error aparecerá en producción en el peor momento.",
        },
        "reto": {
            "enunciado": "Implementa una configuración centralizada que lea variables de entorno, valide las obligatorias y no exponga secretos.",
            "archivo": "config.py",
            "requisitos": [
                "config.py lee DATABASE_URL y SECRET_KEY como obligatorias.",
                "ENTORNO tiene valor por defecto dev y DEBUG por defecto false.",
                "Si falta una obligatoria, el arranque falla con un error claro.",
                "GET /api/config devuelve solo configuración no sensible.",
                ".env.example documenta las variables y .gitignore excluye .env.",
            ],
            "pista": "La configuración se lee una vez al arrancar. Si el código de negocio llama `os.getenv` por todas partes, no hay un único contrato de configuración.",
            "archivos": [
                {
                    "ruta": "config.py",
                    "esqueleto": "%%writefile config.py\nimport os\n\ndef cargar_config():\n    # Lee, valida y devuelve la configuración.\n    pass\n",
                    "descripcion": "Módulo de configuración.",
                },
                {
                    "ruta": ".env.example",
                    "esqueleto": "%%writefile .env.example\n# Documenta las variables necesarias, sin valores reales.\n",
                    "descripcion": "Plantilla de variables.",
                },
                {
                    "ruta": ".gitignore",
                    "esqueleto": "%%writefile .gitignore\n.env\n",
                    "descripcion": "Evita subir secretos.",
                },
                {
                    "ruta": "app.py",
                    "esqueleto": "%%writefile app.py\nfrom fastapi import FastAPI\nfrom config import cargar_config\n\napp = FastAPI(title=\"Configuración segura\")\n\n# Expón GET /api/config sin secretos.\n",
                    "descripcion": "API que usa la configuración.",
                },
            ],
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "env": {
                    "DATABASE_URL": "sqlite:///biblioteca.db",
                    "SECRET_KEY": "clave-de-prueba",
                    "ENTORNO": "dev",
                },
                "casos": [
                    {
                        "descripcion": "La configuración no secreta se expone",
                        "metodo": "GET",
                        "ruta": "/api/config",
                        "estado": 200,
                        "json_contiene": {"entorno": "dev", "debug": False},
                        "no_contiene": ["SECRET_KEY", "clave-de-prueba"],
                    }
                ],
            },
            {
                "tipo": "python",
                "checks": [
                    {
                        "descripcion": "La configuración obligatoria falla rápido",
                        "codigo": """import importlib, os, sys
for clave in ("DATABASE_URL", "SECRET_KEY"):
    os.environ.pop(clave, None)
os.environ["ENTORNO"] = "dev"
sys.modules.pop("config", None)
config = importlib.import_module("config")
try:
    config.cargar_config()
except RuntimeError:
    pass
else:
    raise AssertionError("cargar_config() debería fallar si faltan variables obligatorias")
""",
                    }
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {"ruta": ".env.example", "regex": ["DATABASE_URL", "SECRET_KEY"], "descripcion": "Variables documentadas"},
                    {"ruta": ".gitignore", "exigir": [".env"], "descripcion": ".env fuera del repositorio"},
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion32.md` con la lista de variables y su origen.",
    },
    33: {
        "pregunta": "¿Quién atiende a miles de usuarios a la vez?",
        "prerrequisitos": [
            "Sesión 32: variables de entorno",
            "Saber qué es un proxy inverso",
        ],
        "objetivos": [
            "Configurar workers de Gunicorn/Uvicorn.",
            "Escribir un proxy inverso con Nginx.",
            "Verificar que no se usa --reload en producción.",
        ],
        "conceptos": [
            {
                "termino": "ASGI",
                "definicion": "Interfaz asíncrona entre el servidor y la aplicación Python.",
                "analogia": "Como el enchufe estándar entre el aparato y la corriente.",
            },
            {
                "termino": "Worker",
                "definicion": "Proceso que atiende peticiones en paralelo.",
                "analogia": "Como varias cajas de supermercado abiertas al mismo tiempo.",
            },
            {
                "termino": "Proxy inverso",
                "definicion": "Servidor que recibe el tráfico y lo reparte hacia la aplicación.",
                "analogia": "Como el recepcionista que dirige a cada visitante al área correcta.",
            },
            {
                "termino": "Timeout",
                "definicion": "Tiempo máximo que se espera una respuesta antes de cortar.",
                "analogia": "Como colgar una llamada que lleva demasiado tiempo en espera.",
            },
        ],
        "resultado": {
            "titulo": "Tu configuración de producción se verá así",
            "lenguaje": "text",
            "codigo": """$ gunicorn -c gunicorn_conf.py app:app
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8000
[INFO] Using worker: uvicorn.workers.UvicornWorker
[INFO] Booting worker with pid: 101
[INFO] Booting worker with pid: 102
[INFO] Booting worker with pid: 103

$ curl -I https://api.ejemplo.com/api/libros
HTTP/2 200
server: nginx
content-type: application/json

nginx.conf: proxy_pass -> 127.0.0.1:8000
gunicorn_conf.py: workers = 2 * cpu_count() + 1
start.sh: sin --reload""",
            "nota": "En producción no se usa `uvicorn --reload`: consume memoria y reinicia el proceso en cada cambio.",
        },
        "reto": {
            "enunciado": "Escribe la configuración de Gunicorn, el proxy inverso de Nginx y el script de arranque para producción.",
            "archivo": "gunicorn_conf.py",
            "requisitos": [
                "gunicorn_conf.py calcula workers = 2 * CPU + 1.",
                "Usa uvicorn.workers.UvicornWorker como clase de worker.",
                "nginx.conf hace proxy_pass hacia la aplicación y activa gzip.",
                "Nginx escucha en el puerto 80 y limita el tamaño del cuerpo.",
                "start.sh arranca con gunicorn y no contiene --reload.",
            ],
            "pista": "La fórmula de workers no es un número mágico: equilibra CPU e I/O. Nginx absorbe la red; Gunicorn atiende la aplicación.",
            "archivos": [
                {
                    "ruta": "gunicorn_conf.py",
                    "esqueleto": "%%writefile gunicorn_conf.py\nimport multiprocessing\n\n# Define workers, worker_class, bind y timeout.\n",
                    "descripcion": "Configuración de Gunicorn.",
                },
                {
                    "ruta": "nginx.conf",
                    "esqueleto": "%%writefile nginx.conf\n# Define el upstream, el server, el proxy_pass y gzip.\n",
                    "descripcion": "Proxy inverso.",
                },
                {
                    "ruta": "start.sh",
                    "esqueleto": "%%writefile start.sh\n#!/usr/bin/env bash\nset -e\n# Arranca la aplicación en modo producción.\n",
                    "descripcion": "Script de arranque.",
                },
            ],
        },
        "verificacion": [
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "gunicorn_conf.py",
                        "regex": ["workers\\s*=\\s*\\(?\\s*2\\s*\\*", "cpu_count|multiprocessing", "UvicornWorker"],
                        "descripcion": "Gunicorn usa la fórmula de workers",
                    },
                    {
                        "ruta": "nginx.conf",
                        "regex": ["proxy_pass\\s+http://(127\\.0\\.0\\.1|localhost|api)", "gzip\\s+on", "client_max_body_size", "listen\\s+80"],
                        "descripcion": "Nginx hace proxy y limita el cuerpo",
                    },
                    {
                        "ruta": "start.sh",
                        "exigir": ["gunicorn"],
                        "prohibir": ["--reload"],
                        "descripcion": "Arranque de producción sin reload",
                    },
                ],
            },
            {
                "tipo": "python",
                "checks": [
                    {
                        "descripcion": "La fórmula de workers es la esperada",
                        "codigo": """import multiprocessing
import gunicorn_conf as g
assert g.workers == 2 * multiprocessing.cpu_count() + 1, g.workers
assert "UvicornWorker" in g.worker_class, g.worker_class
""",
                    }
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion33.md` con la arquitectura Nginx → Gunicorn → Uvicorn.",
    },
    34: {
        "pregunta": "¿Cómo pide datos tu página sin recargarse?",
        "prerrequisitos": [
            "Sesión 33: servidores de producción",
            "Saber qué es una promesa en JavaScript",
        ],
        "objetivos": [
            "Consumir una API con fetch y async/await.",
            "Validar response.ok antes de leer el JSON.",
            "Enviar el token en el encabezado Authorization.",
        ],
        "conceptos": [
            {
                "termino": "fetch",
                "definicion": "Función nativa del navegador para hacer peticiones HTTP.",
                "analogia": "Como el mensajero que lleva una solicitud y trae la respuesta.",
            },
            {
                "termino": "Promesa",
                "definicion": "Objeto que representa un resultado que llegará después.",
                "analogia": "Como el ticket de una tintorería: aún no tienes la ropa, pero tienes el comprobante.",
            },
            {
                "termino": "async / await",
                "definicion": "Sintaxis para esperar una promesa sin bloquear la interfaz.",
                "analogia": "Como esperar el autobús mientras sigues viendo el teléfono.",
            },
            {
                "termino": "response.ok",
                "definicion": "Propiedad que indica si el código HTTP está entre 200 y 299.",
                "analogia": "Como el semáforo en verde: indica que puedes continuar.",
            },
        ],
        "resultado": {
            "titulo": "Tu cliente se verá así en el navegador",
            "lenguaje": "javascript",
            "codigo": """// consola del navegador
const respuesta = await fetch("/api/libros");
if (!respuesta.ok) throw new Error(`HTTP ${respuesta.status}`);
const datos = await respuesta.json();
console.log(datos);
// { libros: [ { id: 1, titulo: "Rayuela" } ] }

<!-- HTML renderizado -->
<ul id="lista">
  <li>Rayuela — 1963</li>
</ul>

<!-- petición autenticada -->
fetch("/api/perfil", {
  headers: { Authorization: `Bearer ${token}` }
});""",
            "nota": "fetch no falla en un 404: la promesa se resuelve. Debes revisar response.ok.",
        },
        "reto": {
            "enunciado": "Escribe el cliente JavaScript que consume la API de libros, maneja errores y envía el token cuando corresponde.",
            "archivo": "app.js",
            "requisitos": [
                "La función de carga usa async/await y fetch.",
                "Se valida response.ok antes de parsear el JSON.",
                "Se usa JSON.stringify al enviar un cuerpo.",
                "El token se envía como Authorization: Bearer.",
                "El resultado se muestra en el elemento #lista.",
            ],
            "pista": "Separar la petición de la renderización te permite probar cada parte. `fetch` devuelve una respuesta; `response.json()` devuelve otra promesa.",
            "archivos": [
                {
                    "ruta": "index.html",
                    "esqueleto": "%%writefile index.html\n<!DOCTYPE html>\n<html lang=\"es\">\n<head><meta charset=\"UTF-8\"><title>Biblioteca</title></head>\n<body>\n  <h1>Biblioteca</h1>\n  <ul id=\"lista\"></ul>\n  <script src=\"app.js\"></script>\n</body>\n</html>\n",
                    "descripcion": "Página que contiene la lista.",
                },
                {
                    "ruta": "app.js",
                    "esqueleto": "%%writefile app.js\n// Implementa la carga de libros y el renderizado en #lista.\n",
                    "descripcion": "Cliente Fetch.",
                },
            ],
        },
        "verificacion": [
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "app.js",
                        "regex": ["async\\s+function|async\\s*\\(", "fetch\\(", "await\\s+.*\\.json\\(\\)", "\\.ok", "Authorization", "Bearer", "JSON\\.stringify", "lista"],
                        "descripcion": "El cliente usa fetch, valida la respuesta y autentica",
                    },
                    {
                        "ruta": "index.html",
                        "exigir": ["id=\"lista\"", "app.js"],
                        "descripcion": "La página carga el cliente",
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion34.md` con una captura de la consola y la lista renderizada.",
    },
    35: {
        "pregunta": "¿Cómo cambia la página sin recargarla?",
        "prerrequisitos": [
            "Sesión 34: Fetch API",
            "Saber qué es el DOM",
        ],
        "objetivos": [
            "Mantener un estado del cliente.",
            "Renderizar una lista a partir del estado.",
            "Actualizar la interfaz sin recargar la página.",
        ],
        "conceptos": [
            {
                "termino": "DOM",
                "definicion": "Árbol de nodos que representa el HTML de la página.",
                "analogia": "Como el plano de una casa que puedes modificar en vivo.",
            },
            {
                "termino": "Estado del cliente",
                "definicion": "Datos que la interfaz necesita recordar entre acciones.",
                "analogia": "Como la memoria de lo que llevas en el carrito de compras.",
            },
            {
                "termino": "Render",
                "definicion": "Transformar el estado en elementos visibles.",
                "analogia": "Como pintar el cuadro cada vez que cambia el modelo.",
            },
            {
                "termino": "Evento",
                "definicion": "Acción del usuario o del navegador que dispara una función.",
                "analogia": "Como el timbre que avisa que llegó una visita.",
            },
        ],
        "resultado": {
            "titulo": "Tu interfaz reactiva se verá así",
            "lenguaje": "html",
            "codigo": """<ul id="lista">
  <li data-id="1">Rayuela <button>Eliminar</button></li>
  <li data-id="2">Cien años de soledad <button>Eliminar</button></li>
</ul>

<!-- al hacer clic en Eliminar del id 1 -->
<ul id="lista">
  <li data-id="2">Cien años de soledad <button>Eliminar</button></li>
</ul>

La página no se recarga: solo cambia el DOM.""",
            "nota": "El estado es la fuente de verdad; el DOM es una consecuencia. Si actualizas el DOM sin actualizar el estado, la interfaz miente.",
        },
        "reto": {
            "enunciado": "Implementa una lista reactiva: el estado vive en JavaScript y el DOM se vuelve a renderizar cuando cambia.",
            "archivo": "app.js",
            "requisitos": [
                "Existe un objeto de estado con los libros.",
                "Existe una función render que reconstruye la lista.",
                "La lista se inserta con innerHTML o con nodos del DOM.",
                "Un botón Eliminar actualiza el estado y vuelve a renderizar.",
                "La página no se recarga.",
            ],
            "pista": "Si borras un elemento del DOM a mano pero no del estado, el próximo render lo revive. Cambia el estado y deja que render haga el resto.",
            "archivos": [
                {
                    "ruta": "index.html",
                    "esqueleto": "%%writefile index.html\n<!DOCTYPE html>\n<html lang=\"es\">\n<head><meta charset=\"UTF-8\"><title>Biblioteca reactiva</title></head>\n<body>\n  <h1>Biblioteca</h1>\n  <ul id=\"lista\"></ul>\n  <script src=\"app.js\"></script>\n</body>\n</html>\n",
                    "descripcion": "Página con el contenedor de la lista.",
                },
                {
                    "ruta": "app.js",
                    "esqueleto": "%%writefile app.js\n// Define el estado, render() y el manejo de eventos.\n",
                    "descripcion": "Estado y renderizado.",
                },
            ],
        },
        "verificacion": [
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "app.js",
                        "regex": ["const\\s+estado|let\\s+estado|estado\\s*=", "function\\s+render|const\\s+render", "innerHTML|createElement|appendChild", "addEventListener", "querySelector"],
                        "descripcion": "Hay estado, render y eventos",
                    },
                    {
                        "ruta": "index.html",
                        "exigir": ["id=\"lista\"", "app.js"],
                        "descripcion": "La página carga el renderizador",
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion35.md` con la captura de la lista antes y después de eliminar.",
    },
    36: {
        "pregunta": "¿Cómo navegas entre vistas sin recargar la página?",
        "prerrequisitos": [
            "Sesión 35: DOM y estado",
            "Saber qué es una URL y un hash",
        ],
        "objetivos": [
            "Implementar un ruteador por hash.",
            "Renderizar una vista según la URL.",
            "Verificar que la navegación no recarga el documento.",
        ],
        "conceptos": [
            {
                "termino": "SPA",
                "definicion": "Aplicación que carga una sola página y cambia sus vistas con JavaScript.",
                "analogia": "Como una casa con varias habitaciones: no cambias de casa, cambias de cuarto.",
            },
            {
                "termino": "Ruteador",
                "definicion": "Componente que decide qué vista mostrar según la URL.",
                "analogia": "Como el mapa de un centro comercial: según el número, te dirige a la tienda.",
            },
            {
                "termino": "Hash routing",
                "definicion": "Navegación usando la parte de la URL después de #.",
                "analogia": "Como los marcadores dentro de un mismo libro.",
            },
            {
                "termino": "Vista",
                "definicion": "Bloque de interfaz que se muestra para una ruta.",
                "analogia": "Como una diapositiva dentro de la misma presentación.",
            },
        ],
        "resultado": {
            "titulo": "Tu SPA se verá así",
            "lenguaje": "text",
            "codigo": """http://localhost:8000/#/libros
  -> vista de lista de libros

http://localhost:8000/#/libros/1
  -> vista de detalle del libro 1

http://localhost:8000/#/no-existe
  -> vista 404

Al cambiar el hash no se recarga el documento:
solo se reemplaza el contenido de <div id="app">.""",
            "nota": "El hash no viaja al servidor: el navegador lo entrega a JavaScript y el ruteador decide.",
        },
        "reto": {
            "enunciado": "Implementa una SPA ligera con rutas por hash para listar y ver el detalle de libros.",
            "archivo": "router.js",
            "requisitos": [
                "Escucha el evento hashchange.",
                "La ruta #/libros muestra la lista.",
                "La ruta #/libros/{id} muestra el detalle.",
                "Una ruta desconocida muestra 404.",
                "La vista se renderiza dentro de #app sin recargar la página.",
            ],
            "pista": "El ruteador es una función que lee `location.hash`, elige una vista y la pinta. Si usas enlaces con href=\"#/...\", el navegador no recarga.",
            "archivos": [
                {
                    "ruta": "index.html",
                    "esqueleto": "%%writefile index.html\n<!DOCTYPE html>\n<html lang=\"es\">\n<head><meta charset=\"UTF-8\"><title>Biblioteca SPA</title></head>\n<body>\n  <nav>\n    <a href=\"#/libros\">Libros</a>\n  </nav>\n  <div id=\"app\"></div>\n  <script src=\"router.js\"></script>\n</body>\n</html>\n",
                    "descripcion": "Página única de la SPA.",
                },
                {
                    "ruta": "router.js",
                    "esqueleto": "%%writefile router.js\n// Implementa el ruteador por hash y las vistas.\n",
                    "descripcion": "Ruteador y vistas.",
                },
            ],
        },
        "verificacion": [
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "router.js",
                        "regex": ["hashchange", "location\\.hash", "#/libros", "renderRoute|function\\s+render", "fetch\\(", "app"],
                        "descripcion": "El ruteador escucha el hash y renderiza vistas",
                    },
                    {
                        "ruta": "index.html",
                        "exigir": ["id=\"app\"", "router.js", "href=\"#/libros\""],
                        "descripcion": "La página contiene el contenedor y los enlaces",
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion36.md` con la captura de las tres rutas.",
    },
    37: {
        "pregunta": "¿Cómo demuestras que todo el flujo funciona de principio a fin?",
        "prerrequisitos": [
            "Sesión 36: SPA",
            "Saber qué es una prueba de integración",
        ],
        "objetivos": [
            "Construir una colección Postman con variables.",
            "Encadenar registro, login y acceso autenticado.",
            "Automatizar la suite con Newman.",
        ],
        "conceptos": [
            {
                "termino": "Prueba E2E",
                "definicion": "Prueba que recorre el flujo completo del usuario.",
                "analogia": "Como ensayar una obra de principio a fin, no solo una escena.",
            },
            {
                "termino": "Colección",
                "definicion": "Conjunto ordenado de peticiones con sus pruebas.",
                "analogia": "Como una lista de pasos de un manual de operaciones.",
            },
            {
                "termino": "Aserción",
                "definicion": "Condición que debe cumplirse para que la prueba pase.",
                "analogia": "Como la lista de verificación del piloto.",
            },
            {
                "termino": "Variable de entorno",
                "definicion": "Valor reutilizable entre peticiones, como un token.",
                "analogia": "Como un pase que se reutiliza en cada puerta.",
            },
        ],
        "resultado": {
            "titulo": "Tu suite E2E se verá así",
            "lenguaje": "text",
            "codigo": """$ newman run coleccion.json -e entorno.json
→ registro        [201 Created]  ✅ pasa
→ login           [200 OK]       ✅ pasa
→ crear libro     [201 Created]  ✅ pasa
→ listar libros   [200 OK]       ✅ pasa
→ perfil          [200 OK]       ✅ pasa

5 requests, 0 failures
La variable {{token}} se guardó en el login y se usó en perfil.""",
            "nota": "Una prueba E2E no solo mira el código HTTP: también valida el contenido del JSON.",
        },
        "reto": {
            "enunciado": "Crea una colección Postman/Newman que recorra registro, login, creación, listado y perfil usando el token guardado.",
            "archivo": "coleccion.json",
            "requisitos": [
                "La colección usa el esquema de Postman v2.1.",
                "Contiene al menos cinco peticiones en orden.",
                "El login guarda el token en una variable de entorno.",
                "Las peticiones protegidas usan {{token}}.",
                "Cada petición incluye una aserción sobre el código HTTP y el JSON.",
            ],
            "pista": "En Postman, el orden de los elementos es el orden de ejecución. Guarda el token con `pm.environment.set` y úsalo con `{{token}}` en la siguiente petición.",
            "archivos": [
                {
                    "ruta": "coleccion.json",
                    "esqueleto": "%%writefile coleccion.json\n{\n  \"info\": {\"name\": \"Biblioteca E2E\", \"schema\": \"https://schema.getpostman.com/json/collection/v2.1.0/collection.json\"},\n  \"item\": []\n}\n",
                    "descripcion": "Colección de pruebas.",
                },
                {
                    "ruta": "entorno.json",
                    "esqueleto": "%%writefile entorno.json\n{\n  \"name\": \"local\",\n  \"values\": [{\"key\": \"base_url\", \"value\": \"http://127.0.0.1:8000\"}]\n}\n",
                    "descripcion": "Variables de entorno.",
                },
            ],
        },
        "verificacion": [
            {
                "tipo": "json",
                "checks": [
                    {
                        "ruta": "coleccion.json",
                        "claves": ["info.schema", "item"],
                        "contiene": ["pm.response.to.have.status", "pm.environment.set", "{{token}}"],
                        "descripcion": "La colección tiene aserciones y variables",
                    },
                    {
                        "ruta": "entorno.json",
                        "claves": ["values"],
                        "contiene": ["base_url"],
                        "descripcion": "El entorno define la URL base",
                    },
                ],
            },
            {
                "tipo": "python",
                "checks": [
                    {
                        "descripcion": "La colección tiene al menos cinco peticiones",
                        "codigo": """import json
datos = json.load(open("coleccion.json", encoding="utf-8"))
assert len(datos.get("item", [])) >= 5, len(datos.get("item", []))
""",
                    }
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion37.md` con la salida de Newman.",
    },
    38: {
        "pregunta": "¿Cómo respondes rápido cuando la tarea es lenta?",
        "prerrequisitos": [
            "Sesión 37: pruebas E2E",
            "Saber qué es una tarea en segundo plano",
        ],
        "objetivos": [
            "Responder 202 antes de terminar el trabajo pesado.",
            "Delegar el trabajo con BackgroundTasks.",
            "Verificar el estado de la tarea y su efecto secundario.",
        ],
        "conceptos": [
            {
                "termino": "Tarea en segundo plano",
                "definicion": "Trabajo que se ejecuta después de enviar la respuesta al cliente.",
                "analogia": "Como pedir una pizza: te dan el ticket antes de hornearla.",
            },
            {
                "termino": "HTTP 202",
                "definicion": "La petición fue aceptada, pero el procesamiento aún no termina.",
                "analogia": "Como el comprobante de un trámite: ya lo recibieron, aún no está listo.",
            },
            {
                "termino": "Cola",
                "definicion": "Estructura que guarda tareas pendientes para un worker.",
                "analogia": "Como la fila de pedidos en una cocina.",
            },
            {
                "termino": "Idempotencia",
                "definicion": "Reintentar no debe duplicar el efecto de una tarea.",
                "analogia": "Como no cobrar dos veces si el cliente pulsa dos veces «pagar».",
            },
        ],
        "resultado": {
            "titulo": "Tu tarea en segundo plano se verá así",
            "lenguaje": "http",
            "codigo": """POST /api/reportes  {"email":"ana@ejemplo.com"}
HTTP/1.1 202 Accepted
{"tarea_id":"r1","estado":"en_proceso"}

GET /api/reportes/r1
HTTP/1.1 200 OK
{"tarea_id":"r1","estado":"completado"}

$ cat reportes.log
ana@ejemplo.com""",
            "nota": "El cliente recibe respuesta antes de que termine el trabajo; el log demuestra que sí se ejecutó.",
        },
        "reto": {
            "enunciado": "Implementa un reporte que se procese en segundo plano y pueda consultarse por su identificador.",
            "archivo": "app.py",
            "requisitos": [
                "POST /api/reportes responde 202 con tarea_id y estado en_proceso.",
                "El trabajo se agrega con BackgroundTasks y escribe el email en reportes.log.",
                "GET /api/reportes/{tarea_id} responde 200 con estado completado.",
                "Una tarea inexistente responde 404.",
                "El log existe después de ejecutar la petición.",
            ],
            "pista": "`BackgroundTasks` se inyecta como parámetro y se ejecuta después de la respuesta. No hagas el trabajo pesado antes de responder.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "limpiar": ["reportes.log"],
                "casos": [
                    {
                        "descripcion": "El reporte se acepta de inmediato",
                        "metodo": "POST",
                        "ruta": "/api/reportes",
                        "json": {"email": "ana@ejemplo.com"},
                        "estado": 202,
                        "json_contiene": {"estado": "en_proceso"},
                        "guardar": {"tarea_id": "tarea_id"},
                    },
                    {
                        "descripcion": "La tarea se consulta por id",
                        "metodo": "GET",
                        "ruta": "/api/reportes/{tarea_id}",
                        "estado": 200,
                        "json_contiene": {"estado": "completado"},
                    },
                    {
                        "descripcion": "Una tarea inexistente es 404",
                        "metodo": "GET",
                        "ruta": "/api/reportes/no-existe",
                        "estado": 404,
                    },
                ],
            },
            {
                "tipo": "python",
                "checks": [
                    {
                        "descripcion": "El trabajo quedó registrado en el log",
                        "codigo": """from pathlib import Path
texto = Path("reportes.log").read_text(encoding="utf-8")
assert "ana@ejemplo.com" in texto, texto
""",
                    }
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {"ruta": "app.py", "exigir": ["BackgroundTasks"], "descripcion": "Se usa BackgroundTasks"},
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion38.md` con el tiempo de respuesta y el contenido del log.",
    },
    39: {
        "pregunta": "¿Cómo sabe un balanceador si tu API está sana?",
        "prerrequisitos": [
            "Sesión 38: tareas en segundo plano",
            "Saber qué es un healthcheck",
        ],
        "objetivos": [
            "Exponer un endpoint de salud con dependencias.",
            "Responder 503 cuando la base no está disponible.",
            "Verificar el contrato de monitoreo.",
        ],
        "conceptos": [
            {
                "termino": "Healthcheck",
                "definicion": "Endpoint que reporta si el servicio puede atender tráfico.",
                "analogia": "Como el chequeo médico antes de una competencia.",
            },
            {
                "termino": "Liveness",
                "definicion": "Indica si el proceso sigue vivo.",
                "analogia": "Como comprobar que el corazón sigue latiendo.",
            },
            {
                "termino": "Readiness",
                "definicion": "Indica si el servicio está listo para recibir tráfico.",
                "analogia": "Como comprobar que la cocina ya puede tomar pedidos.",
            },
            {
                "termino": "HTTP 503",
                "definicion": "El servicio no está disponible temporalmente.",
                "analogia": "Como el letrero «cerrado por mantenimiento».",
            },
        ],
        "resultado": {
            "titulo": "Tu healthcheck se verá así",
            "lenguaje": "http",
            "codigo": """GET /health
HTTP/1.1 200 OK
{"status":"ok","db":"ok","version":"1.0.0"}

GET /health?simular_fallo=true
HTTP/1.1 503 Service Unavailable
{"status":"error","db":"error","version":"1.0.0"}

GET /api/metricas
HTTP/1.1 200 OK
{"uptime":12.4,"version":"1.0.0"}""",
            "nota": "Un healthcheck debe ser barato y comprobar las dependencias críticas, no solo que el proceso exista.",
        },
        "reto": {
            "enunciado": "Implementa un endpoint de salud con verificación de base de datos y un endpoint de métricas básicas.",
            "archivo": "app.py",
            "requisitos": [
                "GET /health responde 200 con status ok, db ok y version.",
                "GET /health?simular_fallo=true responde 503 con status error.",
                "GET /api/metricas responde 200 con uptime y version.",
                "El healthcheck consulta la base de datos, no solo el proceso.",
                "La respuesta no expone secretos ni rutas internas.",
            ],
            "pista": "El healthcheck no debe ser costoso. Un `SELECT 1` a la base es suficiente para readiness; no recorras tablas completas.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "El servicio sano responde 200",
                        "metodo": "GET",
                        "ruta": "/health",
                        "estado": 200,
                        "json_contiene": {"status": "ok", "db": "ok"},
                    },
                    {
                        "descripcion": "El fallo simulado responde 503",
                        "metodo": "GET",
                        "ruta": "/health?simular_fallo=true",
                        "estado": 503,
                        "json_contiene": {"status": "error", "db": "error"},
                    },
                    {
                        "descripcion": "Las métricas están disponibles",
                        "metodo": "GET",
                        "ruta": "/api/metricas",
                        "estado": 200,
                        "json_contiene": {"version": "1.0.0"},
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion39.md` con las capturas de 200 y 503.",
    },
    40: {
        "pregunta": "¿Tu aplicación completa resiste una demostración en vivo?",
        "prerrequisitos": [
            "Sesiones 31 a 39: despliegue, frontend y pruebas",
            "Tu proyecto integrador en curso",
        ],
        "objetivos": [
            "Integrar API, base de datos, seguridad y salud en una demo.",
            "Verificar el flujo completo con un solo comando.",
            "Presentar la evidencia en GitHub y en la nube.",
        ],
        "conceptos": [
            {
                "termino": "Full-stack",
                "definicion": "Sistema que integra backend, base de datos y cliente web.",
                "analogia": "Como un restaurante completo: cocina, almacén y sala.",
            },
            {
                "termino": "Demo",
                "definicion": "Demostración reproducible del sistema funcionando.",
                "analogia": "Como el ensayo general antes del estreno.",
            },
            {
                "termino": "Despliegue",
                "definicion": "Poner la aplicación disponible para usuarios reales.",
                "analogia": "Como abrir la tienda al público.",
            },
            {
                "termino": "Evidencia",
                "definicion": "Prueba verificable de que el sistema funciona.",
                "analogia": "Como el acta de una entrega.",
            },
        ],
        "resultado": {
            "titulo": "Tu demostración final se verá así",
            "lenguaje": "http",
            "codigo": """GET  /health                     -> 200 {"status":"ok"}
POST /api/libros                -> 201
GET  /api/libros                -> 200
POST /api/token  (ana)          -> 200 + token
GET  /api/perfil (Bearer ana)   -> 200
GET  /api/admin/panel (ana)     -> 403
GET  /api/admin/panel (admin)   -> 200
OPTIONS /api/libros (CORS)      -> 200

RESUMEN: 8/8 casos correctos. ¡Hito 4 listo!""",
            "nota": "La demo no es un video: es el sistema respondiendo en vivo, con evidencia en el repositorio.",
        },
        "reto": {
            "enunciado": "Integra y demuestra tu API full-stack: persistencia, autenticación, roles, CORS, salud y cliente SPA.",
            "archivo": "app.py",
            "requisitos": [
                "Usuarios de prueba: ana/secreta (user) y admin/admin123 (admin).",
                "La API usa SQLite y conserva los libros entre peticiones.",
                "Existe login con token y roles admin/user.",
                "El panel admin responde 200 a admin y 403 a user.",
                "CORS autoriza https://app.ejemplo.com.",
                "GET /health responde 200.",
                "El cliente SPA (index.html y app.js) consume la API con fetch.",
            ],
            "pista": "Para la demo, prepara datos de prueba y un guion de tres minutos: salud, crear, listar, login, perfil y panel. Si algo falla, el verificador te dice exactamente qué.",
            "archivos": [
                {
                    "ruta": "app.py",
                    "esqueleto": "%%writefile app.py\nfrom fastapi import FastAPI\n\napp = FastAPI(title=\"Biblioteca Full-Stack\")\n\n# Integra persistencia, autenticación, roles, CORS y salud.\n",
                    "descripcion": "API completa del hito final.",
                },
                {
                    "ruta": "index.html",
                    "esqueleto": "%%writefile index.html\n<!DOCTYPE html>\n<html lang=\"es\">\n<head><meta charset=\"UTF-8\"><title>Biblioteca Full-Stack</title></head>\n<body>\n  <h1>Biblioteca</h1>\n  <ul id=\"lista\"></ul>\n  <script src=\"app.js\"></script>\n</body>\n</html>\n",
                    "descripcion": "Cliente SPA.",
                },
                {
                    "ruta": "app.js",
                    "esqueleto": "%%writefile app.js\n// Consume la API con fetch y renderiza la lista.\n",
                    "descripcion": "Lógica del cliente.",
                },
            ],
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "limpiar": ["biblioteca.db"],
                "casos": [
                    {
                        "descripcion": "El sistema está sano",
                        "metodo": "GET",
                        "ruta": "/health",
                        "estado": 200,
                        "json_contiene": {"status": "ok"},
                    },
                    {
                        "descripcion": "Se crea un libro persistente",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Rayuela"},
                    },
                    {
                        "descripcion": "El libro se lista",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1}]},
                    },
                    {
                        "descripcion": "El usuario se autentica",
                        "metodo": "POST",
                        "ruta": "/api/token",
                        "json": {"usuario": "ana", "password": "secreta"},
                        "estado": 200,
                        "guardar": {"token_user": "access_token"},
                    },
                    {
                        "descripcion": "El usuario consulta su perfil",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "headers": {"Authorization": "Bearer {token_user}"},
                        "estado": 200,
                    },
                    {
                        "descripcion": "El usuario no entra al panel admin",
                        "metodo": "GET",
                        "ruta": "/api/admin/panel",
                        "headers": {"Authorization": "Bearer {token_user}"},
                        "estado": 403,
                    },
                    {
                        "descripcion": "El administrador sí entra",
                        "metodo": "POST",
                        "ruta": "/api/token",
                        "json": {"usuario": "admin", "password": "admin123"},
                        "estado": 200,
                        "guardar": {"token_admin": "access_token"},
                    },
                    {
                        "descripcion": "El administrador consulta el panel",
                        "metodo": "GET",
                        "ruta": "/api/admin/panel",
                        "headers": {"Authorization": "Bearer {token_admin}"},
                        "estado": 200,
                    },
                    {
                        "descripcion": "CORS autoriza al cliente",
                        "metodo": "OPTIONS",
                        "ruta": "/api/libros",
                        "headers": {
                            "Origin": "https://app.ejemplo.com",
                            "Access-Control-Request-Method": "POST",
                        },
                        "estado": 200,
                        "headers_contiene": {"access-control-allow-origin": "https://app.ejemplo.com"},
                        "headers_no_contiene": {"access-control-allow-origin": "*"},
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {"ruta": "index.html", "exigir": ["id=\"lista\"", "app.js"], "descripcion": "Cliente SPA presente"},
                    {"ruta": "app.js", "regex": ["fetch\\(", "await\\s+.*\\.json\\(\\)", "Authorization"], "descripcion": "El cliente consume la API"},
                ],
            },
        ],
        "entrega": "Cuaderno en verde, bitácora `auditorias/auditoria_sesion40.md`, demo en vivo y tag `v1.0-final` en tu repositorio.",
    },
}
