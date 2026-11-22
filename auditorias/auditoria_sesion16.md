# Bitácora de la Sesión 16 — OAuth2 Password Flow y Header Authorization Bearer

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu OAuth2 Password Flow se verá así

> Llegué al resultado completo: 4/4 casos HTTP y 1/1 comprobación en verde. El login ahora recibe un formulario (no JSON), devuelve un token Bearer y el perfil rechaza con 401 tanto la falta de token como un esquema que no sea Bearer.

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. El formulario de login emite token
✅ 02. El token Bearer abre el perfil
✅ 03. Sin token se responde 401 con WWW-Authenticate
✅ 04. Un esquema distinto se rechaza
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!

✅ Se usa el flujo OAuth2 de FastAPI
------------------------------------------------------------------------------
RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] El formulario de login emite token → HTTP 200
- [x] El token Bearer abre el perfil → HTTP 200
- [x] Sin token se responde 401 con WWW-Authenticate → HTTP 401
- [x] Un esquema distinto se rechaza → HTTP 401
- [x] Se usa el flujo OAuth2 de FastAPI

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI con `OAuth2PasswordBearer` y `OAuth2PasswordRequestForm` + PyJWT (HS256); clave desde `JWT_SECRET_KEY` |
| **Rol** | Desarrollador backend que adapta el login JWT al flujo estándar OAuth2 *password* |
| **Especificación** | `POST /token` recibe `username` y `password` como `application/x-www-form-urlencoded` → 200 `{"access_token", "token_type": "bearer"}`; credenciales malas → 401; `GET /api/perfil` con `Authorization: Bearer` → 200 `{"usuario", "nombre"}`; sin token, token inválido o esquema distinto → 401 con `WWW-Authenticate: Bearer` |
| **Output** | Solo `app.py` |

### Prompt que utilicé

```text
Rol: desarrollador backend con FastAPI.
Contexto: ya tengo login con JWT (sesión 15); ahora quiero usar el flujo OAuth2 "password" que trae FastAPI para que Swagger tenga el botón Authorize.
- Usa OAuth2PasswordBearer(tokenUrl="token") y OAuth2PasswordRequestForm.
- POST /token recibe username y password como formulario (no JSON). Usuario de prueba: ana / secreta.
  Correcto -> 200 {"access_token": ..., "token_type": "bearer"}. Incorrecto -> 401.
- JWT HS256 con sub, iat y exp (15 min). Clave desde la variable JWT_SECRET_KEY; si no existe, genera una aleatoria.
- GET /api/perfil -> {"usuario","nombre"}. Sin token, token inválido o esquema que no sea Bearer -> 401 con WWW-Authenticate: Bearer. Nunca 500.
- Compara la contraseña con hmac.compare_digest.
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Lo nuevo de esta sesión no es el JWT (ese ya lo tenía), sino **cómo llega el login**. `OAuth2PasswordRequestForm` obliga a mandar `username` y `password` como formulario, que es lo que dice el estándar OAuth2. Por eso el verificador manda `data=` y no `json=`; si mandas JSON, FastAPI responde 422.
>
> `OAuth2PasswordBearer(tokenUrl="token")` hace dos cosas:
> - le dice a Swagger dónde pedir el token (por eso el botón **Authorize** ya funciona solo);
> - lee el encabezado `Authorization`, y si falta o no empieza con `Bearer`, responde 401 con `WWW-Authenticate: Bearer` sin que yo escriba ese `if`.
>
> Dejé el `HTTPException` de "credenciales inválidas" en una constante para reutilizarlo en el login y al validar el token, así el mensaje y el encabezado siempre son los mismos. La contraseña se compara con `hmac.compare_digest` para no dar pistas por tiempo de respuesta.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> Lo primero que me confundió fue que `tokenUrl="token"` va **sin** la diagonal inicial: es una ruta relativa que usa Swagger, y tiene que coincidir con el `@app.post("/token")`. Si pones otra ruta, la API funciona, pero el botón Authorize de `/docs` falla.
>
> También me di cuenta de que `OAuth2PasswordRequestForm` necesita el paquete `python-multipart` para leer formularios; en Colab ya venía instalado por la celda de preparación, pero en mi máquina habría que agregarlo a `requirements.txt` o la app ni arranca.
>
> El caso 04 manda `Authorization: Basic ...`. No tuve que hacer nada especial: `OAuth2PasswordBearer` revisa el esquema y lo rechaza con 401. Lo comprobé en la salida del verificador antes de dar por hecho que funcionaba.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/051d25f
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion16/sesion16_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion16.html

---
**Firma digital:** `XxZoroxX10`
