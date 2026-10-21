"""
Motor de verificación de los laboratorios de Desarrollo de Aplicaciones Web.

La idea es siempre la misma: el estudiante declara (o recibe) el resultado
final esperado y este módulo comprueba, caso por caso, si su implementación
lo alcanza. No hay pasos intermedios: solo resultado esperado vs. resultado
obtenido.

Uso típico dentro de un cuaderno de Colab:

    from verificar import probar_http
    probar_http([...casos...], archivo="app.py")

También disponible para comprobaciones de archivos, JSON y Python.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import traceback
from pathlib import Path

VERDE = "\033[92m"
ROJO = "\033[91m"
AMARILLO = "\033[93m"
GRIS = "\033[90m"
RESET = "\033[0m"


class FallaVerificacion(Exception):
    """Se lanza cuando el resultado del estudiante no coincide con el esperado."""


def _leer(ruta: str | Path) -> str:
    return Path(ruta).read_text(encoding="utf-8", errors="ignore")


def _imprimir_resultado(nombre: str, errores: list[str], detalle: str = "") -> bool:
    if errores:
        print(f"{ROJO}❌ {nombre}{RESET}")
        for error in errores:
            print(f"   · {error}")
        if detalle:
            print(f"   {GRIS}respuesta real: {detalle[:500]}{RESET}")
        return False
    print(f"{VERDE}✅ {nombre}{RESET}")
    return True


# ---------------------------------------------------------------------------
# Comparación de estructuras JSON
# ---------------------------------------------------------------------------
def _coincide(esperado, real, ruta: str = "respuesta") -> list[str]:
    """Devuelve la lista de diferencias entre el JSON esperado y el real.

    Los diccionarios se comparan por subconjunto: basta con que existan las
    claves esperadas. Las listas se comparan por longitud y orden.
    """
    errores: list[str] = []

    if isinstance(esperado, dict):
        if not isinstance(real, dict):
            return [f"{ruta}: se esperaba un objeto JSON, llegó {type(real).__name__}"]
        for clave, valor in esperado.items():
            if clave not in real:
                errores.append(f"{ruta}.{clave}: falta")
            else:
                errores.extend(_coincide(valor, real[clave], f"{ruta}.{clave}"))
        return errores

    if isinstance(esperado, list):
        if not isinstance(real, list):
            return [f"{ruta}: se esperaba una lista, llegó {type(real).__name__}"]
        if len(esperado) != len(real):
            errores.append(f"{ruta}: se esperaban {len(esperado)} elementos, llegaron {len(real)}")
        for indice, (esperado_item, real_item) in enumerate(zip(esperado, real)):
            errores.extend(_coincide(esperado_item, real_item, f"{ruta}[{indice}]"))
        return errores

    if esperado != real:
        return [f"{ruta}: se esperaba {esperado!r}, llegó {real!r}"]
    return []


# ---------------------------------------------------------------------------
# Verificación de APIs HTTP
# ---------------------------------------------------------------------------
def _cargar_app(ruta: str | Path):
    ruta = Path(ruta)
    if not ruta.exists():
        raise FallaVerificacion(
            f"No existe {ruta.name}. Escribe tu implementación en la celda del reto."
        )

    nombre_modulo = "app_alumno_" + re.sub(r"\W+", "_", ruta.resolve().name)
    if nombre_modulo in sys.modules:
        del sys.modules[nombre_modulo]

    spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
    if spec is None or spec.loader is None:
        raise FallaVerificacion(f"No se pudo cargar {ruta.name}.")

    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre_modulo] = modulo
    try:
        spec.loader.exec_module(modulo)
    except Exception as exc:  # noqa: BLE001
        detalle = traceback.format_exc()
        raise FallaVerificacion(
            f"Tu {ruta.name} no se pudo importar: {exc.__class__.__name__}: {exc}\n"
            f"{detalle}"
        ) from exc

    if not hasattr(modulo, "app"):
        raise FallaVerificacion(
            f"{ruta.name} no define una variable `app` (la instancia de FastAPI)."
        )
    return modulo


def probar_http(
    casos: list[dict],
    archivo: str = "app.py",
    limpiar: tuple[str, ...] | list[str] = (),
    env: dict[str, str] | None = None,
) -> None:
    """Ejecuta una lista de casos HTTP contra la app del estudiante.

    Cada caso admite estas claves:
      descripcion, metodo, ruta, json, data, content, headers, cookies,
      estado, json_contiene, json_exacto, cuerpo_contiene, no_contiene,
      headers_contiene, guardar (dict nombre -> campo del JSON de respuesta).

    Los valores guardados se pueden interpolar en encabezados posteriores con
    la sintaxis `{nombre}`. Así se encadenan login -> token -> ruta privada.
    """
    try:
        from fastapi.testclient import TestClient
    except Exception as exc:  # noqa: BLE001
        raise FallaVerificacion(
            "Falta FastAPI/HTTPX en el entorno. Ejecuta la celda de instalación."
        ) from exc

    for ruta_limpiar in limpiar:
        try:
            os.remove(ruta_limpiar)
        except FileNotFoundError:
            pass

    if env:
        os.environ.update({str(k): str(v) for k, v in env.items()})

    modulo = _cargar_app(archivo)
    cliente = TestClient(modulo.app, raise_server_exceptions=False)
    guardado: dict[str, object] = {}
    fallos = 0

    print("=" * 78)
    print(f"VERIFICACIÓN DEL RESULTADO · {len(casos)} casos · {archivo}")
    print("=" * 78)

    for indice, caso in enumerate(casos, start=1):
        metodo = caso.get("metodo", "GET").upper()
        ruta = caso["ruta"].format(**guardado) if isinstance(caso["ruta"], str) else caso["ruta"]
        descripcion = caso.get("descripcion", f"{metodo} {ruta}")

        kwargs: dict[str, object] = {}
        if "json" in caso:
            kwargs["json"] = caso["json"]
        if "data" in caso:
            kwargs["data"] = caso["data"]
        if "content" in caso:
            kwargs["content"] = caso["content"]

        if "headers" in caso:
            headers: dict[str, str] = {}
            for clave, valor in caso["headers"].items():
                headers[clave] = valor.format(**guardado) if isinstance(valor, str) else valor
            kwargs["headers"] = headers

        if "cookies" in caso:
            kwargs["cookies"] = caso["cookies"]

        try:
            respuesta = cliente.request(metodo, ruta, **kwargs)
        except Exception as exc:  # noqa: BLE001
            print(f"{ROJO}❌ {indice:02d}. {descripcion}{RESET}")
            print(f"   · el servidor lanzó {exc.__class__.__name__}: {exc}")
            fallos += 1
            continue

        errores: list[str] = []

        estado_esperado = caso.get("estado")
        if estado_esperado is not None and respuesta.status_code != estado_esperado:
            errores.append(
                f"HTTP {respuesta.status_code} (se esperaba HTTP {estado_esperado})"
            )

        if "json_contiene" in caso or "json_exacto" in caso or "guardar" in caso:
            try:
                cuerpo = respuesta.json()
            except Exception:  # noqa: BLE001
                cuerpo = None
                if "json_contiene" in caso or "json_exacto" in caso:
                    errores.append("la respuesta no es JSON válido")

            if cuerpo is not None:
                if "json_contiene" in caso:
                    errores.extend(_coincide(caso["json_contiene"], cuerpo))
                if "json_exacto" in caso and cuerpo != caso["json_exacto"]:
                    errores.append(
                        f"cuerpo: se esperaba {caso['json_exacto']!r}, llegó {cuerpo!r}"
                    )
                for nombre, campo in caso.get("guardar", {}).items():
                    if isinstance(campo, str) and campo in cuerpo:
                        guardado[nombre] = cuerpo[campo]
                    else:
                        errores.append(f"no se encontró el campo «{campo}» para guardar {nombre}")

        for texto in caso.get("cuerpo_contiene", []):
            if texto not in respuesta.text:
                errores.append(f"falta en el cuerpo: {texto!r}")

        for texto in caso.get("no_contiene", []):
            if texto in respuesta.text:
                errores.append(f"no debería aparecer en el cuerpo: {texto!r}")

        for clave, valor in caso.get("headers_contiene", {}).items():
            real = respuesta.headers.get(clave)
            if real is None:
                errores.append(f"falta el encabezado «{clave}»")
            elif str(valor).lower() not in str(real).lower():
                errores.append(f"encabezado «{clave}»: {real!r} no contiene {valor!r}")

        for clave, valor in caso.get("headers_no_contiene", {}).items():
            real = respuesta.headers.get(clave)
            if real is not None and str(valor).lower() in str(real).lower():
                errores.append(f"el encabezado «{clave}» no debería contener {valor!r}: {real!r}")

        if not _imprimir_resultado(f"{indice:02d}. {descripcion}", errores, respuesta.text):
            fallos += 1

    print("-" * 78)
    if fallos:
        print(
            f"{ROJO}RESULTADO: {fallos} de {len(casos)} casos fallaron. "
            f"Todavía no llegas al resultado esperado.{RESET}"
        )
        raise AssertionError(f"{fallos} caso(s) no cumplieron el resultado esperado")
    print(f"{VERDE}RESULTADO: {len(casos)}/{len(casos)} casos correctos. "
          f"¡Resultado logrado!{RESET}")


# ---------------------------------------------------------------------------
# Verificación de archivos
# ---------------------------------------------------------------------------
def revisar_archivo(
    ruta: str | Path,
    exigir: tuple[str, ...] | list[str] = (),
    prohibir: tuple[str, ...] | list[str] = (),
    regex: tuple[str, ...] | list[str] = (),
    descripcion: str | None = None,
) -> bool:
    """Comprueba que un archivo exista y contenga / no contenga ciertos textos."""
    ruta = Path(ruta)
    nombre = descripcion or f"Archivo {ruta}"
    errores: list[str] = []

    if not ruta.exists():
        errores.append(f"no existe el archivo «{ruta}»")
        return _imprimir_resultado(nombre, errores)

    texto = _leer(ruta)
    for fragmento in exigir:
        if fragmento not in texto:
            errores.append(f"falta: {fragmento!r}")
    for fragmento in prohibir:
        if fragmento in texto:
            errores.append(f"no debe aparecer: {fragmento!r}")
    for patron in regex:
        if not re.search(patron, texto, flags=re.MULTILINE | re.IGNORECASE):
            errores.append(f"no cumple el patrón: {patron!r}")

    return _imprimir_resultado(nombre, errores)


def revisar_json(
    ruta: str | Path,
    claves: tuple[str, ...] | list[str] = (),
    contiene: tuple[str, ...] | list[str] = (),
    descripcion: str | None = None,
) -> bool:
    """Valida que un archivo sea JSON y contenga claves (notación con puntos)."""
    ruta = Path(ruta)
    nombre = descripcion or f"JSON {ruta}"
    errores: list[str] = []

    try:
        datos = json.loads(_leer(ruta))
    except FileNotFoundError:
        return _imprimir_resultado(nombre, [f"no existe el archivo «{ruta}»"])
    except json.JSONDecodeError as exc:
        return _imprimir_resultado(nombre, [f"no es JSON válido: {exc}"])

    for clave in claves:
        actual = datos
        encontrada = True
        for parte in clave.split("."):
            if isinstance(actual, dict) and parte in actual:
                actual = actual[parte]
            else:
                encontrada = False
                break
        if not encontrada:
            errores.append(f"falta la clave «{clave}»")

    for fragmento in contiene:
        if fragmento not in _leer(ruta):
            errores.append(f"falta en el JSON: {fragmento!r}")

    return _imprimir_resultado(nombre, errores)


def revisar_python(codigo: str, descripcion: str = "Comprobación de Python") -> bool:
    """Ejecuta un bloque de Python que debe terminar sin excepciones.

    Dentro del bloque se puede usar `assert` y `Path`, `os`, `json`, `re`.
    """
    try:
        exec(compile(codigo, "<verificacion>", "exec"), {"__name__": "__verificacion__"})
    except Exception as exc:  # noqa: BLE001
        detalle = traceback.format_exc(limit=3)
        return _imprimir_resultado(descripcion, [f"{exc.__class__.__name__}: {exc}"], detalle)
    return _imprimir_resultado(descripcion, [])


def resumen(resultados: list[bool]) -> None:
    """Cierra una verificación con varios archivos/comprobaciones."""
    total = len(resultados)
    correctos = sum(1 for resultado in resultados if resultado)
    print("-" * 78)
    if correctos != total:
        print(f"{ROJO}RESULTADO: {correctos}/{total} comprobaciones correctas. "
              f"Aún falta ajustar el resultado.{RESET}")
        raise AssertionError(f"{total - correctos} comprobación(es) fallaron")
    print(f"{VERDE}RESULTADO: {correctos}/{total} comprobaciones correctas. "
          f"¡Resultado logrado!{RESET}")
