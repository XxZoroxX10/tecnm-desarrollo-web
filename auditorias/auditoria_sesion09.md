# Bitácora de la Sesión 09 — Middleware Web, Intercepción y Logging de Transacciones

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Todas tus respuestas llevarán estas cabeceras

> Llegué al resultado completo: 3/3 casos en verde (tiempo y traza en el 200, el X-Request-ID del cliente se conserva y el middleware también cubre los 404).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 3 casos · app.py
==============================================================================
✅ 01. Una respuesta correcta trae tiempo y traza
✅ 02. El X-Request-ID del cliente se conserva
✅ 03. El middleware también cubre los 404
------------------------------------------------------------------------------
RESULTADO: 3/3 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Una respuesta correcta trae tiempo y traza → HTTP 200
- [x] El X-Request-ID del cliente se conserva → HTTP 200
- [x] El middleware también cubre los 404 → HTTP 404

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI con `@app.middleware("http")`, que envuelve a todos los endpoints, incluidas las respuestas 404 del router |
| **Rol** | Desarrollador backend responsable de la observabilidad de la API |
| **Especificación** | Toda respuesta lleva `X-Process-Time` (segundos con decimales) y `X-Request-ID`; si el cliente manda un `X-Request-ID` válido se conserva, si no se genera un UUID; también aplica a los 404; `GET /api/libros` → 200; no leer el body en el middleware |
| **Output** | Solo `app.py`, con el middleware y un log de acceso por petición |

### Prompt que utilicé

```text
Rol: desarrollador backend enfocado en observabilidad.
Contexto: FastAPI.
Quiero un middleware HTTP que:
- Mida cuánto tarda cada petición y lo mande en el header X-Process-Time (segundos con decimales).
- Agregue X-Request-ID a TODAS las respuestas, incluidas las 404. Si el cliente ya manda X-Request-ID, conservarlo; si no, generar un UUID4.
- Valide que el X-Request-ID del cliente sea seguro (solo letras, números, punto, guion y guion bajo, máximo 64).
- Escriba una línea de log por petición (id, método, ruta, estado y milisegundos).
- No lea el body de la petición.
Además GET /api/libros -> 200. Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> El middleware sigue el modelo de cebolla: tomo el tiempo **antes** de `call_next`, dejo que la petición llegue al endpoint, y al regresar agrego los dos encabezados a la respuesta ya construida.
>
> Usé `time.perf_counter()` en lugar de `time.time()` porque está hecho para medir intervalos y no le afectan los cambios del reloj del sistema.
>
> El `X-Request-ID` del cliente solo lo acepto si cumple `^[A-Za-z0-9._-]{1,64}$`; si no, genero un UUID. Así nadie puede meter saltos de línea en mis logs o en las cabeceras. Además lo guardo en `request.state` para que los endpoints lo puedan usar (el listado lo regresa en el JSON).
>
> No leo `request.body()` en el middleware: si lo consumo ahí, el endpoint ya no lo podría leer.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Pensé que el 404 de una ruta inexistente no pasaría por el middleware porque "no hay endpoint", pero sí pasa: el middleware envuelve al router completo, y el 404 se genera dentro. Por eso el caso 03 sale en verde sin código extra.
>
> Al principio regresaba el `X-Request-ID` del cliente tal cual. Luego caí en que es una entrada externa que termina en los logs: si alguien manda texto con saltos de línea podría falsificar líneas del log. Por eso le agregué la validación con expresión regular.
>
> Aprendí que el middleware es para lo transversal (tiempos, trazas, seguridad), no para la lógica de negocio.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/4ed6873
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion09/sesion09_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion09.html

---
**Firma digital:** `XxZoroxX10`
