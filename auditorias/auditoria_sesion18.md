# Bitácora de la Sesión 18 — Rate Limiting, Throttling y Prevención de Abuso

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu límite de peticiones se verá así

> Llegué al resultado completo: 4/4 casos en verde. Las tres primeras peticiones pasan y la cuarta dentro del mismo minuto recibe 429 con el encabezado Retry-After.

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. Primera petición permitida
✅ 02. Segunda petición permitida
✅ 03. Tercera petición permitida
✅ 04. La cuarta petición se limita
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Primera petición permitida → HTTP 200
- [x] Segunda petición permitida → HTTP 200
- [x] Tercera petición permitida → HTTP 200
- [x] La cuarta petición se limita → HTTP 429

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI con un middleware HTTP propio; estado en memoria con `collections.deque`; reloj `time.monotonic()` |
| **Rol** | Desarrollador backend que protege la API contra abuso (rate limiting) |
| **Especificación** | Máximo 3 peticiones por cliente cada 60 s en rutas `/api/`; la petición que excede → 429 `{"error", "reintentar_en_segundos"}` con `Retry-After`; respuestas permitidas con `X-RateLimit-Limit` y `X-RateLimit-Remaining`; `GET /api/recurso` → 200 `{"mensaje": "recurso disponible"}` |
| **Output** | Solo `app.py` |

### Prompt que utilicé

```text
Rol: desarrollador backend.
Contexto: FastAPI, sin librerías externas de rate limiting (quiero entender cómo funciona).
- Middleware HTTP que limite a 3 peticiones por cliente cada 60 segundos, solo en rutas que empiecen con /api/.
- Usa ventana deslizante: guarda las marcas de tiempo por cliente en un deque y descarta las que ya salieron de la ventana. Usa time.monotonic().
- El cliente se identifica por request.client.host.
- Si excede -> 429 con JSON {"error": "límite de peticiones alcanzado", "reintentar_en_segundos": N} y encabezado Retry-After.
- En respuestas permitidas agrega X-RateLimit-Limit y X-RateLimit-Remaining.
- GET /api/recurso -> 200 {"mensaje": "recurso disponible"}.
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Usé una **ventana deslizante** y no una ventana fija. Con ventana fija (contador que se reinicia cada minuto "de reloj") alguien puede mandar 3 peticiones a las 12:00:59 y otras 3 a las 12:01:00: seis en un segundo. Con el `deque` guardo la hora de cada petición y solo cuento las de los últimos 60 s.
>
> Detalles que cuidé:
> - `time.monotonic()` en lugar de `time.time()`, porque el reloj del sistema puede ajustarse hacia atrás y el monotónico no.
> - El contador es **por cliente** (`request.client.host`), no global, para que un abusador no bloquee a todos.
> - La respuesta 429 lleva `Retry-After` con los segundos que faltan, redondeados hacia arriba, y mínimo 1.
> - Solo limito rutas `/api/`; la documentación no cuenta.
>
> Lo hice como middleware porque así aplica a todas las rutas sin tocar cada endpoint.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Un detalle en el que me fijé al revisar el código: el `append` de la marca de tiempo tiene que ir **después** de revisar el límite. Si se hiciera antes, las peticiones rechazadas también se contarían y un cliente que siguiera insistiendo nunca saldría del bloqueo. Por eso solo se registran las peticiones permitidas.
>
> Hallazgos que dejo anotados para cuando esto vaya a producción:
> - El historial vive en la memoria del proceso. Si la app corre con varios *workers*, cada uno tiene su propio contador y el límite real se multiplica; ahí se usa algo compartido como Redis.
> - Detrás de un proxy o balanceador, `request.client.host` es la IP del proxy y todos los usuarios compartirían el mismo límite; habría que leer `X-Forwarded-For`, pero solo si el proxy es de confianza, porque ese encabezado lo puede falsificar el cliente.
> - El `defaultdict` nunca borra clientes viejos; con mucho tráfico crecería sin límite.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/b38980d
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion18/sesion18_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion18.html

---
**Firma digital:** `XxZoroxX10`
