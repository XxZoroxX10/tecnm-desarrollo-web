# Bitácora de la Sesión 06 — Validación Estricta, Constraints y Params Query/Body

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 17/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tus límites de negocio responderán así

> Llegué al resultado completo: 6/6 casos en verde (creación válida, 422 por título corto, año fuera de rango y precio 0, y paginación validada).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 6 casos · app.py
==============================================================================
✅ 01. Un libro dentro de los límites se crea
✅ 02. Un título demasiado corto produce 422
✅ 03. Un año fuera de rango produce 422
✅ 04. Un precio no positivo produce 422
✅ 05. El límite de paginación debe ser al menos 1
✅ 06. Un límite válido responde 200
------------------------------------------------------------------------------
RESULTADO: 6/6 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Un libro dentro de los límites se crea → HTTP 201
- [x] Un título demasiado corto produce 422 → HTTP 422
- [x] Un año fuera de rango produce 422 → HTTP 422
- [x] Un precio no positivo produce 422 → HTTP 422
- [x] El límite de paginación debe ser al menos 1 → HTTP 422
- [x] Un límite válido responde 200 → HTTP 200

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + Pydantic v2 en Colab; las reglas viven en el DTO (`Field`, `StringConstraints`) y en `Query`, no en `if` dentro del endpoint |
| **Rol** | Desarrollador backend que traduce reglas de negocio a restricciones declarativas |
| **Especificación** | `POST /api/libros`: `titulo` 3–80 caracteres (sin contar espacios a los lados), `anio` 1450–2100, `precio` > 0 → 201; fuera de rango → 422. `GET /api/libros?limite=` con `limite` 1–100 (0 → 422) y `desde` ≥ 0 |
| **Output** | Solo `app.py`, con las restricciones en el DTO y en los parámetros de consulta |

### Prompt que utilicé

```text
Actúa como desarrollador backend con FastAPI y Pydantic v2.
Reglas de negocio para un libro:
- titulo: 3 a 80 caracteres, sin contar espacios al inicio y al final ("   " debe fallar).
- anio: entre 1450 y 2100.
- precio: mayor que 0 (el 0 NO es válido).
- Campos extra prohibidos.
POST /api/libros -> 201 con id; si algo no cumple -> 422.
GET /api/libros con query "limite" (1 a 100, por defecto 10) y "desde" (>= 0) para paginar.
Pon las reglas en el DTO y en Query, nada de if dentro del endpoint. Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Puse todas las reglas en el DTO. Para el título usé `StringConstraints(strip_whitespace=True, min_length=3, max_length=80)`, que primero quita los espacios y después mide, así `"   "` o `"  Ya "` no pasan.
>
> Para el precio usé `gt=0` y no `ge=0`, porque el contrato dice *mayor que* 0; con `ge` el caso del precio 0 se habría colado. También le puse un máximo para no aceptar números absurdos.
>
> En el listado, `limite` va con `Query(10, ge=1, le=100)` y agregué `desde` para paginar. La respuesta incluye `total`, `limite` y `desde`, así el cliente sabe si hay más páginas.
>
> La validación queda en el borde (el DTO); el endpoint solo guarda y responde.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Lo que más cuidé fue la diferencia entre `gt` y `ge`: es una sola letra, pero cambia si el 0 es válido o no. El caso 04 (precio 0) es justo el que lo detecta.
>
> También aprendí que `min_length` sin `strip` cuenta los espacios: `"   "` tiene 3 caracteres y habría pasado como título válido. Es uno de los antipatrones de la presentación.
>
> Con `limite=0` decidí responder 422 en lugar de "corregirlo" en silencio a 1: si el cliente manda algo inválido es mejor avisarle que adivinar lo que quiso.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/136e831
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion06/sesion06_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion06.html

---
**Firma digital:** `XxZoroxX10`
