# Laboratorio 00 · Git, GitHub Codespaces y tu primer commit

**Antes de la Sesión 01** · Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente:** MCC. Iván Márquez Larios (`ijmarquezl`) · TecNM Cancún

---

## 🖥️ Así se verá el resultado final

```bash
$ git status
On branch main
nothing to commit, working tree clean

$ git log --oneline -1
a1b2c3d feat: agrega soporte para PATCH en el despachador HTTP

$ git push origin main
To https://github.com/<tu-usuario>/tecnm-desarrollo-web.git
   a1b2c3d..e4f5g6h  main -> main
```

En GitHub se ve tu commit con tu nombre, el mensaje y el archivo `app_http_test.py`. Ese es el resultado: **tu trabajo publicado**, no solo guardado en el Codespace.

---

## 🎯 Al finalizar podrás

- Abrir un Codespace desde tu fork y trabajar en un entorno Linux sin instalar nada.
- Ejecutar un script de Python que simula el despacho de métodos HTTP.
- Publicar un cambio con el ciclo `git status` → `git add` → `git commit` → `git push`.
- Explicar por qué un archivo que solo vive en el Codespace no cuenta como entrega.

## 🧩 El reto (sin pasos)

Tu repositorio debe terminar con **un commit propio** que agregue el archivo `app_http_test.py` con soporte para el método `PATCH`, y ese commit debe estar visible en GitHub. Tú decides cómo editar, cómo probar y qué mensaje de commit usar; el resultado es lo que se evalúa.

### Primer script

Crea `app_http_test.py` con un despachador que devuelva el resultado de cada método:

```python
import sys

def procesar_metodo(metodo: str):
    metodos_validos = {
        "GET": "200 OK - Lectura de recurso exitosa",
        "POST": "201 Created - Nuevo recurso creado",
        "PUT": "200 OK - Recurso actualizado",
        "DELETE": "204 No Content - Recurso eliminado",
        "PATCH": "200 OK - Recurso modificado parcialmente",
    }
    return metodos_validos.get(metodo.upper(), "405 Method Not Allowed")

if __name__ == "__main__":
    metodo_prueba = sys.argv[1] if len(sys.argv) > 1 else "GET"
    print(f"[Simulador HTTP] Petición recibida: {metodo_prueba}")
    print(f"Respuesta del Servidor: {procesar_metodo(metodo_prueba)}")
```

Ejecútalo con `python app_http_test.py PATCH` y comprueba que responde `200 OK - Recurso modificado parcialmente`.

> **Pista conceptual:** Git tiene tres zonas: tu carpeta de trabajo, el área de preparación (`add`) y el historial (`commit`). `push` solo envía lo que ya está en el historial.

## ✅ Criterios de aceptación

- [ ] El Codespace abre desde **tu fork**, no desde el repositorio del docente.
- [ ] `python app_http_test.py PATCH` responde con `200 OK`.
- [ ] `git status` muestra el árbol de trabajo limpio al terminar.
- [ ] `git log --oneline -1` muestra un commit con un mensaje descriptivo.
- [ ] El commit es visible en tu repositorio de GitHub (no solo en el Codespace).
- [ ] Tu `README.md` tiene tu nombre y matrícula.

## 🆘 Si algo falla

| Síntoma | Causa probable | Qué revisar |
| :--- | :--- | :--- |
| `fatal: not a git repository` | Abriste la terminal fuera del repositorio | `pwd` y `git status`; abre el Codespace desde tu fork. |
| `nothing to commit` | No guardaste el archivo o no hiciste `git add` | `git status` y vuelve a preparar el archivo. |
| `rejected (fetch first)` | Tu remoto tiene cambios que no tienes | `git pull --rebase origin main` y vuelve a empujar. |
| `Permission denied` | Estás empujando al repositorio del docente | Revisa `git remote -v`; debe apuntar a tu usuario. |

## 📦 Entregable

Tu fork con el commit publicado y el `README.md` identificado. La presentación de esta sesión previa está en `presentaciones/lab00-git-codespaces.html`.
