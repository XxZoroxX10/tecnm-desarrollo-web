# Bitácora de la Sesión 17 — Control de Acceso Basado en Roles (RBAC)

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tus respuestas de autorización se verán así

> Llegué al resultado completo: 6/6 casos en verde. El admin entra al panel, el usuario normal recibe 403 en el panel pero sí ve su perfil, y sin token la respuesta es 401.

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 6 casos · app.py
==============================================================================
✅ 01. El administrador obtiene su token
✅ 02. El usuario normal obtiene su token
✅ 03. El admin entra al panel
✅ 04. El usuario normal recibe 403
✅ 05. Sin token recibe 401
✅ 06. El perfil funciona para el usuario normal
------------------------------------------------------------------------------
RESULTADO: 6/6 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] El administrador obtiene su token → HTTP 200
- [x] El usuario normal obtiene su token → HTTP 200
- [x] El admin entra al panel → HTTP 200
- [x] El usuario normal recibe 403 → HTTP 403
- [x] Sin token recibe 401 → HTTP 401
- [x] El perfil funciona para el usuario normal → HTTP 200

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + PyJWT (HS256) con `HTTPBearer(auto_error=False)`; clave desde `JWT_SECRET_KEY` |
| **Rol** | Desarrollador backend que implementa control de acceso basado en roles (RBAC) |
| **Especificación** | `POST /api/token` `{"usuario","password"}` emite un JWT con `sub`, `rol` y `exp`; `GET /api/perfil` para cualquier usuario autenticado; `GET /api/admin/panel` solo para `admin`; sin token o token inválido → 401, autenticado sin el rol → 403 |
| **Output** | Solo `app.py`, con las dependencias `usuario_actual` y `requiere_rol(*roles)` |

### Prompt que utilicé

```text
Rol: desarrollador backend que implementa RBAC en FastAPI.
Contexto: FastAPI + PyJWT HS256, clave desde JWT_SECRET_KEY (aleatoria si no existe).
Usuarios de prueba: admin/admin123 con rol "admin" y ana/secreta con rol "user".
- POST /api/token {"usuario","password"} -> 200 {"access_token","token_type":"bearer"}; el token incluye sub, rol y exp (15 min). Credenciales malas -> 401.
- Dependencia usuario_actual: valida el Bearer; sin token o inválido -> 401 con WWW-Authenticate: Bearer.
- Fábrica de dependencias requiere_rol(*roles): si el rol no está permitido -> 403.
- GET /api/perfil (cualquier autenticado) -> {"usuario","rol"}.
- GET /api/admin/panel (solo admin) -> {"panel":"admin","usuario"}.
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Separé las dos preguntas en dos dependencias distintas:
> 1. `usuario_actual` responde **¿quién eres?** → si no lo puedo saber, **401**.
> 2. `requiere_rol("admin")` responde **¿te alcanza el permiso?** → si no, **403**.
>
> `requiere_rol` es una función que **devuelve** otra función (una fábrica). Así, proteger una ruta es una sola línea: `Depends(requiere_rol("admin"))`, y si mañana hay un rol `moderador` solo cambio los argumentos.
>
> El rol viaja dentro del token, que está **firmado**: el cliente puede leerlo, pero si lo cambia a `admin` la firma ya no coincide y recibe 401. Además valido que el rol sea uno de los conocidos (`admin` o `user`); uno raro también es 401.
>
> Usé `HTTPBearer(auto_error=False)` para controlar yo mismo la respuesta cuando no hay token, y que siempre sea 401 (no 403).

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> El caso que más me hizo pensar fue el 05: **sin token al panel de admin**. Mi primer impulso fue "es una ruta de admin, entonces 403", pero no: si no sé quién eres, no puedo decir que te falta permiso. Primero va la autenticación (401) y solo después la autorización (403). Eso salió bien porque `requiere_rol` depende de `usuario_actual`, así que el 401 siempre ocurre antes.
>
> Un hallazgo que dejé anotado: como el rol va en el token, si a alguien le quitan el rol de admin, su token viejo **sigue diciendo admin** hasta que expire. Con 15 minutos el riesgo es pequeño, pero en el Hito 2 (sesión 20) lo corregí leyendo el rol actual desde el repositorio de usuarios y no solo desde el token.
>
> Lo que haría distinto: no repetir el `HTTPException` del 401 en varios lugares; lo dejé en una función `no_autenticado()` para que el encabezado `WWW-Authenticate` nunca se me olvide.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/4779118
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion17/sesion17_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion17.html

---
**Firma digital:** `XxZoroxX10`
