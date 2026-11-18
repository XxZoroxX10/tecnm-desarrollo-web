# Bitácora de la Sesión 10 — Hito 1: Mock API RESTful con OpenAPI y Validation Harness

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu Mock API del Hito 1 se comportará así

> Llegué al resultado completo del Hito 1: 9/9 casos en verde (CRUD completo, 404 después de borrar, 422 por datos inválidos, 405 en PATCH y OpenAPI con el esquema `Libro`).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 9 casos · app.py
==============================================================================
✅ 01. Listado inicial vacío
✅ 02. Creación válida
✅ 03. Consulta del libro creado
✅ 04. Actualización del libro
✅ 05. Eliminación del libro
✅ 06. El libro eliminado ya no existe
✅ 07. Validación de datos inválidos
✅ 08. Método no permitido
✅ 09. Contrato OpenAPI disponible
------------------------------------------------------------------------------
RESULTADO: 9/9 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Listado inicial vacío → HTTP 200
- [x] Creación válida → HTTP 201
- [x] Consulta del libro creado → HTTP 200
- [x] Actualización del libro → HTTP 200
- [x] Eliminación del libro → HTTP 204
- [x] El libro eliminado ya no existe → HTTP 404
- [x] Validación de datos inválidos → HTTP 422
- [x] Método no permitido → HTTP 405
- [x] Contrato OpenAPI disponible → HTTP 200

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + Pydantic v2, Mock API en memoria (sin BD) que integra todo el Bloque 1: CRUD, DTOs, OpenAPI, errores uniformes y middleware |
| **Rol** | Arquitecto backend que trabaja contract-first: primero la tabla de casos y después el código |
| **Especificación** | CRUD `/api/libros` con ids asignados por el servidor (201/200/204/404); `titulo` no vacío y `anio` 1450–2100, si no 422 con sobre `VALIDACION`; `PATCH` → 405; `/openapi.json` con el esquema `Libro`; ningún 500 con traceback |
| **Output** | Solo `app.py`, organizado por secciones: DTOs, errores, middleware, repositorio y rutas |

### Prompt que utilicé

```text
Rol: arquitecto backend. Trabajo contract-first.
Contexto: FastAPI + Pydantic v2, Mock API en memoria para el Hito 1.
Tabla de casos que debe cumplir:
1. GET /api/libros -> 200 {"libros": []}
2. POST /api/libros {"titulo","anio"} -> 201 con id 1 (y header Location)
3. GET /api/libros/1 -> 200
4. PUT /api/libros/1 -> 200 (reemplazo total)
5. DELETE /api/libros/1 -> 204 sin cuerpo
6. GET /api/libros/1 -> 404
7. POST con titulo vacío o anio 1200 -> 422
8. PATCH /api/libros/1 -> 405
9. GET /openapi.json con /api/libros y el esquema Libro
Requisitos extra: errores con sobre {"error": {"codigo","mensaje"}}, handler de último recurso sin traceback,
middleware con X-Request-ID y X-Process-Time, extra="forbid" en la entrada, responses de error documentadas.
Devuelve solo app.py organizado por secciones.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Armé el archivo por capas, aunque todavía sea un solo `app.py`: DTOs → errores → middleware → repositorio en memoria → rutas. Esto me prepara para la sesión 11, donde se separa en archivos.
>
> Reutilicé lo de cada sesión: ids con contador (02), `extra="forbid"` y `StringConstraints` con `strip` (05–06), `response_model` y `responses` documentadas (07), sobre de error único con handlers globales (08) y middleware de trazabilidad (09). Además, el 201 regresa el encabezado `Location` con la URL del recurso nuevo.
>
> En el borde valido forma y rangos (DTO); la regla "el libro debe existir" es de negocio y vive en `_buscar()`, que lanza `LibroNoEncontrado`.
>
> Si otro equipo la consumiera, versionaría las rutas (`/api/v1/...`) antes de cambiar el contrato.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Empecé por la tabla de los 9 casos, como dice la pista, y eso me evitó un error: en el caso 07 el título viene vacío **y** el año es 1200, así que hay dos errores de validación al mismo tiempo. Mi handler junta todos los campos con error en el mensaje, en lugar de quedarse solo con el primero.
>
> Al juntar los handlers de la sesión 08 con el middleware de la 09, revisé que el 405 de PATCH siguiera llevando el encabezado `Allow`: lo conservo pasando `headers` en el handler de `StarletteHTTPException`.
>
> Lo que haría distinto: escribir la tabla de casos dentro del README del proyecto integrador, porque el Hito 1 del equipo se evalúa igual (8 pruebas mínimas).

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/1ce293c
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion10/sesion10_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion10.html

---
**Firma digital:** `XxZoroxX10`
