# Bitácora de la Sesión 05 — Pydantic v2 / DTOs en PHP y Tipado Estático

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 17/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu DTO aceptará y rechazará exactamente esto

> Llegué al resultado completo: 5/5 casos en verde (creación válida, coerción de "1966" a 1966, 422 por año no numérico, 422 por campo extra y listado).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 5 casos · app.py
==============================================================================
✅ 01. Un libro válido se crea con 201
✅ 02. La cadena numérica se convierte a entero
✅ 03. Un año no numérico produce 422
✅ 04. Un campo extra produce 422
✅ 05. El listado devuelve los libros creados
------------------------------------------------------------------------------
RESULTADO: 5/5 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Un libro válido se crea con 201 → HTTP 201
- [x] La cadena numérica se convierte a entero → HTTP 201
- [x] Un año no numérico produce 422 → HTTP 422
- [x] Un campo extra produce 422 → HTTP 422
- [x] El listado devuelve los libros creados → HTTP 200

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + Pydantic v2 (modo lax por defecto, que permite la coerción de "1966" a 1966) en Colab |
| **Rol** | Desarrollador backend que define contratos de datos (DTO) cerrados y separa la entrada de la salida |
| **Especificación** | `POST /api/libros` con `titulo:str`, `anio:int`, `precio:float`, `disponible:bool` y `extra="forbid"` → 201 con `id`; tipo no convertible o campo extra → 422; `GET /api/libros` → 200 `{"libros": [...]}` con el DTO de salida |
| **Output** | Solo `app.py`, con `LibroEntrada`, `LibroSalida` y `response_model` en cada ruta |

### Prompt que utilicé

```text
Actúa como desarrollador backend con Pydantic v2.
Contexto: FastAPI, libros guardados en memoria.
Especificación:
- DTO de entrada LibroEntrada: titulo (str), anio (int), precio (float), disponible (bool). Contrato cerrado con model_config = ConfigDict(extra="forbid").
- "1966" debe convertirse a 1966; "mil novecientos" debe responder 422. Un campo desconocido (ej. "color") debe responder 422.
- DTO de salida LibroSalida con id + los mismos campos; la respuesta no inventa campos.
- POST /api/libros -> 201 con el libro creado (id empieza en 1). GET /api/libros -> 200 {"libros": [...]}.
Output: solo app.py, usando response_model en las rutas.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Hice tres modelos: `LibroEntrada` (lo que el cliente **puede** mandar), `LibroSalida` (lo que el cliente **puede** ver) y `ListaLibros` para el listado. Aunque hoy tienen casi los mismos campos, separarlos me sirve para el proyecto: cuando haya base de datos no quiero exponer campos internos por accidente.
>
> `extra="forbid"` lo puse solo en la entrada. Eso evita el *mass assignment*: si alguien manda `"admin": true` o `"color": "rojo"`, se rechaza con 422 en vez de ignorarlo en silencio.
>
> Además de los tipos, agregué reglas: `titulo` de 1 a 200 caracteres, `anio` entre 0 y 2100 y `precio >= 0`, porque un precio negativo pasa el tipo `float` pero no tiene sentido para el negocio.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> La coerción me sorprendió en los dos sentidos. Pydantic convierte `"1966"` → `1966` (lo que pide el contrato), pero en modo lax también acepta cosas que yo no esperaba: por ejemplo, para un `bool` acepta `"yes"`, `"true"` o `1`, y en `precio` el entero `180` llega como `180.0`. El verificador no lo revisa, pero lo anoto porque en un campo delicado convendría `strict=True`.
>
> El caso que más me ayudó a entender el 422 fue `"mil novecientos"`: el JSON está bien escrito (no es un 400), pero el dato no cumple el esquema, por eso es **422 Unprocessable Entity**, con el detalle del campo que falló.
>
> La próxima vez pensaría desde el principio en qué valores válidos de tipo son inválidos de negocio (como un precio negativo).

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/0019541
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion05/sesion05_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion05.html

---
**Firma digital:** `XxZoroxX10`
