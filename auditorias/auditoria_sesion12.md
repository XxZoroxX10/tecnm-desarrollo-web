# Bitácora de la Sesión 12 — Inyección de Dependencias (FastAPI Depends / Contenedor IoC)

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu endpoint recibirá el repositorio inyectado

> Llegué al resultado completo: 4/4 casos HTTP y 2/2 comprobaciones en verde (diagnóstico `RepositorioMemoria`, el estado se conserva entre peticiones y la validación sigue en el borde).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. El diagnóstico revela el repositorio inyectado
✅ 02. El endpoint inyectado crea un libro
✅ 03. El repositorio conserva el estado
✅ 04. La validación sigue en el borde
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!

✅ El endpoint usa Depends
✅ Existe la función de inyección
------------------------------------------------------------------------------
RESULTADO: 2/2 comprobaciones correctas. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] El diagnóstico revela el repositorio inyectado → HTTP 200
- [x] El endpoint inyectado crea un libro → HTTP 201
- [x] El repositorio conserva el estado → HTTP 200
- [x] La validación sigue en el borde → HTTP 422
- [x] El endpoint usa Depends
- [x] Existe la función de inyección

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI `Depends` como mecanismo de inyección; repositorio en memoria con una sola instancia compartida (`lru_cache`) |
| **Rol** | Arquitecto backend que aplica inversión de control: los endpoints dependen de un contrato (`Protocol`), no de una clase concreta |
| **Especificación** | `get_repositorio()` devuelve `RepositorioMemoria`; los endpoints lo reciben con `Depends(get_repositorio)`; `GET /api/diagnostico` → `{"repositorio": "RepositorioMemoria"}`; `POST /api/libros` → 201 y `GET` → 200 conservando el estado; tipo inválido → 422 |
| **Output** | Solo `app.py`, sin `RepositorioMemoria()` dentro de ningún endpoint |

### Prompt que utilicé

```text
Actúa como arquitecto backend con FastAPI.
Quiero aplicar inyección de dependencias:
- Una interfaz (typing.Protocol) Repositorio con agregar(titulo, anio) y listar().
- Una clase RepositorioMemoria que la cumpla.
- Una función get_repositorio() que devuelva SIEMPRE la misma instancia de RepositorioMemoria (para que los libros no se pierdan entre peticiones).
- Endpoints que reciban el repositorio con Depends(get_repositorio), nunca creándolo adentro:
  GET /api/diagnostico -> {"repositorio": "<nombre de la clase inyectada>"}
  POST /api/libros -> 201; GET /api/libros -> 200 {"libros": [...]}; datos inválidos -> 422.
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Definí un `Protocol` llamado `Repositorio` con los dos métodos que necesitan los endpoints. Los endpoints dependen de ese contrato, no de `RepositorioMemoria`; eso es la inversión de control.
>
> `get_repositorio()` tiene `@lru_cache`, así FastAPI recibe siempre **la misma instancia** y los libros se conservan entre peticiones. Sin eso, cada request crearía un repositorio vacío y el caso 03 fallaría.
>
> Usé `Annotated[Repositorio, Depends(get_repositorio)]` en un alias (`RepoDep`) para no repetir el `Depends` en cada endpoint.
>
> `listar()` regresa una copia de la lista para que nadie modifique los datos internos desde afuera.
>
> La gran ventaja: en pruebas puedo cambiar la implementación con `app.dependency_overrides[get_repositorio]` sin tocar un solo endpoint.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Mi primera versión de `get_repositorio()` hacía `return RepositorioMemoria()` sin caché. El diagnóstico salía bien, pero cada petición recibía un repositorio nuevo y vacío, así que después del POST el GET regresaba la lista vacía. Lo detecté al pensar en el caso 03 ("el repositorio conserva el estado") y lo arreglé con `lru_cache`.
>
> También aprendí la diferencia que marca la pista: si el endpoint hace `RepositorioMemoria()` adentro, está **acoplado**; si lo recibe como parámetro, está **inyectado**.
>
> Una advertencia que anoto de la presentación: una instancia compartida con estado mutable puede tener problemas de concurrencia; con una base de datos real, la dependencia debe abrir y cerrar la sesión por petición (con `yield` y `finally`).

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/04cbde7
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion12/sesion12_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion12.html

---
**Firma digital:** `XxZoroxX10`
