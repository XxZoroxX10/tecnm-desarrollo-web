"""
Contenido enriquecido del Bloque 1 (sesiones 01 a 10).

Cada sesión declara lo que el estudiante verá en la presentación y el
resultado exacto que debe alcanzar en el laboratorio. El laboratorio no se
divide en pasos: se declara el resultado y el estudiante decide cómo llegar.
"""

BLOQUE_1 = {
    1: {
        "pregunta": "¿Qué ocurre exactamente entre que escribes una URL y ves una respuesta?",
        "prerrequisitos": [
            "Cuenta de GitHub y navegador actualizado",
            "Ninguna instalación local: todo se ejecuta en Google Colab",
        ],
        "objetivos": [
            "Identificar las partes de una petición y de una respuesta HTTP.",
            "Ejecutar un servidor FastAPI dentro de Google Colab.",
            "Verificar con código el estado, los encabezados y el cuerpo de una respuesta.",
        ],
        "conceptos": [
            {
                "termino": "Cliente y servidor",
                "definicion": "El cliente envía una petición; el servidor la procesa y devuelve una respuesta.",
                "analogia": "Como en un restaurante: tú pides y la cocina responde con un platillo.",
            },
            {
                "termino": "Petición HTTP",
                "definicion": "Mensaje con un método, una ruta, encabezados y un cuerpo opcional.",
                "analogia": "Como un sobre: lleva destinatario, instrucciones y contenido.",
            },
            {
                "termino": "Respuesta HTTP",
                "definicion": "Mensaje con un código de estado, encabezados y un cuerpo opcional.",
                "analogia": "Como un recibo: te dice si salió bien (200) o qué falló (404).",
            },
            {
                "termino": "JSON",
                "definicion": "Formato de texto con pares clave-valor que humanos y máquinas pueden leer.",
                "analogia": "Como una ficha de datos con etiquetas: nombre, precio, disponible.",
            },
        ],
        "resultado": {
            "titulo": "Tu servidor responderá exactamente así",
            "lenguaje": "http",
            "codigo": """$ curl http://127.0.0.1:8000/api/estado
HTTP/1.1 200 OK
content-type: application/json

{"servidor":"ok","curso":"DAB-2201"}

$ curl -X POST http://127.0.0.1:8000/api/eco \\
       -H "Content-Type: application/json" \\
       -d '{"mensaje":"hola"}'
HTTP/1.1 200 OK
content-type: application/json

{"mensaje":"hola","recibido":true}

$ curl -X POST http://127.0.0.1:8000/api/eco \\
       -H "Content-Type: application/json" \\
       -d '{'
HTTP/1.1 422 Unprocessable Entity""",
            "nota": "Si el JSON está mal formado, tu API no debe caerse: debe responder 422.",
        },
        "reto": {
            "enunciado": "Construye una API mínima que demuestre que el servidor recibe y responde JSON. Debe tener una ruta de estado y una ruta de eco.",
            "archivo": "app.py",
            "requisitos": [
                "GET /api/estado devuelve {\"servidor\": \"ok\", \"curso\": \"DAB-2201\"} con HTTP 200.",
                "POST /api/eco recibe un JSON con la clave mensaje y devuelve {\"mensaje\": <mensaje>, \"recibido\": true} con HTTP 200.",
                "Un JSON mal formado debe producir HTTP 422, no un error 500.",
            ],
            "pista": "FastAPI valida el cuerpo con un modelo de Pydantic antes de entrar a tu función. Tú decides el modelo; la validación es el resultado.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "El servidor está vivo y responde JSON",
                        "metodo": "GET",
                        "ruta": "/api/estado",
                        "estado": 200,
                        "json_contiene": {"servidor": "ok", "curso": "DAB-2201"},
                    },
                    {
                        "descripcion": "El eco devuelve el mensaje recibido",
                        "metodo": "POST",
                        "ruta": "/api/eco",
                        "json": {"mensaje": "hola"},
                        "estado": 200,
                        "json_exacto": {"mensaje": "hola", "recibido": True},
                    },
                    {
                        "descripcion": "Un JSON roto no tumba el servidor",
                        "metodo": "POST",
                        "ruta": "/api/eco",
                        "content": "{",
                        "headers": {"Content-Type": "application/json"},
                        "estado": 422,
                    },
                    {
                        "descripcion": "El método incorrecto se rechaza con 405",
                        "metodo": "GET",
                        "ruta": "/api/eco",
                        "estado": 405,
                    },
                ],
            }
        ],
        "entrega": "Fork del repositorio con tu nombre y matrícula en el README, más la bitácora `auditorias/auditoria_sesion01.md`.",
    },
    2: {
        "pregunta": "¿Por qué no basta con usar POST para todo?",
        "prerrequisitos": [
            "Sesión 01: un servidor FastAPI y respuestas JSON",
            "Saber qué es una ruta (endpoint)",
        ],
        "objetivos": [
            "Distinguir el significado de GET, POST, PUT, PATCH y DELETE.",
            "Implementar un CRUD mínimo sobre una colección de libros.",
            "Verificar la diferencia entre 404 (no existe) y 405 (método no permitido).",
        ],
        "conceptos": [
            {
                "termino": "Recurso",
                "definicion": "Cualquier cosa que la API expone y que se puede nombrar: un libro, un usuario, un préstamo.",
                "analogia": "Como un expediente dentro de un archivador.",
            },
            {
                "termino": "Verbo HTTP",
                "definicion": "La acción que el cliente quiere ejecutar sobre el recurso.",
                "analogia": "Como las instrucciones de una ficha: leerla, crearla, reemplazarla o borrarla.",
            },
            {
                "termino": "Idempotencia",
                "definicion": "Propiedad por la que repetir la misma petición produce el mismo estado final.",
                "analogia": "Como pulsar varias veces el botón del ascensor: el ascensor llega una sola vez.",
            },
            {
                "termino": "HTTP 405",
                "definicion": "La ruta existe, pero el verbo utilizado no está permitido en ella.",
                "analogia": "La puerta existe, pero tu llave no abre esa cerradura.",
            },
        ],
        "resultado": {
            "titulo": "Tu CRUD de libros responderá exactamente así",
            "lenguaje": "http",
            "codigo": """$ curl -X POST http://127.0.0.1:8000/api/libros \\
       -H "Content-Type: application/json" \\
       -d '{"titulo":"Cien años de soledad","anio":1967}'
HTTP/1.1 201 Created
{"id":1,"titulo":"Cien años de soledad","anio":1967}

$ curl http://127.0.0.1:8000/api/libros
HTTP/1.1 200 OK
{"libros":[{"id":1,"titulo":"Cien años de soledad","anio":1967}]}

$ curl -X PUT http://127.0.0.1:8000/api/libros/1 \\
       -H "Content-Type: application/json" \\
       -d '{"titulo":"Cien años de soledad (edición conmemorativa)","anio":1967}'
HTTP/1.1 200 OK
{"id":1,"titulo":"Cien años de soledad (edición conmemorativa)","anio":1967}

$ curl -X DELETE http://127.0.0.1:8000/api/libros/1
HTTP/1.1 204 No Content""",
            "nota": "La colección se guarda en memoria: no necesitas base de datos todavía.",
        },
        "reto": {
            "enunciado": "Implementa un CRUD completo de libros en memoria. La colección empieza vacía y cada operación debe devolver el código HTTP que le corresponde.",
            "archivo": "app.py",
            "requisitos": [
                "GET /api/libros responde 200 con {\"libros\": [...]}.",
                "POST /api/libros responde 201 con el libro creado y un id asignado por el servidor.",
                "GET /api/libros/{id} responde 200 con el libro o 404 si no existe.",
                "PUT /api/libros/{id} reemplaza el libro y responde 200; DELETE responde 204 sin cuerpo.",
                "Un verbo no implementado sobre una ruta existente debe responder 405, no 404.",
            ],
            "pista": "En FastAPI, si defines GET/PUT/DELETE para `/api/libros/{id}` pero no PATCH, el framework responde 405 automáticamente. No programes ese caso: deja que el contrato hable.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "La colección inicia vacía",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": []},
                    },
                    {
                        "descripcion": "POST crea el libro con id 1",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Cien años de soledad", "anio": 1967},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Cien años de soledad", "anio": 1967},
                    },
                    {
                        "descripcion": "GET lista el libro creado",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {
                            "libros": [
                                {"id": 1, "titulo": "Cien años de soledad", "anio": 1967}
                            ]
                        },
                    },
                    {
                        "descripcion": "GET por id encuentra el libro",
                        "metodo": "GET",
                        "ruta": "/api/libros/1",
                        "estado": 200,
                        "json_contiene": {"id": 1, "titulo": "Cien años de soledad"},
                    },
                    {
                        "descripcion": "PUT reemplaza el libro",
                        "metodo": "PUT",
                        "ruta": "/api/libros/1",
                        "json": {"titulo": "Cien años de soledad (edición conmemorativa)", "anio": 1967},
                        "estado": 200,
                        "json_contiene": {"id": 1, "titulo": "Cien años de soledad (edición conmemorativa)"},
                    },
                    {
                        "descripcion": "DELETE elimina el libro",
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
                    {
                        "descripcion": "PATCH no está implementado: 405, no 404",
                        "metodo": "PATCH",
                        "ruta": "/api/libros/1",
                        "estado": 405,
                    },
                ],
            }
        ],
        "entrega": "Cuaderno ejecutado de principio a fin y bitácora `auditorias/auditoria_sesion02.md`.",
    },
    3: {
        "pregunta": "¿Cómo sabe el servidor qué formato le estás enviando?",
        "prerrequisitos": [
            "Sesión 02: CRUD de libros y códigos HTTP",
            "Saber que un cuerpo HTTP viaja como bytes",
        ],
        "objetivos": [
            "Leer y emitir encabezados HTTP correctamente.",
            "Diferenciar Content-Type (lo que envío) de Accept (lo que acepto).",
            "Rechazar formatos no soportados con 415 y 406.",
        ],
        "conceptos": [
            {
                "termino": "Encabezado (header)",
                "definicion": "Metadato que acompaña a la petición o a la respuesta sin formar parte del cuerpo.",
                "analogia": "Como la etiqueta de un paquete: dice qué lleva y cómo tratarlo.",
            },
            {
                "termino": "Content-Type",
                "definicion": "Indica el formato del cuerpo que se está enviando, por ejemplo application/json.",
                "analogia": "Como decir «este sobre contiene una fotografía, no una carta».",
            },
            {
                "termino": "Accept",
                "definicion": "Indica qué formatos de respuesta puede entender el cliente.",
                "analogia": "Como pedir el menú en español porque no lees inglés.",
            },
            {
                "termino": "HTTP 415 / 406",
                "definicion": "415 significa formato de entrada no soportado; 406, que no puedes producir el formato solicitado.",
                "analogia": "415: no sé abrir ese tipo de archivo. 406: no tengo ese formato disponible.",
            },
        ],
        "resultado": {
            "titulo": "Tu API negociará el formato exactamente así",
            "lenguaje": "http",
            "codigo": """$ curl -X POST http://127.0.0.1:8000/api/libros \\
       -H "Content-Type: application/json" \\
       -H "Accept: application/json" \\
       -d '{"titulo":"Rayuela","anio":1963}'
HTTP/1.1 201 Created
content-type: application/json
{"id":1,"titulo":"Rayuela","anio":1963}

$ curl -X POST http://127.0.0.1:8000/api/libros \\
       -H "Content-Type: text/plain" \\
       -d 'Rayuela'
HTTP/1.1 415 Unsupported Media Type

$ curl http://127.0.0.1:8000/api/libros \\
       -H "Accept: application/xml"
HTTP/1.1 406 Not Acceptable""",
            "nota": "El navegador envía Accept por ti; una herramienta como curl te obliga a ser explícito.",
        },
        "reto": {
            "enunciado": "Implementa la creación y el listado de libros, pero haz que la API negocie el formato de entrada y de salida.",
            "archivo": "app.py",
            "requisitos": [
                "POST /api/libros solo acepta Content-Type: application/json; si no, responde 415.",
                "GET /api/libros solo responde si el cliente acepta application/json; si pide XML, responde 406.",
                "Las respuestas correctas llevan Content-Type: application/json.",
                "Un POST válido responde 201 con el libro creado.",
            ],
            "pista": "Puedes inspeccionar `request.headers` dentro de una dependencia o middleware antes de que se procese el cuerpo. El formato no se adivina: se declara.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "POST válido en JSON",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "headers": {"Content-Type": "application/json", "Accept": "application/json"},
                        "json": {"titulo": "Rayuela", "anio": 1963},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Rayuela", "anio": 1963},
                        "headers_contiene": {"content-type": "application/json"},
                    },
                    {
                        "descripcion": "POST en texto plano se rechaza con 415",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "content": "Rayuela",
                        "headers": {"Content-Type": "text/plain"},
                        "estado": 415,
                    },
                    {
                        "descripcion": "GET que pide XML se rechaza con 406",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "headers": {"Accept": "application/xml"},
                        "estado": 406,
                    },
                    {
                        "descripcion": "GET que acepta JSON responde 200",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "headers": {"Accept": "application/json"},
                        "estado": 200,
                        "headers_contiene": {"content-type": "application/json"},
                    },
                ],
            }
        ],
        "entrega": "Cuaderno con los cuatro casos en verde y bitácora `auditorias/auditoria_sesion03.md`.",
    },
    4: {
        "pregunta": "¿La URL debe describir una acción o un recurso?",
        "prerrequisitos": [
            "Sesión 03: encabezados y negociación de contenido",
            "Saber qué es una ruta con parámetros",
        ],
        "objetivos": [
            "Diseñar URIs jerárquicas basadas en sustantivos.",
            "Elegir entre parámetros de ruta y parámetros de consulta.",
            "Responder 404 cuando el recurso solicitado no existe.",
        ],
        "conceptos": [
            {
                "termino": "URI",
                "definicion": "Identificador único de un recurso dentro de la API.",
                "analogia": "Como la dirección de una casa: no dice qué hacer allí, solo dónde está.",
            },
            {
                "termino": "Parámetro de ruta",
                "definicion": "Parte de la URI que identifica un recurso concreto, por ejemplo /libros/7.",
                "analogia": "Como el número de expediente: identifica exactamente un documento.",
            },
            {
                "termino": "Parámetro de consulta",
                "definicion": "Filtro opcional después de ?, por ejemplo /libros?genero=novela.",
                "analogia": "Como los filtros de una búsqueda: no cambian el recurso, acotan la lista.",
            },
            {
                "termino": "Colección y recurso",
                "definicion": "Una colección es /libros; un recurso concreto es /libros/7.",
                "analogia": "Como el estante completo frente a un libro específico.",
            },
        ],
        "resultado": {
            "titulo": "Tu jerarquía de recursos responderá así",
            "lenguaje": "http",
            "codigo": """$ curl "http://127.0.0.1:8000/api/autores/1/libros"
HTTP/1.1 200 OK
{"autor_id":1,"libros":[
  {"id":1,"titulo":"Cien años de soledad","genero":"novela"},
  {"id":2,"titulo":"Doce cuentos peregrinos","genero":"cuento"}
]}

$ curl "http://127.0.0.1:8000/api/autores/1/libros?genero=cuento&limite=1"
HTTP/1.1 200 OK
{"autor_id":1,"libros":[
  {"id":2,"titulo":"Doce cuentos peregrinos","genero":"cuento"}
]}

$ curl "http://127.0.0.1:8000/api/autores/99/libros"
HTTP/1.1 404 Not Found
{"detail":"Autor no encontrado"}""",
            "nota": "La ruta dice qué recurso; el verbo dice qué hacer. Nunca /obtenerLibros.",
        },
        "reto": {
            "enunciado": "Diseña una API de autores y libros donde las rutas nombren recursos, no acciones.",
            "archivo": "app.py",
            "requisitos": [
                "GET /api/autores/{autor_id}/libros responde 200 con los libros del autor.",
                "El parámetro opcional `genero` filtra por género y `limite` recorta la lista.",
                "GET /api/autores/99/libros responde 404 si el autor no existe.",
                "No incluyas verbos en las rutas: la acción la define el método HTTP.",
                "Siembra exactamente: autor 1 Gabriel García Márquez con «Cien años de soledad» (novela) y «Doce cuentos peregrinos» (cuento); autor 2 Julio Cortázar con «Rayuela» (novela).",
            ],
            "pista": "Un parámetro de ruta identifica; un parámetro de consulta filtra. Si tu ruta responde «lo mismo pero más pequeño», probablemente es un filtro y va después del signo de interrogación.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "Libros del autor 1",
                        "metodo": "GET",
                        "ruta": "/api/autores/1/libros",
                        "estado": 200,
                        "json_contiene": {
                            "autor_id": 1,
                            "libros": [
                                {"id": 1, "titulo": "Cien años de soledad", "genero": "novela"},
                                {"id": 2, "titulo": "Doce cuentos peregrinos", "genero": "cuento"},
                            ],
                        },
                    },
                    {
                        "descripcion": "Filtro por género y límite",
                        "metodo": "GET",
                        "ruta": "/api/autores/1/libros?genero=cuento&limite=1",
                        "estado": 200,
                        "json_contiene": {
                            "autor_id": 1,
                            "libros": [
                                {"id": 2, "titulo": "Doce cuentos peregrinos", "genero": "cuento"}
                            ],
                        },
                    },
                    {
                        "descripcion": "Un autor inexistente produce 404",
                        "metodo": "GET",
                        "ruta": "/api/autores/99/libros",
                        "estado": 404,
                    },
                    {
                        "descripcion": "La colección completa de libros",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1}, {"id": 2}, {"id": 3}]},
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion04.md` con tu decisión de diseño de URIs.",
    },
    5: {
        "pregunta": "¿Qué pasa si el JSON no trae el tipo de dato que esperas?",
        "prerrequisitos": [
            "Sesión 04: rutas y parámetros",
            "Saber qué es un tipo de dato (str, int, float, bool)",
        ],
        "objetivos": [
            "Definir un DTO con Pydantic v2.",
            "Explicar la coerción de tipos y el error 422.",
            "Separar el modelo de entrada del modelo de salida.",
        ],
        "conceptos": [
            {
                "termino": "DTO",
                "definicion": "Objeto que define exactamente qué datos entran o salen de la API.",
                "analogia": "Como el formulario de una ventanilla: solo acepta los campos impresos.",
            },
            {
                "termino": "Validación",
                "definicion": "Comprobar que los datos cumplen el tipo y las reglas antes de usarlos.",
                "analogia": "Como el filtro de seguridad de un aeropuerto: nada pasa sin revisión.",
            },
            {
                "termino": "Coerción",
                "definicion": "Conversión controlada de un tipo a otro, por ejemplo \"1967\" a 1967.",
                "analogia": "Como traducir una fecha escrita con letras a formato numérico.",
            },
            {
                "termino": "HTTP 422",
                "definicion": "La petición está bien formada, pero los datos no cumplen el esquema.",
                "analogia": "El formulario llegó completo, pero un campo tiene un valor inválido.",
            },
        ],
        "resultado": {
            "titulo": "Tu DTO aceptará y rechazará exactamente esto",
            "lenguaje": "http",
            "codigo": """$ curl -X POST http://127.0.0.1:8000/api/libros \\
       -H "Content-Type: application/json" \\
       -d '{"titulo":"Rayuela","anio":"1963","precio":250.5,"disponible":true}'
HTTP/1.1 201 Created
{"id":1,"titulo":"Rayuela","anio":1963,"precio":250.5,"disponible":true}

$ curl -X POST http://127.0.0.1:8000/api/libros \\
       -H "Content-Type: application/json" \\
       -d '{"titulo":"Rayuela","anio":"mil novecientos"}'
HTTP/1.1 422 Unprocessable Entity

$ curl -X POST http://127.0.0.1:8000/api/libros \\
       -H "Content-Type: application/json" \\
       -d '{"titulo":"Rayuela","anio":1963,"color":"rojo"}'
HTTP/1.1 422 Unprocessable Entity""",
            "nota": "El campo extra también se rechaza: el contrato es estricto, no tolerante.",
        },
        "reto": {
            "enunciado": "Define el contrato de un libro con un DTO de entrada y otro de salida. El servidor decide qué es válido antes de guardar.",
            "archivo": "app.py",
            "requisitos": [
                "El modelo de entrada exige titulo (str), anio (int), precio (float) y disponible (bool).",
                "La coerción de \"1967\" a 1967 debe funcionar; \"mil novecientos\" debe fallar con 422.",
                "Los campos desconocidos se rechazan con 422 (extra=\"forbid\").",
                "La respuesta nunca inventa campos: devuelve el id y los datos del libro.",
            ],
            "pista": "En Pydantic v2, `model_config = ConfigDict(extra=\"forbid\")` convierte el DTO en un contrato cerrado.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "Un libro válido se crea con 201",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963, "precio": 250.5, "disponible": True},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Rayuela", "anio": 1963, "precio": 250.5, "disponible": True},
                    },
                    {
                        "descripcion": "La cadena numérica se convierte a entero",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "La casa verde", "anio": "1966", "precio": 180, "disponible": False},
                        "estado": 201,
                        "json_contiene": {"id": 2, "anio": 1966},
                    },
                    {
                        "descripcion": "Un año no numérico produce 422",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": "mil novecientos", "precio": 250.5, "disponible": True},
                        "estado": 422,
                    },
                    {
                        "descripcion": "Un campo extra produce 422",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963, "precio": 250.5, "disponible": True, "color": "rojo"},
                        "estado": 422,
                    },
                    {
                        "descripcion": "El listado devuelve los libros creados",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": [{"id": 1}, {"id": 2}]},
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion05.md` con tu DTO de entrada y salida.",
    },
    6: {
        "pregunta": "¿Dónde pones los límites: en el cliente o en el servidor?",
        "prerrequisitos": [
            "Sesión 05: DTO y validación de tipos",
            "Saber qué es un rango numérico y una longitud de texto",
        ],
        "objetivos": [
            "Aplicar restricciones de negocio con Field y Query.",
            "Explicar por qué el servidor no puede confiar en el cliente.",
            "Verificar errores 422 por rangos, longitudes y valores negativos.",
        ],
        "conceptos": [
            {
                "termino": "Restricción (constraint)",
                "definicion": "Regla que un dato debe cumplir para ser aceptado: mínimo, máximo, longitud o patrón.",
                "analogia": "Como las reglas de un formulario: edad mínima, código postal de cinco dígitos.",
            },
            {
                "termino": "Validación de entrada",
                "definicion": "Rechazar datos inválidos en el borde de la API, antes de la lógica de negocio.",
                "analogia": "Como el portero de un club: revisa la identificación antes de dejar pasar.",
            },
            {
                "termino": "Query parameter",
                "definicion": "Valor opcional en la URL que filtra o pagina una colección.",
                "analogia": "Como los filtros de una tienda en línea: talla, color, precio.",
            },
            {
                "termino": "Error de validación",
                "definicion": "Respuesta 422 que explica qué campo no cumplió la regla.",
                "analogia": "Como la nota del profesor: «el año debe estar entre 1450 y 2100».",
            },
        ],
        "resultado": {
            "titulo": "Tus límites de negocio responderán así",
            "lenguaje": "http",
            "codigo": """$ curl -X POST http://127.0.0.1:8000/api/libros \\
       -H "Content-Type: application/json" \\
       -d '{"titulo":"Rayuela","anio":1963,"precio":250.5}'
HTTP/1.1 201 Created
{"id":1,"titulo":"Rayuela","anio":1963,"precio":250.5}

$ curl -X POST http://127.0.0.1:8000/api/libros \\
       -H "Content-Type: application/json" \\
       -d '{"titulo":"Ya","anio":1200,"precio":-5}'
HTTP/1.1 422 Unprocessable Entity

$ curl "http://127.0.0.1:8000/api/libros?limite=0"
HTTP/1.1 422 Unprocessable Entity""",
            "nota": "Un título de dos letras, un año de 1200 y un precio negativo son datos, no errores del servidor.",
        },
        "reto": {
            "enunciado": "Implementa el contrato de libros con reglas de negocio explícitas y un listado paginado.",
            "archivo": "app.py",
            "requisitos": [
                "titulo: entre 3 y 80 caracteres.",
                "anio: entre 1450 y 2100.",
                "precio: mayor que 0.",
                "El parámetro `limite` de GET /api/libros acepta entre 1 y 100.",
                "Los datos inválidos producen 422; los válidos, 201.",
            ],
            "pista": "`Field(min_length=3, max_length=80, ge=1450, le=2100, gt=0)` describe el resultado esperado directamente en el DTO. La lógica de validación no se repite en cada endpoint.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "Un libro dentro de los límites se crea",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963, "precio": 250.5},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Rayuela", "anio": 1963},
                    },
                    {
                        "descripcion": "Un título demasiado corto produce 422",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Ya", "anio": 1963, "precio": 250.5},
                        "estado": 422,
                    },
                    {
                        "descripcion": "Un año fuera de rango produce 422",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1200, "precio": 250.5},
                        "estado": 422,
                    },
                    {
                        "descripcion": "Un precio no positivo produce 422",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963, "precio": 0},
                        "estado": 422,
                    },
                    {
                        "descripcion": "El límite de paginación debe ser al menos 1",
                        "metodo": "GET",
                        "ruta": "/api/libros?limite=0",
                        "estado": 422,
                    },
                    {
                        "descripcion": "Un límite válido responde 200",
                        "metodo": "GET",
                        "ruta": "/api/libros?limite=5",
                        "estado": 200,
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion06.md` con la tabla de restricciones.",
    },
    7: {
        "pregunta": "¿Cómo puede un cliente saber qué endpoints existen sin leer tu código?",
        "prerrequisitos": [
            "Sesión 06: validación estricta",
            "Saber qué es un contrato de API",
        ],
        "objetivos": [
            "Publicar una especificación OpenAPI viva.",
            "Documentar endpoints, modelos y códigos de respuesta.",
            "Verificar que Swagger UI y ReDoc consumen esa especificación.",
        ],
        "conceptos": [
            {
                "termino": "OpenAPI",
                "definicion": "Estándar en JSON o YAML que describe rutas, parámetros, respuestas y modelos de una API.",
                "analogia": "Como el manual de instrucciones de un electrodoméstico: dice qué botones existen y qué hacen.",
            },
            {
                "termino": "Swagger UI",
                "definicion": "Interfaz web que lee la especificación OpenAPI y permite probar los endpoints.",
                "analogia": "Como un tablero de pruebas con botones para cada operación.",
            },
            {
                "termino": "Esquema (schema)",
                "definicion": "Definición de la forma de un dato: campos, tipos y obligatoriedad.",
                "analogia": "Como el molde de una pieza: todo lo que salga debe encajar.",
            },
            {
                "termino": "Contrato de API",
                "definicion": "Acuerdo explícito entre quien consume y quien provee el servicio.",
                "analogia": "Como un contrato de obra: si cambia una cláusula, ambas partes deben enterarse.",
            },
        ],
        "resultado": {
            "titulo": "Tu contrato OpenAPI se verá así",
            "lenguaje": "json",
            "codigo": """GET /openapi.json  ->  HTTP 200

{
  "openapi": "3.1.0",
  "info": {
    "title": "Biblioteca API",
    "version": "1.0.0",
    "description": "API de libros del curso DAB-2201"
  },
  "paths": {
    "/api/libros": {
      "get":  {"summary": "Listar libros",  "responses": {"200": {...}}},
      "post": {"summary": "Crear un libro", "responses": {"201": {...}}}
    }
  },
  "components": {
    "schemas": {"Libro": {"type": "object", ...}}
  }
}

GET /docs   ->  HTTP 200 (Swagger UI)
GET /redoc  ->  HTTP 200 (ReDoc)""",
            "nota": "La documentación no se escribe aparte: se genera del mismo código que atiende las peticiones.",
        },
        "reto": {
            "enunciado": "Publica una API de libros con metadatos y modelos documentados. El contrato debe describir lo que el servidor realmente hace.",
            "archivo": "app.py",
            "requisitos": [
                "La app se llama «Biblioteca API», versión 1.0.0, con una descripción.",
                "GET /openapi.json responde 200 y contiene las rutas /api/libros.",
                "El esquema `Libro` aparece en components.schemas porque un endpoint lo usa.",
                "GET /docs y GET /redoc responden 200.",
                "GET /api/libros responde 200 con el listado.",
            ],
            "pista": "En FastAPI, `title`, `version`, `description` y los modelos Pydantic alimentan OpenAPI automáticamente. Si el contrato y el código se contradicen, el contrato miente.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "OpenAPI responde con metadatos",
                        "metodo": "GET",
                        "ruta": "/openapi.json",
                        "estado": 200,
                        "json_contiene": {
                            "openapi": "3.1.0",
                            "info": {"title": "Biblioteca API", "version": "1.0.0"},
                            "paths": {"/api/libros": {}},
                            "components": {"schemas": {"Libro": {}}},
                        },
                    },
                    {
                        "descripcion": "Swagger UI está disponible",
                        "metodo": "GET",
                        "ruta": "/docs",
                        "estado": 200,
                        "cuerpo_contiene": ["swagger"],
                    },
                    {
                        "descripcion": "ReDoc está disponible",
                        "metodo": "GET",
                        "ruta": "/redoc",
                        "estado": 200,
                    },
                    {
                        "descripcion": "El endpoint documentado responde",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": []},
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion07.md` con la captura del contrato.",
    },
    8: {
        "pregunta": "¿Qué debe ver el cliente cuando algo falla?",
        "prerrequisitos": [
            "Sesión 07: OpenAPI y contrato",
            "Saber qué es una excepción en Python",
        ],
        "objetivos": [
            "Lanzar excepciones de negocio con códigos HTTP semánticos.",
            "Centralizar el formato de error en un manejador global.",
            "Evitar respuestas 500 y fugas de detalles internos.",
        ],
        "conceptos": [
            {
                "termino": "Excepción",
                "definicion": "Situación que interrumpe el flujo normal y debe manejarse de forma explícita.",
                "analogia": "Como un semáforo en rojo: el viaje se detiene y hay que decidir qué hacer.",
            },
            {
                "termino": "Manejador de errores",
                "definicion": "Función central que transforma una excepción en una respuesta HTTP consistente.",
                "analogia": "Como la mesa de atención al cliente: recibe el problema y da una respuesta uniforme.",
            },
            {
                "termino": "Sobre de error (envelope)",
                "definicion": "Estructura JSON común para todos los errores, con código y mensaje.",
                "analogia": "Como un formato único de queja: siempre tiene folio y descripción.",
            },
            {
                "termino": "404 vs 422",
                "definicion": "404: el recurso no existe; 422: el recurso existe pero los datos no son válidos.",
                "analogia": "404: la dirección no existe; 422: la dirección existe pero el paquete está mal armado.",
            },
        ],
        "resultado": {
            "titulo": "Tus errores se verán exactamente así",
            "lenguaje": "json",
            "codigo": """GET /api/libros/99
HTTP/1.1 404 Not Found
{"error":{"codigo":"NO_ENCONTRADO","mensaje":"El libro 99 no existe"}}

POST /api/libros  {"titulo": ""}
HTTP/1.1 422 Unprocessable Entity
{"error":{"codigo":"VALIDACION","mensaje":"Revisa los datos enviados"}}

Nunca:
HTTP/1.1 500 Internal Server Error
{"detail":"Traceback (most recent call last)..."}""",
            "nota": "El cliente necesita saber qué corregir; tú necesitas que no se filtre la implementación.",
        },
        "reto": {
            "enunciado": "Implementa un manejo de errores uniforme: una excepción de negocio para libros inexistentes y un manejador para los errores de validación.",
            "archivo": "app.py",
            "requisitos": [
                "Define `LibroNoEncontrado` y regístralo con un handler que responda 404.",
                "El cuerpo del 404 es {\"error\": {\"codigo\": \"NO_ENCONTRADO\", \"mensaje\": ...}}.",
                "Los errores de validación responden 422 con el mismo sobre y codigo VALIDACION.",
                "Un título vacío debe rechazarse con 422.",
                "La API inicia con el libro 1 (Rayuela) para que el caso feliz exista.",
                "GET /api/libros/1 responde 200; GET /api/libros/99 responde 404.",
                "Ningún caso debe producir 500.",
            ],
            "pista": "FastAPI permite registrar handlers con `@app.exception_handler(...)`. El formato de error es parte del contrato, igual que el formato de éxito.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "Un libro existente responde 200",
                        "metodo": "GET",
                        "ruta": "/api/libros/1",
                        "estado": 200,
                        "json_contiene": {"id": 1},
                    },
                    {
                        "descripcion": "Un libro inexistente responde 404 con sobre de error",
                        "metodo": "GET",
                        "ruta": "/api/libros/99",
                        "estado": 404,
                        "json_contiene": {"error": {"codigo": "NO_ENCONTRADO"}},
                    },
                    {
                        "descripcion": "Los datos inválidos responden 422 con sobre de error",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": ""},
                        "estado": 422,
                        "json_contiene": {"error": {"codigo": "VALIDACION"}},
                    },
                    {
                        "descripcion": "Un libro válido sigue respondiendo 201",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963},
                        "estado": 201,
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion08.md` con el formato de error elegido.",
    },
    9: {
        "pregunta": "¿Cómo mides cuánto tarda cada petición sin repetir código en cada endpoint?",
        "prerrequisitos": [
            "Sesión 08: excepciones y respuestas de error",
            "Saber qué es una función que envuelve a otra",
        ],
        "objetivos": [
            "Explicar qué es un middleware y dónde se ejecuta.",
            "Agregar encabezados de trazabilidad a todas las respuestas.",
            "Verificar que el middleware también actúa en errores.",
        ],
        "conceptos": [
            {
                "termino": "Middleware",
                "definicion": "Capa que intercepta cada petición antes o después del endpoint.",
                "analogia": "Como el detector de metales de un aeropuerto: todos pasan por allí.",
            },
            {
                "termino": "Cadena de middleware",
                "definicion": "Serie ordenada de capas por las que atraviesa una petición.",
                "analogia": "Como las estaciones de una línea de ensamblaje.",
            },
            {
                "termino": "Trazabilidad",
                "definicion": "Capacidad de seguir una petición concreta a través de logs y encabezados.",
                "analogia": "Como el número de guía de un paquete.",
            },
            {
                "termino": "X-Process-Time",
                "definicion": "Encabezado personalizado con el tiempo que tardó el servidor en procesar la petición.",
                "analogia": "Como el cronómetro de una carrera: dice cuánto tardó cada vuelta.",
            },
        ],
        "resultado": {
            "titulo": "Todas tus respuestas llevarán estas cabeceras",
            "lenguaje": "http",
            "codigo": """$ curl -i http://127.0.0.1:8000/api/libros
HTTP/1.1 200 OK
content-type: application/json
x-process-time: 0.0017
x-request-id: 4f2c9a1e

{"libros":[]}

$ curl -i http://127.0.0.1:8000/api/libros \\
       -H "X-Request-ID: prueba-123"
HTTP/1.1 200 OK
x-request-id: prueba-123
x-process-time: 0.0012

$ curl -i http://127.0.0.1:8000/api/no-existe
HTTP/1.1 404 Not Found
x-process-time: 0.0009
x-request-id: 7c1d...""",
            "nota": "Si el cliente ya envía un X-Request-ID, se respeta; si no, el servidor genera uno.",
        },
        "reto": {
            "enunciado": "Agrega un middleware que mida el tiempo de cada petición y propague un identificador de traza en todas las respuestas.",
            "archivo": "app.py",
            "requisitos": [
                "Toda respuesta incluye X-Process-Time con un número decimal de segundos.",
                "Toda respuesta incluye X-Request-ID.",
                "Si la petición trae X-Request-ID, la respuesta conserva ese valor.",
                "El middleware también se aplica a respuestas 404.",
                "El endpoint GET /api/libros sigue respondiendo 200.",
            ],
            "pista": "El middleware envuelve la llamada al endpoint: mide antes y después, y agrega los encabezados a la respuesta que ya se construyó.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "Una respuesta correcta trae tiempo y traza",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "headers_contiene": {"x-process-time": "", "x-request-id": ""},
                    },
                    {
                        "descripcion": "El X-Request-ID del cliente se conserva",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "headers": {"X-Request-ID": "prueba-123"},
                        "estado": 200,
                        "headers_contiene": {"x-request-id": "prueba-123"},
                    },
                    {
                        "descripcion": "El middleware también cubre los 404",
                        "metodo": "GET",
                        "ruta": "/api/no-existe",
                        "estado": 404,
                        "headers_contiene": {"x-process-time": "", "x-request-id": ""},
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde y bitácora `auditorias/auditoria_sesion09.md` con una captura de las cabeceras.",
    },
    10: {
        "pregunta": "¿Tu API ya se comporta como un servicio profesional?",
        "prerrequisitos": [
            "Sesiones 02 a 09: CRUD, validación, OpenAPI, errores y middleware",
            "Ganas de integrar todo en una sola API",
        ],
        "objetivos": [
            "Integrar los conceptos del bloque en una Mock API coherente.",
            "Verificar el contrato completo con una suite de casos.",
            "Etiquetar la entrega del primer hito en GitHub.",
        ],
        "conceptos": [
            {
                "termino": "Mock API",
                "definicion": "API que responde con datos simulados antes de conectarse a una base de datos real.",
                "analogia": "Como un simulador de vuelo: practicas el procedimiento sin riesgo.",
            },
            {
                "termino": "Contract-first",
                "definicion": "Diseñar primero el contrato y después implementarlo.",
                "analogia": "Como dibujar los planos antes de levantar las paredes.",
            },
            {
                "termino": "Suite de pruebas",
                "definicion": "Conjunto ordenado de casos que verifican el comportamiento completo.",
                "analogia": "Como la lista de verificación de un piloto antes de despegar.",
            },
            {
                "termino": "Hito",
                "definicion": "Entrega evaluable que demuestra un conjunto de competencias.",
                "analogia": "Como un examen parcial: no basta un tema, se evalúa el conjunto.",
            },
        ],
        "resultado": {
            "titulo": "Tu Mock API del Hito 1 se comportará así",
            "lenguaje": "http",
            "codigo": """POST /api/libros              -> 201 Created
GET  /api/libros              -> 200 OK
GET  /api/libros/1            -> 200 OK
PUT  /api/libros/1            -> 200 OK
DELETE /api/libros/1          -> 204 No Content
GET  /api/libros/1            -> 404 Not Found
POST /api/libros (inválido)   -> 422 Unprocessable Entity
PATCH /api/libros/1           -> 405 Method Not Allowed
GET  /openapi.json            -> 200 OK

RESUMEN: 9/9 casos correctos. ¡Hito 1 listo!""",
            "nota": "La suite completa es el resultado: si un caso falla, el hito aún no está listo.",
        },
        "reto": {
            "enunciado": "Integra una Mock API de libros que cumpla el contrato completo del Bloque 1: CRUD, validación, documentación y errores semánticos.",
            "archivo": "app.py",
            "requisitos": [
                "CRUD completo de /api/libros con ids asignados por el servidor.",
                "Validación de titulo y anio con 422 cuando corresponda.",
                "OpenAPI disponible en /openapi.json con el esquema Libro.",
                "Errores 404 y 405 semánticos, sin 500.",
                "Los nueve casos de la suite deben quedar en verde.",
            ],
            "pista": "No empieces por el código: empieza por la tabla de casos. Cada fila es una promesa que tu API debe cumplir.",
        },
        "verificacion": [
            {
                "tipo": "http",
                "archivo": "app.py",
                "casos": [
                    {
                        "descripcion": "Listado inicial vacío",
                        "metodo": "GET",
                        "ruta": "/api/libros",
                        "estado": 200,
                        "json_contiene": {"libros": []},
                    },
                    {
                        "descripcion": "Creación válida",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "Rayuela", "anio": 1963},
                        "estado": 201,
                        "json_contiene": {"id": 1, "titulo": "Rayuela"},
                    },
                    {
                        "descripcion": "Consulta del libro creado",
                        "metodo": "GET",
                        "ruta": "/api/libros/1",
                        "estado": 200,
                        "json_contiene": {"id": 1, "titulo": "Rayuela"},
                    },
                    {
                        "descripcion": "Actualización del libro",
                        "metodo": "PUT",
                        "ruta": "/api/libros/1",
                        "json": {"titulo": "Rayuela (edición crítica)", "anio": 1963},
                        "estado": 200,
                        "json_contiene": {"id": 1, "titulo": "Rayuela (edición crítica)"},
                    },
                    {
                        "descripcion": "Eliminación del libro",
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
                    {
                        "descripcion": "Validación de datos inválidos",
                        "metodo": "POST",
                        "ruta": "/api/libros",
                        "json": {"titulo": "", "anio": 1200},
                        "estado": 422,
                    },
                    {
                        "descripcion": "Método no permitido",
                        "metodo": "PATCH",
                        "ruta": "/api/libros/1",
                        "estado": 405,
                    },
                    {
                        "descripcion": "Contrato OpenAPI disponible",
                        "metodo": "GET",
                        "ruta": "/openapi.json",
                        "estado": 200,
                        "json_contiene": {"paths": {"/api/libros": {}}, "components": {"schemas": {"Libro": {}}}},
                    },
                ],
            }
        ],
        "entrega": "Cuaderno en verde, bitácora `auditorias/auditoria_sesion10.md` y tag `v0.1-hito1` en tu repositorio.",
    },
}
