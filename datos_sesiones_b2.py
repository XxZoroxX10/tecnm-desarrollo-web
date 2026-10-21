"""
Contenido enriquecido del Bloque 2 (sesiones 11 a 20).
Lógica de negocio, controladores y autenticación segura.
"""

BLOQUE_2 = {
    11: {
        "pregunta": "¿Dónde vive la lógica de negocio de una API?",
        "prerrequisitos": [
            "Sesión 10: Mock API del Hito 1",
            "Saber qué es un módulo y un import en Python",
        ],
        "objetivos": [
            "Separar router, servicio y repositorio en archivos distintos.",
            "Explicar qué responsabilidad tiene cada capa.",
            "Verificar que la separación no cambia el contrato HTTP.",
        ],
        "conceptos": [
            {
                "termino": "Router",
                "definicion": "Capa que traduce una petición HTTP en una llamada al servicio.",
                "analogia": "Como la recepción de un hotel: recibe al huésped y lo dirige al área correcta.",
            },
            {
                "termino": "Servicio",
                "definicion": "Capa que contiene las reglas de negocio y decide qué hacer con los datos.",
                "analogia": "Como el chef: sabe la receta y coordina los ingredientes.",
            },
            {
                "termino": "Repositorio",
                "definicion": "Capa que habla con la fuente de datos: memoria, archivo o base de datos.",
                "analogia": "Como el almacén: guarda y entrega los ingredientes sin cocinarlos.",
            },
            {
                "termino": "Separación de responsabilidades",
                "definicion": "Cada pieza hace una cosa y la hace bien; los cambios se aíslan.",
                "analogia": "Como un equipo de cocina: cada quien tiene su estación.",
            },
        ],
        "resultado": {
            "titulo": "El mismo contrato, ahora repartido en capas",
            "lenguaje": "text",
            "codigo": """biblioteca/
├── app.py           # crea FastAPI e incluye el router
├── router.py        # define APIRouter y las rutas /api/libros
├── servicio.py      # reglas: crear, listar, validar
└── repositorio.py   # almacenamiento en memoria

GET  /api/libros  -> 200 {"libros":[]}
POST /api/libros  -> 201 {"id":1,"titulo":"Rayuela","anio":1963}

La respuesta HTTP no cambia: cambia quién hace cada cosa.""",
            "nota": "La arquitectura no se ve en la URL; se ve en la facilidad para cambiar una pieza sin romper las demás.",
        },
        "reto": {
            "enunciado": "Refactoriza el CRUD de libros en cuatro capas: app, router, servicio y repositorio. El contrato HTTP debe seguir siendo el mismo.",
            "archivo": "app.py",
            "requisitos": [
                "app.py crea la app e incluye el router.",
                "router.py define un APIRouter con las rutas de libros.",
                "servicio.py contiene las reglas de creación y listado.",
                "repositorio.py guarda los libros en memoria.",
                "El contrato HTTP de la sesión 02 se mantiene: GET 200, POST 201, datos inválidos 422.",
            ],
            "pista": "Si el router conoce la base de datos o el repositorio conoce HTTP, las capas están mezcladas. El router no debería importar `sqlite3`; el repositorio no debería importar `FastAPI`.",
            "archivos": [
                {
                    "ruta": "app.py",
                    "esqueleto": "%%writefile app.py\nfrom fastapi import FastAPI\n\napp = FastAPI(title=\"Biblioteca por capas\")\n\n# Incluye aquí el router cuando lo tengas.\n",
                    "descripcion": "Punto de entrada de la aplicación.",
                },
                {
                    "ruta": "repositorio.py",
                    "esqueleto": "%%writefile repositorio.py\n# Guarda y recupera libros. No conoce HTTP.\n",
                    "descripcion": "Capa de acceso a datos.",
                },
                {
                    "ruta": "servicio.py",
                    "esqueleto": "%%writefile servicio.py\n# Reglas de negocio: crear y listar libros.\n",
                    "descripcion": "Capa de lógica de negocio.",
                },
                {
                    "ruta": "router.py",
                    "esqueleto": "%%writefile router.py\nfrom fastapi import APIRouter\n\nrouter = APIRouter()\n\n# Define aquí las rutas /api/libros.\n",
                    "descripcion": "Capa de exposición HTTP.",
                },
            ],
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "El listado inicia vacío",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": []},
                    },
                    {
                        "descripcion": "El servicio crea un libro",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Rayuela", "anio": 1963},
                    },
                    {
                        "descripcion": "El listado conserva el contrato",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1, "titulo": "Rayuela"}]},
                    },
                    {
                        "descripcion": "La validación del router sigue funcionando",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": "mil novecientos"},
                        "estado": 422,
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {"ruta": "router.py", "exigir": ["APIRouter"], "descripcion": "Existe la capa de router"},
                    {"ruta": "app.py", "exigir": ["include_router"], "descripcion": "La app incluye el router"},
                    {"ruta": "servicio.py", "exigir": [], "descripcion": "Existe la capa de servicio"},
                    {"ruta": "repositorio.py", "exigir": [], "descripcion": "Existe la capa de repositorio"},
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion11.md` con el diagrama de capas.",
    },
    12: {
        "pregunta": "¿Cómo cambias una dependencia sin tocar el endpoint?",
        "prerrequisitos": [
            "Sesión 11: router, servicio y repositorio",
            "Saber qué es una función que devuelve otra función",
        ],
        "objetivos": [
            "Inyectar un repositorio con Depends de FastAPI.",
            "Sustituir una dependencia sin reescribir el endpoint.",
            "Verificar el efecto de la inyección en el contrato HTTP.",
        ],
        "conceptos": [
            {
                "termino": "Dependencia",
                "definicion": "Objeto o función que un endpoint necesita para trabajar.",
                "analogia": "Como la batería de un control: el control no la fabrica, solo la usa.",
            },
            {
                "termino": "Inyección de dependencias",
                "definicion": "Recibir las dependencias desde afuera en lugar de crearlas dentro del endpoint.",
                "analogia": "Como pedir los ingredientes a la despensa en vez de salir a cosecharlos.",
            },
            {
                "termino": "Depends",
                "definicion": "Mecanismo de FastAPI que resuelve una dependencia antes de ejecutar el endpoint.",
                "analogia": "Como el asistente que prepara la mesa antes de que llegue el comensal.",
            },
            {
                "termino": "Inversión de control",
                "definicion": "El código de alto nivel no decide qué implementación concreta usar.",
                "analogia": "Como un enchufe estándar: no importa qué aparato conectes, encaja.",
            },
        ],
        "resultado": {
            "titulo": "Tu endpoint recibirá el repositorio inyectado",
            "lenguaje": "http",
            "codigo": """GET /api/diagnostico
HTTP/1.1 200 OK
{"repositorio":"RepositorioMemoria"}

POST /api/libros
{"titulo":"Rayuela","anio":1963}
HTTP/1.1 201 Created
{"id":1,"titulo":"Rayuela","anio":1963}

GET /api/libros
HTTP/1.1 200 OK
{"libros":[{"id":1,"titulo":"Rayuela","anio":1963}]}""",
            "nota": "El endpoint no crea el repositorio: lo recibe. Esa es la diferencia entre acoplarse y depender de una interfaz.",
        },
        "reto": {
            "enunciado": "Implementa un repositorio en memoria y inyéctalo en los endpoints con Depends. El diagnóstico debe evidenciar qué implementación se está usando.",
            "archivo": "app.py",
            "requisitos": [
                "Existe una función `get_repositorio()` que devuelve una instancia de `RepositorioMemoria`.",
                "Los endpoints de libros reciben el repositorio con `Depends(get_repositorio)`.",
                "GET /api/diagnostico responde {\"repositorio\": \"RepositorioMemoria\"}.",
                "El CRUD mantiene el contrato: GET 200, POST 201, datos inválidos 422.",
            ],
            "pista": "Si el endpoint hace `RepositorioMemoria()` dentro de la función, no está inyectando: está acoplando. La dependencia debe llegar como parámetro.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "El diagnóstico revela el repositorio inyectado",
                        "metodo": "GET",
                        "ruta": "/api/diagnostico",
                        "estado": 200,
                        "json_exacto": {"repositorio": "RepositorioMemoria"},
                    },
                    {
                        "descripcion": "El endpoint inyectado crea un libro",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Rayuela"},
                    },
                    {
                        "descripcion": "El repositorio conserva el estado",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1}]},
                    },
                    {
                        "descripcion": "La validación sigue en el borde",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": "malo"},
                        "estado": 422,
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {"ruta": "app.py", "exigir": ["Depends"], "descripcion": "El endpoint usa Depends"},
                    {"ruta": "app.py", "exigir": ["get_repositorio"], "descripcion": "Existe la función de inyección"},
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion12.md` explicando qué dependencia inyectaste.",
    },
    13: {
        "pregunta": "¿Cómo recuerda el servidor que ya iniciaste sesión?",
        "prerrequisitos": [
            "Sesión 12: inyección de dependencias",
            "Saber qué es una cookie y para qué sirve",
        ],
        "objetivos": [
            "Implementar una sesión con estado en el servidor.",
            "Emitir una cookie segura y leerla en peticiones posteriores.",
            "Diferenciar sesión con estado de un token sin estado.",
        ],
        "conceptos": [
            {
                "termino": "Cookie",
                "definicion": "Pequeño dato que el navegador guarda y envía automáticamente al mismo dominio.",
                "analogia": "Como el boleto de un guardarropa: lo muestras para recuperar tu abrigo.",
            },
            {
                "termino": "Sesión con estado",
                "definicion": "El servidor guarda los datos de la sesión y el cliente solo conserva el identificador.",
                "analogia": "Como una ficha en la recepción: tú llevas el número, el hotel guarda el resto.",
            },
            {
                "termino": "HttpOnly",
                "definicion": "Atributo que impide que JavaScript lea la cookie.",
                "analogia": "Como una caja fuerte que solo abre el servidor.",
            },
            {
                "termino": "Expiración",
                "definicion": "Momento en que la sesión deja de ser válida aunque la cookie siga existiendo.",
                "analogia": "Como la hora de cierre de un estacionamiento.",
            },
        ],
        "resultado": {
            "titulo": "Tu flujo de sesión se verá así",
            "lenguaje": "http",
            "codigo": """POST /api/login  {"usuario":"ana","password":"secreta"}
HTTP/1.1 200 OK
Set-Cookie: session_id=...; HttpOnly; Path=/; SameSite=Lax
{"mensaje":"sesión iniciada"}

GET /api/perfil   (con la cookie)
HTTP/1.1 200 OK
{"usuario":"ana"}

POST /api/logout  (con la cookie)
HTTP/1.1 204 No Content

GET /api/perfil   (después del logout)
HTTP/1.1 401 Unauthorized""",
            "nota": "La cookie viaja sola: el cliente no tiene que copiar el identificador en cada petición.",
        },
        "reto": {
            "enunciado": "Implementa login, perfil y logout usando sesiones en memoria y una cookie HttpOnly.",
            "archivo": "app.py",
            "requisitos": [
                "El usuario de prueba es ana con contraseña secreta.",
                "POST /api/login valida usuario y contraseña y responde 200.",
                "La respuesta de login incluye una cookie session_id con HttpOnly y SameSite=Lax.",
                "GET /api/perfil devuelve el usuario si la cookie es válida; si no, 401.",
                "POST /api/logout invalida la sesión y responde 204.",
                "Después del logout, /api/perfil vuelve a responder 401.",
            ],
            "pista": "El cliente solo guarda un identificador opaco. Todo lo demás (usuario, expiración, permisos) vive en el servidor.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "Login correcto y cookie HttpOnly",
                        "metodo": "POST",
                        "ruta": "/api/login",
                        "json": {"usuario": "ana", "password": "secreta"},
                        "estado": 200,
                        "headers_contiene": {"set-cookie": ["httponly", "samesite"]},
                    },
                    {
                        "descripcion": "El perfil se obtiene con la cookie",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "estado": 200,
                        "json_contiene": {"usuario": "ana"},
                    },
                    {
                        "descripcion": "El logout cierra la sesión",
                        "metodo": "POST",
                        "ruta": "/api/logout",
                        "estado": 204,
                    },
                    {
                        "descripcion": "Después del logout el perfil es 401",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "estado": 401,
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion13.md` con la diferencia entre sesión y token.",
    },
    14: {
        "pregunta": "¿Por qué nunca se guarda una contraseña tal cual?",
        "prerrequisitos": [
            "Sesión 13: cookies y sesiones",
            "Saber qué es una función hash",
        ],
        "objetivos": [
            "Guardar contraseñas con bcrypt y salt.",
            "Verificar una contraseña sin descifrarla.",
            "Comprobar que la API nunca devuelve el hash ni la contraseña.",
        ],
        "conceptos": [
            {
                "termino": "Hash",
                "definicion": "Huella digital irreversible de un dato: cambia si cambia la entrada.",
                "analogia": "Como la huella de una persona: identifica, pero no reconstruye a la persona.",
            },
            {
                "termino": "Salt",
                "definicion": "Valor aleatorio que se agrega a cada contraseña antes de hashearla.",
                "analogia": "Como una sal secreta distinta para cada platillo: dos comidas iguales saben distinto.",
            },
            {
                "termino": "Bcrypt",
                "definicion": "Algoritmo de hashing lento y ajustable, diseñado para contraseñas.",
                "analogia": "Como una cerradura que tarda a propósito: molesta al atacante, no al usuario.",
            },
            {
                "termino": "Verificación",
                "definicion": "Comparar la contraseña recibida con el hash guardado, sin deshacer el hash.",
                "analogia": "Como probar una llave en la cerradura en vez de copiar la cerradura.",
            },
        ],
        "resultado": {
            "titulo": "Tu registro y login se verán así",
            "lenguaje": "http",
            "codigo": """POST /api/registro  {"usuario":"ana","password":"secreta"}
HTTP/1.1 201 Created
{"usuario":"ana"}

POST /api/login  {"usuario":"ana","password":"secreta"}
HTTP/1.1 200 OK
{"usuario":"ana","autenticado":true}

POST /api/login  {"usuario":"ana","password":"incorrecta"}
HTTP/1.1 401 Unauthorized

La respuesta NUNCA contiene "password" ni el hash.""",
            "nota": "El hash se guarda en el servidor; la contraseña original no se almacena en ningún lado.",
        },
        "reto": {
            "enunciado": "Implementa registro y login con hashing seguro. La contraseña nunca debe viajar de vuelta al cliente.",
            "archivo": "app.py",
            "requisitos": [
                "POST /api/registro recibe usuario y password, guarda solo el hash y responde 201.",
                "La respuesta de registro no incluye password ni hash.",
                "POST /api/login compara la contraseña con el hash y responde 200 o 401.",
                "Debes usar bcrypt (o passlib) para el hash.",
                "Un usuario repetido no debe sobrescribir la contraseña existente.",
            ],
            "pista": "No compares hashes con `==` si puedes usar la función de verificación del algoritmo. Bcrypt ya incluye el salt dentro del hash.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "El registro responde sin filtrar la contraseña",
                        "metodo": "POST",
                        "ruta": "/api/registro",
                        "json": {"usuario": "ana", "password": "secreta"},
                        "estado": 201,
                        "json_contiene": {"usuario": "ana"},
                        "no_contiene": ["password", "hash"],
                    },
                    {
                        "descripcion": "El login correcto autentica",
                        "metodo": "POST",
                        "ruta": "/api/login",
                        "json": {"usuario": "ana", "password": "secreta"},
                        "estado": 200,
                        "json_contiene": {"usuario": "ana", "autenticado": True},
                    },
                    {
                        "descripcion": "La contraseña incorrecta se rechaza",
                        "metodo": "POST",
                        "ruta": "/api/login",
                        "json": {"usuario": "ana", "password": "incorrecta"},
                        "estado": 401,
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "app.py",
                        "regex": ["bcrypt|passlib"],
                        "descripcion": "Se usa un algoritmo de hashing para contraseñas",
                    },
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion14.md` explicando por qué no se puede «deshashear».",
    },
    15: {
        "pregunta": "¿Cómo demuestras quién eres sin que el servidor guarde tu sesión?",
        "prerrequisitos": [
            "Sesión 14: hashing de contraseñas",
            "Saber qué es una firma digital",
        ],
        "objetivos": [
            "Emitir un JWT firmado con expiración.",
            "Validar la firma y el token en una ruta protegida.",
            "Rechazar tokens alterados con 401.",
        ],
        "conceptos": [
            {
                "termino": "JWT",
                "definicion": "Token firmado con tres partes: cabecera, payload y firma.",
                "analogia": "Como un pasaporte sellado: cualquiera lo lee, pero solo la autoridad puede emitirlo.",
            },
            {
                "termino": "Claim",
                "definicion": "Dato dentro del payload del token, por ejemplo sub, rol o exp.",
                "analogia": "Como los campos de una credencial: nombre, cargo, vigencia.",
            },
            {
                "termino": "Firma HMAC",
                "definicion": "Código que demuestra que el token no fue alterado sin la clave secreta.",
                "analogia": "Como el sello de lacre de un sobre: si se rompe, se nota.",
            },
            {
                "termino": "Estado sin sesión",
                "definicion": "El servidor no guarda la sesión: toda la información viaja firmada en el token.",
                "analogia": "Como un boleto con código de barras: el lector verifica, no consulta una lista.",
            },
        ],
        "resultado": {
            "titulo": "Tu flujo JWT se verá así",
            "lenguaje": "http",
            "codigo": """POST /api/token  {"usuario":"ana","password":"secreta"}
HTTP/1.1 200 OK
{"access_token":"eyJhbGciOiJIUzI1NiIs...","token_type":"bearer"}

GET /api/perfil   Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
HTTP/1.1 200 OK
{"usuario":"ana"}

GET /api/perfil   Authorization: Bearer token_alterado
HTTP/1.1 401 Unauthorized""",
            "nota": "El token es visible: no es secreto. Lo que lo protege es la firma, no el ocultamiento.",
        },
        "reto": {
            "enunciado": "Implementa un endpoint de token y una ruta protegida que valide un JWT firmado.",
            "archivo": "app.py",
            "requisitos": [
                "El usuario de prueba es ana con contraseña secreta.",
                "POST /api/token valida usuario y contraseña y responde 200 con access_token y token_type.",
                "El token incluye el usuario y una expiración (exp).",
                "GET /api/perfil exige Authorization: Bearer y valida la firma.",
                "Un token alterado o vencido responde 401.",
                "La clave secreta no debe estar escrita en el código de producción: usa una variable de entorno.",
            ],
            "pista": "La firma se calcula con la clave secreta. Si cambias un solo carácter del token, la verificación falla y debes responder 401, no 500.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "El login emite un token",
                        "metodo": "POST",
                        "ruta": "/api/token",
                        "json": {"usuario": "ana", "password": "secreta"},
                        "estado": 200,
                        "json_contiene": {"token_type": "bearer"},
                        "guardar": {"token": "access_token"},
                    },
                    {
                        "descripcion": "El token válido abre el perfil",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "headers": {"Authorization": "Bearer {token}"},
                        "estado": 200,
                        "json_contiene": {"usuario": "ana"},
                    },
                    {
                        "descripcion": "Un token alterado es rechazado",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "headers": {"Authorization": "Bearer {token}x"},
                        "estado": 401,
                    },
                    {
                        "descripcion": "Sin token no hay acceso",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "estado": 401,
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {"ruta": "app.py", "regex": ["jwt|jose"], "descripcion": "Se usa una librería JWT"},
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion15.md` con un token decodificado (sin datos reales).",
    },
    16: {
        "pregunta": "¿Por qué el estándar OAuth2 usa un formulario y no JSON para el login?",
        "prerrequisitos": [
            "Sesión 15: JWT y rutas protegidas",
            "Saber qué es application/x-www-form-urlencoded",
        ],
        "objetivos": [
            "Implementar el Password Flow de OAuth2 con FastAPI.",
            "Enviar y validar el encabezado Authorization: Bearer.",
            "Responder 401 con el reto WWW-Authenticate correcto.",
        ],
        "conceptos": [
            {
                "termino": "OAuth2",
                "definicion": "Marco estándar para delegar acceso mediante tokens.",
                "analogia": "Como una credencial de visitante: el edificio no guarda tu contraseña, solo valida tu pase.",
            },
            {
                "termino": "Password Flow",
                "definicion": "Flujo en el que el usuario entrega credenciales una vez y recibe un token de acceso.",
                "analogia": "Como registrarte en la entrada y recibir un brazalete para todo el día.",
            },
            {
                "termino": "Formulario URL-encoded",
                "definicion": "Formato de cuerpo con pares clave=valor separados por &.",
                "analogia": "Como una ficha de papel con campos simples, no un sobre complejo.",
            },
            {
                "termino": "WWW-Authenticate",
                "definicion": "Encabezado que le dice al cliente qué esquema de autenticación debe usar.",
                "analogia": "Como un letrero en la puerta: «se requiere credencial Bearer».",
            },
        ],
        "resultado": {
            "titulo": "Tu OAuth2 Password Flow se verá así",
            "lenguaje": "http",
            "codigo": """POST /token
Content-Type: application/x-www-form-urlencoded
username=ana&password=secreta
HTTP/1.1 200 OK
{"access_token":"...","token_type":"bearer"}

GET /api/perfil   Authorization: Bearer ...
HTTP/1.1 200 OK
{"usuario":"ana"}

GET /api/perfil   (sin token)
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer""",
            "nota": "El formulario y el encabezado no son un capricho: son el contrato que esperan los clientes OAuth2.",
        },
        "reto": {
            "enunciado": "Implementa el Password Flow de OAuth2 con formulario y protege una ruta con OAuth2PasswordBearer.",
            "archivo": "app.py",
            "requisitos": [
                "El usuario de prueba es ana con contraseña secreta.",
                "POST /token recibe username y password como formulario, no como JSON.",
                "Responde 200 con access_token y token_type bearer.",
                "GET /api/perfil exige Authorization: Bearer y responde 200 con el usuario.",
                "Sin token responde 401 e incluye WWW-Authenticate: Bearer.",
                "Un esquema distinto de Bearer también responde 401.",
            ],
            "pista": "`OAuth2PasswordRequestForm` se encarga del formulario; `OAuth2PasswordBearer` se encarga del encabezado y del 401 con el reto correcto.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "El formulario de login emite token",
                        "metodo": "POST",
                        "ruta": "/token",
                        "data": {"username": "ana", "password": "secreta"},
                        "estado": 200,
                        "json_contiene": {"token_type": "bearer"},
                        "guardar": {"token": "access_token"},
                    },
                    {
                        "descripcion": "El token Bearer abre el perfil",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "headers": {"Authorization": "Bearer {token}"},
                        "estado": 200,
                        "json_contiene": {"usuario": "ana"},
                    },
                    {
                        "descripcion": "Sin token se responde 401 con WWW-Authenticate",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "estado": 401,
                        "headers_contiene": {"www-authenticate": "bearer"},
                    },
                    {
                        "descripcion": "Un esquema distinto se rechaza",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "headers": {"Authorization": "Basic YW5hOnNlY3JldGE="},
                        "estado": 401,
                    },
                ],
            },
            {
                "tipo": "archivos",
                "checks": [
                    {
                        "ruta": "app.py",
                        "regex": ["OAuth2PasswordBearer", "OAuth2PasswordRequestForm"],
                        "descripcion": "Se usa el flujo OAuth2 de FastAPI",
                    },
                ],
            },
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion16.md` con la diferencia entre el formulario y el encabezado.",
    },
    17: {
        "pregunta": "¿Qué diferencia hay entre no estar autenticado y no tener permiso?",
        "prerrequisitos": [
            "Sesión 16: OAuth2 y Bearer",
            "Saber qué es un rol",
        ],
        "objetivos": [
            "Incluir el rol dentro de los claims del token.",
            "Distinguir 401 (no autenticado) de 403 (sin permiso).",
            "Proteger una ruta administrativa con RBAC.",
        ],
        "conceptos": [
            {
                "termino": "Autenticación",
                "definicion": "Demostrar quién eres.",
                "analogia": "Como mostrar tu identificación en la entrada.",
            },
            {
                "termino": "Autorización",
                "definicion": "Decidir qué puedes hacer una vez que ya sabemos quién eres.",
                "analogia": "Como el pase de empleado que abre solo algunas puertas.",
            },
            {
                "termino": "Rol",
                "definicion": "Conjunto de permisos asociado a un tipo de usuario.",
                "analogia": "Como el puesto de trabajo: define a qué áreas tienes acceso.",
            },
            {
                "termino": "401 vs 403",
                "definicion": "401: no sé quién eres; 403: sé quién eres, pero no puedes pasar.",
                "analogia": "401: no traes credencial; 403: tu credencial no tiene este acceso.",
            },
        ],
        "resultado": {
            "titulo": "Tus respuestas de autorización se verán así",
            "lenguaje": "http",
            "codigo": """GET /api/admin/panel   Authorization: Bearer <token_admin>
HTTP/1.1 200 OK
{"panel":"admin"}

GET /api/admin/panel   Authorization: Bearer <token_user>
HTTP/1.1 403 Forbidden

GET /api/admin/panel   (sin token)
HTTP/1.1 401 Unauthorized

GET /api/perfil        Authorization: Bearer <token_user>
HTTP/1.1 200 OK
{"usuario":"ana","rol":"user"}""",
            "nota": "El 403 no es un error de credenciales: es una decisión de autorización.",
        },
        "reto": {
            "enunciado": "Implementa autenticación con roles: un usuario normal y un administrador. El panel administrativo solo debe abrirse para admin.",
            "archivo": "app.py",
            "requisitos": [
                "Usuarios de prueba: admin/admin123 (rol admin) y ana/secreta (rol user).",
                "El token incluye el rol del usuario en sus claims.",
                "GET /api/admin/panel responde 200 solo para rol admin.",
                "Un usuario autenticado con rol user recibe 403.",
                "Sin token se responde 401, no 403.",
                "GET /api/perfil funciona para cualquier usuario autenticado.",
            ],
            "pista": "Primero autentica (¿quién eres?) y después autoriza (¿tu rol alcanza?). Si devuelves 403 a quien no tiene token, estás mezclando las dos preguntas.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "El administrador obtiene su token",
                        "metodo": "POST",
                        "ruta": "/api/token",
                        "json": {"usuario": "admin", "password": "admin123"},
                        "estado": 200,
                        "guardar": {"token_admin": "access_token"},
                    },
                    {
                        "descripcion": "El usuario normal obtiene su token",
                        "metodo": "POST",
                        "ruta": "/api/token",
                        "json": {"usuario": "ana", "password": "secreta"},
                        "estado": 200,
                        "guardar": {"token_user": "access_token"},
                    },
                    {
                        "descripcion": "El admin entra al panel",
                        "metodo": "GET",
                        "ruta": "/api/admin/panel",
                        "headers": {"Authorization": "Bearer {token_admin}"},
                        "estado": 200,
                        "json_contiene": {"panel": "admin"},
                    },
                    {
                        "descripcion": "El usuario normal recibe 403",
                        "metodo": "GET",
                        "ruta": "/api/admin/panel",
                        "headers": {"Authorization": "Bearer {token_user}"},
                        "estado": 403,
                    },
                    {
                        "descripcion": "Sin token recibe 401",
                        "metodo": "GET",
                        "ruta": "/api/admin/panel",
                        "estado": 401,
                    },
                    {
                        "descripcion": "El perfil funciona para el usuario normal",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "headers": {"Authorization": "Bearer {token_user}"},
                        "estado": 200,
                        "json_contiene": {"usuario": "ana", "rol": "user"},
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion17.md` con la matriz rol → permiso.",
    },
    18: {
        "pregunta": "¿Cómo evitas que un script sature tu API?",
        "prerrequisitos": [
            "Sesión 17: autenticación y autorización",
            "Saber qué es una ventana de tiempo",
        ],
        "objetivos": [
            "Implementar un límite de peticiones por cliente.",
            "Responder 429 con Retry-After.",
            "Explicar la diferencia entre limitar y bloquear.",
        ],
        "conceptos": [
            {
                "termino": "Rate limiting",
                "definicion": "Limitar cuántas peticiones puede hacer un cliente en un periodo.",
                "analogia": "Como el turno de una taquilla: cierto número de fichas por hora.",
            },
            {
                "termino": "Ventana de tiempo",
                "definicion": "Periodo durante el cual se cuenta el consumo del cliente.",
                "analogia": "Como el reloj de un parquímetro: al reiniciarse, vuelves a tener cupo.",
            },
            {
                "termino": "HTTP 429",
                "definicion": "Demasiadas peticiones: el cliente debe esperar antes de reintentar.",
                "analogia": "Como el letrero «vuelva más tarde» de una oficina saturada.",
            },
            {
                "termino": "Retry-After",
                "definicion": "Encabezado que indica cuántos segundos esperar antes de reintentar.",
                "analogia": "Como el tiempo aproximado que te dan en la fila.",
            },
        ],
        "resultado": {
            "titulo": "Tu límite de peticiones se verá así",
            "lenguaje": "http",
            "codigo": """GET /api/recurso   -> 200 OK   (1.ª petición)
GET /api/recurso   -> 200 OK   (2.ª petición)
GET /api/recurso   -> 200 OK   (3.ª petición)
GET /api/recurso   -> 429 Too Many Requests
Retry-After: 60
{"error":"límite de peticiones alcanzado"}""",
            "nota": "El límite protege el servicio para todos; no es un castigo al cliente.",
        },
        "reto": {
            "enunciado": "Implementa un límite de tres peticiones por minuto por cliente y responde 429 cuando se exceda.",
            "archivo": "app.py",
            "requisitos": [
                "GET /api/recurso permite tres peticiones por cliente en una ventana de 60 segundos.",
                "La cuarta petición responde 429.",
                "La respuesta 429 incluye Retry-After.",
                "Las tres primeras responden 200 con un JSON simple.",
                "El contador se reinicia al iniciar la aplicación.",
            ],
            "pista": "El cliente se identifica por IP o por token. Un contador global castiga a todos; un contador por cliente protege a todos.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {"descripcion": "Primera petición permitida", "metodo": "GET", "ruta": "/api/recurso", "estado": 200},
                    {"descripcion": "Segunda petición permitida", "metodo": "GET", "ruta": "/api/recurso", "estado": 200},
                    {"descripcion": "Tercera petición permitida", "metodo": "GET", "ruta": "/api/recurso", "estado": 200},
                    {
                        "descripcion": "La cuarta petición se limita",
                        "metodo": "GET",
                        "ruta": "/api/recurso",
                        "estado": 429,
                        "headers_contiene": {"retry-after": ""},
                        "json_contiene": {"error": "límite de peticiones alcanzado"},
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion18.md` con el cálculo de la ventana.",
    },
    19: {
        "pregunta": "¿Qué haces con el HTML que llega del usuario?",
        "prerrequisitos": [
            "Sesión 18: rate limiting",
            "Saber qué es un script y cómo se ejecuta en el navegador",
        ],
        "objetivos": [
            "Escapar HTML antes de guardar o devolver texto.",
            "Explicar por qué la validación de entrada no sustituye al escape de salida.",
            "Probar payloads de XSS y verificar que no se ejecutan.",
        ],
        "conceptos": [
            {
                "termino": "XSS",
                "definicion": "Inyección de script que se ejecuta en el navegador de otro usuario.",
                "analogia": "Como dejar una nota con una orden escondida en un tablero público.",
            },
            {
                "termino": "Escape",
                "definicion": "Convertir caracteres especiales en texto seguro: < se vuelve &lt;.",
                "analogia": "Como poner comillas alrededor de una frase para que no se confunda con una orden.",
            },
            {
                "termino": "Sanitización",
                "definicion": "Limpiar o neutralizar el contenido antes de almacenarlo o mostrarlo.",
                "analogia": "Como desinfectar el agua antes de beberla.",
            },
            {
                "termino": "Contexto de salida",
                "definicion": "El lugar donde se inserta el dato (HTML, atributo, JavaScript, URL) determina cómo escaparlo.",
                "analogia": "Como usar el idioma correcto según el país donde estás.",
            },
        ],
        "resultado": {
            "titulo": "Tu API neutralizará el HTML peligroso",
            "lenguaje": "http",
            "codigo": """POST /api/comentarios  {"texto":"<script>alert(1)</script>"}
HTTP/1.1 201 Created
{"id":1,"texto":"&lt;script&gt;alert(1)&lt;/script&gt;"}

GET /api/comentarios
HTTP/1.1 200 OK
{"comentarios":[{"id":1,"texto":"&lt;script&gt;alert(1)&lt;/script&gt;"}]}

En el cuerpo nunca aparece <script> sin escapar.""",
            "nota": "Guardar texto escapado es una decisión; escapar al mostrar es otra. En esta sesión hacemos ambas para que el resultado sea seguro.",
        },
        "reto": {
            "enunciado": "Implementa un endpoint de comentarios que neutralice el HTML peligroso y devuelva el texto seguro.",
            "archivo": "app.py",
            "requisitos": [
                "POST /api/comentarios recibe un texto y responde 201 con el comentario creado.",
                "El texto se escapa antes de guardarse o devolverse.",
                "GET /api/comentarios devuelve los comentarios sin etiquetas ejecutables.",
                "Un comentario normal no se altera.",
                "La respuesta nunca contiene la cadena <script>.",
            ],
            "pista": "En Python, `html.escape` convierte `<`, `>` y `&` en entidades. Escapar no es lo mismo que eliminar: el usuario ve el texto, el navegador no lo ejecuta.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "Un comentario normal se guarda",
                        "metodo": "POST",
                        "ruta": "/api/comentarios",
                        "json": {"texto": "Muy bueno"},
                        "estado": 201,
                        "json_contiene": {"id": 1, "texto": "Muy bueno"},
                    },
                    {
                        "descripcion": "El script se neutraliza",
                        "metodo": "POST",
                        "ruta": "/api/comentarios",
                        "json": {"texto": "<script>alert(1)</script>"},
                        "estado": 201,
                        "cuerpo_contiene": ["&lt;script&gt;"],
                        "no_contiene": ["<script>"],
                    },
                    {
                        "descripcion": "El listado tampoco devuelve scripts",
                        "metodo": "GET",
                        "ruta": "/api/comentarios",
                        "estado": 200,
                        "cuerpo_contiene": ["&lt;script&gt;"],
                        "no_contiene": ["<script>"],
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion19.md` con el payload de prueba y el resultado seguro.",
    },
    20: {
        "pregunta": "¿La seguridad de tu API resiste una auditoría?",
        "prerrequisitos": [
            "Sesiones 11 a 19: capas, DI, sesiones, hashing, JWT, OAuth2, RBAC, rate limiting y sanitización",
            "Tu API del Hito 1 como base",
        ],
        "objetivos": [
            "Integrar registro, login, token, perfil y panel administrativo.",
            "Verificar 401, 403 y 200 en el mismo flujo.",
            "Demostrar que las contraseñas nunca se filtran.",
        ],
        "conceptos": [
            {
                "termino": "Pipeline de autenticación",
                "definicion": "Secuencia registro → login → token → ruta protegida.",
                "analogia": "Como el recorrido de un aeropuerto: documentación, control, sala y abordaje.",
            },
            {
                "termino": "RBAC",
                "definicion": "Control de acceso basado en roles.",
                "analogia": "Como las llaves de un edificio según el puesto de trabajo.",
            },
            {
                "termino": "Prueba de intrusión",
                "definicion": "Intento controlado de acceder sin credenciales o con privilegios insuficientes.",
                "analogia": "Como un simulacro de incendio: se prueba la reacción sin provocar el incendio.",
            },
            {
                "termino": "Hito",
                "definicion": "Entrega que demuestra el dominio de un bloque completo.",
                "analogia": "Como un examen integrador: no basta un tema aislado.",
            },
        ],
        "resultado": {
            "titulo": "Tu Hito 2 completo se verá así",
            "lenguaje": "http",
            "codigo": """POST /api/registro   {"usuario":"ana","password":"secreta"}  -> 201
POST /api/token      {"usuario":"ana","password":"secreta"}  -> 200 + token
GET  /api/perfil     Bearer <token_user>                     -> 200
GET  /api/admin/panel Bearer <token_user>                    -> 403
POST /api/token      {"usuario":"admin","password":"admin123"} -> 200 + token
GET  /api/admin/panel Bearer <token_admin>                   -> 200
GET  /api/perfil     sin token                               -> 401

RESUMEN: 7/7 casos correctos. ¡Hito 2 listo!""",
            "nota": "La seguridad no es una capa al final: es una propiedad de todo el flujo.",
        },
        "reto": {
            "enunciado": "Integra el pipeline de seguridad completo del Bloque 2 en una API de libros con usuarios, roles y rutas protegidas.",
            "archivo": "app.py",
            "requisitos": [
                "El administrador precargado es admin/admin123; el usuario ana se registra en el flujo.",
                "Registro de usuarios con contraseña hasheada (nunca en texto plano).",
                "Login que emite un JWT con el rol del usuario.",
                "Perfil protegido con Bearer para cualquier usuario autenticado.",
                "Panel administrativo solo para rol admin; usuario normal recibe 403.",
                "Sin token se responde 401 y las contraseñas nunca aparecen en las respuestas.",
            ],
            "pista": "Ordena el flujo como lo vive el cliente: registro, login, token, perfil, panel. Cada paso debe poder probarse de forma independiente.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "Registro sin filtrar contraseñas",
                        "metodo": "POST",
                        "ruta": "/api/registro",
                        "json": {"usuario": "ana", "password": "secreta"},
                        "estado": 201,
                        "no_contiene": ["password", "hash"],
                    },
                    {
                        "descripcion": "Login del usuario registrado",
                        "metodo": "POST",
                        "ruta": "/api/token",
                        "json": {"usuario": "ana", "password": "secreta"},
                        "estado": 200,
                        "guardar": {"token_user": "access_token"},
                    },
                    {
                        "descripcion": "El usuario accede a su perfil",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "headers": {"Authorization": "Bearer {token_user}"},
                        "estado": 200,
                        "json_contiene": {"usuario": "ana"},
                    },
                    {
                        "descripcion": "El usuario no entra al panel admin",
                        "metodo": "GET",
                        "ruta": "/api/admin/panel",
                        "headers": {"Authorization": "Bearer {token_user}"},
                        "estado": 403,
                    },
                    {
                        "descripcion": "El administrador obtiene su token",
                        "metodo": "POST",
                        "ruta": "/api/token",
                        "json": {"usuario": "admin", "password": "admin123"},
                        "estado": 200,
                        "guardar": {"token_admin": "access_token"},
                    },
                    {
                        "descripcion": "El administrador entra al panel",
                        "metodo": "GET",
                        "ruta": "/api/admin/panel",
                        "headers": {"Authorization": "Bearer {token_admin}"},
                        "estado": 200,
                    },
                    {
                        "descripcion": "Sin token no hay acceso",
                        "metodo": "GET",
                        "ruta": "/api/perfil",
                        "estado": 401,
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde, bitácora `auditorias/auditoria_sesion20.md` y tag `v0.2-hito2` en tu repositorio.",
    },
}
