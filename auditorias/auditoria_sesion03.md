# Bitácora de la Sesión 03 — Headers, Content-Type y Negociación de Contenido

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 17/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu API negociará el formato exactamente así

> Llegué al resultado completo: 4/4 casos en verde (201 en JSON, 415 con texto plano, 406 cuando se pide XML y 200 con Accept JSON).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. POST válido en JSON
✅ 02. POST en texto plano se rechaza con 415
✅ 03. GET que pide XML se rechaza con 406
✅ 04. GET que acepta JSON responde 200
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] POST válido en JSON → HTTP 201
- [x] POST en texto plano se rechaza con 415 → HTTP 415
- [x] GET que pide XML se rechaza con 406 → HTTP 406
- [x] GET que acepta JSON responde 200 → HTTP 200

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + Pydantic v2 en Colab; revisión de encabezados con dependencias (`Depends`) antes de procesar el cuerpo |
| **Rol** | Desarrollador backend que cuida el protocolo HTTP y la negociación de formatos |
| **Especificación** | `POST /api/libros` solo con `Content-Type: application/json` (si no → 415) y responde 201; `GET /api/libros` → 200 JSON si `Accept` admite JSON, si pide XML → 406; ignorar `; charset=...` y mayúsculas al comparar tipos MIME |
| **Output** | Solo `app.py`, con las comprobaciones de encabezados en funciones reutilizables |

### Prompt que utilicé

```text
Actúa como desarrollador backend experto en el protocolo HTTP.
Contexto: FastAPI + Pydantic v2.
Quiero:
- POST /api/libros que solo acepte Content-Type: application/json. Si llega otro tipo (por ejemplo text/plain) responde 415, sin intentar leer el cuerpo.
- GET /api/libros que solo responda si el header Accept admite application/json (también */* o si no viene Accept). Si piden application/xml responde 406.
- Las respuestas correctas con Content-Type: application/json. Un POST válido responde 201 con {"id", "titulo", "anio"}.
- Compara los tipos MIME sin importar mayúsculas y quitando parámetros como "; charset=utf-8".
Hazlo con dependencias reutilizables. Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Usé dos dependencias, `exigir_json_entrada` (415) y `exigir_json_salida` (406), y las conecté con `dependencies=[Depends(...)]` en cada ruta. Las preferí sobre un middleware porque así cada ruta declara qué formato acepta, y si mañana agrego una ruta que reciba un archivo no se rompe.
>
> Para comparar tipos MIME hice `tipo_mime()`, que corta lo que viene después del `;` y pasa a minúsculas. Así `application/json; charset=utf-8` y `Application/JSON` también son válidos.
>
> Si el cliente no manda `Accept`, lo trato como `*/*` (acepta todo), que es lo que dice HTTP.
>
> Si otro equipo consumiera la API, documentaría en OpenAPI que solo se produce y consume JSON.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Lo que más me hizo pensar fue el orden: si el `Content-Type` es `text/plain`, ¿qué sale primero, el 415 o un 422 por el body? Al ponerlo como dependencia de la ruta, la revisión del encabezado corta la petición con 415 antes de que importe el cuerpo, y eso es lo que comprueba el caso 02.
>
> También me di cuenta de que comparar con `==` el header completo hubiera fallado con clientes reales que mandan `application/json; charset=utf-8`; el verificador no lo prueba, pero es un error típico.
>
> Aprendí la diferencia: **Content-Type** describe lo que yo envío; **Accept** dice lo que yo puedo recibir. 415 es "no entiendo lo que me mandaste"; 406 es "no puedo responderte en ese formato".

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/d603ddf
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion03/sesion03_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion03.html

---
**Firma digital:** `XxZoroxX10`
