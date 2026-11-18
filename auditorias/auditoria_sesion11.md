# Bitácora de la Sesión 11 — Arquitectura en Capas: Router, Servicio y Capa de Datos

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** El mismo contrato, ahora repartido en capas

> Llegué al resultado completo: 4/4 casos HTTP y 4/4 comprobaciones de archivos en verde. El contrato de la sesión 02 se mantuvo igual después de separar las capas.

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. El listado inicia vacío
✅ 02. El servicio crea un libro
✅ 03. El listado conserva el contrato
✅ 04. La validación del router sigue funcionando
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!

✅ Existe la capa de router
✅ La app incluye el router
✅ Existe la capa de servicio
✅ Existe la capa de repositorio
------------------------------------------------------------------------------
RESULTADO: 4/4 comprobaciones correctas. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] El listado inicia vacío → HTTP 200
- [x] El servicio crea un libro → HTTP 201
- [x] El listado conserva el contrato → HTTP 200
- [x] La validación del router sigue funcionando → HTTP 422
- [x] Existe la capa de router
- [x] La app incluye el router
- [x] Existe la capa de servicio
- [x] Existe la capa de repositorio

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + Pydantic v2, el CRUD en memoria refactorizado en 4 archivos: `app.py`, `router.py`, `servicio.py` y `repositorio.py` |
| **Rol** | Arquitecto backend que separa responsabilidades sin cambiar el contrato HTTP |
| **Especificación** | `GET /api/libros` → 200 `{"libros": [...]}`; `POST /api/libros` → 201 con id; tipo inválido → 422; título repetido → 409 (regla de negocio en el servicio); el router no conoce los datos y el repositorio no importa FastAPI |
| **Output** | Los 4 archivos, cada uno con una sola responsabilidad y dependencias en una sola dirección: router → servicio → repositorio |

### Prompt que utilicé

```text
Rol: arquitecto backend.
Contexto: FastAPI + Pydantic v2. Tengo un CRUD de libros en un solo archivo y quiero separarlo en capas sin cambiar el contrato HTTP.
Archivos:
- app.py: solo crea la app y hace include_router.
- router.py: APIRouter con GET /api/libros (200 {"libros": [...]}) y POST /api/libros (201). Aquí van los DTO de Pydantic y la traducción de errores a HTTP.
- servicio.py: reglas de negocio (crear y listar; no permitir títulos duplicados). No debe importar FastAPI.
- repositorio.py: guarda los libros en memoria. No debe importar FastAPI ni saber de HTTP.
Las dependencias solo van hacia abajo: router -> servicio -> repositorio.
Devuelve los 4 archivos.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Separé en cuatro capas con una sola dirección de dependencias:
>
> - `app.py` solo arma la aplicación (`include_router`); no tiene ni una regla.
> - `router.py` es la única capa que sabe de HTTP: tiene los DTO, los `status_code` y convierte la excepción `TituloDuplicado` en un **409 Conflict**.
> - `servicio.py` tiene las reglas (normalizar espacios del título y no permitir duplicados). No importa nada de FastAPI, así que podría usarlo desde un script o una prueba unitaria.
> - `repositorio.py` solo guarda y lee usando un `dataclass`. Si mañana cambio a SQLite, solo cambia este archivo.
>
> En el borde (router) valido forma y tipos; en el servicio, la regla de negocio de duplicados.
>
> Por ahora el router arma el servicio a mano (`_servicio = ServicioLibros(RepositorioLibros())`); eso es justo lo que se mejora en la sesión 12 con `Depends`.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Lo que más me costó fue decidir dónde poner la validación. Al principio quería revisar el título duplicado en el router, pero eso es una regla de negocio y no de HTTP, así que la moví al servicio y le hice su propia excepción. El router solo la traduce a 409.
>
> También tuve cuidado con los imports: `app.py` importa `router`, `router` importa `servicio`, y `servicio` importa `repositorio`. Si el repositorio importara algo del router se haría un import circular.
>
> Aprendí que separar en capas no cambia lo que ve el cliente: el verificador probó exactamente el mismo contrato que en la sesión 02 y todo siguió en verde.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/588a6aa
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion11/sesion11_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion11.html

---
**Firma digital:** `XxZoroxX10`
