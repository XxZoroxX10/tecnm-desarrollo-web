# Bitácora de la Sesión 07 — Especificación OpenAPI (Swagger) y ReDoc

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 17/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu contrato OpenAPI se verá así

> Llegué al resultado completo: 4/4 casos en verde (OpenAPI 3.1.0 con metadatos y esquema `Libro`, Swagger UI, ReDoc y el endpoint documentado).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. OpenAPI responde con metadatos
✅ 02. Swagger UI está disponible
✅ 03. ReDoc está disponible
✅ 04. El endpoint documentado responde
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] OpenAPI responde con metadatos → HTTP 200
- [x] Swagger UI está disponible → HTTP 200
- [x] ReDoc está disponible → HTTP 200
- [x] El endpoint documentado responde → HTTP 200

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI genera OpenAPI 3.1 automáticamente a partir de `title`, `version`, `description` y los modelos Pydantic; Swagger UI en `/docs` y ReDoc en `/redoc` |
| **Rol** | Desarrollador backend que documenta el contrato para que otro equipo consuma la API sin tener que preguntar |
| **Especificación** | App «Biblioteca API» v1.0.0 con descripción; `GET /api/libros` → 200 `{"libros": []}` usando el modelo `Libro` (para que aparezca en `components.schemas`); `GET /api/libros/{id}` documenta su respuesta 404 |
| **Output** | Solo `app.py`, con `response_model`, `summary`, `tags`, ejemplos y respuestas de error documentadas |

### Prompt que utilicé

```text
Rol: desarrollador backend que documenta APIs con OpenAPI.
Contexto: FastAPI (genera OpenAPI 3.1 solo).
Quiero:
- App con title "Biblioteca API", version "1.0.0" y una descripción.
- Modelo Pydantic Libro (id, titulo, anio) con descripciones y ejemplos.
- GET /api/libros -> 200 {"libros": [...]} usando response_model, para que Libro aparezca en components.schemas.
- GET /api/libros/{id} que documente también su respuesta 404.
- Tags y summary en las rutas. /docs y /redoc deben funcionar.
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Usé los parámetros de `FastAPI(...)` para los metadatos (título, versión, descripción y contacto), y `openapi_tags` para agrupar las rutas en la documentación.
>
> El punto clave fue que el esquema `Libro` solo aparece en `components.schemas` si **algún endpoint lo usa**. Por eso el listado tiene `response_model=ListaLibros`, que contiene una lista de `Libro`. Si regresara un `dict` suelto, la documentación no mostraría la forma del libro.
>
> En `GET /api/libros/{id}` agregué `responses={404: ...}` para que la documentación muestre también el error y no solo el 200, que es uno de los antipatrones de la presentación.
>
> Les puse ejemplos (`examples`) a los campos para que Swagger UI muestre datos reales en lugar de `"string"`.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Mi primera idea fue regresar `{"libros": []}` directo, sin modelo. Funciona, pero el caso 01 pide que `Libro` exista en `components.schemas`, y sin `response_model` FastAPI no tiene forma de saberlo. Ahí entendí que la documentación sale del código: si el código no declara el modelo, el contrato no lo muestra.
>
> También vi que `/docs` regresa 200 aunque las hojas de estilo de Swagger se carguen desde internet (CDN): el verificador solo revisa que el HTML exista y diga "swagger".
>
> Aprendí que OpenAPI no es un documento aparte que se escribe a mano: es el contrato vivo que se genera del código, por eso nunca se desactualiza.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/169dd36
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion07/sesion07_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion07.html

---
**Firma digital:** `XxZoroxX10`
