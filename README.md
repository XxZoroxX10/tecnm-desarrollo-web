# Desarrollo de Aplicaciones Web (DAB-2201)

Repositorio oficial y entorno de laboratorio interactivo del curso de **Desarrollo de Aplicaciones Web** del Tecnológico Nacional de México / Instituto Tecnológico de Cancún.

**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Sitio del curso:** [ijmarquezl.github.io/tecnm-desarrollo-web](https://ijmarquezl.github.io/tecnm-desarrollo-web/)

---

## 🚀 Flujo de trabajo en la nube (100% en navegador)

1. Realiza un **fork** de este repositorio a tu cuenta personal de GitHub.
2. Identifícate editando este `README.md` con tu nombre, matrícula y track.
3. Abre la sesión con el botón **Open in Colab**.
4. Lee la presentación, resuelve el **reto** y ejecuta la **verificación**.
5. Copia la plantilla de `plantillas/auditoria_sesionXX.md` a `auditorias/auditoria_sesionXX.md` y haz commit.

> **Track de los laboratorios:** los cuadernos están implementados en **Python / FastAPI**. El track **PHP 8+** comparte los mismos contratos HTTP y puede resolverse con las herramientas equivalentes de PHP; la verificación automática del cuaderno está construida para Python.

---

## 🧭 Cómo leer una sesión

Cada presentación tiene **7 diapositivas** con la misma estructura:

1. **Portada:** tema explícito, pregunta detonadora y objetivos de la clase.
2. **Mapa de la sesión:** qué veremos, en qué orden y qué necesitas traer.
3. **Conceptos desde cero:** cuatro términos clave con definición y analogía.
4. **Fundamentos:** la teoría central del tema.
5. **Cómo funciona por dentro:** arquitectura y modelo mental.
6. **Errores comunes:** antipatrones y cómo los detecta la verificación.
7. **Resultado final:** el comportamiento exacto que debe tener tu API y el enlace al cuaderno.

Cada laboratorio sigue el principio de **resultado primero**:

- Abre con **“Así se verá el resultado final”**: la salida exacta esperada.
- Declara los **criterios de aceptación** y el contrato, **sin pasos intermedios**.
- Te da un esqueleto mínimo y tú decides la estructura.
- Cierra con un **verificador automático** que compara esperado vs. obtenido y te dice qué falta.

La evaluación no premia “seguir instrucciones”: premia **alcanzar el resultado** y poder explicarlo.

---

## 🧰 Antes de la sesión 01: Git y Codespaces

Si es tu primera vez en el curso, empieza por la **sesión previa 00**: abrir tu Codespace, ejecutar tu primer script y publicar tu primer commit.

- [Presentación: Git, Codespaces y primer commit](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/lab00-git-codespaces.html)
- [Guía del Laboratorio 00](https://github.com/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/lab00-git-codespaces.md)

---

## 🏗️ Proyecto Integrador Semestral (30%)

- **Hito 1 (Sesión 10):** Mock API RESTful con especificación OpenAPI y validation harness.
- **Hito 2 (Sesión 20):** API con inyección de dependencias, autenticación JWT y roles (RBAC).
- **Hito 3 (Sesión 30):** API persistente con base de datos relacional, migraciones y blindaje OWASP.
- **Hito 4 (Sesión 40):** Demostración de API full-stack desplegada en producción con cliente SPA.

---

## 🗺️ Mapa del curso

| Bloque | Sesiones | Foco |
| :--- | :--- | :--- |
| **1** | 01–10 | Arquitectura web, protocolo HTTP y REST APIs |
| **2** | 11–20 | Lógica de negocio, controladores y autenticación segura |
| **3** | 21–30 | Persistencia relacional, ORM y seguridad OWASP |
| **4** | 31–40 | Despliegue en producción, cliente Fetch/SPA y pruebas E2E |

---

## 📚 Índice general de las 40 sesiones

| Sesión | Tema principal | Presentación | Laboratorio |
| :--- | :--- | :---: | :---: |
| **01** | Encuadre, Diagnóstico HTTP y Servidores en la Nube | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion01.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion01/sesion01_laboratorio.ipynb) |
| **02** | Gestión en GitHub Web y Métodos HTTP (GET, POST, PUT, DELETE) | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion02.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion02/sesion02_laboratorio.ipynb) |
| **03** | Headers, Content-Type y Negociación de Contenido | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion03.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion03/sesion03_laboratorio.ipynb) |
| **04** | Anatomía RESTful, URIs Nombres y Recursos | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion04.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion04/sesion04_laboratorio.ipynb) |
| **05** | Pydantic v2 / DTOs en PHP y Tipado Estático | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion05.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion05/sesion05_laboratorio.ipynb) |
| **06** | Validación Estricta, Constraints y Params Query/Body | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion06.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion06/sesion06_laboratorio.ipynb) |
| **07** | Especificación OpenAPI (Swagger) y ReDoc | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion07.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion07/sesion07_laboratorio.ipynb) |
| **08** | Respuestas Semánticas y Excepciones HTTP Personalizadas | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion08.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion08/sesion08_laboratorio.ipynb) |
| **09** | Middleware Web, Intercepción y Logging de Transacciones | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion09.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion09/sesion09_laboratorio.ipynb) |
| **10** | Hito 1: Mock API RESTful con OpenAPI y Validation Harness | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion10.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion10/sesion10_laboratorio.ipynb) |
| **11** | Arquitectura en Capas: Router, Servicio y Capa de Datos | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion11.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion11/sesion11_laboratorio.ipynb) |
| **12** | Inyección de Dependencias (FastAPI Depends / Contenedor IoC) | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion12.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion12/sesion12_laboratorio.ipynb) |
| **13** | Manejo de Sesiones Stateful vs Stateless Tokens | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion13.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion13/sesion13_laboratorio.ipynb) |
| **14** | Hashing Seguro de Contraseñas (Bcrypt / Argon2) | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion14.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion14/sesion14_laboratorio.ipynb) |
| **15** | Autenticación Stateless con JSON Web Tokens (JWT) | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion15.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion15/sesion15_laboratorio.ipynb) |
| **16** | OAuth2 Password Flow y Header Authorization Bearer | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion16.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion16/sesion16_laboratorio.ipynb) |
| **17** | Control de Acceso Basado en Roles (RBAC) | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion17.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion17/sesion17_laboratorio.ipynb) |
| **18** | Rate Limiting, Throttling y Prevención de Abuso | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion18.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion18/sesion18_laboratorio.ipynb) |
| **19** | Sanitización de Entradas, Prevención de XSS e Inyecciones | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion19.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion19/sesion19_laboratorio.ipynb) |
| **20** | Hito 2: API con Inyección de Dependencias, Auth JWT y RBAC | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion20.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion20/sesion20_laboratorio.ipynb) |
| **21** | Fundamentos de Persistencia: SQLite / PostgreSQL y Drivers | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion21.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion21/sesion21_laboratorio.ipynb) |
| **22** | Modelado Relacional (1:1, 1:N, N:M) con ORMs | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion22.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion22/sesion22_laboratorio.ipynb) |
| **23** | Operaciones CRUD Transaccionales y Async Sessions | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion23.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion23/sesion23_laboratorio.ipynb) |
| **24** | Migraciones de Base de Datos con Alembic / Phinx | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion24.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion24/sesion24_laboratorio.ipynb) |
| **25** | Consultas Complejas, Joins y Carga Ansiosa (Eager Loading) | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion25.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion25/sesion25_laboratorio.ipynb) |
| **26** | Transacciones ACID, Aislamiento y Rollback | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion26.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion26/sesion26_laboratorio.ipynb) |
| **27** | Blindaje OWASP: Prevención Total de SQL Injection (SQLi) | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion27.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion27/sesion27_laboratorio.ipynb) |
| **28** | Blindaje Web: Cross-Origin Resource Sharing (CORS) | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion28.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion28/sesion28_laboratorio.ipynb) |
| **29** | Protección Anti-CSRF y Cookies HttpOnly / SameSite | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion29.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion29/sesion29_laboratorio.ipynb) |
| **30** | Hito 3: API Persistente con ORM, Migraciones y Blindaje OWASP | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion30.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion30/sesion30_laboratorio.ipynb) |
| **31** | Contenedorización Básica con Docker y Dockerfiles | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion31.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion31/sesion31_laboratorio.ipynb) |
| **32** | Despliegue en la Nube (Render / Codespaces) y Env Vars | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion32.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion32/sesion32_laboratorio.ipynb) |
| **33** | Servidores ASGI / WSGI en Producción (Uvicorn / Nginx) | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion33.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion33/sesion33_laboratorio.ipynb) |
| **34** | Integración Frontend: Fetch API y JavaScript Asíncrono | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion34.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion34/sesion34_laboratorio.ipynb) |
| **35** | Renderizado Dinámico del DOM y Estado del Cliente | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion35.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion35/sesion35_laboratorio.ipynb) |
| **36** | Arquitectura Single Page Application (SPA) Ligera | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion36.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion36/sesion36_laboratorio.ipynb) |
| **37** | Pruebas Automatizadas E2E con Postman / Newman CLI | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion37.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion37/sesion37_laboratorio.ipynb) |
| **38** | Tareas en Segundo Plano (Background Tasks) Asíncronas | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion38.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion38/sesion38_laboratorio.ipynb) |
| **39** | Monitoreo, Métricas de Salud (/health) y Profiling Web | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion39.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion39/sesion39_laboratorio.ipynb) |
| **40** | Hito 4: Demostración API Full-Stack en Producción con SPA | [Presentación](https://ijmarquezl.github.io/tecnm-desarrollo-web/presentaciones/sesion40.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion40/sesion40_laboratorio.ipynb) |

---

## 🛠️ Mantenimiento del curso

El contenido se genera desde una sola fuente de verdad:

- `datos_teoria.py`: teoría de las 40 sesiones.
- `datos_sesiones_b1.py` … `datos_sesiones_b4.py`: objetivos, conceptos, resultado final, reto y casos de verificación.
- `generar_curso.py`: regenera las 40 presentaciones, los 40 cuadernos, las 40 bitácoras y este README.
- `laboratorios/verificar.py`: motor compartido que descargan los cuadernos desde el commit fijado en `VERIFICADOR_COMMIT`.

Para regenerar todo:

```bash
python3 generar_curso.py
```

Para regenerar una sesión específica:

```bash
python3 generar_curso.py --solo 2
```

---

## 📋 Criterios de evaluación oficial

- **40% Laboratorios diarios:** cuadernos de Colab ejecutados y bitácoras en GitHub.
- **30% Proyecto Integrador:** API RESTful full-stack con persistencia y frontend (4 hitos).
- **20% Evaluaciones prácticas:** 4 hitos prácticos de unidad.
- **10% Participación activa:** sesiones sincrónicas en MS Teams.

---

**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Tecnológico Nacional de México — Campus Cancún**
