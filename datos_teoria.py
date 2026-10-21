"""
Datos teóricos del curso Desarrollo de Aplicaciones Web (DAB-2201).
Consolidado a partir de los cuatro bloques originales.
Cada sesión contiene: tema, unidad y (salvo el encuadre) teoria_principal,
arquitectura_memoria y casos_borde.
"""

TEORIA = {1: {'tema': 'Encuadre, Diagnóstico HTTP y Servidores en la Nube',
     'unidad': 'Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs',
     'es_encuadre': True},
 2: {'tema': 'Gestión en GitHub Web y Métodos HTTP (GET, POST, PUT, DELETE)',
     'unidad': 'Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs',
     'es_encuadre': False,
     'teoria_principal': {'titulo': 'Semántica del Protocolo HTTP y Métodos de Petición',
                          'lead': 'El protocolo HTTP define acciones estandarizadas sobre recursos identificables mediante verbos con '
                                  'semántica de idempotencia y seguridad.',
                          'tarjetas': [('01. GET & DELETE (Lectura y Baja)',
                                        'GET recupera una representación del recurso sin alterar su estado; DELETE remueve la entidad.',
                                        'Ambos deben ser idempotentes: múltiples peticiones idénticas producen el mismo estado en el '
                                        'servidor.'),
                                       ('02. POST vs PUT / PATCH (Creación vs Edición)',
                                        'POST crea recursos subordinados con ID generado por el servidor; PUT reemplaza totalmente el '
                                        'recurso; PATCH realiza modificaciones parciales.',
                                        'POST no es idempotente (múltiples POST crean múltiples recursos).'),
                                       ('03. Código HTTP 405 Method Not Allowed',
                                        'Respuesta emitida cuando la URI existe pero el verbo HTTP utilizado no está implementado en la '
                                        'ruta.',
                                        "Debe incluir el encabezado 'Allow' informando los métodos aceptados.")]},
     'arquitectura_memoria': {'titulo': 'Enrutamiento Semántico y Despacho en Servidor',
                              'descripcion': 'Cómo el servidor web mapea la dupla (Verbo, Ruta) hacia el controlador:',
                              'tarjetas': [('Tabla de Rutas (Routing Table)',
                                            'Mapeo interno del framework: `(VERBO, PATRON_URI) -> FUNCION_CONTROLADOR`.',
                                            'El middleware de ruteo inspecciona la primera línea de la petición HTTP antes de deserializar '
                                            'el payload.'),
                                           ('Idempotencia en APIs REST',
                                            'Garantía de que reintentar una petición fallida por problemas de red no corromperá el estado '
                                            'de la base de datos.',
                                            'Esencial para construir clientes web resilientes.')]},
     'casos_borde': {'titulo': 'Antipatrones en Métodos HTTP',
                     'items': ['Usar GET para modificar o eliminar datos en el servidor (ej. `/api/eliminar_usuario?id=5`), rompiendo la '
                               'seguridad del protocolo.',
                               "Usar POST para todo (Antipatrón 'RPC sobre HTTP') ignorando la semántica de PUT, PATCH y DELETE.",
                               'Retornar HTTP 200 OK en respuestas de error de método no permitido.']}},
 3: {'tema': 'Headers, Content-Type y Negociación de Contenido',
     'unidad': 'Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs',
     'es_encuadre': False,
     'teoria_principal': {'titulo': 'Metadatos HTTP y Negociación de Representación',
                          'lead': 'Los encabezados (*Headers*) transportan metadatos esenciales para la autenticación, almacenamiento en '
                                  'caché y formato de transferencia.',
                          'tarjetas': [('01. Content-Type (Formato del Payload)',
                                        'Indica el tipo MIME de los bytes transportados en el cuerpo del mensaje (ej. `application/json`, '
                                        '`multipart/form-data`).',
                                        'Permite al servidor seleccionar el parser adecuado para deserializar la entrada.'),
                                       ('02. Accept Header (Negociación)',
                                        'Enviado por el cliente para indicar qué formatos de respuesta puede procesar (ej. `Accept: '
                                        'application/json`).',
                                        'Si el servidor no puede emitir un formato aceptado, debe responder con HTTP 406 Not Acceptable.'),
                                       ('03. Encabezados Personalizados (X-Headers)',
                                        'Metadatos adicionales como trazabilidad de peticiones (`X-Request-ID`) o tiempos de ejecución '
                                        '(`X-Process-Time`).',
                                        'Proporcionan observabilidad sin alterar el cuerpo JSON del mensaje.')]},
     'arquitectura_memoria': {'titulo': 'Procesamiento de Streams y Parser MIME',
                              'descripcion': 'Transformación de flujo de bytes a estructuras en memoria:',
                              'tarjetas': [('Deserialización del Stream',
                                            'El servidor lee los bytes puros de la conexión TCP y utiliza el `Content-Type` para invocar '
                                            'el decodificador JSON.',
                                            'Si los bytes no corresponden a un JSON válido, se emite un error HTTP 400 Bad Request.'),
                                           ('Código HTTP 415 Unsupported Media Type',
                                            'Respuesta automática cuando el cliente envía un cuerpo en un formato no soportado por el '
                                            'endpoint.',
                                            'Protege al servidor de intentar parsear payloads incompatibles.')]},
     'casos_borde': {'titulo': 'Puntos de Falla en Negociación de Contenido',
                     'items': ['Omitir el encabezado `Content-Type: application/json` al enviar payloads JSON en peticiones POST.',
                               'Asumir que el cuerpo de la petición es una cadena de texto sin validar la codificación de caracteres '
                               '(UTF-8).',
                               'Retornar respuestas en texto plano cuando el cliente solicitó explícitamente `application/json`.']}},
 4: {'tema': 'Anatomía RESTful, URIs Nombres y Recursos',
     'unidad': 'Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs',
     'es_encuadre': False,
     'teoria_principal': {'titulo': 'Principios de Diseño de APIs RESTful',
                          'lead': 'REST (Representational State Transfer) organiza la arquitectura web en torno a recursos identificados '
                                  'por URIs jerárquicas y sustantivas.',
                          'tarjetas': [('01. URIs Basadas en Sustantivos Plurales',
                                        'Las URIs identifican recursos (`/api/v1/usuarios`), nunca acciones (`/api/v1/obtenerUsuarios`).',
                                        'La acción a realizar sobre el recurso la determina exclusivamente el verbo HTTP.'),
                                       ('02. Jerarquía y Sub-Recursos',
                                        'Representación de relaciones entre entidades mediante anidamiento lógico: '
                                        '`/api/v1/usuarios/{id}/pedidos`.',
                                        'Mantiene la estructura de rutas intuitiva y predecible.'),
                                       ('03. Desacoplamiento Cliente-Servidor',
                                        'El servidor expone datos y estado; el cliente se encarga de la presentación y la interfaz de '
                                        'usuario.',
                                        'Permite reutilizar la misma API para clientes Web, Móviles e Integraciones IoT.')]},
     'arquitectura_memoria': {'titulo': 'Parámetros de Ruta vs Query Parameters',
                              'descripcion': 'Selección de canales de entrada según la intención de la búsqueda:',
                              'tarjetas': [('Path Parameters (`/recursos/{id}`)',
                                            'Se utilizan para identificar un recurso específico de forma única en la jerarquía.',
                                            'Su ausencia en la URI provoca un error de ruteo HTTP 404 Not Found.'),
                                           ('Query Parameters (`/recursos?limit=10&page=2`)',
                                            'Se utilizan para filtrar, ordenar, paginar o buscar sobre una colección de recursos.',
                                            'Son opcionales y no alteran la identidad base de la URI.')]},
     'casos_borde': {'titulo': 'Antipatrones en Diseño RESTful',
                     'items': ['Incluir verbos dentro de la URI (ej. `/api/v1/crear_producto` en lugar de `POST /api/v1/productos`).',
                               'Anidamiento excesivo de recursos (> 2 niveles de profundidad como '
                               '`/tiendas/1/estantes/2/cajas/3/productos`), volviendo la API difícil de mantener.',
                               "Retornar arreglos JSON crudos en la raíz en lugar de objetos JSON envueltos (`{'data': [...]}`)."]}},
 5: {'tema': 'Pydantic v2 / DTOs en PHP y Tipado Estático',
     'unidad': 'Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs',
     'es_encuadre': False,
     'teoria_principal': {'titulo': 'Data Transfer Objects (DTO) y Validación Estricta',
                          'lead': 'Un DTO define el esquema rígido de los datos que ingresan o salen de la API, garantizando tipado seguro '
                                  'en tiempo de ejecución.',
                          'tarjetas': [('01. Validación en Tiempo de Ejecución',
                                        'Python y PHP son dinámicos; Pydantic/DTOs fuerzan la conversión y validación de tipos al recibir '
                                        'el JSON.',
                                        'Si la entrada no coincide exactamente con el esquema, la petición es derivada automáticamente a '
                                        'un manejador de errores.'),
                                       ('02. Coerción de Tipos Controlada',
                                        'Pydantic v2 convierte cadenas numéricas `"123"` a enteros `123` si el esquema lo define como '
                                        '`int`.',
                                        'Evita fallos silenciosos en la capa de lógica de negocio.'),
                                       ('03. Deserialización y Serialización',
                                        'Transformación bidireccional: `JSON -> DTO (Entrada)` y `Objeto/Model -> DTO -> JSON (Salida)`.',
                                        'Aísla el modelo interno de la base de datos de la representación pública enviada al cliente.')]},
     'arquitectura_memoria': {'titulo': 'Arquitectura de Pydantic v2 (Rust Core)',
                              'descripcion': 'Rendimiento y seguridad de esquemas de datos:',
                              'tarjetas': [('Motor Pydantic-Core (Rust)',
                                            'Pydantic v2 ejecuta la validación de esquemas compilada en Rust, alcanzando velocidades de 5x '
                                            'a 50x superiores a v1.',
                                            'Garantiza consumo de memoria mínimo bajo tráfico masivo.'),
                                           ('Código HTTP 422 Unprocessable Entity',
                                            'Respuesta estándar cuando el JSON es sintácticamente válido pero viola los tipos o '
                                            'restricciones del DTO.',
                                            'Devuelve una lista detallada con los campos exactos que fallaron.')]},
     'casos_borde': {'titulo': 'Puntos de Falla en DTOs',
                     'items': ['Exponer entidades de base de datos directamente en el endpoint en lugar de usar DTOs de salida.',
                               'Permitir la inyección de campos no declarados en el esquema (*Mass Assignment Vulnerability*).',
                               'Omitir valores por defecto en campos opcionales causando errores de atributo nulo (`NoneType`).']}},
 6: {'tema': 'Validación Estricta, Constraints y Params Query/Body',
     'unidad': 'Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs',
     'es_encuadre': False,
     'teoria_principal': {'titulo': 'Reglas de Dominio y Restricciones de Entrada',
                          'lead': 'La validación no se limita al tipo de dato; debe certificar que los valores respeten las restricciones '
                                  'del dominio del negocio.',
                          'tarjetas': [('01. Restricciones Numéricas y de Cadenas',
                                        'Uso de `Field(ge=18, le=100)` para límites numéricos y `Field(min_length=3, max_length=50)` para '
                                        'texto.',
                                        'Detiene entradas absurdas o maliciosas en la frontera de la API.'),
                                       ('02. Expresiones Regulares (Regex Validation)',
                                        'Validación de formatos complejos mediante patrones: emails, RFCs, teléfonos o UUIDs.',
                                        'Garantiza la consistencia del formato antes de consultar la base de datos.'),
                                       ('03. Validadores Personalizados (@field_validator)',
                                        'Métodos que ejecutan lógica condicional avanzada sobre uno o más campos del DTO.',
                                        "Permite verificar reglas como: 'la fecha_fin debe ser posterior a la fecha_inicio'.")]},
     'arquitectura_memoria': {'titulo': 'Procesamiento de Fuentes de Entrada Múltiples',
                              'descripcion': 'Extracción simultánea de datos en un solo handler:',
                              'tarjetas': [('Anotaciones de Ubicación',
                                            'FastAPI/Frameworks diferencian entre `Path()`, `Query()`, `Header()` y `Body()`.',
                                            'Garantiza que un parámetro de búsqueda no sea confundido con un atributo del payload JSON.'),
                                           ('Generación de Documentación Automática',
                                            'Las restricciones declaradas en `Field()` se compilan directamente en el esquema OpenAPI JSON '
                                            'del servidor.',
                                            'Mantiene la documentación viva y sincronizada con el código.')]},
     'casos_borde': {'titulo': 'Antipatrones en Validación de Entrada',
                     'items': ['Validar datos manualmente con sentencias `if/else` dentro del controlador en lugar de usar el DTO.',
                               'Permitir cadenas compuestas únicamente por espacios en blanco (`"   "`) al no aplicar `.strip()`.',
                               'No limitar el tamaño máximo de listas o archivos subidos saturando la memoria RAM del servidor.']}},
 7: {'tema': 'Especificación OpenAPI (Swagger) y ReDoc',
     'unidad': 'Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs',
     'es_encuadre': False,
     'teoria_principal': {'titulo': 'Documentación Viva e Interoperabilidad de APIs',
                          'lead': 'OpenAPI es el estándar industrial neutro para describir APIs RESTful de forma legible tanto por humanos '
                                  'como por máquinas.',
                          'tarjetas': [('01. Especificación OpenAPI v3.1',
                                        'Documento JSON/YAML que describe rutas, verbos, parámetros, esquemas de payload y códigos de '
                                        'respuesta.',
                                        'Sustituye la documentación manual desactualizada por un contrato auditable.'),
                                       ('02. Swagger UI (Cliente Interactivo)',
                                        'Interfaz gráfica que permite probar endpoints directamente desde el navegador enviando peticiones '
                                        'HTTP reales.',
                                        'Acelera el desarrollo del frontend al proporcionar un entorno de pruebas inmediato.'),
                                       ('03. ReDoc (Documentación Estática Enriquecida)',
                                        'Renderizado alternativo enfocado en la lectura limpia de esquemas de datos y contratos técnicos.',
                                        'Ideal para publicar portales de desarrolladores y especificaciones oficiales.')]},
     'arquitectura_memoria': {'titulo': 'Generación Automática del Esquema JSON',
                              'descripcion': 'Reflexión e inspección de código en el servidor:',
                              'tarjetas': [('Endpoint `/openapi.json`',
                                            'El servidor inspecciona las rutas registradas y sus tipos Pydantic para construir el JSON '
                                            'OpenAPI dinámicamente.',
                                            'Permite a herramientas externas (Postman, SDK Generators) consumir el esquema al instante.'),
                                           ('Generación de SDKs de Cliente',
                                            'A partir del documento OpenAPI, es posible autogenerar clientes en TypeScript, Swift o Kotlin '
                                            'sin escribir código de red manual.',
                                            'Garantiza sincronización total entre backend y aplicaciones móviles/web.')]},
     'casos_borde': {'titulo': 'Puntos de Falla en Documentación OpenAPI',
                     'items': ['Exponer endpoints privados o de diagnóstico interno en el esquema OpenAPI público.',
                               'Omitir la documentación de respuestas de error (400, 401, 403, 404, 422) mostrando únicamente la respuesta '
                               '200 OK.',
                               'Mantener descripciones genéricas en los esquemas sin ejemplos reales de uso.']}},
 8: {'tema': 'Respuestas Semánticas y Excepciones HTTP Personalizadas',
     'unidad': 'Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs',
     'es_encuadre': False,
     'teoria_principal': {'titulo': 'Manejo Global de Errores y Estandarización de Respuestas',
                          'lead': 'Una API profesional nunca debe colapsar emitiendo un traceback de código o un error HTTP 500 no '
                                  'capturado.',
                          'tarjetas': [('01. Excepciones Semánticas (HTTPException)',
                                        'Lanzamiento de excepciones estructuradas indicando código de estado y detalle JSON legible.',
                                        'Interrumpe la ejecución del handler actual y delega la respuesta al middleware de errores.'),
                                       ('02. Manejadores Globales de Excepciones',
                                        'Capturadores centralizados (`@app.exception_handler`) que transforman excepciones no controladas '
                                        'en JSONs uniformes.',
                                        'Previene la fuga de información sensible (variables de entorno, rutas de código o passwords) al '
                                        'cliente.'),
                                       ('03. Estructura Estándar de Errores JSON',
                                        "Respuesta uniforme de error: `{'status': 'error', 'code': 404, 'detail': '...', 'timestamp': "
                                        "'...'}`.",
                                        'Facilita la captura y despliegue de alertas en las aplicaciones frontend.')]},
     'arquitectura_memoria': {'titulo': 'Flujo de Intercepción de Excepciones',
                              'descripcion': 'Ciclo de captura dentro de la pila de middlewares del servidor:',
                              'tarjetas': [('Captura de Errores no Manejados',
                                            'Si ocurre una división por cero o falla de DB, el manejador raíz intercepta el fallo, '
                                            'registra el log interno y emite un HTTP 500 limpio.',
                                            'Mantiene la estabilidad del proceso del servidor web.'),
                                           ('Respuestas de Error en Pydantic',
                                            'FastAPI captura automáticamente `RequestValidationError` y lo transforma en un HTTP 422 '
                                            'detallado.',
                                            'Ahorra código repetitivo de validación manual.')]},
     'casos_borde': {'titulo': 'Antipatrones en Respuestas de Error',
                     'items': ['Retornar un traceback de Python o PHP en la respuesta HTTP expuesto al usuario en producción.',
                               "Retornar HTTP 200 OK con un cuerpo JSON que contiene `{'error': 'Usuario no encontrado'}`.",
                               'Uso indiscriminado de errores HTTP 500 para fallos causados por datos inválidos del cliente (que '
                               'corresponden a 400/422).']}},
 9: {'tema': 'Middleware Web, Intercepción y Logging de Transacciones',
     'unidad': 'Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs',
     'es_encuadre': False,
     'teoria_principal': {'titulo': 'Patrón Pipeline y Procesamiento Transversal',
                          'lead': 'Los middlewares son componentes colocados en la tubería de peticiones que interceptan y modifican '
                                  'Requests y Responses.',
                          'tarjetas': [('01. Modelo de Cebolla (Onion Architecture)',
                                        'La petición atraviesa cada middleware hacia adentro hasta llegar al handler, y la respuesta '
                                        'regresa atravesando la tubería hacia afuera.',
                                        'Permite ejecutar código antes y después de la lógica del endpoint.'),
                                       ('02. Casos de Uso Transversales',
                                        'Auditoría de logs, medición de tiempo de ejecución, inyección de encabezados de seguridad, '
                                        'compresión Gzip.',
                                        'Desacopla responsabilidades que no pertenecen a la lógica de negocio del endpoint.'),
                                       ('03. Medición de Tiempos y Trazabilidad',
                                        'Inyección del encabezado `X-Process-Time` y generación de UUIDs de rastreo (`X-Request-ID`).',
                                        'Permite auditar cuellos de botella de rendimiento en entornos distribuidos.')]},
     'arquitectura_memoria': {'titulo': 'Ciclo de Vida de una Petición Interceptada',
                              'descripcion': 'Flujo de ejecución del objeto Request a través del pipeline:',
                              'tarjetas': [('Pre-procesamiento (Incoming Request)',
                                            'El middleware puede leer encabezados, validar tokens o rechazar la petición antes de que '
                                            'consuma recursos en el handler.',
                                            'Si rechaza la petición, devuelve una respuesta inmediata cortocircuitando la cadena.'),
                                           ('Post-procesamiento (Outgoing Response)',
                                            'El middleware modifica la respuesta generada agregando encabezados de seguridad o registrando '
                                            'métricas en base de datos.',
                                            'Asegura que todos los endpoints emitan los mismos encabezados estándar.')]},
     'casos_borde': {'titulo': 'Puntos de Falla en Middlewares',
                     'items': ['Consumir el stream del cuerpo de la petición (`request.body()`) en un middleware sin clonarlo, impidiendo '
                               'que el handler vuelva a leerlo.',
                               'Middlewares lentos o bloqueantes que añaden latencia excesiva a absolutamente todas las rutas de la API.',
                               'Capturar excepciones dentro del middleware sin re-lanzarlas, ocultando errores del servidor.']}},
 10: {'tema': 'Hito 1: Mock API RESTful con OpenAPI y Validation Harness',
      'unidad': 'Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs',
      'es_encuadre': False,
      'teoria_principal': {'titulo': 'Integración del Primer Hito de Arquitectura Web',
                           'lead': 'Culminación del Bloque 1. Ensamblaje de una Mock API completa con ruteo semántico, DTOs Pydantic v2, '
                                   'contrato OpenAPI y manejador global de errores.',
                           'tarjetas': [('01. API Desacoplada y Contract-First',
                                         'Servicio web que cumple strictly con la especificación OpenAPI semántica sin depender aún de una '
                                         'base de datos real.',
                                         'Proporciona datos de prueba (*Mock Data*) para acelerar la integración con equipos frontend.'),
                                        ('02. Validation Harness Completo',
                                         'Toda entrada es filtrada por esquemas DTO estrictos, rechazando tipos inválidos con HTTP 422 y '
                                         'datos fuera de rango con HTTP 400.',
                                         'Garantiza que la API sea inmune a payloads mal formados.'),
                                        ('03. Entrega de Hito 1 (Git Tag)',
                                         'Etiquetado formal de versión en el repositorio de GitHub del estudiante: `git tag v0.1-hito1`.',
                                         'Representa el 20% del Proyecto Integrador Semestral.')]},
      'arquitectura_memoria': {'titulo': 'Auditoría Automática de Respuestas HTTP',
                               'descripcion': 'Evaluación de cumplimiento del protocolo web:',
                               'tarjetas': [('Test Harness Integrado con HTTPX',
                                             'Batería de pruebas automatizadas que somete al servidor embebido en Colab a peticiones '
                                             'válidas y destructivas.',
                                             'Verifica códigos de estado 200, 201, 400, 404, 405 y 422.'),
                                            ('Verificación de Encabezados Semánticos',
                                             'Certifica que las respuestas emitan `Content-Type: application/json` y los metadatos de '
                                             'trazabilidad esperados.',
                                             'Garantiza calidad de software nivel producción.')]},
      'casos_borde': {'titulo': 'Criterios de Rechazo del Hito 1',
                      'items': ['Servidor que se desploma o emite errores HTTP 500 ante entradas maliciosas o campos vacíos.',
                                'Rutas que incluyen verbos en la URI en lugar de utilizar los métodos HTTP estándar.',
                                'Documentación OpenAPI inaccesible en `/docs` o desincronizada del código de los endpoints.']}},
 11: {'tema': 'Arquitectura en Capas: Router, Servicio y Capa de Datos',
      'unidad': 'Bloque 2: Lógica de Negocio, Controladores y Auth',
      'teoria_principal': {'titulo': 'Separación de Responsabilidades y Patrón Service Layer',
                           'lead': 'El desacoplamiento en capas aísla la capa de transporte HTTP de las reglas del negocio y el acceso a '
                                   'la base de datos.',
                           'tarjetas': [('01. Capa de Rutas / Controladores',
                                         'Recibe la petición HTTP, valida el esquema DTO de entrada y delega la ejecución al servicio.',
                                         'No debe contener lógica de negocio ni sentencias SQL directas.'),
                                        ('02. Capa de Servicio (Service Layer)',
                                         'Orquesta las reglas de negocio puras, cálculos de dominio y validaciones complejas.',
                                         'Es independiente del framework web; puede reutilizarse en scripts CLI, tareas en background o '
                                         'gRPC.'),
                                        ('03. Capa de Acceso a Datos (Repository / DAO)',
                                         'Encapsula las operaciones de persistencia (ORM / SQL) y transacciones.',
                                         'Permite cambiar el motor de base de datos sin alterar la lógica de negocio.')]},
      'arquitectura_memoria': {'titulo': 'Flujo Unidireccional de Datos en Memoria',
                               'descripcion': 'Ciclo de vida de los objetos a través de las capas de la aplicación:',
                               'tarjetas': [('Transformación DTO -> Entidad -> DTO',
                                             'El Router pasa DTOs al Servicio; el Servicio opera con Entidades de Dominio y devuelve DTOs '
                                             'de salida.',
                                             'Previene la fuga accidental de modelos internos o contraseñas al cliente.'),
                                            ('Aislamiento de Pruebas Unitarias',
                                             'Permite mockear la capa de datos en memoria para probar las reglas de negocio en '
                                             'milisegundos sin tocar la base de datos.',
                                             'Aumenta la cobertura y velocidad del pipeline CI/CD.')]},
      'casos_borde': {'titulo': 'Antipatrones en Arquitectura en Capas',
                      'items': ["Controladores 'Gordos' (*Fat Controllers*) con cientos de líneas mezclando parsing HTTP, SQL y lógica de "
                                'negocio.',
                                'Saltarse la capa de servicio invocando consultas de base de datos directamente desde los endpoints.',
                                'Dependencia circular entre servicios al no definir interfaces o contratos claros.']}},
 12: {'tema': 'Inyección de Dependencias (FastAPI Depends / Contenedor IoC)',
      'unidad': 'Bloque 2: Lógica de Negocio, Controladores y Auth',
      'teoria_principal': {'titulo': 'Inversión de Control (IoC) y Gestión de Recursos',
                           'lead': 'La inyección de dependencias permite que los componentes reciban sus colaboradores externos en lugar '
                                   'de instanciarlos directamente.',
                           'tarjetas': [('01. Inversión de Control (IoC)',
                                         'En lugar de hacer `servicio = UsuarioService()` dentro del endpoint, el framework inyecta la '
                                         'instancia lista para usar.',
                                         'Promueve el bajo acoplamiento y la alta cohesión del código.'),
                                        ('02. Sistema `Depends()` en FastAPI',
                                         'Declara dependencias como parámetros de función evaluados automáticamente en cada request.',
                                         'Permite componer grafos de dependencias jerárquicos (ej. Auth -> Permisos -> Base de Datos).'),
                                        ('03. Ciclo de Vida por Petición (Request-Scoped)',
                                         'Garantiza que recursos compartidos (como conexiones de DB) se abran al inicio de la petición y '
                                         'se cierren al terminar.',
                                         'Utiliza generadores (`yield`) para asegurar limpieza determinista de recursos.')]},
      'arquitectura_memoria': {'titulo': 'Gestión de Contexto y Limpieza Automática',
                               'descripcion': 'Patrón Context Manager en dependencias web:',
                               'tarjetas': [('Dependencias con Yield',
                                             '`def get_db(): db = Session(); try: yield db; finally: db.close()`.',
                                             'El bloque `finally` se ejecuta siempre, incluso si el endpoint lanza una excepción HTTP.'),
                                            ('Sustitución en Pruebas (Dependency Overrides)',
                                             '`app.dependency_overrides[get_db] = get_test_db`.',
                                             'Permite inyectar bases de datos SQLite en memoria durante las pruebas automatizadas.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en Inyección de Dependencias',
                      'items': ['Instanciar conexiones de base de datos como variables globales sin control de pool ni cierre por '
                                'petición.',
                                'Dependencias con estado mutable compartido entre hilos (*Race Conditions* en concurrencia).',
                                'Olvidar el bloque `finally` provocando fugas de conexiones (*Connection Leaks*) en la base de datos.']}},
 13: {'tema': 'Manejo de Sesiones Stateful vs Stateless Tokens',
      'unidad': 'Bloque 2: Lógica de Negocio, Controladores y Auth',
      'teoria_principal': {'titulo': 'Paradigmas de Autenticación y Escalabilidad Web',
                           'lead': 'La elección entre sesiones basadas en servidor (Stateful) o tokens criptográficos (Stateless) define '
                                   'la arquitectura de escalado del sistema.',
                           'tarjetas': [('01. Sesiones Stateful (Cookies de Sesión)',
                                         'El servidor guarda el estado del usuario en RAM/Redis y emite un `session_id` opaco en una '
                                         'cookie.',
                                         'Requiere replicación de memoria o almacenamiento centralizado cuando se escala horizontalmente a '
                                         'múltiples servidores.'),
                                        ('02. Autenticación Stateless (Tokens)',
                                         'El estado viaja firmado digitalmente dentro del token que porta el cliente en cada petición.',
                                         'Cualquier nodo del clúster puede verificar la firma sin consultar una base de datos '
                                         'centralizada.'),
                                        ('03. Criterio de Revocación',
                                         'Las sesiones stateful se revocan al instante borrando el ID del servidor; los tokens stateless '
                                         'requieren listas de bloqueo (*Blacklists*).',
                                         'Balance crítico entre rendimiento y control de revocación inmediata.')]},
      'arquitectura_memoria': {'titulo': 'Escalabilidad Horizontal y Servidores Stateless',
                               'descripcion': 'Comportamiento bajo balanceadores de carga (Load Balancers):',
                               'tarjetas': [("Problema de 'Sticky Sessions'",
                                             'En arquitecturas stateful, el balanceador debe enrutar al usuario siempre al mismo servidor '
                                             'físico.',
                                             'Si ese nodo colapsa, la sesión del usuario se pierde.'),
                                            ('Arquitectura Shared-Nothing',
                                             'Con tokens stateless, las peticiones pueden distribuirse aleatoriamente entre decenas de '
                                             'contenedores independientes.',
                                             'Facilita el auto-escalado elástico en la nube (AWS / Render / GCP).')]},
      'casos_borde': {'titulo': 'Antipatrones en Gestión de Sesiones',
                      'items': ['Almacenar objetos de sesión gigantes en memoria saturando la RAM del proceso web.',
                                'Tokens stateless con tiempos de expiración infinitos que no pueden ser invalidados ante un robo de '
                                'credenciales.',
                                'Transmitir identificadores de sesión en la URL en lugar de encabezados o cookies seguras.']}},
 14: {'tema': 'Hashing Seguro de Contraseñas (Bcrypt / Argon2)',
      'unidad': 'Bloque 2: Lógica de Negocio, Controladores y Auth',
      'teoria_principal': {'titulo': 'Criptografía Aplicada y Protección de Credenciales',
                           'lead': 'Las contraseñas nunca deben almacenarse en texto plano ni con algoritmos de hash rápidos diseñados '
                                   'para integridad (MD5, SHA-256).',
                           'tarjetas': [('01. Algoritmos Lentos Adaptativos (Bcrypt / Argon2)',
                                         'Diseñados intencionalmente para consumir tiempo de CPU y memoria, mitigando ataques de fuerza '
                                         'bruta masiva.',
                                         'Argon2 es el estándar ganador de la Password Hashing Competition (PHC).'),
                                        ('02. Salting Criptográfico Automático',
                                         'Secuencia aleatoria única de bytes generada para cada contraseña antes de aplicar el hash.',
                                         'Invalida por completo el uso de tablas precalculadas (*Rainbow Tables*).'),
                                        ('03. Factor de Costo de Trabajo (Work Factor)',
                                         'Parámetro configurable que duplica el tiempo de cómputo por cada incremento unitario.',
                                         'Permite ajustar la dificultad del algoritmo conforme el hardware se vuelve más rápido con los '
                                         'años.')]},
      'arquitectura_memoria': {'titulo': 'Prevención de Ataques de Tiempo (Timing Attacks)',
                               'descripcion': 'Verificación de hashes en tiempo constante:',
                               'tarjetas': [('Comparación en Tiempo Constante',
                                             'La función `verify()` tarda exactamente el mismo tiempo sin importar cuántos caracteres '
                                             'coincidan.',
                                             'Evita que un atacante deduzca la contraseña midiendo microsegundos de respuesta del '
                                             'servidor.'),
                                            ('Estructura Modular del Hash',
                                             'Cadena compacta: `$2b$12$salthex...hashbytes...` que incluye algoritmo, costo, sal y '
                                             'resultado.',
                                             'Permite verificar contraseñas antiguas y actualizarlas al nuevo costo de forma '
                                             'transparente.')]},
      'casos_borde': {'titulo': 'Vulnerabilidades Críticas en Hashing',
                      'items': ['Usar algoritmos obsoletos como MD5 o SHA-1 vulnerables a colisiones y cracking instantáneo por GPUs.',
                                "Aplicar 'doble hash' manual (`md5(sha256(pwd))`), reduciendo la entropía del algoritmo.",
                                'Registrar contraseñas en texto plano en los archivos de logs o trazas de depuración del servidor.']}},
 15: {'tema': 'Autenticación Stateless con JSON Web Tokens (JWT)',
      'unidad': 'Bloque 2: Lógica de Negocio, Controladores y Auth',
      'teoria_principal': {'titulo': 'Estructura, Firma Digital y Validación de JWT',
                           'lead': 'Un JWT (RFC 7519) es un contenedor compacto y seguro que transporta afirmaciones (*claims*) '
                                   'verificables entre partes.',
                           'tarjetas': [('01. Las 3 Secciones del Token',
                                         '`Header.Payload.Signature` codificadas individualmente en formato Base64Url.',
                                         'El Header indica el algoritmo (`HS256`); el Payload contiene los claims del usuario; la Firma '
                                         'valida la autenticidad.'),
                                        ('02. Firma Criptográfica HMAC-SHA256',
                                         "Calculada como: `HMACSHA256(base64(Header) + '.' + base64(Payload), SECRET_KEY)`.",
                                         'Cualquier modificación al Payload por parte del cliente invalida la firma matemática.'),
                                        ('03. Claims Estándar de Seguridad',
                                         '`sub` (ID del usuario), `iat` (fecha de emisión), `exp` (fecha de expiración estricta).',
                                         'El servidor rechaza automáticamente cualquier token cuyo tiempo actual supere `exp`.')]},
      'arquitectura_memoria': {'titulo': 'Decodificación y Validación en Servidor',
                               'descripcion': 'Pipeline de verificación criptográfica sin consultar base de datos:',
                               'tarjetas': [('Verificación de Firma en Memoria',
                                             'El servidor recalcula el hash con su `SECRET_KEY` privada; si coincide con la firma '
                                             'recibida, el token es legítimo.',
                                             'Operación puramente matemática en memoria RAM con costo sub-milisegundo.'),
                                            ('Manejo de Excepciones JWT',
                                             'Captura de `ExpiredSignatureError` (HTTP 401) y `JWTError` (firma manipulada).',
                                             'Garantiza mensajes de error claros sin filtrar detalles internos.')]},
      'casos_borde': {'titulo': 'Puntos de Falla y Vulnerabilidades JWT',
                      'items': ['Guardar información sensible (contraseñas, tarjetas de crédito) en el Payload, recordando que Base64 no '
                                'es cifrado.',
                                "Usar claves secretas débiles (`SECRET_KEY = '123456'`) susceptibles a ataques de diccionario offline.",
                                "Aceptar el algoritmo `'none'` en el Header desactivando la verificación de firma."]}},
 16: {'tema': 'OAuth2 Password Flow y Header Authorization Bearer',
      'unidad': 'Bloque 2: Lógica de Negocio, Controladores y Auth',
      'teoria_principal': {'titulo': 'Protocolo de Autorización Estándar y Esquema Bearer',
                           'lead': 'OAuth2 define flujos estandarizados para que las aplicaciones intercambien credenciales por tokens de '
                                   'acceso.',
                           'tarjetas': [('01. Endpoint `/token` (OAuth2 Password Flow)',
                                         'Recibe credenciales mediante `application/x-www-form-urlencoded` con campos `username` y '
                                         '`password`.',
                                         'Valida las credenciales contra la base de datos y devuelve un JSON con `access_token` y '
                                         '`token_type: bearer`.'),
                                        ('02. Encabezado `Authorization: Bearer <token>`',
                                         'El estándar HTTP para enviar el token de acceso en cada petición protegida subsecuente.',
                                         'Separado del cuerpo de datos para facilitar el filtrado en proxies y firewalls.'),
                                        ('03. Código HTTP 401 Unauthorized',
                                         'Emitido con el encabezado `WWW-Authenticate: Bearer` cuando el token está ausente, vencido o es '
                                         'inválido.',
                                         'Indica al cliente que debe re-autenticarse para obtener un nuevo token.')]},
      'arquitectura_memoria': {'titulo': 'Integración con OpenAPI y Swagger UI',
                               'descripcion': 'Esquema `OAuth2PasswordBearer` en FastAPI:',
                               'tarjetas': [('Inyección de Seguridad en Swagger',
                                             "Agrega el botón interactivo 'Authorize' en la documentación `/docs`.",
                                             'Swagger UI almacena el token y lo inyecta automáticamente en los encabezados de cada '
                                             'prueba.'),
                                            ('Dependencia `get_current_user`',
                                             'Función central reutilizable que extrae el token, verifica el JWT y retorna el usuario '
                                             'autenticado.',
                                             'Se inyecta con `Depends(get_current_user)` en cualquier ruta protegida.')]},
      'casos_borde': {'titulo': 'Antipatrones en Flujos OAuth2',
                      'items': ['Enviar credenciales en parámetros de consulta URL (`?user=x&pass=y`) quedando expuestas en logs de '
                                'servidores proxy.',
                                'Omitir el encabezado `WWW-Authenticate` en respuestas 401 violando el estándar RFC 6750.',
                                'No renovar tokens mediante Refresh Tokens obligando al usuario a iniciar sesión repetidamente.']}},
 17: {'tema': 'Control de Acceso Basado en Roles (RBAC)',
      'unidad': 'Bloque 2: Lógica de Negocio, Controladores y Auth',
      'teoria_principal': {'titulo': 'Autorización Granular y Jerarquía de Privilegios',
                           'lead': "La autenticación responde '¿Quién eres?'; la autorización responde '¿Tienes permiso para ejecutar esta "
                                   "acción?'.",
                           'tarjetas': [('01. Modelo RBAC (Role-Based Access Control)',
                                         'Los usuarios se asocian a roles (`admin`, `docente`, `estudiante`), y los roles poseen permisos '
                                         'sobre recursos.',
                                         'Desacopla la gestión de usuarios individuales de la configuración de permisos.'),
                                        ('02. Claim de Rol en JWT',
                                         "El token transporta el rol del usuario: `{'sub': '123', 'rol': 'admin'}`.",
                                         'Permite verificar privilegios en memoria sin consultar tablas de permisos en cada petición.'),
                                        ('03. Código HTTP 403 Forbidden vs 401',
                                         "HTTP 401: 'No sé quién eres' (No autenticado). HTTP 403: 'Sé quién eres, pero no tienes permiso' "
                                         '(No autorizado).',
                                         'Distinción semántica fundamental en APIs REST profesionales.')]},
      'arquitectura_memoria': {'titulo': 'Decoradores y Factorías de Dependencias RBAC',
                               'descripcion': 'Restricción declarativa de endpoints por rol:',
                               'tarjetas': [('Factoría `require_role(roles_permitidos)`',
                                             'Crea una dependencia que inspecciona el usuario autenticado y lanza `HTTPException(403)` si '
                                             'no posee el rol.',
                                             "Uso limpio: `@app.delete('/usuarios/{id}', "
                                             "dependencies=[Depends(require_role(['admin']))])`."),
                                            ('Principio de Menor Privilegio (PoLP)',
                                             'Cada rol debe tener acceso exclusivamente a los recursos mínimos necesarios para sus '
                                             'funciones.',
                                             'Limita el impacto de seguridad ante el compromiso de una cuenta de usuario.')]},
      'casos_borde': {'titulo': 'Fallas Críticas de Autorización (BOLA / IDOR)',
                      'items': ['Broken Object Level Authorization (BOLA): Permitir que un usuario modifique el recurso de otro usuario '
                                'cambiando el ID en la URI.',
                                'Retornar HTTP 401 cuando el usuario sí está autenticado pero carece de permisos de administrador (debe '
                                'ser 403).',
                                'Confiar en roles enviados por el cliente en el cuerpo de la petición sin validarlos contra el token '
                                'firmado.']}},
 18: {'tema': 'Rate Limiting, Throttling y Prevención de Abuso',
      'unidad': 'Bloque 2: Lógica de Negocio, Controladores y Auth',
      'teoria_principal': {'titulo': 'Protección de Disponibilidad y Mitigación de DoS',
                           'lead': 'El Rate Limiting restringe la cantidad de peticiones que un cliente puede realizar en una ventana de '
                                   'tiempo determinada.',
                           'tarjetas': [('01. Algoritmos de Ventana (Token Bucket / Sliding Window)',
                                         'Permiten ráfagas cortas controladas pero limitan el promedio sostenido de peticiones por minuto.',
                                         'Previene la saturación del servidor por scripts automatizados o ataques de denegación de '
                                         'servicio (DoS).'),
                                        ('02. Identificación del Cliente (IP vs Token)',
                                         'Límite por IP para rutas públicas (login/registro) y límite por ID de usuario autenticado para '
                                         'la API interna.',
                                         'Evita que un atacante consuma recursos en endpoints de procesamiento pesado.'),
                                        ('03. Código HTTP 429 Too Many Requests',
                                         'Respuesta estándar emitida cuando el cliente supera su cuota de peticiones permitidas.',
                                         'Debe incluir el encabezado `Retry-After: <segundos>` indicando cuándo puede reintentar.')]},
      'arquitectura_memoria': {'titulo': 'Almacenamiento de Contadores en Memoria y Redis',
                               'descripcion': 'Gestión de estado de cuotas de consumo:',
                               'tarjetas': [('Contadores en Memoria (Desarrollo)',
                                             'Diccionario en RAM con timestamps de peticiones por cliente.',
                                             'Fácil de auditar en pruebas unitarias dentro de Google Colab.'),
                                            ('Contadores en Redis con TTL (Producción)',
                                             'Claves con expiración atómica (`INCR` + `EXPIRE`) compartidas entre todos los nodos del '
                                             'clúster.',
                                             'Garantiza control de tráfico unificado en sistemas distribuidos.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en Rate Limiting',
                      'items': ['Bloquear proxies o balanceadores de carga al usar `request.client.host` sin leer encabezados '
                                '`X-Forwarded-For`.',
                                'Omitir el encabezado `Retry-After` provocando que los clientes realicen reintentos inmediatos agresivos.',
                                'No aplicar límites estrictos en el endpoint de autenticación permitiendo ataques de fuerza bruta a '
                                'contraseñas.']}},
 19: {'tema': 'Sanitización de Entradas, Prevención de XSS e Inyecciones',
      'unidad': 'Bloque 2: Lógica de Negocio, Controladores y Auth',
      'teoria_principal': {'titulo': 'Defensa en Profundidad y Validación de Datos No Confiables',
                           'lead': 'Todo dato proveniente del cliente debe tratarse como hostil hasta que sea validado, tipado y '
                                   'sanitizado.',
                           'tarjetas': [('01. Cross-Site Scripting (XSS)',
                                         'Inyección de código JavaScript malicioso (`<script>alert(1)</script>`) en campos de texto que '
                                         'luego se renderizan en el navegador de otros usuarios.',
                                         'Permite a un atacante robar tokens de sesión o suplantar la identidad de la víctima.'),
                                        ('02. Sanitización vs Escape de Salida',
                                         'Sanitización: Elimina etiquetas y caracteres peligrosos al entrar a la API. Escape: Codifica '
                                         'entidades HTML (`&lt;`, `&gt;`) al renderizar.',
                                         'Ambas capas deben implementarse para una defensa integral.'),
                                        ('03. Inyecciones de Comandos y NoSQL',
                                         'Entradas maliciosas que buscan ser ejecutadas como llamadas al sistema operativo o consultas no '
                                         'estructuradas.',
                                         'Se neutralizan forzando tipado estricto y listas blancas de caracteres permitidos.')]},
      'arquitectura_memoria': {'titulo': 'Sanitizadores Automáticos en el Pipeline DTO',
                               'descripcion': 'Limpieza de cadenas en la capa de deserialización:',
                               'tarjetas': [('Limpieza de Espacios y Tags',
                                             'Uso de validadores Pydantic que aplican `strip()`, eliminan caracteres de control y escapan '
                                             'HTML.',
                                             'Garantiza que la base de datos almacene texto limpio y normalizado.'),
                                            ('Encabezados de Seguridad HTTP',
                                             'Inyección de `Content-Security-Policy (CSP)`, `X-Content-Type-Options: nosniff` y '
                                             '`X-Frame-Options: DENY`.',
                                             'Instruye al navegador para bloquear la ejecución de scripts no autorizados.')]},
      'casos_borde': {'titulo': 'Vulnerabilidades Frecuentes',
                      'items': ['Confiar en validaciones hechas solo en el frontend con JavaScript, fácilmente eludibles con herramientas '
                                'como Postman o cURL.',
                                'Almacenar HTML crudo ingresado por usuarios en campos de comentarios o perfiles.',
                                'No escapar comillas dobles y simples en atributos HTML generando rupturas de contexto de seguridad.']}},
 20: {'tema': 'Hito 2: API con Inyección de Dependencias, Auth JWT y RBAC',
      'unidad': 'Bloque 2: Lógica de Negocio, Controladores y Auth',
      'teoria_principal': {'titulo': 'Integración del Segundo Hito: Seguridad y Control de Acceso',
                           'lead': 'Culminación del Bloque 2. La API ahora cuenta con arquitectura en capas, autenticación segura con JWT, '
                                   'hashing de contraseñas y autorización por roles (RBAC).',
                           'tarjetas': [('01. Pipeline de Autenticación Completo',
                                         'Flujo integrado: Registro con Bcrypt -> Login con OAuth2 `/token` -> Emisión de JWT firmado -> '
                                         'Acceso a rutas protegidas con Bearer token.',
                                         'Garantiza protección completa de los recursos del sistema.'),
                                        ('02. Control de Acceso por Roles (RBAC)',
                                         'Endpoints administrativos bloqueados con HTTP 403 para usuarios comunes; endpoints privados '
                                         'protegidos con HTTP 401 para usuarios anónimos.',
                                         'Verificado mediante pruebas automatizadas de intrusión.'),
                                        ('03. Entrega de Hito 2 (Git Tag)',
                                         'Etiquetado formal de versión en el repositorio de GitHub del estudiante: `git tag v0.2-hito2`.',
                                         'Representa el 25% del Proyecto Integrador Semestral.')]},
      'arquitectura_memoria': {'titulo': 'Auditoría Integral de Seguridad con Test Harness',
                               'descripcion': 'Batería de pruebas automatizadas sobre el servidor en Colab:',
                               'tarjetas': [('Suite de Intrusión Automatizada',
                                             'Pruebas con tokens manipulados, tokens expirados, contraseñas erróneas y accesos con roles '
                                             'insuficientes.',
                                             'Certifica que la API no tenga fugas de seguridad ni accesos no autorizados.'),
                                            ('Inspección de Encabezados y Respuestas',
                                             'Verificación de que las contraseñas nunca se devuelvan en las respuestas JSON y los errores '
                                             'emitan los códigos HTTP estándar.',
                                             'Cumplimiento estricto de las mejores prácticas de la industria.')]},
      'casos_borde': {'titulo': 'Criterios de Rechazo del Hito 2',
                      'items': ['Almacenar contraseñas en texto plano o con algoritmos no seguros (MD5/SHA).',
                                'Permitir el acceso a rutas administrativas a usuarios con roles no autorizados.',
                                'Fallas del servidor (HTTP 500) al recibir tokens mal formados o cadenas corruptas en el encabezado '
                                'Authorization.']}},
 21: {'tema': 'Fundamentos de Persistencia: SQLite / PostgreSQL y Drivers',
      'unidad': 'Bloque 3: Persistencia Relacional, ORM y OWASP',
      'teoria_principal': {'titulo': 'Persistencia Relacional, Motores y Drivers Asíncronos',
                           'lead': 'La capa de persistencia garantiza que el estado de la aplicación sobreviva al reinicio del servidor o '
                                   'proceso web.',
                           'tarjetas': [('01. Motores SQLite vs PostgreSQL',
                                         'SQLite es un motor embebido basado en archivos para desarrollo/testing; PostgreSQL es un SGBD '
                                         'relacional cliente-servidor para producción.',
                                         'Ambos implementan el estándar SQL pero difieren en concurrencia y tipos avanzadores.'),
                                        ('02. Drivers y Conectores (psycopg3 / aiorsqlite)',
                                         'Bibliotecas de bajo nivel que gestionan la comunicación por sockets TCP o archivos con el motor '
                                         'SQL.',
                                         'Los drivers asíncronos evitan bloquear el bucle de eventos del servidor web durante '
                                         'lecturas/escrituras.'),
                                        ('03. Pool de Conexiones (Connection Pooling)',
                                         'Administración de un conjunto reutilizable de conexiones abiertas a la base de datos.',
                                         'Elimina la latencia de handshakes TCP y autenticación en cada petición HTTP.')]},
      'arquitectura_memoria': {'titulo': 'Gestión del Pool de Conexiones en Memoria',
                               'descripcion': 'Ciclo de vida de sockets hacia la base de datos:',
                               'tarjetas': [('Concurrencia sin Agotamiento',
                                             'El pool limita el número máximo de conexiones abiertas simultáneamente (ej. '
                                             '`max_overflow=10`).',
                                             'Previene que ráfagas de tráfico tumben el servidor de base de datos por saturación de '
                                             'conexiones.'),
                                            ('Patrón Singleton en la Engine',
                                             'Instancia única `create_async_engine()` compartida en toda la aplicación.',
                                             'Garantiza un control centralizado de los parámetros de reconexión y timeouts.')]},
      'casos_borde': {'titulo': 'Antipatrones en Conectividad a Bases de Datos',
                      'items': ['Crear una nueva instancia de `Engine` o reconectar a la DB dentro de cada llamada a handler HTTP.',
                                'Dejar conexiones colgadas sin devolver al pool al ocurrir excepciones en la ejecución de la consulta.',
                                'Usar SQLite en producción con peticiones de escritura concurrentes masivas provocando bloqueos de base de '
                                'datos (`database is locked`).']}},
 22: {'tema': 'Modelado Relacional (1:1, 1:N, N:M) con ORMs',
      'unidad': 'Bloque 3: Persistencia Relacional, ORM y OWASP',
      'teoria_principal': {'titulo': 'Mapeo Objeto-Relacional (ORM) y Relaciones',
                           'lead': 'Un ORM (Object-Relational Mapping) traduce tablas y filas de SQL a clases y objetos en el lenguaje de '
                                   'programación.',
                           'tarjetas': [('01. Mapeo Tablas -> Clases (SQLAlchemy 2.0)',
                                         'Las tablas se declaran como clases derivadas de `DeclarativeBase` con atributos tipados '
                                         '`Mapped[T]`.',
                                         'Aísla la estructura de código de las peculiaridades del dialecto SQL subyacente.'),
                                        ('02. Llaves Foráneas e Integridad Referencial',
                                         "Uso de `ForeignKey('tabla.id')` para vincular registros entre tablas relacionales.",
                                         'El motor SQL rechaza automáticamente la inserción de huérfanos o relaciones inexistentes.'),
                                        ('03. Tipos de Relaciones (1:1, 1:N, N:M)',
                                         'Declaración explicita con `relationship()` e hiper-tablas intermedias de asociación para '
                                         'relaciones N:M.',
                                         'Permite navegar el grafo de objetos directamente en código: `usuario.pedidos`.')]},
      'arquitectura_memoria': {'titulo': 'Mapeo de Clases a Tablas Físicas',
                               'descripcion': 'Metadatos del ORM y sincronización de estado:',
                               'tarjetas': [('Registro `MetaData`',
                                             'Contiene el catálogo dinámico de todas las tablas y restricciones registradas en la '
                                             'aplicación.',
                                             'Utilizado por el ORM para generar sentencias `CREATE TABLE` o scripts de migración.'),
                                            ("Opciones Cascade (`cascade='all, delete-orphan'`)",
                                             'Define el comportamiento al eliminar un registro padre sobre sus entidades secundarias '
                                             'relacionadas.',
                                             'Garantiza limpieza automática de registros en cascada en la base de datos.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en Modelado ORM',
                      'items': ['Definir relaciones bidireccionales sin especificar `back_populates` causando desincronización de objetos '
                                'en memoria.',
                                'Omitir índices explícitos (`index=True`) en llaves foráneas y campos de búsqueda frecuente.',
                                'Intentar mapear tablas N:M sin una tabla de asociación explicita con llaves compuestas.']}},
 23: {'tema': 'Operaciones CRUD Transaccionales y Async Sessions',
      'unidad': 'Bloque 3: Persistencia Relacional, ORM y OWASP',
      'teoria_principal': {'titulo': 'Sesiones Asíncronas y Patrón Unit of Work',
                           'lead': 'La sesión del ORM actúa como un espacio de trabajo (*Unit of Work*) que rastrea cambios sobre objetos '
                                   'antes de persistirlos.',
                           'tarjetas': [('01. Asincronía con `AsyncSession`',
                                         'Uso de `await session.execute()`, `await session.commit()` y `await session.refresh()`.',
                                         'Libera el hilo principal del evento web mientras la base de datos procesa la consulta.'),
                                        ('02. Estados de Objetos en el ORM',
                                         'Un objeto atraviesa estados: Transient (nuevo), Pending (agregado), Persistent (guardado) y '
                                         'Detached (cerrado).',
                                         'El ORM solo emite sentencias SQL `UPDATE` sobre atributos que hayan sufrido modificaciones '
                                         'reales.'),
                                        ('03. Ciclo de Vida por Petición HTTP',
                                         'La sesión se crea al recibir el Request y se cierra obligatoriamente al terminar mediante '
                                         'inyección de dependencias.',
                                         'Garantiza un aislamiento estricto de transacciones entre peticiones de distintos usuarios.')]},
      'arquitectura_memoria': {'titulo': 'Identity Map y Cache de Sesión',
                               'descripcion': 'Seguimiento de unificación de objetos en memoria:',
                               'tarjetas': [('Patrón Identity Map',
                                             'Garantiza que dentro de la misma sesión, dos consultas al mismo ID retornen exactamente la '
                                             'misma instancia en RAM.',
                                             'Evita inconsistencias de estado si dos partes del código modifican la misma entidad.'),
                                            ('Flush vs Commit',
                                             '`flush()` envía las sentencias SQL pendientes a la DB sin cerrar la transacción; `commit()` '
                                             'las consolida permanentemente.',
                                             'Permite obtener IDs autogenerados antes de confirmar la transacción final.')]},
      'casos_borde': {'titulo': 'Antipatrones en Operaciones CRUD',
                      'items': ['Acceder a atributos con carga perezosa (*Lazy Loading*) fuera de la sesión asíncrona lanzando '
                                '`MissingGreenlet` error.',
                                'No ejecutar `await session.rollback()` tras una excepción dejando la sesión en estado corrupto.',
                                'Olvidar llamar `await session.refresh(obj)` para obtener valores autogenerados por la base de datos '
                                '(timestamps, IDs).']}},
 24: {'tema': 'Migraciones de Base de Datos con Alembic / Phinx',
      'unidad': 'Bloque 3: Persistencia Relacional, ORM y OWASP',
      'teoria_principal': {'titulo': 'Control de Versiones de Esquema de Base de Datos',
                           'lead': 'Las migraciones permiten evolucionar la estructura de la base de datos mediante cambios incrementales, '
                                   'reversibles y auditables.',
                           'tarjetas': [('01. Problemática de Cambios Manuales',
                                         'Modificar tablas con SQL directo rompe la sincronización entre el código de producción y los '
                                         'entornos de desarrollo.',
                                         'Inviable en equipos distribuidos y sistemas de despliegue continuo (CD).'),
                                        ('02. Scripts de Migración (Upgrade / Downgrade)',
                                         'Cada revisión contiene dos funciones: `upgrade()` (aplica cambios) y `downgrade()` (los '
                                         'revierte).',
                                         'Permite avanzar o retroceder el esquema a cualquier punto de la historia del proyecto.'),
                                        ('03. Autogeneración de Revision Script',
                                         'Alembic compara los modelos de SQLAlchemy contra la base de datos real y genera la migración '
                                         'automáticamente.',
                                         'Acelera el desarrollo reduciendo la escritura manual de DDL.')]},
      'arquitectura_memoria': {'titulo': 'Tabla de Versiones `alembic_version`',
                               'descripcion': 'Rastreo de estado de la base de datos:',
                               'tarjetas': [('Tabla Centinela `alembic_version`',
                                             'Tabla especial en la DB que almacena una sola fila con el hash de la versión activa '
                                             '(`version_num`).',
                                             'Informa a Alembic qué revisiones faltan por aplicar durante el despliegue automático.'),
                                            ('Integración con CI/CD',
                                             'Ejecución de `alembic upgrade head` en el pipeline de despliegue antes de reiniciar el '
                                             'servidor web.',
                                             'Asegura que las nuevas tablas existan antes de que el nuevo código reciba tráfico.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en Migraciones',
                      'items': ['Agregar columnas `NOT NULL` sin definir un valor por defecto (*default*) en tablas que ya contienen '
                                'datos.',
                                'Editar modelos sin generar el script de migración correspondiente desincronizando código y DB.',
                                'Eliminar columnas en migraciones sin haber migrado previamente los datos existentes a una nueva '
                                'estructura.']}},
 25: {'tema': 'Consultas Complejas, Joins y Carga Ansiosa (Eager Loading)',
      'unidad': 'Bloque 3: Persistencia Relacional, ORM y OWASP',
      'teoria_principal': {'titulo': 'Optimización de Consultas ORM y Problema N+1',
                           'lead': 'El uso ingenuo de relaciones en ORMs puede desencadenar cientos de consultas repetitivas degradando '
                                   'drásticamente el rendimiento.',
                           'tarjetas': [('01. El Problema del N+1',
                                         'Ocurre cuando se consulta 1 lista de N elementos y luego el ORM emite N consultas individuales '
                                         'para traer sus hijos.',
                                         'Convierte una operación de milisegundos en segundos de latencia de red.'),
                                        ('02. Carga Ansiosa (`selectinload` / `joinedload`)',
                                         'Estrategias de precarga que traen el objeto y sus relaciones en 1 o 2 consultas SQL optimizadas.',
                                         '`selectinload` usa `WHERE id IN (...)`; `joinedload` realiza un `LEFT OUTER JOIN`.'),
                                        ('03. Filtros, Agregaciones y Paginación',
                                         'Uso de `select()`, `where()`, `group_by()`, `func.count()`, `limit()` y `offset()`.',
                                         'Sustituye el procesamiento en RAM de Python/PHP por el motor optimizado de SQL.')]},
      'arquitectura_memoria': {'titulo': 'Estrategias de Prefetching en Memoria',
                               'descripcion': 'Comparativa de rendimiento en consultas relacionales:',
                               'tarjetas': [('Diferencia entre Joined vs Selectin',
                                             '`joinedload` es ideal para relaciones 1:1 o M:1; `selectinload` es óptimo para relaciones '
                                             '1:N y N:M.',
                                             'Evita la multiplicación cartesiana de filas en arreglos grandes.'),
                                            ('Paginación Eficiente (`offset` / `limit`)',
                                             'Obligatoria en colecciones masivas para no cargar cientos de miles de registros en RAM.',
                                             'Reduce la huella de memoria del proceso del servidor.')]},
      'casos_borde': {'titulo': 'Antipatrones en Consultas ORM',
                      'items': ['Iterar sobre una colección de objetos sin usar `selectinload`, disparando el problema N+1.',
                                'Cargar colecciones enteras con `.all()` sin paginar en endpoints públicos.',
                                'Realizar filtrado de listas en memoria con Python (`[x for x in res if x.activo]`) en lugar de usar '
                                'cláusulas `where()` en SQL.']}},
 26: {'tema': 'Transacciones ACID, Aislamiento y Rollback',
      'unidad': 'Bloque 3: Persistencia Relacional, ORM y OWASP',
      'teoria_principal': {'titulo': 'Garantías de Consistencia A.C.I.D. en la Base de Datos',
                           'lead': 'Las transacciones agrupan múltiples operaciones de escritura bajo una garantía de todo-o-nada.',
                           'tarjetas': [('01. Propiedades A.C.I.D.',
                                         'Atomicidad (todo o nada), Consistencia (respeta reglas), Aislamiento (concurrencia), Durabilidad '
                                         '(persistencia en disco).',
                                         'Garantía fundamental en sistemas bancarios, reservas y comercio electrónico.'),
                                        ('02. Niveles de Aislamiento (Isolation Levels)',
                                         'Read Committed, Repeatable Read, Serializable.',
                                         'Controlan la visibilidad de cambios no confirmados entre consultas concurrentes.'),
                                        ('03. Manejo Estricto de Rollback',
                                         'Si ocurre cualquier error dentro del bloque transaccional, se invoca `await session.rollback()`.',
                                         'Descarta todos los cambios pendientes devolviendo la base de datos a su estado consistente '
                                         'previo.')]},
      'arquitectura_memoria': {'titulo': 'Manejador Transaccional Implícito',
                               'descripcion': 'Bloque `async with session.begin()`:',
                               'tarjetas': [('Gestión de Transacción Automática',
                                             'Abre la transacción al entrar; si el bloque concluye sin excepciones, emite `commit()`; si '
                                             'hay error, ejecuta `rollback()`.',
                                             'Elimina el código repetitivo de manejo manual de excepciones.'),
                                            ('Bloqueos Pessimistic vs Optimistic Locking',
                                             'Bloqueos explícitos (`SELECT FOR UPDATE`) para prevenir condiciones de carrera en '
                                             'inventarios o saldos.',
                                             'Garantiza exclusión mutua durante la modificación concorriente.')]},
      'casos_borde': {'titulo': 'Puntos de Falla Transaccionales',
                      'items': ['Condiciones de carrera (*Race Conditions*) por no usar transacciones o bloqueos al actualizar recursos '
                                'escasos.',
                                'Bloqueos mutuos (*Deadlocks*) causados por acceder a múltiples tablas en orden inverso en transacciones '
                                'paralelas.',
                                'Ignorar excepciones transaccionales y continuar ejecutando la lógica como si la escritura hubiese sido '
                                'exitosa.']}},
 27: {'tema': 'Blindaje OWASP: Prevención Total de SQL Injection (SQLi)',
      'unidad': 'Bloque 3: Persistencia Relacional, ORM y OWASP',
      'teoria_principal': {'titulo': 'Inyección SQL (OWASP Top 10 A03) y Consultas Parametrizadas',
                           'lead': 'SQL Injection ocurre cuando entradas no confiables se concatenan directamente en cadenas de consulta '
                                   'SQL.',
                           'tarjetas': [('01. Mecánica del Ataque SQLi',
                                         "Un atacante ingresa `' OR '1'='1` alterando la lógica del parser SQL para saltarse la "
                                         'autenticación o extraer tablas enteras.',
                                         'Es una de las vulnerabilidades más destructivas en la historia de la web.'),
                                        ('02. Consultas Parametrizadas (Prepared Statements)',
                                         'Separación física entre el código de la consulta y los datos de entrada.',
                                         'El motor SQL compila la plantilla primero; los datos se tratan estrictamente como valores '
                                         'literales, nunca como código ejecutable.'),
                                        ('03. Protección Nativa del ORM',
                                         'Los ORMs como SQLAlchemy compilan todas las consultas utilizando sentencias preparadas por '
                                         'defecto.',
                                         'Neutralizan automáticamente los intentos de inyección SQL sin esfuerzo adicional del '
                                         'desarrollador.')]},
      'arquitectura_memoria': {'titulo': 'Compilación de Sentencias Preparadas',
                               'descripcion': 'Diferencia entre concatenación frágil y parametrización:',
                               'tarjetas': [('Concatenación Vulnerable (Prohibida)',
                                             "`sql = 'SELECT * FROM users WHERE email = ' + input_usuario`.",
                                             'El texto del usuario altera el árbol sintáctico de la consulta SQL.'),
                                            ('Parametrización Segura',
                                             "`sql = 'SELECT * FROM users WHERE email = :email'`, `params={'email': input_usuario}`.",
                                             'El motor trata `:email` como un contenedor aislado de datos de texto.')]},
      'casos_borde': {'titulo': 'Vulnerabilidades Frecuentes de SQLi',
                      'items': ["Uso de SQL crudo con interpolación de cadenas `f'SELECT * FROM {tabla}'` o `text(...)` mal utilizado en "
                                'ORMs.',
                                'Concatenar nombres de columnas o tablas dinámicamente desde parámetros de la URL.',
                                "Confiar en filtros de palabras clave manuales (`replace('UNION', '')`) en lugar de usar sentencias "
                                'preparadas.']}},
 28: {'tema': 'Blindaje Web: Cross-Origin Resource Sharing (CORS)',
      'unidad': 'Bloque 3: Persistencia Relacional, ORM y OWASP',
      'teoria_principal': {'titulo': 'Política de Mismo Origen (SOP) y Configuración CORS',
                           'lead': 'CORS es un mecanismo de seguridad de los navegadores para restringir solicitudes HTTP originadas desde '
                                   'un dominio distinto.',
                           'tarjetas': [('01. Same-Origin Policy (SOP)',
                                         'Los navegadores bloquean por defecto que un script de `app.com` lea respuestas de `api.com` a '
                                         'menos que la API lo autorice.',
                                         'Protege a los usuarios de que sitios maliciosos consuman sus APIs privadas en segundo plano.'),
                                        ('02. Encabezados CORS (`Access-Control-Allow-*`)',
                                         'Respuestas enviadas por el servidor indicando dominios permitidos (`Origin`), métodos '
                                         '(`Methods`) y encabezados (`Headers`).',
                                         'Permite que la Single Page Application (SPA) se comunique legítimamente con el backend.'),
                                        ('03. Peticiones Pre-flight (OPTIONS)',
                                         'Petición preliminar automática del navegador para verificar si la operación real es segura antes '
                                         'de enviarla.',
                                         'El servidor debe responder con HTTP 200/204 y los encabezados CORS correspondientes.')]},
      'arquitectura_memoria': {'titulo': 'Middleware CORS en Servidor Web',
                               'descripcion': 'Inyección centralizada de encabezados de origen:',
                               'tarjetas': [('Configuración con Lista Blanca',
                                             "`CORSMiddleware(allow_origins=['https://midominio.com'], allow_credentials=True)`.",
                                             'Define explícitamente qué orígenes tienen acceso a los recursos.'),
                                            ("Peligro del Comodín `allow_origins=['*']`",
                                             'Permite que cualquier sitio web del mundo consuma la API.',
                                             'Incompatible y peligroso cuando se combina con envío de credenciales '
                                             '(`allow_credentials=True`).')]},
      'casos_borde': {'titulo': 'Antipatrones en Configuración CORS',
                      'items': ["Usar `allow_origins=['*']` en APIs de producción que manejan autenticación con cookies o tokens de "
                                'usuario.',
                                'Olvidar incluir encabezados personalizados (ej. `Authorization`, `X-Custom-Header`) en `allow_headers` '
                                'provocando bloqueos en el cliente.',
                                'Configurar CORS en el servidor web sin manejar correctamente las peticiones preliminares `OPTIONS`.']}},
 29: {'tema': 'Protección Anti-CSRF y Cookies HttpOnly / SameSite',
      'unidad': 'Bloque 3: Persistencia Relacional, ORM y OWASP',
      'teoria_principal': {'titulo': 'Falsificación de Peticiones (CSRF) y Seguridad de Cookies',
                           'lead': 'CSRF fuerza al navegador de una víctima autenticada a enviar peticiones no deseadas a una aplicación '
                                   'web confiable.',
                           'tarjetas': [('01. Mecánica del Ataque CSRF',
                                         'Si la autenticación usa Cookies automáticas, un sitio malicioso puede incluir un formulario '
                                         'oculto hacia `banco.com/transferir`.',
                                         'El navegador adjunta la Cookie de sesión automáticamente ejecutando la transacción sin el '
                                         'conocimiento del usuario.'),
                                        ('02. Flags de Seguridad en Cookies',
                                         '`HttpOnly` (impide acceso desde JavaScript/XSS), `Secure` (exige HTTPS), `SameSite=Lax/Strict` '
                                         '(restringe envío trans-sitio).',
                                         '`SameSite=Lax` es la defensa moderna más efectiva contra ataques CSRF.'),
                                        ('03. Tokens Anti-CSRF (Pattern Synchronizer Token)',
                                         'Token aleatorio único adjunto a la sesión que debe enviarse en el cuerpo/encabezado de cada '
                                         'petición mutable.',
                                         'Invalida peticiones originadas desde sitios externos que no poseen el token.')]},
      'arquitectura_memoria': {'titulo': 'Atributos de Cookies de Sesión Seguras',
                               'descripcion': 'Configuración del encabezado `Set-Cookie`:',
                               'tarjetas': [('Set-Cookie Header Estandarizado',
                                             '`Set-Cookie: session=xyz; Secure; HttpOnly; SameSite=Lax; Path=/; Max-Age=3600`.',
                                             'Blindaje multicapa que protege la sesión tanto en tránsito como en reposo en el cliente.'),
                                            ('Tokens Stateless vs CSRF',
                                             'Las APIs que leen el JWT exclusivamente desde el encabezado `Authorization: Bearer` son '
                                             'inmunes a CSRF de forma natural.',
                                             'El navegador no adjunta encabezados Authorization automáticamente.')]},
      'casos_borde': {'titulo': 'Vulnerabilidades de Sesión y Cookies',
                      'items': ['Omitir el flag `HttpOnly` permitiendo que un script XSS robe el identificador de sesión mediante '
                                '`document.cookie`.',
                                'Usar `SameSite=None` sin configurar la bandera `Secure` (rechazado por los navegadores modernos).',
                                'Confiar únicamente en el encabezado `Referer` para validar el origen de la petición en lugar de tokens '
                                'Anti-CSRF o cookies SameSite.']}},
 30: {'tema': 'Hito 3: API Persistente con ORM, Migraciones y Blindaje OWASP',
      'unidad': 'Bloque 3: Persistencia Relacional, ORM y OWASP',
      'teoria_principal': {'titulo': 'Integración del Tercer Hito: Persistencia y Seguridad Total',
                           'lead': 'Culminación del Bloque 3. La API cuenta con base de datos relacional, modelos ORM, migraciones de '
                                   'esquemas y protección OWASP.',
                           'tarjetas': [('01. Capa de Datos Transaccional Completa',
                                         'API que realiza operaciones CRUD sobre PostgreSQL/SQLite utilizando SQLAlchemy asíncrono, '
                                         'migraciones Alembic y repositorios desacoplados.',
                                         'Soporta consultas relacionales complejas sin incurrir en el problema N+1.'),
                                        ('02. Blindaje OWASP Verificado',
                                         'Protección completa contra SQLi (consultas parametrizadas), CORS configurado con listas blancas, '
                                         'cookies `HttpOnly; SameSite` y sanitización.',
                                         'Garantiza resiliencia técnica ante intentos de intrusión y ataques de inyección.'),
                                        ('03. Entrega de Hito 3 (Git Tag)',
                                         'Etiquetado formal de versión en el repositorio de GitHub del estudiante: `git tag v0.3-hito3`.',
                                         'Representa el 25% del Proyecto Integrador Semestral.')]},
      'arquitectura_memoria': {'titulo': 'Auditoría de Integridad de Persistencia y Seguridad',
                               'descripcion': 'Evaluación con el Test Harness de Base de Datos y Pen-Testing:',
                               'tarjetas': [('Pruebas de Estrés Transaccional y Penetración',
                                             'Ejecución automatizada de payloads SQLi, pruebas de rollbacks ante fallos, migraciones '
                                             '`upgrade/downgrade` y carga de datos.',
                                             'Certifica que la base de datos se mantenga consistente y la API inmune a exploits.'),
                                            ('Verificación de Conexiones y Migraciones',
                                             'Asegura que las migraciones se apliquen limpiamente con `alembic upgrade head` sin pérdida '
                                             'de información.',
                                             'Garantiza un entorno listo para el despliegue final en la nube.')]},
      'casos_borde': {'titulo': 'Criterios de Rechazo del Hito 3',
                      'items': ['API vulnerable a SQL Injection o que utilice consultas crudas concatenadas con cadenas.',
                                'Fallas de consistencia transaccional (datos huérfanos o commit parcial tras una excepción).',
                                'Incapacidad de ejecutar las migraciones de base de datos desde cero en una instancia limpia.']}},
 31: {'tema': 'Contenedorización Básica con Docker y Dockerfiles',
      'unidad': 'Bloque 4: Despliegue, Frontend SPA y Pruebas E2E',
      'teoria_principal': {'titulo': 'Contenedorización, Inmutabilidad y Aislamiento de Entornos',
                           'lead': 'Docker empaqueta el código, el runtime, las dependencias del sistema y la configuración en un '
                                   'contenedor inmutable.',
                           'tarjetas': [('01. Contenedores vs Máquinas Virtuales',
                                         'Los contenedores comparten el kernel del sistema operativo anfitrión, siendo órdenes de magnitud '
                                         'más ligeros y rápidos que una VM.',
                                         "Garantiza el principio 'corre exactamente igual en mi máquina que en producción'."),
                                        ('02. Anatomía de un Dockerfile',
                                         'Instrucciones base: `FROM python:3.11-slim`, `WORKDIR /app`, `COPY requirements.txt .`, `RUN pip '
                                         'install`, `COPY . .`, `CMD [...]`.',
                                         'Cada instrucción genera una capa de solo lectura en el sistema de archivos de la imagen.'),
                                        ('03. Construcción Multi-Etapa (Multi-Stage Builds)',
                                         'Separa el entorno de compilación (con compiladores pesados) del entorno final de ejecución '
                                         'ligero.',
                                         'Reduce el tamaño de la imagen de producción de cientos de MB a menos de 50 MB.')]},
      'arquitectura_memoria': {'titulo': 'Caché de Capas y Optimización de Imágenes',
                               'descripcion': 'Estrategias de construcción eficiente en Docker:',
                               'tarjetas': [('Orden de Instrucciones para Caché',
                                             'Copiar e instalar `requirements.txt` o `composer.json` antes de copiar el código fuente de '
                                             'la aplicación.',
                                             'Evita reinstalar dependencias en cada cambio de código, acelerando los builds en segundos.'),
                                            ('Archivo `.dockerignore`',
                                             'Excluye `.git`, `__pycache__`, `.env` y carpetas de pruebas de la imagen final.',
                                             'Previene la fuga accidental de credenciales y reduce el contexto de construcción.')]},
      'casos_borde': {'titulo': 'Antipatrones en Contenedorización',
                      'items': ['Ejecutar el contenedor como usuario `root` en producción, exponiendo el host a riesgos de escalamiento de '
                                'privilegios.',
                                'Copiar archivos de entorno `.env` con contraseñas dentro de la imagen pública de Docker.',
                                'Usar tags genéricos como `latest` en lugar de versiones fijas (`python:3.11.8-slim`), provocando roturas '
                                'inesperadas.']}},
 32: {'tema': 'Despliegue en la Nube (Render / Codespaces) y Env Vars',
      'unidad': 'Bloque 4: Despliegue, Frontend SPA y Pruebas E2E',
      'teoria_principal': {'titulo': 'Metodología 12-Factor App y Despliegue Continuo (CD)',
                           'lead': 'El despliegue moderno desacopla la configuración del código fuente mediante variables de entorno '
                                   'inyectadas en tiempo de ejecución.',
                           'tarjetas': [('01. The Twelve-Factor App (Configuración)',
                                         'Toda configuración que cambie entre entornos (Dev, Staging, Prod) debe residir en variables de '
                                         'entorno del sistema operativo.',
                                         'El código base es estrictamente el mismo en todos los despliegues.'),
                                        ('02. Plataformas PaaS (Render / Codespaces)',
                                         'Plataformas que automatizan la construcción, aprovisionamiento de certificados SSL/TLS y '
                                         'despliegue directo desde Git.',
                                         'Cada `git push origin main` dispara una compilación y despliegue sin tiempo de inactividad '
                                         '(*Zero-Downtime*).'),
                                        ('03. Gestión de Secretos y Variables Sensibles',
                                         'Las claves secretas (`SECRET_KEY`, `DATABASE_URL`) se configuran en el panel de la nube, nunca '
                                         'en el repositorio.',
                                         'Protege las credenciales corporativas ante repositorios públicos o filtraciones de código.')]},
      'arquitectura_memoria': {'titulo': 'Carga de Variables en Tiempo de Arranque',
                               'descripcion': 'Lectura segura con `pydantic-settings` o `getenv`:',
                               'tarjetas': [('Validación de Configuración al Arrancar',
                                             'La aplicación valida que todas las variables requeridas existan antes de abrir puertos de '
                                             'red.',
                                             'Falla rápido (*Fail-Fast*) si falta una variable crítica de base de datos.'),
                                            ('Terminación SSL/TLS Automática',
                                             "El PaaS gestiona los certificados HTTPS mediante Let's Encrypt de forma automática en el "
                                             'borde de la red.',
                                             'Cifra todo el tráfico entre el navegador del cliente y el balanceador del PaaS.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en Despliegues Cloud',
                      'items': ['Hacer commit del archivo `.env` local en GitHub exponiendo contraseñas de producción.',
                                'Codificar rutas locales fijas (`C:\\Users\\...` o `/home/ivan/...`) que no existen en el contenedor Linux '
                                'de producción.',
                                'No configurar el puerto dinámico asignado por el PaaS mediante la variable `$PORT`.']}},
 33: {'tema': 'Servidores ASGI / WSGI en Producción (Uvicorn / Nginx)',
      'unidad': 'Bloque 4: Despliegue, Frontend SPA y Pruebas E2E',
      'teoria_principal': {'titulo': 'Arquitectura de Servidores Web de Alto Rendimiento',
                           'lead': 'En producción, la aplicación web se ejecuta detrás de un servidor de aplicaciones concurrente '
                                   'coordinado por un Proxy Inverso.',
                           'tarjetas': [('01. ASGI (Asynchronous Server Gateway Interface)',
                                         'Estándar asíncrono para Python que maneja miles de conexiones concurrentes I/O mediante un bucle '
                                         'de eventos.',
                                         'Uvicorn implementa ASGI sobre uvloop (escrito en C) para máxima velocidad de despacho.'),
                                        ('02. Gestor de Procesos Worker (Gunicorn / Uvicorn Workers)',
                                         'Un proceso maestro coordina múltiples procesos trabajadores (*workers*) aprovechando todos los '
                                         'núcleos de la CPU.',
                                         'Si un worker colapsa por un error fatal, el maestro levanta uno nuevo instantáneamente.'),
                                        ('03. Proxy Inverso (Nginx)',
                                         'Servidor frontal que maneja SSL/TLS, compresión Gzip, archivos estáticos y balanceo hacia los '
                                         'workers de la API.',
                                         'Protege a los servidores de aplicaciones de ataques directos de saturación lenta '
                                         '(*Slowloris*).')]},
      'arquitectura_memoria': {'titulo': 'Modelo de Procesos Multi-Worker en Producción',
                               'descripcion': 'Distribución de carga sobre núcleos de hardware:',
                               'tarjetas': [('Fórmula de Workers de CPU',
                                             '`Num_Workers = (2 * Num_Cores) + 1`.',
                                             'Maximiza el uso de CPU manteniendo un worker activo mientras otros esperan operaciones de '
                                             'I/O de base de datos.'),
                                            ('Buffers y Timeouts de Nginx',
                                             'Nginx absorbe peticiones lentas de clientes móviles y las entrega a Uvicorn a velocidad de '
                                             'red local.',
                                             'Optimiza el rendimiento del runtime de backend.')]},
      'casos_borde': {'titulo': 'Antipatrones en Configuración de Servidores',
                      'items': ['Ejecutar `uvicorn main:app --reload` en producción (la bandera `--reload` consume memoria y degrada el '
                                'rendimiento).',
                                'Configurar un solo worker en servidores multi-core desaprovechando la capacidad de la máquina.',
                                'Servir archivos multimedia o estáticos pesados directamente desde FastAPI/PHP en lugar de usar Nginx o un '
                                'CDN.']}},
 34: {'tema': 'Integración Frontend: Fetch API y JavaScript Asíncrono',
      'unidad': 'Bloque 4: Despliegue, Frontend SPA y Pruebas E2E',
      'teoria_principal': {'titulo': 'Consumo de APIs REST desde el Navegador Cliente',
                           'lead': 'La API `fetch()` nativa permite al navegador realizar peticiones HTTP asíncronas sin recargar la '
                                   'página web.',
                           'tarjetas': [('01. Promesas y Sintaxis `async / await`',
                                         'Manejo limpio de operaciones asíncronas no bloqueantes en JavaScript.',
                                         'Permite escribir código asíncrono de red con estructura secuencial y legible.'),
                                        ('02. Configuración de Encabezados y Verbos',
                                         "Envío explicito de `method: 'POST'`, `headers: {'Content-Type': 'application/json'}` y `body: "
                                         'JSON.stringify(data)`.',
                                         'Conecta directamente la interfaz de usuario con los contratos de la API backend.'),
                                        ('03. Inyección del Token Authorization Bearer',
                                         'Extracción del JWT desde `localStorage` o memoria y envío en el encabezado `Authorization: '
                                         'Bearer ${token}`.',
                                         'Permite al cliente acceder a rutas privadas autenticadas.')]},
      'arquitectura_memoria': {'titulo': 'Ciclo de Respuesta y Parseo de JSON en Navegador',
                               'descripcion': 'Transformación de respuesta HTTP a objetos JavaScript:',
                               'tarjetas': [('Parseo en Dos Fases',
                                             '`const response = await fetch(...); const data = await response.json();`.',
                                             'La primera fase valida el código de estado (`response.ok`); la segunda deserializa el '
                                             'payload JSON.'),
                                            ('Manejo de Errores de Red vs HTTP',
                                             '`catch()` solo captura fallos de red físicos (sin conexión); los errores 4xx y 5xx deben '
                                             'validarse con `if (!response.ok)`.',
                                             'Garantiza mensajes de error adecuados para el usuario.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en Consumo de APIs',
                      'items': ['Olvidar usar `JSON.stringify()` al enviar objetos en el body, enviando `[object Object]` corrupto.',
                                'No capturar errores HTTP 401 para redirigir automáticamente al usuario a la pantalla de login.',
                                'Almacenar tokens sensibles en variables globales accesibles fácilmente por scripts de terceros.']}},
 35: {'tema': 'Renderizado Dinámico del DOM y Estado del Cliente',
      'unidad': 'Bloque 4: Despliegue, Frontend SPA y Pruebas E2E',
      'teoria_principal': {'titulo': 'Manipulación del DOM y Reactividad Ligera',
                           'lead': 'El cliente web moderno actualiza dinámicamente secciones específicas de la interfaz en respuesta a '
                                   'cambios de datos.',
                           'tarjetas': [('01. Document Object Model (DOM)',
                                         'Representación en árbol de nodos de la estructura HTML que JavaScript puede mutar en tiempo '
                                         'real.',
                                         'Permite insertar, modificar o eliminar elementos sin refrescar el navegador.'),
                                        ('02. Template Literals para Renderizado',
                                         'Uso de plantillas con backticks: `container.innerHTML = users.map(u => '
                                         "`<li>${u.nombre}</li>`).join('')`.",
                                         'Construye vistas dinámicas a partir de los arreglos JSON recibidos de la API.'),
                                        ('03. Gestión de Estado en Cliente (Client State)',
                                         'Objeto JavaScript centralizado que almacena los datos activos de la sesión y la vista actual.',
                                         'Cualquier mutación del estado dispara el re-renderizado de la interfaz correspondiente.')]},
      'arquitectura_memoria': {'titulo': 'Flujo de Renderizado Reactivo en Navegador',
                               'descripcion': 'Sincronización entre datos del backend y la pantalla:',
                               'tarjetas': [('Event Delegation en el DOM',
                                             'Escuchar eventos en un contenedor padre en lugar de asignar cientos de listeners a elementos '
                                             'hijos dinámicos.',
                                             'Optimiza el consumo de memoria en interfaces con tablas o listas extensas.'),
                                            ('Prevención de XSS en Renderizado',
                                             'Uso de `textContent` o funciones de escape en lugar de insertar cadenas no confiables '
                                             'directamente con `innerHTML`.',
                                             'Protege a los usuarios de scripts inyectados en la interfaz.')]},
      'casos_borde': {'titulo': 'Antipatrones en Manipulación del DOM',
                      'items': ['Reescribir todo el `document.body.innerHTML` en cada cambio de datos, destruyendo el foco del usuario y '
                                'el estado de formularios.',
                                'Fugas de memoria por no desvincular event listeners en elementos eliminados.',
                                'Insertar entradas de usuarios directamente con `innerHTML` permitiendo vulnerabilidades XSS en el '
                                'cliente.']}},
 36: {'tema': 'Arquitectura Single Page Application (SPA) Ligera',
      'unidad': 'Bloque 4: Despliegue, Frontend SPA y Pruebas E2E',
      'teoria_principal': {'titulo': 'Navegación Sin Recarga y Ruteo del Lado del Cliente',
                           'lead': 'Una SPA carga un solo documento HTML inicial y actualiza las vistas dinámicamente interceptando la '
                                   'navegación.',
                           'tarjetas': [('01. Ruteo por Hash (`#route`) y History API',
                                         'El navegador detecta cambios de ruta mediante `window.onhashchange` o `history.pushState()` sin '
                                         'solicitar una página nueva al servidor.',
                                         'Proporciona una experiencia de usuario fluida idéntica a una aplicación de escritorio.'),
                                        ('02. Arquitectura Basada en Componentes Vistas',
                                         'Cada ruta (`#/login`, `#/dashboard`, `#/usuarios`) se mapea a una función renderizadora '
                                         'independiente.',
                                         'Mantiene el código frontend modular, escalable y fácil de mantener.'),
                                        ('03. Desacoplamiento Total Frontend/Backend',
                                         'El frontend es un conjunto de archivos estáticos (HTML/CSS/JS); el backend es exclusivamente una '
                                         'API REST JSON.',
                                         'Permite alojar el frontend en servicios CDN ultrarrápidos (GitHub Pages / Vercel).')]},
      'arquitectura_memoria': {'titulo': 'Ruteador Minimalista en JavaScript',
                               'descripcion': 'Mapeo declarativo de rutas cliente:',
                               'tarjetas': [('Diccionario de Rutas',
                                             "`const routes = { '#/': HomeView, '#/login': LoginView, '#/perfil': ProfileView };`.",
                                             'El despachador lee `location.hash` e invoca la vista correspondiente en el contenedor '
                                             'principal.'),
                                            ('Guardias de Navegación (Route Guards)',
                                             'Funciones que verifican la existencia del JWT antes de renderizar una vista protegida.',
                                             'Si el usuario no está autenticado, redirige automáticamente a `#/login`.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en SPAs',
                      'items': ['Fallo de recarga en servidores al usar History API sin configurar el fallback a `index.html` (error 404 '
                                'en refresco).',
                                'Permitir que el usuario navegue a vistas privadas mediante manipulación del hash sin validar el token con '
                                'la API.',
                                'Acumular datos en memoria entre cambios de pantalla sin limpiar formularios ni tablas.']}},
 37: {'tema': 'Pruebas Automatizadas E2E con Postman / Newman CLI',
      'unidad': 'Bloque 4: Despliegue, Frontend SPA y Pruebas E2E',
      'teoria_principal': {'titulo': 'Pruebas de Integración End-to-End y Automatización CI/CD',
                           'lead': 'Las pruebas E2E verifican que el sistema completo (red, auth, lógica y base de datos) funcione '
                                   'armónicamente de inicio a fin.',
                           'tarjetas': [('01. Colecciones de Pruebas en Postman',
                                         'Flujos secuenciales de peticiones HTTP: 1. Registro -> 2. Login -> 3. Guardar Token -> 4. Crear '
                                         'Recurso -> 5. Consultar Recurso.',
                                         'Simula el comportamiento real de un usuario interactuando con la API.'),
                                        ('02. Aserciones JavaScript en Postman Tests',
                                         'Scripts de validación: `pm.response.to.have.status(200)`, '
                                         "`pm.expect(pm.response.json().status).to.eql('success')`.",
                                         'Valida automáticamente tanto los códigos de estado como el contenido de los payloads.'),
                                        ('03. Ejecución Automatizada con Newman CLI',
                                         'Herramienta de línea de comandos para ejecutar colecciones de Postman dentro de pipelines de '
                                         'GitHub Actions o scripts locales.',
                                         'Bloquea el paso a producción si alguna prueba de la suite falla.')]},
      'arquitectura_memoria': {'titulo': 'Variables Dinámicas de Entorno en Pruebas',
                               'descripcion': 'Paso de datos entre pasos de prueba consecutivos:',
                               'tarjetas': [('Extracción Automática de Tokens',
                                             "`pm.environment.set('token', pm.response.json().access_token);`.",
                                             'Inyecta el token obtenido en el login directamente en las peticiones subsecuentes de la '
                                             'colección.'),
                                            ('Reportes de Cobertura y Fallos',
                                             'Newman emite reportes en formato CLI, HTML o JUnit XML.',
                                             'Facilita la auditoría visual y la trazabilidad de regresiones en el código.')]},
      'casos_borde': {'titulo': 'Antipatrones en Pruebas E2E',
                      'items': ['Pruebas interdependientes que fallan si no se ejecutan en un orden estricto específico.',
                                'No limpiar los datos de prueba creados en la base de datos tras la ejecución de la suite.',
                                'Escribir aserciones que solo verifican el código HTTP (200) sin validar la estructura del JSON '
                                'devuelto.']}},
 38: {'tema': 'Tareas en Segundo Plano (Background Tasks) Asíncronas',
      'unidad': 'Bloque 4: Despliegue, Frontend SPA y Pruebas E2E',
      'teoria_principal': {'titulo': 'Procesamiento Diferido y Operaciones No Bloqueantes',
                           'lead': 'Las tareas pesadas (envío de correos, generación de reportes, procesamiento de imágenes) deben '
                                   'ejecutarse fuera del ciclo Request/Response.',
                           'tarjetas': [('01. Respuesta Inmediata (HTTP 202 Accepted)',
                                         'El servidor acepta la petición, delega el procesamiento a un worker en segundo plano y responde '
                                         'al cliente de inmediato.',
                                         'Reduce la latencia de respuesta de segundos a milisegundos.'),
                                        ('02. FastAPI `BackgroundTasks`',
                                         'Mecanismo nativo ligero para ejecutar funciones asíncronas inmediatamente después de devolver la '
                                         'respuesta HTTP.',
                                         'Ideal para operaciones secundarias que no requieren colas distribuidas complejas.'),
                                        ('03. Colas Distribuidas (Celery / Redis / RabbitMQ)',
                                         'Arquitectura industrial para procesamiento masivo distribuido con reintentos y persistencia de '
                                         'tareas.',
                                         'Permite procesar millones de trabajos en paralelo desacoplados de la API web.')]},
      'arquitectura_memoria': {'titulo': 'Ciclo de Ejecución en Background',
                               'descripcion': 'Separación del hilo web y el worker de procesamiento:',
                               'tarjetas': [('Inyección de `BackgroundTasks`',
                                             '`def registrar(user: UserDTO, bg: BackgroundTasks): bg.add_task(enviar_email, user.email); '
                                             "return {'ok': True}`.",
                                             'El email se procesa después de enviar los bytes de respuesta al cliente.'),
                                            ('Manejo de Errores en Tareas Asíncronas',
                                             'Las excepciones en background no afectan la respuesta enviada al usuario.',
                                             'Requiere registro centralizado de logs para auditar fallos en tareas diferidas.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en Background Tasks',
                      'items': ['Pasar sesiones de base de datos activas a tareas en background que se cierran al terminar la petición '
                                'HTTP.',
                                'Saturar el pool de hilos del servidor con tareas intensivas en CPU que bloquean el bucle de eventos.',
                                'Perder tareas críticas en memoria si el servidor se reinicia antes de ejecutarlas (requiere colas '
                                'persistentes).']}},
 39: {'tema': 'Monitoreo, Métricas de Salud (/health) y Profiling Web',
      'unidad': 'Bloque 4: Despliegue, Frontend SPA y Pruebas E2E',
      'teoria_principal': {'titulo': 'Observabilidad, Healthchecks y Métricas en Producción',
                           'lead': 'Una aplicación en producción debe exponer su estado interno para que balanceadores y sistemas de '
                                   'monitoreo puedan supervisarla.',
                           'tarjetas': [('01. Endpoint de Salud (`/health` o `/status`)',
                                         'Ruta estandarizada que verifica la conectividad con la base de datos, memoria disponible y '
                                         'servicios externos.',
                                         'Devuelve `HTTP 200 OK` si el sistema está operativo o `HTTP 503 Service Unavailable` si hay '
                                         'fallas.'),
                                        ('02. Liveness vs Readiness Probes',
                                         "Liveness: '¿El proceso del servidor está vivo?'. Readiness: '¿El servidor está listo para "
                                         "recibir tráfico y la DB conectada?'.",
                                         'Estándar utilizado por Kubernetes, Render y AWS para reiniciar contenedores colgados.'),
                                        ('03. Métricas de Rendimiento (Latencia P95 / P99)',
                                         'Monitoreo del percentil de tiempo de respuesta para identificar el 5% o 1% de peticiones más '
                                         'lentas del sistema.',
                                         'Permite detectar cuellos de botella antes de que afecten a la mayoría de los usuarios.')]},
      'arquitectura_memoria': {'titulo': 'Diagnóstico y Profiling en Tiempo Real',
                               'descripcion': 'Inspección de salud del servicio web:',
                               'tarjetas': [('Estructura JSON de Healthcheck',
                                             "`{'status': 'healthy', 'db': 'connected', 'version': '1.0.0', 'uptime': 3600}`.",
                                             'Permite a herramientas como UptimeRobot o Prometheus alertar incidentes en tiempo real.'),
                                            ('Profiling de Endpoints Lentos',
                                             'Uso de middlewares de tiempo para identificar qué consultas de base de datos consumen más de '
                                             '500 ms.',
                                             'Guía las optimizaciones de índices y caché en la aplicación.')]},
      'casos_borde': {'titulo': 'Antipatrones en Monitoreo Web',
                      'items': ['Healthchecks pesados que ejecutan consultas masivas en la base de datos en cada sondeo cada 5 segundos.',
                                'Retornar HTTP 200 en `/health` a pesar de que la base de datos esté desconectada.',
                                'Exponer información sensible de infraestructura (versiones exactas de kernels o contraseñas) en el '
                                'endpoint público de salud.']}},
 40: {'tema': 'Hito 4: Demostración API Full-Stack en Producción con SPA',
      'unidad': 'Bloque 4: Despliegue, Frontend SPA y Pruebas E2E',
      'teoria_principal': {'titulo': 'Evaluación Integradora y Demostración de la Plataforma Web',
                           'lead': 'Culminación del curso. Demostración práctica de una plataforma web Full-Stack completa, segura y '
                                   'desplegada en la nube con SPA reactiva.',
                           'tarjetas': [('01. Sistema Full-Stack Integrado',
                                         'Backend RESTful asíncrono con base de datos relacional, auth JWT, RBAC, validación estricta y '
                                         'frontend SPA dinámico.',
                                         'Demuestra el dominio de la arquitectura web de extremo a extremo.'),
                                        ('02. Despliegue Público en Producción',
                                         'API y cliente web accesibles públicamente con HTTPS en la nube (Render / Codespaces / GitHub '
                                         'Pages).',
                                         'Evidencia formal de software desplegado con estándares profesionales de la industria.'),
                                        ('03. Entrega Final y Release en GitHub',
                                         'Etiquetado formal de la versión definitiva en el repositorio: `git tag v1.0-final`.',
                                         'Concluye el 30% del Proyecto Integrador y la acreditación final del curso.')]},
      'arquitectura_memoria': {'titulo': 'Auditoría Final y Criterios de Acreditación',
                               'descripcion': 'Verificación del ecosistema en vivo:',
                               'tarjetas': [('Suite E2E Automatizada Exitosa',
                                             'Ejecución al 100% de la colección de pruebas en Newman/Postman validando todos los flujos de '
                                             'usuario.',
                                             'Certifica la solidez técnica y ausencia de regresiones en la plataforma.'),
                                            ('Documentación de Arquitectura Completa',
                                             'Especificación OpenAPI viva, esquemas de base de datos, diagrama de capas y bitácoras de '
                                             'auditoría en GitHub.',
                                             'Constituye el portafolio profesional de evidencias del estudiante.')]},
      'casos_borde': {'titulo': 'Criterios de Acreditación del Hito 4',
                      'items': ['La aplicación debe estar desplegada en la nube y accesible mediante HTTPS sin errores de servidor.',
                                'El frontend SPA debe consumir la API REST de forma reactiva con manejo de tokens JWT y roles.',
                                'El repositorio en GitHub debe contener las 40 bitácoras de auditoría completas y el tag `v1.0-final`.']}}}
