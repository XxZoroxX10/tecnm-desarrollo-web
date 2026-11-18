# Bitácora de la Sesión 01 — Encuadre, Diagnóstico HTTP y Servidores en la Nube

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 17/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu servidor responderá exactamente así

> Llegué al resultado completo: los 4 casos en verde a la primera ejecución completa del cuaderno en Colab.

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. El servidor está vivo y responde JSON
✅ 02. El eco devuelve el mensaje recibido
✅ 03. Un JSON roto no tumba el servidor
✅ 04. El método incorrecto se rechaza con 405
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] El servidor está vivo y responde JSON → HTTP 200
- [x] El eco devuelve el mensaje recibido → HTTP 200
- [x] Un JSON roto no tumba el servidor → HTTP 422
- [x] El método incorrecto se rechaza con 405 → HTTP 405

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + Pydantic v2 en Python 3, en Google Colab; el verificador usa `TestClient` |
| **Rol** | Desarrollador backend que diseña una API mínima de diagnóstico cuidando códigos HTTP y respuestas JSON |
| **Especificación** | `GET /api/estado` → 200 `{"servidor":"ok","curso":"DAB-2201"}`; `POST /api/eco` con `{"mensaje": str}` → 200 `{"mensaje", "recibido": true}`; JSON roto o sin `mensaje` → 422; `GET /api/eco` → 405 |
| **Output** | Un solo archivo `app.py` con la variable `app` y modelos Pydantic de entrada y salida, sin texto extra |

### Prompt que utilicé

```text
Actúa como desarrollador backend con FastAPI y Pydantic v2 (Python 3.10+).
Necesito un app.py con:
- GET /api/estado que responda 200 con {"servidor": "ok", "curso": "DAB-2201"}.
- POST /api/eco que reciba {"mensaje": string} y responda 200 con {"mensaje": <el mismo>, "recibido": true}.
- Si el JSON viene roto o sin "mensaje", la API no debe caerse: debe responder 422.
- GET /api/eco debe responder 405 (la ruta existe pero el verbo no).
Usa un modelo Pydantic para la entrada y otro para la salida (response_model).
Devuélveme solo el código de app.py, sin explicación.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Hice dos modelos: `Eco` para lo que entra y `EcoRespuesta` para lo que sale, así el `response_model` me garantiza que la respuesta tiene justo esos dos campos y nada más. A `mensaje` le puse `min_length=1` y `max_length=500` porque un eco vacío no tiene sentido y no quiero que me manden un texto gigante.
>
> En el borde de la API (Pydantic) validé el tipo y la longitud; lógica de negocio casi no hay, solo regresar lo mismo con `recibido: true`.
>
> Para el 405 no programé nada: como solo existe `@app.post("/api/eco")`, FastAPI ya sabe que la ruta existe pero el verbo GET no, y responde 405 con el encabezado `Allow: POST`.
>
> Si otro equipo consumiera mi API, le agregaría `version` a `/api/estado` para que sepan contra qué versión están hablando.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> En la versión anterior del laboratorio yo había hecho que un JSON roto respondiera **400** (porque técnicamente el servidor no lo pudo leer). En este contrato el profe pide **422**, que es justo lo que FastAPI hace por defecto, así que quité mi manejador personalizado y dejé el comportamiento estándar. Aprendí que no hay que "mejorar" algo que el contrato ya define: primero se cumple el contrato.
>
> También me di cuenta de que el verificador no levanta un servidor real, usa `TestClient`, entonces no hace falta `uvicorn` ni hilos dentro de `app.py`; el archivo solo tiene que exponer la variable `app`.
>
> La próxima vez leo primero los criterios de aceptación antes de escribir una sola línea.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/f627182
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion01/sesion01_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion01.html

---
**Firma digital:** `XxZoroxX10`
