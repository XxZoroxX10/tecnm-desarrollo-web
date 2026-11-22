# Bitácora de la Sesión 20 — Hito 2: API con Inyección de Dependencias, Auth JWT y RBAC

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu Hito 2 completo se verá así

> Llegué al resultado completo: 7/7 casos en verde. El registro guarda solo el hash bcrypt y no devuelve la contraseña, el login emite un JWT con rol, el usuario ve su perfil pero recibe 403 en el panel, el admin sí entra, y sin token la respuesta es 401.

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 7 casos · app.py
==============================================================================
✅ 01. Registro sin filtrar contraseñas
✅ 02. Login del usuario registrado
✅ 03. El usuario accede a su perfil
✅ 04. El usuario no entra al panel admin
✅ 05. El administrador obtiene su token
✅ 06. El administrador entra al panel
✅ 07. Sin token no hay acceso
------------------------------------------------------------------------------
RESULTADO: 7/7 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Registro sin filtrar contraseñas → HTTP 201
- [x] Login del usuario registrado → HTTP 200
- [x] El usuario accede a su perfil → HTTP 200
- [x] El usuario no entra al panel admin → HTTP 403
- [x] El administrador obtiene su token → HTTP 200
- [x] El administrador entra al panel → HTTP 200
- [x] Sin token no hay acceso → HTTP 401

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI 0.2.0 + `bcrypt` (costo 12) + PyJWT HS256 con `HTTPBearer(auto_error=False)`; clave desde `JWT_SECRET_KEY`; usuarios en memoria (solo hashes) |
| **Rol** | Desarrollador backend que integra registro, autenticación y RBAC (Hito 2) |
| **Especificación** | `POST /api/registro` → 201 `{"usuario", "rol": "user"}` (duplicado → 409); `POST /api/token` → 200 `{"access_token", "token_type", "expires_in"}` o 401; `GET /api/perfil` → 200 o 401; `GET /api/admin/panel` → 200 para admin, 403 para user, 401 sin token; usuario 3–30 caracteres `[a-zA-Z0-9_.-]`, contraseña 6–72 bytes |
| **Output** | Solo `app.py`, organizado en secciones: configuración, repositorio, DTOs, seguridad y rutas |

### Prompt que utilicé

```text
Rol: desarrollador backend; esto es el Hito 2 (registro + login + roles).
Contexto: FastAPI + bcrypt + PyJWT HS256. Clave desde JWT_SECRET_KEY (aleatoria si falta). Usuarios en memoria pero SOLO con hash.
- Usuario admin precargado (admin/admin123, rol admin) guardado con hash.
- POST /api/registro {"usuario","password"} -> 201 {"usuario","rol":"user"}. Nunca devuelvas la contraseña ni el hash. El rol NO lo elige el cliente. Duplicado -> 409.
- Validación: usuario 3-30 caracteres [a-zA-Z0-9_.-]; password mínimo 6 y máximo 72 bytes (límite de bcrypt).
- POST /api/token -> 200 {"access_token","token_type":"bearer","expires_in"}; credenciales malas -> 401. Usa un hash señuelo para que el tiempo de respuesta no revele si el usuario existe.
- JWT con sub, rol, iat, exp (15 min); decodifica con algorithms=["HS256"] y require exp/sub/rol.
- GET /api/perfil (autenticado) y GET /api/admin/panel (solo admin) -> 401 sin token, 403 sin rol.
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Organicé el archivo en el mismo orden que las capas del Hito 2: **configuración → repositorio → DTOs → seguridad → rutas**. Aunque aquí todo está en `app.py`, cada sección se puede mover a su carpeta (`core/`, `repositories/`, `schemas/`, `routers/`) sin reescribirla.
>
> Lo que validé en el borde (Pydantic) y lo que dejé a la lógica:
> - **Borde:** formato del usuario con `pattern`, largo mínimo de la contraseña y el límite de **72 bytes** de bcrypt (son bytes, no caracteres: una ñ ocupa 2).
> - **Lógica:** que el usuario no exista (409), que la contraseña coincida y qué rol tiene.
>
> Decisiones de seguridad:
> - Solo se guarda el hash (`bcrypt.hashpw` con costo 12); el DTO de salida `UsuarioPublico` no tiene campo de contraseña, así que es imposible filtrarla por accidente.
> - El rol de un registro nuevo **siempre** es `user`; aunque el cliente mande `"rol": "admin"`, se ignora.
> - Si el usuario no existe, igual comparo contra un hash señuelo, para que el login tarde lo mismo y no se pueda adivinar qué usuarios existen.
> - Al validar el token tomo el rol **del repositorio**, no solo del token, para que un cambio de rol se note de inmediato.
>
> Si otro equipo consumiera esta API, documentaría en OpenAPI los 401/403/409 y movería los usuarios a una base de datos (sesiones 21–22).

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Ningún caso falló, pero sí encontré dos cosas al revisar el código antes de ejecutar:
>
> 1. **El límite de 72 bytes de bcrypt.** Si no se valida, depende de la versión de la librería: algunas versiones cortan la contraseña en silencio (dos contraseñas distintas con los mismos 72 primeros bytes serían "iguales") y otras lanzan un error que terminaría en 500. Por eso lo valido en el DTO y respondo 422.
> 2. **Comparar `datos["hash"] if datos else _SEÑUELO`.** Si hubiera hecho `if not datos: raise 401` antes de llamar a `checkpw`, el login de un usuario inexistente sería mucho más rápido que el de uno existente (bcrypt tarda a propósito), y eso revela qué usuarios existen.
>
> **Relación con mi proyecto integrador:** este laboratorio es el ensayo del **Hito 2** de *Reporte Ciudadano*. Lo que tengo que llevar al proyecto: separar `src/` en capas, registro con bcrypt, JWT con `sub`/`rol`/`exp`, que cada ciudadano vea solo sus tableros, que solo el dueño o un admin pueda borrar una tarea (403 para los demás) y las diez pruebas del hito, con el tag `v0.2-hito2`.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/6553fbb
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion20/sesion20_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion20.html

## 7. Avance del Proyecto Integrador (Hito 2)

- **Repositorio:** https://github.com/XxZoroxX10/Proyecto-Integrador_ReporteCiudadano_DesarrolloWeb · el Hito 2 se publica con el tag `v0.2-hito2`
- **Qué se llevó del laboratorio al proyecto:** `src/` separado en `routers/`, `services/`, `repositories/`, `schemas/`, `models/` y `core/`; registro con bcrypt; login con JWT (`sub`, `rol`, `exp`); 401 sin token o con token alterado; un ciudadano solo ve sus tableros y solo el dueño o un admin puede borrar una tarea (403 para los demás); el admin lista todo.
- **Inyección de dependencias:** los repositorios se entregan con `Depends` y las pruebas los reemplazan con `app.dependency_overrides`, sin tocar los endpoints.
- **Pruebas:** 18 en verde en Colab (8 del contrato del Hito 1 con token + las 10 del Hito 2).
- **Decisiones:** registradas en `docs/decisiones.md`, en la página del Hito 2.

---
**Firma digital:** `XxZoroxX10`
