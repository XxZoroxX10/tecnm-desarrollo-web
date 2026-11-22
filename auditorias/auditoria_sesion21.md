# Bitácora de la Sesión 21 — Fundamentos de Persistencia: SQLite / PostgreSQL y Drivers

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tus libros sobrevivirán al reinicio

> Llegué al resultado completo: 3/3 casos HTTP y 1/1 comprobación en verde. La tabla se crea sola al arrancar, el POST inserta en biblioteca.db y el verificador encontró la fila 'Rayuela' leyendo el archivo directamente.

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 3 casos · app.py
==============================================================================
✅ 01. La base inicia sin libros
✅ 02. El libro se inserta en SQLite
✅ 03. El listado lee la base
------------------------------------------------------------------------------
RESULTADO: 3/3 casos correctos. ¡Resultado logrado!

✅ La fila existe en el archivo SQLite
------------------------------------------------------------------------------
RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] La base inicia sin libros → HTTP 200
- [x] El libro se inserta en SQLite → HTTP 201
- [x] El listado lee la base → HTTP 200
- [x] La fila existe en el archivo SQLite

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + `sqlite3` de la biblioteca estándar; archivo `biblioteca.db`; la tabla se crea al importar el módulo y en el `lifespan` |
| **Rol** | Desarrollador backend que pasa del almacenamiento en memoria a persistencia real |
| **Especificación** | `CREATE TABLE IF NOT EXISTS libros (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, anio INTEGER NOT NULL)` con `CHECK`; `POST /api/libros` `{"titulo","anio"}` → 201 `{"id","titulo","anio"}` usando parámetros `?`; `GET /api/libros` → 200 `{"libros": [...]}` leído de la base; cada conexión se cierra y el insert hace commit |
| **Output** | Solo `app.py` |

### Prompt que utilicé

```text
Rol: desarrollador backend que agrega persistencia.
Contexto: FastAPI + sqlite3 (sin ORM todavía), archivo biblioteca.db.
- Al arrancar, CREATE TABLE IF NOT EXISTS libros (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, anio INTEGER NOT NULL) con CHECK de rango.
- POST /api/libros {"titulo","anio"} -> 201 {"id","titulo","anio"}. Usa SIEMPRE parámetros "?" (nada de f-strings en SQL) y haz commit.
- GET /api/libros -> 200 {"libros":[...]} leyendo de la base, ordenado por id.
- Abre y cierra la conexión en cada operación; usa row_factory = sqlite3.Row.
- Valida con Pydantic: titulo 1-200, anio 1450-2100, extra="forbid".
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> La diferencia con las sesiones anteriores es que ahora los datos **sobreviven al reinicio**: ya no viven en un diccionario de Python, sino en el archivo `biblioteca.db`.
>
> Decisiones:
> - **Parámetros `?` siempre.** `con.execute("INSERT ... VALUES (?, ?)", (titulo, anio))` deja que el driver escape los valores; nunca armo SQL pegando texto, que es la puerta a la inyección SQL.
> - **`with closing(conectar()) as con, con:`** — el `closing` cierra la conexión y el `with con` hace `commit` si todo salió bien o `rollback` si hubo error.
> - **Validé dos veces:** Pydantic en el borde (para responder 422 claro) y `CHECK` en la tabla (por si algún día otro programa escribe en la base).
> - `row_factory = sqlite3.Row` para convertir cada fila en diccionario con `dict(fila)` y no depender del orden de las columnas.
>
> Para pasar a PostgreSQL cambiaría el driver (`psycopg`) y el marcador de parámetros (`%s` en lugar de `?`), pero la idea es la misma.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> El hallazgo de esta sesión fue con **cuándo se crea la tabla**. Primero la creé solo en el `lifespan` (lo que se ejecuta al arrancar el servidor). Antes de correr el verificador me di cuenta de que `TestClient` **no ejecuta el lifespan** si no se usa dentro de un `with TestClient(app)`, y como el verificador borra `biblioteca.db` antes de probar, el primer `GET` habría fallado con `no such table: libros` (un 500). Lo resolví llamando `crear_esquema()` también al importar el módulo; como uso `IF NOT EXISTS`, llamarlo dos veces no hace daño.
>
> Otra cosa que aprendí: `with con:` en `sqlite3` **no cierra** la conexión, solo maneja la transacción. Sin el `closing()` las conexiones se quedarían abiertas.
>
> Lo que haría distinto la próxima vez: poner la ruta de la base en una variable de entorno, para que las pruebas usen un archivo distinto al de desarrollo.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/9f0ff0e
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion21/sesion21_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion21.html

---
**Firma digital:** `XxZoroxX10`
