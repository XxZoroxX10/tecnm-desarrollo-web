# Bitácora de la Sesión 15 — Autenticación Stateless con JSON Web Tokens (JWT)

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu flujo JWT se verá así

> Llegué al resultado completo: 4/4 casos HTTP y 1/1 comprobación en verde (emisión del token, perfil con token válido y 401 con token alterado o sin token).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. El login emite un token
✅ 02. El token válido abre el perfil
✅ 03. Un token alterado es rechazado
✅ 04. Sin token no hay acceso
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!

✅ Se usa una librería JWT
------------------------------------------------------------------------------
RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] El login emite un token → HTTP 200
- [x] El token válido abre el perfil → HTTP 200
- [x] Un token alterado es rechazado → HTTP 401
- [x] Sin token no hay acceso → HTTP 401
- [x] Se usa una librería JWT

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + PyJWT con HS256; la clave secreta viene de la variable de entorno `JWT_SECRET_KEY` y nunca se escribe en el código |
| **Rol** | Desarrollador backend responsable de la autenticación stateless |
| **Especificación** | `POST /api/token` con `ana`/`secreta` → 200 `{"access_token", "token_type": "bearer", "expires_in"}`; el token lleva `sub` y `exp` (15 min); `GET /api/perfil` exige `Authorization: Bearer`; token alterado, vencido o ausente → 401 (nunca 500); solo se acepta HS256 |
| **Output** | Solo `app.py`, con `crear_token`, la dependencia `usuario_actual` y las rutas |

### Prompt que utilicé

```text
Rol: desarrollador backend que implementa autenticación con JWT.
Contexto: FastAPI + PyJWT, algoritmo HS256.
- La clave secreta se lee de la variable de entorno JWT_SECRET_KEY; NO la escribas en el código. Si no existe, genera una aleatoria al arrancar.
- POST /api/token {"usuario","password"} con el usuario de prueba ana/secreta -> 200 {"access_token","token_type":"bearer","expires_in"}; credenciales malas -> 401.
- El token lleva los claims sub (usuario), iat y exp (15 minutos).
- GET /api/perfil protegido con HTTPBearer: valida firma y expiración. Token alterado, vencido o ausente -> 401 con WWW-Authenticate: Bearer, nunca 500.
- Fija algorithms=["HS256"] al decodificar para no aceptar "none".
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> La clave sale de `os.environ["JWT_SECRET_KEY"]`. Como el verificador no define esa variable, si no existe genero una aleatoria con `secrets.token_urlsafe(48)` al arrancar. Así **nunca** hay una clave fija escrita en el repositorio; la consecuencia es que los tokens dejan de servir si se reinicia el servidor, lo cual en un laboratorio está bien.
>
> El token lleva `sub` (usuario), `iat` y `exp` a 15 minutos. Al decodificar:
> - `algorithms=["HS256"]` fijo, para que no se acepte un token con algoritmo `none`;
> - `require: ["exp", "sub"]`, para que un token sin expiración no sirva;
> - cualquier `InvalidTokenError` (firma mala, formato roto) → 401, y `ExpiredSignatureError` → 401 con mensaje de "vencido".
>
> La validación está en una dependencia (`usuario_actual`), así cualquier ruta futura se protege solo con agregar `Depends(usuario_actual)`.
>
> En el payload no va nada sensible: Base64 **no es cifrado** y cualquiera puede leer el contenido del token.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> El caso 03 agrega una `x` al final del token. Mi primera idea era atrapar solo `ExpiredSignatureError`, pero un token alterado lanza `DecodeError` o `InvalidSignatureError`, y sin capturarlos el servidor respondía **500**. Lo corregí atrapando la clase padre `jwt.InvalidTokenError`, que cubre todos los casos de token inválido.
>
> Para el caso 04 (sin token) usé `HTTPBearer(auto_error=False)`; así yo controlo la respuesta y siempre es 401 con `WWW-Authenticate: Bearer`, sin depender del comportamiento por defecto de la versión de FastAPI (en versiones anteriores, el error automático era 403).
>
> Aprendí la diferencia con la sesión 13: con JWT el servidor no guarda nada (**stateless**), pero por lo mismo no puede "cerrar" un token antes de que expire; por eso la expiración debe ser corta.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/a12eb8a
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion15/sesion15_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion15.html

---
**Firma digital:** `XxZoroxX10`
