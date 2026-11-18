# Bitácora de la Sesión 13 — Manejo de Sesiones Stateful vs Stateless Tokens

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu flujo de sesión se verá así

> Llegué al resultado completo: 4/4 casos en verde (login con cookie HttpOnly y SameSite, perfil con la cookie, logout 204 y perfil 401 después del logout).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. Login correcto y cookie HttpOnly
✅ 02. El perfil se obtiene con la cookie
✅ 03. El logout cierra la sesión
✅ 04. Después del logout el perfil es 401
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] Login correcto y cookie HttpOnly → HTTP 200
- [x] El perfil se obtiene con la cookie → HTTP 200
- [x] El logout cierra la sesión → HTTP 204
- [x] Después del logout el perfil es 401 → HTTP 401

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI con sesiones stateful guardadas en la memoria del servidor y una cookie `session_id`; el verificador usa `TestClient`, que conserva las cookies entre peticiones |
| **Rol** | Desarrollador backend responsable de la autenticación con sesiones seguras |
| **Especificación** | Usuario de prueba `ana`/`secreta`; `POST /api/login` → 200 y cookie `session_id` con `HttpOnly` y `SameSite=Lax`, credenciales malas → 401; `GET /api/perfil` → 200 con el usuario si la sesión existe y no expiró, si no 401; `POST /api/logout` → 204 e invalida la sesión en el servidor |
| **Output** | Solo `app.py`, con id de sesión generado con `secrets.token_urlsafe` y expiración |

### Prompt que utilicé

```text
Rol: desarrollador backend que implementa sesiones con estado.
Contexto: FastAPI, sesiones guardadas en un diccionario en memoria del servidor.
Usuario de prueba: ana / secreta.
- POST /api/login {"usuario","password"}: si es correcto, crea un session_id aleatorio (secrets), guarda {usuario, expira} en el servidor y manda la cookie session_id con HttpOnly, SameSite=Lax y max_age de 30 min. Responde 200. Si no, 401.
- GET /api/perfil: lee la cookie; si la sesión existe y no expiró responde 200 {"usuario": ...}; si no, 401.
- POST /api/logout: borra la sesión del servidor y la cookie; responde 204.
Compara la contraseña en tiempo constante. Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> El cliente solo guarda un identificador **opaco** (`secrets.token_urlsafe(32)`, imposible de adivinar); el usuario y la expiración viven en el diccionario `SESIONES` del servidor.
>
> La cookie lleva:
> - `HttpOnly`: JavaScript no la puede leer, así que un XSS no puede robarla.
> - `SameSite=Lax`: no viaja en POST que vengan de otros sitios (mitiga CSRF).
> - `max_age` de 30 minutos, y además el servidor revisa `expira`. Si la sesión venció, la borra y responde 401.
> - `secure=False` solo porque el `TestClient` usa `http://`; en producción con HTTPS va en `True`.
>
> El logout invalida la sesión **en el servidor** (no basta con borrar la cookie del navegador) y responde 204.
>
> La contraseña se compara con `hmac.compare_digest` para que tarde lo mismo acierte o no. En esta sesión sigue en texto plano solo porque es el usuario de prueba; en la 14 se guarda con hash.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Al principio puse `secure=True` en la cookie porque "así es en producción", y el caso 02 falló: el `TestClient` usa `http://testserver`, y una cookie `Secure` solo se manda por HTTPS, así que nunca regresaba al servidor. Lo dejé en `False` con un comentario explicando que en producción va en `True`.
>
> También pensé que con `delete_cookie` bastaba para el logout, pero si alguien copió el `session_id` antes, la sesión seguiría viva. Por eso primero la borro del diccionario del servidor; el caso 04 confirma el 401 después del logout.
>
> Aprendí la diferencia: en una sesión **stateful** el servidor puede invalidarla cuando quiera (logout real), pero tiene que guardar estado; eso cambia en la sesión 15 con JWT.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/dec339a
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion13/sesion13_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion13.html

---
**Firma digital:** `XxZoroxX10`
