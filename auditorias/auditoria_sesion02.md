# Bitácora de la Sesión 02 — Gestión en GitHub Web y Métodos HTTP (GET, POST, PUT, DELETE)

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 17/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu CRUD de libros responderá exactamente así

> Llegué al resultado completo: 8/8 casos en verde (CRUD completo, 404 después de borrar y 405 para PATCH).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 8 casos · app.py
==============================================================================
✅ 01. La colección inicia vacía
✅ 02. POST crea el libro con id 1
✅ 03. GET lista el libro creado
✅ 04. GET por id encuentra el libro
✅ 05. PUT reemplaza el libro
✅ 06. DELETE elimina el libro
✅ 07. El libro eliminado ya no existe
✅ 08. PATCH no está implementado: 405, no 404
------------------------------------------------------------------------------
RESULTADO: 8/8 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] La colección inicia vacía → HTTP 200
- [x] POST crea el libro con id 1 → HTTP 201
- [x] GET lista el libro creado → HTTP 200
- [x] GET por id encuentra el libro → HTTP 200
- [x] PUT reemplaza el libro → HTTP 200
- [x] DELETE elimina el libro → HTTP 204
- [x] El libro eliminado ya no existe → HTTP 404
- [x] PATCH no está implementado: 405, no 404 → HTTP 405

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + Pydantic v2, colección en memoria (sin base de datos), verificado con `TestClient` en Colab |
| **Rol** | Desarrollador backend que respeta la semántica de los verbos HTTP |
| **Especificación** | `GET /api/libros` → 200 `{"libros": [...]}`; `POST` → 201 con id asignado por el servidor; `GET /{id}` → 200 o 404; `PUT /{id}` → 200 (reemplazo total); `DELETE /{id}` → 204 sin cuerpo; `PATCH` no implementado → 405 |
| **Output** | Solo `app.py`, con modelo de entrada y de salida y `status_code` explícito en cada ruta |

### Prompt que utilicé

```text
Rol: desarrollador backend que respeta la semántica HTTP.
Contexto: FastAPI + Pydantic v2, guardando los libros en memoria (sin base de datos).
Especificación:
- GET /api/libros -> 200 {"libros": [...]} (empieza vacía).
- POST /api/libros con {"titulo": str, "anio": int} -> 201 con el libro y un id que asigna el servidor (empieza en 1).
- GET /api/libros/{id} -> 200 o 404 si no existe.
- PUT /api/libros/{id} -> reemplaza todo el libro, 200; 404 si no existe.
- DELETE /api/libros/{id} -> 204 sin cuerpo; 404 si no existe.
- PATCH no se implementa: debe responder 405, no 404.
Output: solo el código de app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Guardé los libros en un diccionario `id -> Libro` en lugar de una lista, porque buscar, reemplazar y borrar por id es directo. El id lo saco de un contador (`siguiente_id`) y no de `len(libros) + 1`: si borro el libro 1 y luego creo otro con `len + 1`, se repetirían ids y eso rompe la identidad del recurso.
>
> Hice una función `buscar()` que lanza el 404, y la reutilizo en GET, PUT y DELETE para no repetir el mismo `if` tres veces.
>
> PUT lo hice como reemplazo total: si el libro no existe respondo 404 en vez de crearlo, porque el id lo controla el servidor.
>
> Si otro equipo consumiera la API, agregaría el encabezado `Location: /api/libros/{id}` en el 201 para que sepan dónde quedó el recurso nuevo.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Mi primer error de concepto fue pensar en programar el caso de PATCH a mano (por ejemplo, una ruta PATCH que regresara 405). No hace falta: si la ruta `/api/libros/{id}` ya existe con GET/PUT/DELETE, FastAPI responde **405** solo para los verbos que no definí, y además manda el encabezado `Allow`. Si lo hubiera programado mal podría haber salido un 404, que es justo lo que el caso 08 detecta.
>
> También cuidé que DELETE regrese 204 **sin cuerpo**: regresar un JSON con 204 está mal según HTTP.
>
> Aprendí la diferencia clave: 404 = el recurso no existe; 405 = el recurso existe pero ese verbo no está permitido.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/aede242
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion02/sesion02_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion02.html

---
**Firma digital:** `XxZoroxX10`
