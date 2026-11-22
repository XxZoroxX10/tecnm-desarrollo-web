# Bitácora de la Sesión 22 — Modelado Relacional (1:1, 1:N, N:M) con ORMs

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu relación autor → libros se verá así

> Llegué al resultado completo: 4/4 casos HTTP y 1/1 comprobación en verde. Autor y Libro quedaron relacionados 1:N con SQLAlchemy, y GET /api/autores/1 devuelve al autor con sus libros anidados sin que yo escribiera ningún JOIN.

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. Se crea el autor
✅ 02. Se crea el libro asociado
✅ 03. El autor devuelve sus libros
✅ 04. El listado de libros funciona
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!

✅ La relación ORM está declarada
------------------------------------------------------------------------------
RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Se crea el autor → HTTP 201
- [x] Se crea el libro asociado → HTTP 201
- [x] El autor devuelve sus libros → HTTP 200
- [x] El listado de libros funciona → HTTP 200
- [x] La relación ORM está declarada

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + SQLAlchemy 2.0 (`DeclarativeBase`, `Mapped`, `mapped_column`) sobre `sqlite:///biblioteca.db`; tablas con `Base.metadata.create_all` |
| **Rol** | Desarrollador backend que modela datos relacionales con un ORM |
| **Especificación** | Modelos `Autor` y `Libro` (1:N) con `ForeignKey("autores.id")` y `relationship(back_populates=...)`; sesión por petición con `Depends(get_db)`; `POST /api/autores` → 201; `POST /api/autores/{id}/libros` → 201 `{"id","titulo","anio","autor_id"}` o 404 si el autor no existe; `GET /api/autores/{id}` → autor con `libros` anidados; `GET /api/libros` → `{"libros": [...]}`; respuestas con esquemas Pydantic |
| **Output** | Solo `app.py` |

### Prompt que utilicé

```text
Rol: desarrollador backend que modela una base relacional con ORM.
Contexto: FastAPI + SQLAlchemy 2.0 (estilo Mapped/mapped_column) con SQLite (biblioteca.db).
- Modelos: Autor(id, nombre) y Libro(id, titulo, anio, autor_id -> FK autores.id). Relación 1:N con relationship y back_populates en ambos lados.
- Base.metadata.create_all(engine) al iniciar.
- Una sesión por petición con una dependencia get_db que use yield y siempre se cierre.
- POST /api/autores {"nombre"} -> 201 {"id","nombre"}.
- POST /api/autores/{id}/libros {"titulo","anio"} -> 201 {"id","titulo","anio","autor_id"}; si el autor no existe -> 404.
- GET /api/autores/{id} -> {"id","nombre","libros":[{"id","titulo"}]}; usa selectinload para evitar N+1.
- GET /api/libros -> {"libros":[...]}.
- No devuelvas modelos ORM directamente: usa esquemas Pydantic con from_attributes=True.
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> La llave foránea va en el lado **N** (`Libro.autor_id`), y `relationship` en ambos lados con `back_populates`. Eso me permite trabajar con objetos: `Libro(titulo=..., autor=autor)` y SQLAlchemy llena `autor_id` solo; y `autor.libros` me da la lista sin escribir el JOIN.
>
> Otras decisiones:
> - **Una sesión por petición** con `get_db()` y `yield`: se abre al llegar la petición y se cierra siempre, aunque haya error.
> - **Esquemas Pydantic separados de los modelos ORM** (`AutorSalida`, `AutorConLibros`, `LibroSalida`) con `from_attributes=True`. Así decido exactamente qué campos salen y no expongo columnas internas por accidente.
> - **`selectinload(Autor.libros)`** en el detalle del autor: trae todos los libros en una segunda consulta, en lugar de una consulta por cada libro (el problema **N+1**).
> - **404 si el autor no existe** al crear un libro: así no quedan libros huérfanos (integridad referencial desde la API). Tengo presente que SQLite no revisa las llaves foráneas a menos que se active `PRAGMA foreign_keys=ON`, así que esta validación en la API sí importa.
> - `check_same_thread=False` porque FastAPI puede atender la petición en un hilo distinto al que creó la conexión.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> No falló ningún caso, pero sí aprendí cosas al revisar:
>
> - Lo más rápido habría sido devolver directamente el objeto `Autor` del ORM. Funciona con `response_model`, pero si después agrego una columna sensible al modelo, saldría en la API sin darme cuenta. Separar esquema de modelo es más trabajo, pero más seguro.
> - Sin `selectinload`, `autor.libros` se carga "perezosamente" (*lazy*): se hace una consulta extra en el momento en que se accede. Con muchos autores en un listado eso se convierte en N+1 consultas. Preferí cargarlo de forma explícita.
> - `create_all` solo **crea** tablas que no existen; si cambio un modelo, no altera la tabla. Para eso existen las migraciones (Alembic), que es lo que usaría en mi proyecto integrador.
>
> **Relación con mi proyecto integrador:** en *Reporte Ciudadano* la relación es la misma: un **tablero** tiene muchas **tareas/reportes** (1:N) y un usuario tiene muchos tableros. Esta sesión es la base para el Hito 3, cuando el repositorio en memoria del Hito 2 se cambie por uno con SQLAlchemy sin tocar los routers.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/978393f
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion22/sesion22_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion22.html

---
**Firma digital:** `XxZoroxX10`
