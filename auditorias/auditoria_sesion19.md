# Bitácora de la Sesión 19 — Sanitización de Entradas, Prevención de XSS e Inyecciones

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu API neutralizará el HTML peligroso

> Llegué al resultado completo: 3/3 casos en verde. Un comentario normal se guarda tal cual, y uno con <script> se guarda y se devuelve escapado (&lt;script&gt;), tanto al crearlo como en el listado.

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 3 casos · app.py
==============================================================================
✅ 01. Un comentario normal se guarda
✅ 02. El script se neutraliza
✅ 03. El listado tampoco devuelve scripts
------------------------------------------------------------------------------
RESULTADO: 3/3 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Un comentario normal se guarda → HTTP 201
- [x] El script se neutraliza → HTTP 201
- [x] El listado tampoco devuelve scripts → HTTP 200

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + Pydantic v2 (`field_validator`); módulos `html` y `unicodedata` de la biblioteca estándar |
| **Rol** | Desarrollador backend que previene XSS almacenado |
| **Especificación** | `POST /api/comentarios` `{"texto"}` (1–1000 caracteres) → 201 `{"id", "texto"}` con el texto normalizado y escapado; `GET /api/comentarios` → 200 `{"comentarios": [...]}` sin ninguna etiqueta `<script>` ejecutable; campos extra → 422 |
| **Output** | Solo `app.py` |

### Prompt que utilicé

```text
Rol: desarrollador backend preocupado por la seguridad.
Contexto: FastAPI + Pydantic v2. Los comentarios de usuarios se mostrarán después en una página web.
- POST /api/comentarios {"texto"} -> 201 {"id","texto"}; GET /api/comentarios -> {"comentarios":[...]}.
- En un field_validator: normaliza Unicode (NFC), quita caracteres de control (deja \n y \t), recorta espacios, rechaza texto vacío y escapa el HTML con html.escape(v, quote=True).
- Ni la respuesta del POST ni el listado deben contener "<script>".
- extra="forbid" y máximo 1000 caracteres.
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> La idea central: **no confiar en nada que escribe el usuario** si después se va a mostrar en HTML. Con `html.escape` los caracteres `<`, `>`, `&`, `"` y `'` se convierten en entidades (`&lt;`, `&gt;`…), y el navegador los muestra como texto en lugar de ejecutarlos.
>
> Puse la limpieza en un `field_validator` de Pydantic para que ocurra en el borde de la API, antes de que el dato llegue a guardarse. Antes de escapar:
> - normalizo Unicode a NFC, para que dos textos que se ven iguales se guarden igual;
> - quito caracteres de control invisibles (dejando saltos de línea y tabuladores);
> - si después de limpiar queda vacío, es un error de validación (422).
>
> Usé `quote=True` para escapar también comillas, porque si el texto termina dentro de un atributo HTML (`title="..."`) una comilla sin escapar rompería el atributo.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> El hallazgo más importante para mí fue entender que **dónde** se escapa importa. En este laboratorio escapo al **guardar**, porque el contrato pide que ni la respuesta del POST traiga `<script>`. Pero eso tiene un costo: el dato queda guardado como `&lt;script&gt;`, y si después una plantilla Jinja2 (que escapa automáticamente) lo vuelve a escapar, el usuario vería `&amp;lt;` en pantalla: **doble escape**.
>
> La práctica más común es guardar el texto original y escapar al **mostrar**, según el contexto (HTML, atributo, JavaScript, URL). Lo dejo anotado porque en mi proyecto integrador sí uso plantillas Jinja2.
>
> También aprendí que escapar no reemplaza a otras defensas: un encabezado `Content-Security-Policy` y las cookies `HttpOnly` (sesión 13) ayudan a que, aunque se cuele algo, haga menos daño.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/386cffa
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion19/sesion19_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion19.html

---
**Firma digital:** `XxZoroxX10`
