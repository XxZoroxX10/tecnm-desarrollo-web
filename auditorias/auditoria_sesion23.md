# Bitácora de la Sesión 23 — Operaciones CRUD Transaccionales y Async Sessions

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu CRUD asíncrono se verá así

> Llegué al resultado completo: 5/5 casos HTTP y 1/1 comprobación en verde. El CRUD completo (crear, listar, actualizar, borrar y confirmar el 404) funciona con SQLAlchemy asíncrono y aiosqlite.

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 5 casos · app.py
==============================================================================
✅ 01. Crear un libro
✅ 02. Listar los libros
✅ 03. Actualizar el libro
✅ 04. Eliminar el libro
✅ 05. El libro eliminado ya no existe
------------------------------------------------------------------------------
RESULTADO: 5/5 casos correctos. ¡Resultado logrado!

✅ La persistencia es asíncrona
------------------------------------------------------------------------------
RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Crear un libro → HTTP 201
- [x] Listar los libros → HTTP 200
- [x] Actualizar el libro → HTTP 200
- [x] Eliminar el libro → HTTP 204
- [x] El libro eliminado ya no existe → HTTP 404
- [x] La persistencia es asíncrona

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + SQLAlchemy 2.0 asíncrono (`create_async_engine`, `async_sessionmaker`, `AsyncSession`) con el driver `aiosqlite` sobre `biblioteca.db` |
| **Rol** | Desarrollador backend que migra un CRUD síncrono a uno asíncrono sin bloquear el event loop |
| **Especificación** | `POST /api/libros` → 201 con `id`; `GET /api/libros` → 200 `{"libros": [...]}`; `GET /api/libros/{id}` → 200 o 404; `PUT /api/libros/{id}` → 200; `DELETE /api/libros/{id}` → 204 sin cuerpo; una sesión por petición con `Depends` y `await` en las operaciones de base de datos |
| **Output** | Solo `app.py` |

### Prompt que utilicé

```text
Rol: desarrollador backend con FastAPI y SQLAlchemy 2.0.
Contexto: tengo un CRUD de libros con SQLAlchemy síncrono (sesión 22) y quiero que sea asíncrono para no bloquear el servidor mientras espera a la base.
- Usa create_async_engine("sqlite+aiosqlite:///biblioteca.db") y async_sessionmaker con expire_on_commit=False.
- Modelo Libro(id, titulo, anio). Crea las tablas con run_sync(Base.metadata.create_all).
- Dependencia get_db asíncrona: una AsyncSession por petición que siempre se cierre.
- POST /api/libros -> 201 {"id","titulo","anio"}; GET /api/libros -> {"libros":[...]};
  GET /api/libros/{id} -> 200 o 404; PUT /api/libros/{id} -> 200; DELETE /api/libros/{id} -> 204 sin cuerpo.
- Valida con Pydantic (titulo 1-200, anio 1450-2100, extra="forbid") y responde con un esquema, no con el modelo ORM.
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Lo único que cambia respecto a la sesión 22 es **cómo espera la aplicación**: cada operación con la base lleva `await` (`commit`, `refresh`, `get`, `scalars`, `delete`). Mientras SQLite responde, el event loop puede atender otras peticiones.
>
> Decisiones:
> - **`sqlite+aiosqlite://`**: el driver es lo que hace posible el `await`; con el driver normal, SQLAlchemy asíncrono no funciona.
> - **`expire_on_commit=False`**: después del `commit` puedo devolver el objeto sin que SQLAlchemy intente recargarlo.
> - **Una sesión por petición** con `get_db()` y `async with`: es el *Unit of Work* de la sesión; se cierra siempre, aunque haya error.
> - **`buscar()`** concentra el 404 y lo reutilizo en GET, PUT y DELETE.
> - **`create_all` dentro de `run_sync`**: crear tablas es una operación síncrona, así que se ejecuta dentro de la conexión asíncrona.
> - El `PUT` cambia los atributos con `setattr`; el ORM solo genera el `UPDATE` de los campos que cambiaron.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> No falló ningún caso, pero tomé dos precauciones al revisar el código:
>
> 1. **`expire_on_commit=False`.** Por defecto, después de un `commit` SQLAlchemy marca los objetos como "vencidos" y los recarga cuando se leen. En modo asíncrono esa recarga implícita no puede hacer `await` y termina en un error (`MissingGreenlet`). Con esta opción, o con un `refresh` explícito, se evita.
> 2. **Cuándo se crean las tablas.** Aprendí en la sesión 21 que `TestClient` no ejecuta el `lifespan` si no se usa con `with`. Como aquí no puedo crear las tablas al importar (es asíncrono), las creo la primera vez que se pide una sesión (`get_db`) y también en el `lifespan`.
>
> Lo que haría distinto: en una app grande pondría el motor y la sesión en `core/database.py` y los modelos en su propio módulo, como en el Hito 2 del proyecto integrador.

## 6. Evidencia

- **Commit:** [se completa al hacer commit]
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion23/sesion23_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion23.html

---
**Firma digital:** `XxZoroxX10`
