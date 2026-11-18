# Bitácora de la Sesión 08 — Respuestas Semánticas y Excepciones HTTP Personalizadas

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tus errores se verán exactamente así

> Llegué al resultado completo: 4/4 casos en verde (200 para el libro 1, 404 con sobre `NO_ENCONTRADO`, 422 con sobre `VALIDACION` y 201 para un libro válido).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. Un libro existente responde 200
✅ 02. Un libro inexistente responde 404 con sobre de error
✅ 03. Los datos inválidos responden 422 con sobre de error
✅ 04. Un libro válido sigue respondiendo 201
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Un libro existente responde 200 → HTTP 200
- [x] Un libro inexistente responde 404 con sobre de error → HTTP 404
- [x] Los datos inválidos responden 422 con sobre de error → HTTP 422
- [x] Un libro válido sigue respondiendo 201 → HTTP 201

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI con manejadores globales `@app.exception_handler` para excepciones de negocio, de validación y HTTP |
| **Rol** | Desarrollador backend que estandariza las respuestas de error y nunca expone tracebacks |
| **Especificación** | Sobre único `{"error": {"codigo", "mensaje"}}`; `LibroNoEncontrado` → 404 `NO_ENCONTRADO`; validación → 422 `VALIDACION` (incluye título vacío); semilla libro 1 «Rayuela»; `GET /api/libros/1` → 200, `/99` → 404; `POST` válido → 201; ningún caso produce 500 |
| **Output** | Solo `app.py`, con la excepción, los handlers y los modelos |

### Prompt que utilicé

```text
Actúa como desarrollador backend que diseña el manejo de errores de una API.
Contexto: FastAPI + Pydantic v2.
Especificación:
- Excepción de negocio LibroNoEncontrado con un handler que responda 404:
  {"error": {"codigo": "NO_ENCONTRADO", "mensaje": "..."}}
- Handler para RequestValidationError: 422 con el mismo sobre y codigo "VALIDACION" (un titulo vacío debe fallar).
- Que los 404/405 del router también usen el sobre.
- Un handler de último recurso que responda 500 sin mostrar el traceback.
- Datos iniciales: libro 1 "Rayuela" (1963). GET /api/libros/{id} y POST /api/libros (201).
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Hice una función `sobre()` que arma siempre `{"error": {"codigo", "mensaje"}}`, y todos los handlers la usan. Así el cliente procesa cualquier error de la misma forma.
>
> Registré cuatro manejadores:
> 1. `LibroNoEncontrado` → 404 `NO_ENCONTRADO` (error de negocio).
> 2. `RequestValidationError` → 422 `VALIDACION`, con una lista de `campo` + `mensaje`. No regreso el valor que mandó el cliente para no reflejar datos que podrían ser maliciosos.
> 3. `StarletteHTTPException` → 404/405 del router con el mismo sobre.
> 4. `Exception` → 500 `ERROR_INTERNO` genérico: el detalle se queda en el log del servidor y no se le muestra al usuario.
>
> El endpoint solo hace `raise LibroNoEncontrado(id)`; no sabe nada del formato HTTP del error, eso lo decide el handler.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Al principio registré el handler con `fastapi.HTTPException`, pero los 404 de rutas que no existen y los 405 los lanza Starlette, no FastAPI, y salían con el formato por defecto (`{"detail": ...}`). Lo corregí registrando `starlette.exceptions.HTTPException`, que es la clase padre y cubre los dos casos.
>
> Otro detalle: en `exc.errors()` la ubicación viene como `("body", "titulo")`; quité el primer elemento para que el cliente vea solo `titulo`.
>
> Aprendí que el formato de error es parte del contrato, igual que el de éxito, y que un 500 con traceback es una fuga de información.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/a2536ee
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion08/sesion08_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion08.html

---
**Firma digital:** `XxZoroxX10`
