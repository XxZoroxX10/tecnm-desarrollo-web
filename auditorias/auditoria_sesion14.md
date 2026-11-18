# Bitácora de la Sesión 14 — Hashing Seguro de Contraseñas (Bcrypt / Argon2)

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Pedro Pablo Pool Ché  
**Matrícula:** 23531067  
**Track:** Python/FastAPI  
**Fecha:** 18/11/2026

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu registro y login se verán así

> Llegué al resultado completo: 3/3 casos HTTP y 1/1 comprobación en verde (registro sin filtrar la contraseña ni el hash, login correcto y 401 con contraseña incorrecta).

```text
==============================================================================
VERIFICACIÓN DEL RESULTADO · 3 casos · app.py
==============================================================================
✅ 01. El registro responde sin filtrar la contraseña
✅ 02. El login correcto autentica
✅ 03. La contraseña incorrecta se rechaza
------------------------------------------------------------------------------
RESULTADO: 3/3 casos correctos. ¡Resultado logrado!

✅ Se usa un algoritmo de hashing para contraseñas
------------------------------------------------------------------------------
RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!
```

## 2. Criterios de aceptación

- [x] El registro responde sin filtrar la contraseña → HTTP 201
- [x] El login correcto autentica → HTTP 200
- [x] La contraseña incorrecta se rechaza → HTTP 401
- [x] Se usa un algoritmo de hashing para contraseñas

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | FastAPI + la librería `bcrypt` (hash lento que ya incluye el salt), con usuarios en memoria |
| **Rol** | Desarrollador backend responsable de guardar credenciales de forma segura |
| **Especificación** | `POST /api/registro` guarda solo el hash bcrypt y responde 201 `{"usuario", "mensaje"}` sin contraseña ni hash; usuario repetido → 409 sin sobrescribir; `POST /api/login` verifica con `bcrypt.checkpw` → 200 `{"usuario", "autenticado": true}` o 401 con mensaje genérico; contraseña de máximo 72 bytes |
| **Output** | Solo `app.py`, con un DTO de salida que nunca incluya el hash |

### Prompt que utilicé

```text
Actúa como desarrollador backend especializado en seguridad.
Contexto: FastAPI + bcrypt (sin passlib), usuarios en un diccionario en memoria.
- POST /api/registro {"usuario","password"}: guarda SOLO el hash bcrypt (gensalt con costo 12) y responde 201 {"usuario","mensaje"}. La respuesta no debe incluir la contraseña ni el hash. Si el usuario ya existe -> 409 y NO sobrescribir.
- POST /api/login: verifica con bcrypt.checkpw -> 200 {"usuario","autenticado": true}; si falla -> 401 con mensaje genérico (sin decir si falló el usuario o la contraseña).
- Evita que se pueda saber si un usuario existe midiendo el tiempo de respuesta.
- Rechaza contraseñas de más de 72 bytes (límite de bcrypt).
Devuelve solo app.py.
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> Usé `bcrypt` directamente: `hashpw(password, gensalt(12))` para guardar y `checkpw` para verificar. Nunca comparo hashes con `==`; `checkpw` saca el salt del propio hash y hace la comparación.
>
> El costo 12 hace que cada hash tarde unos cientos de milisegundos: casi nada para un login, pero muy caro para alguien que quiere probar millones de contraseñas.
>
> La salida pasa por el DTO `UsuarioPublico` (`usuario` + `mensaje`), así es imposible que el hash se escape en la respuesta aunque cambie el código del endpoint.
>
> Si el usuario ya existe respondo **409** y no toco el hash guardado; si no, cualquiera podría "registrarse" otra vez con tu nombre y cambiarte la contraseña.
>
> En el login, si el usuario no existe igual corro `checkpw` contra un hash señuelo, para que la respuesta tarde lo mismo y no se pueda saber qué usuarios existen. El mensaje del 401 es el mismo en los dos casos.

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> El caso 01 tiene una trampa: revisa que la respuesta **no contenga** las palabras `password` ni `hash`. Mi primer mensaje de éxito decía "contraseña guardada con hash" y habría fallado aunque no filtrara nada real. Lo cambié a "Cuenta creada".
>
> Investigando bcrypt aprendí que solo usa los primeros **72 bytes** de la contraseña; las versiones nuevas lanzan error si son más largas. Por eso agregué un validador que la rechaza con 422 en lugar de truncarla en silencio o de provocar un 500.
>
> También descarté `passlib`, aunque el cuaderno lo instala: con las versiones recientes de `bcrypt` da advertencias de compatibilidad, y usar `bcrypt` directo es más simple y cumple el requisito.

## 6. Evidencia

- **Commit:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/commit/0b277c7
- **Cuaderno ejecutado:** https://github.com/XxZoroxX10/tecnm-desarrollo-web/blob/main/laboratorios/sesion14/sesion14_laboratorio.ipynb
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion14.html

---
**Firma digital:** `XxZoroxX10`
