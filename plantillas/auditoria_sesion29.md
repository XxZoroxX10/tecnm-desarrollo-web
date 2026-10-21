# Bitácora de la Sesión 29 — Protección Anti-CSRF y Cookies HttpOnly / SameSite

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Nombre completo]  
**Matrícula:** [Número de control]  
**Track:** [Python/FastAPI | PHP 8+]  
**Fecha:** [DD/MM/AAAA]

---

## 1. Resultado al que llegué

**Resultado esperado:** Tu protección CSRF se verá así

> Pega aquí la salida de la celda de verificación (los casos en verde) o describe exactamente qué obtuviste.

```text
[Pega aquí la salida de la verificación]
```

## 2. Criterios de aceptación

- [ ] El login emite una cookie HttpOnly y SameSite → HTTP 200
- [ ] El logout sin token se rechaza → HTTP 403
- [ ] El token CSRF se obtiene → HTTP 200
- [ ] El logout con token funciona → HTTP 204

## 3. Mi contrato C-R-E-O

| Elemento | Definición |
| :--- | :--- |
| **Contexto** | [Framework, versión, entorno] |
| **Rol** | [Papel técnico que asumió la IA] |
| **Especificación** | [Rutas, entradas, salidas, validaciones y códigos HTTP] |
| **Output** | [Formato exacto solicitado] |

### Prompt que utilicé

```text
[Pega aquí tu prompt]
```

## 4. Decisiones de diseño

- ¿Qué estructura elegiste y por qué?
- ¿Qué validaste en el borde de la API y qué dejaste a la lógica de negocio?
- ¿Qué cambiarías si mañana otro equipo consumiera tu API?

> 

## 5. Errores, hallazgos y correcciones

- ¿Qué caso de la verificación falló primero?
- ¿Qué aprendiste al corregirlo?
- ¿Qué harías distinto la próxima vez?

> 

## 6. Evidencia

- **Commit:** [enlace al commit]
- **Cuaderno ejecutado:** [enlace al cuaderno en tu fork]
- **Presentación:** https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion29.html

---
**Firma digital:** [Usuario de GitHub]
