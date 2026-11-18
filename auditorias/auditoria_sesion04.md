# Bitácora de la Sesión 04 — Anatomía RESTful, URIs Nombres y Recursos

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 17/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu jerarquía de recursos responderá así

> Llegué al resultado completo: 4/4 casos en verde (sub-recurso por autor, filtros por query, 404 para autor inexistente y colección completa).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. Libros del autor 1
✅ 02. Filtro por género y límite
✅ 03. Un autor inexistente produce 404
✅ 04. La colección completa de libros
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Libros del autor 1 → HTTP 200
- [x] Filtro por género y límite → HTTP 200
- [x] Un autor inexistente produce 404 → HTTP 404
- [x] La colección completa de libros → HTTP 200

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + Pydantic v2 en Colab, con datos sembrados en memoria (2 autores y 3 libros) |
| **Rol** | Diseñador de APIs REST que nombra recursos con sustantivos en plural y nunca usa verbos en la URI |
| **Especificación** | `GET /api/libros` → 200 con los 3 libros; `GET /api/autores/{autor_id}/libros` → 200 `{"autor_id", "libros"}` con query opcionales `genero` (filtro) y `limite` (1–100); autor inexistente → 404; respuestas siempre envueltas en un objeto |
| **Output** | Solo `app.py`, con los datos semilla exactos del enunciado |

### Prompt que utilicé

```text
Rol: diseñador de APIs REST.
Contexto: FastAPI, datos en memoria.
Siembra: autor 1 Gabriel García Márquez con "Cien años de soledad" (novela, id 1) y "Doce cuentos peregrinos" (cuento, id 2); autor 2 Julio Cortázar con "Rayuela" (novela, id 3).
Especificación:
- GET /api/libros -> 200 {"libros": [...]} con los 3 libros.
- GET /api/autores/{autor_id}/libros -> 200 {"autor_id": n, "libros": [...]}.
- Query params opcionales: genero (filtra) y limite (recorta, entero >= 1).
- Si el autor no existe -> 404.
- Nada de verbos en las rutas; respuestas siempre como objeto, nunca un arreglo suelto.
Output: solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Separé los datos en `AUTORES` (diccionario por id, para saber rápido si existe) y `LIBROS` (lista con `autor_id`, como sería una llave foránea en una base de datos).
>
> El `autor_id` va en la **ruta** porque identifica al padre; `genero` y `limite` van en la **consulta** porque solo achican la lista. A `limite` le puse `ge=1, le=100` con `Query`, así un `limite=0` o `limite=-5` responde 422 en lugar de devolver cosas raras.
>
> Si el autor existe pero no tiene libros del género pedido, regreso 200 con lista vacía, no 404: el recurso padre sí existe.
>
> Agregué también `GET /api/autores` porque la colección de autores es el punto de partida natural para un cliente.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Al principio pensé en devolver la lista de libros directo (`return LIBROS`), pero el contrato pide un objeto `{"libros": [...]}`. Devolver un arreglo crudo en la raíz es uno de los antipatrones de la presentación: no puedes agregarle después metadatos como paginación sin romper a los clientes.
>
> Otro detalle: el orden importa. El verificador compara las listas en orden y por cantidad, así que filtrar primero por autor, luego por género y al final recortar con `limite` fue necesario para que el caso 02 diera exactamente el libro 2.
>
> Aprendí que la URL describe **qué** (recurso) y el método HTTP describe **qué hacer**.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/a0f9d2a
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion04/sesion04_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion04.html

## 7. Avance del Proyecto Integrador (entregable de la sesión 4: propuesta)

- **Propuesta:** [docs/propuesta.md](https://github.com/XxZoroxX10/Proyecto-Integrador_ReporteCiudadano_DesarrolloWeb/blob/main/docs/propuesta.md): equipo, entidades (Tablero → Tarea adaptado a reportes ciudadanos), 10 endpoints, reglas de negocio, riesgos y plan por hito.
- **Acuerdo de equipo:** [docs/equipo.md](https://github.com/XxZoroxX10/Proyecto-Integrador_ReporteCiudadano_DesarrolloWeb/blob/main/docs/equipo.md).
- **Cómo se conecta con esta sesión:** las rutas del proyecto siguen la misma jerarquía de recursos del laboratorio: el padre en la ruta (`/api/tableros/{id}/tareas`) y los filtros en la consulta (`?estado=pendiente`, planeado para el Hito 3).

---
**Firma digital:** `XxZoroxX10`
