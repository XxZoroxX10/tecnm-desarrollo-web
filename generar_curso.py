#!/usr/bin/env python3
"""
Generador oficial del curso Desarrollo de Aplicaciones Web (DAB-2201).

Produce, a partir de una sola fuente de datos:
  - 40 presentaciones HTML (7 diapositivas: objetivos, conceptos, teoría,
    arquitectura, errores y resultado final).
  - 40 cuadernos de laboratorio con enfoque "resultado primero": el
    estudiante ve exactamente qué debe lograr y un verificador automático
    comprueba el resultado, sin pasos intermedios.
  - 40 plantillas de bitácora.
  - README con el índice del curso.

Uso:
    python3 generar_curso.py                # genera todo
    python3 generar_curso.py --solo 1 2 3   # genera solo esas sesiones
    python3 generar_curso.py --sin-readme   # no reescribe el README

Autor: MCC. Iván Márquez Larios (ijmarquezl) · TecNM Campus Cancún
"""

from __future__ import annotations

import argparse
import html
import json
import os
import pprint
import re
import shutil
from pathlib import Path

from datos_teoria import TEORIA
from datos_sesiones_b1 import BLOQUE_1
from datos_sesiones_b2 import BLOQUE_2
from datos_sesiones_b3 import BLOQUE_3
from datos_sesiones_b4 import BLOQUE_4

RAIZ = Path(__file__).resolve().parent
REPO = "https://github.com/ijmarquezl/tecnm-desarrollo-web"
SITIO = "https://ijmarquezl.github.io/tecnm-desarrollo-web"

ENRIQUECIMIENTO = {**BLOQUE_1, **BLOQUE_2, **BLOQUE_3, **BLOQUE_4}

CAMPOS_OBLIGATORIOS = {
    "pregunta",
    "prerrequisitos",
    "objetivos",
    "conceptos",
    "resultado",
    "reto",
    "verificacion",
    "entrega",
}

CSS = r"""
:root {
  --bg: #f3f7fb;
  --bg-2: #e8f1f8;
  --card: rgba(255, 255, 255, 0.94);
  --card-hover: #ffffff;
  --border: #d3dfea;
  --border-strong: #b9cad9;
  --accent: #0969da;
  --accent-soft: #ddf4ff;
  --green: #1a7f37;
  --green-soft: #dafbe1;
  --orange: #b35900;
  --orange-soft: #fff1d6;
  --red: #b42318;
  --red-soft: #ffebe9;
  --silver: #5b6b7c;
  --text: #334155;
  --text-bright: #0f172a;
  --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; }
body {
  background:
    radial-gradient(1200px 600px at 10% -10%, #e3f0fb 0%, transparent 60%),
    radial-gradient(900px 500px at 110% 110%, #e8f8ee 0%, transparent 55%),
    var(--bg);
  color: var(--text);
  font-family: var(--sans);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
header {
  flex: 0 0 auto;
  height: 56px;
  padding: 0 28px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.brand { font-weight: 800; color: var(--text-bright); font-size: 0.92rem; letter-spacing: 0.2px; }
.brand span { color: var(--accent); }
.tag {
  background: var(--accent-soft);
  color: var(--accent);
  border: 1px solid #b6e3ff;
  padding: 4px 11px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-family: var(--mono);
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 62vw;
}
main { flex: 1 1 auto; position: relative; overflow: hidden; }
.slide {
  position: absolute;
  inset: 0;
  padding: 26px 52px 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  opacity: 0;
  visibility: hidden;
  transform: translateX(18px);
  transition: opacity 0.25s ease, transform 0.25s ease, visibility 0.25s;
}
.slide.active { opacity: 1; visibility: visible; transform: translateX(0); }
.slide-inner { width: 100%; max-width: 1380px; margin: auto; }
.kicker {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--mono);
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
  background: var(--accent-soft);
  border: 1px solid #b6e3ff;
  border-radius: 999px;
  padding: 5px 12px;
  margin-bottom: 12px;
}
.kicker.green { color: var(--green); background: var(--green-soft); border-color: #aceebb; }
.kicker.orange { color: var(--orange); background: var(--orange-soft); border-color: #ffd8a8; }
.kicker.red { color: var(--red); background: var(--red-soft); border-color: #ffcecb; }
h1 { font-size: 2.35rem; line-height: 1.12; color: var(--text-bright); margin-bottom: 10px; letter-spacing: -0.02em; }
h2 { font-size: 1.7rem; line-height: 1.18; color: var(--text-bright); margin-bottom: 8px; letter-spacing: -0.01em; }
h3 { font-size: 0.98rem; color: var(--text-bright); margin-bottom: 4px; }
.lead { font-size: 1.04rem; line-height: 1.48; color: #475569; max-width: 1050px; margin-bottom: 14px; }
.lead strong { color: var(--text-bright); }
.small { font-size: 0.82rem; color: var(--silver); line-height: 1.45; }
.grid-2, .grid-3, .grid-4 { display: grid; gap: 14px; align-items: stretch; }
.grid-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.grid-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 15px 16px;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
  transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}
.card.clickable { cursor: pointer; }
.card.clickable:hover { border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 22px rgba(9, 105, 218, 0.10); }
.card.expanded { border-color: var(--accent); background: #fff; }
.card-head { display: flex; justify-content: space-between; gap: 10px; align-items: flex-start; margin-bottom: 6px; }
.card p, .card li { font-size: 0.9rem; line-height: 1.45; color: var(--text); }
.card ul { padding-left: 18px; }
.card li { margin-bottom: 5px; }
.card-details {
  max-height: 0;
  overflow: hidden;
  opacity: 0;
  transition: all 0.25s ease;
  font-size: 0.8rem;
  color: #4b5b6b;
  line-height: 1.45;
}
.card.expanded .card-details { max-height: 320px; opacity: 1; margin-top: 9px; padding-top: 9px; border-top: 1px dashed var(--border); }
.expand-hint { font-size: 0.72rem; color: var(--accent); font-family: var(--mono); white-space: nowrap; }
.num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 26px;
  height: 26px;
  border-radius: 8px;
  background: var(--accent-soft);
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.75rem;
  font-weight: 800;
  margin-right: 8px;
}
.term { font-size: 1.02rem; font-weight: 800; color: var(--text-bright); margin-bottom: 4px; }
.analogy { margin-top: 7px; padding-top: 7px; border-top: 1px dashed var(--border); font-size: 0.8rem; color: #4b5b6b; font-style: italic; }
.theory-detail { margin-top: 8px; padding-top: 8px; border-top: 1px dashed var(--border); font-size: 0.82rem; line-height: 1.42; color: #4b5b6b; }
.analogy::before { content: "En la vida diaria: "; font-style: normal; font-weight: 700; color: var(--silver); }
.objective { min-height: 92px; }
.objective p { font-size: 0.88rem; }
.timeline { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 12px 0; }
.step { position: relative; background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 13px 14px; }
.step::before { content: ""; position: absolute; top: 0; left: 14px; right: 14px; height: 3px; border-radius: 3px; background: var(--accent); }
.step .time { font-family: var(--mono); font-size: 0.72rem; font-weight: 800; color: var(--accent); margin-bottom: 4px; }
.step strong { display: block; color: var(--text-bright); font-size: 0.9rem; margin-bottom: 3px; }
.step p { font-size: 0.78rem; line-height: 1.4; color: #4b5b6b; }
.interactive-box {
  margin-top: 12px;
  padding: 12px 15px;
  background: #fff;
  border: 1px solid var(--border);
  border-left: 4px solid var(--accent);
  border-radius: 8px;
  font-size: 0.85rem;
  line-height: 1.5;
}
.interactive-box strong { color: var(--text-bright); }
.terminal {
  background: #0d1726;
  border: 1px solid #26364a;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 10px 26px rgba(2, 8, 20, 0.22);
}
.terminal-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 11px;
  background: #132033;
  border-bottom: 1px solid #26364a;
}
.dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
.dot.r { background: #ff5f56; } .dot.y { background: #ffbd2e; } .dot.g { background: #27c93f; }
.terminal-title { margin-left: 8px; font-family: var(--mono); font-size: 0.7rem; color: #8ea4bd; }
pre.code {
  margin: 0;
  padding: 13px 15px;
  color: #e6edf6;
  font-family: var(--mono);
  font-size: 0.76rem;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 52vh;
  overflow: auto;
}
pre.code.small { font-size: 0.7rem; }
table.cases { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
table.cases th, table.cases td { text-align: left; padding: 7px 8px; border-bottom: 1px solid var(--border); vertical-align: top; }
table.cases th { font-family: var(--mono); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--silver); }
table.cases code { font-family: var(--mono); font-size: 0.74rem; background: #f1f5f9; padding: 1px 4px; border-radius: 4px; }
.checklist { display: grid; gap: 7px; }
.check { display: flex; gap: 9px; align-items: flex-start; font-size: 0.82rem; line-height: 1.4; }
.check .box { flex: 0 0 16px; width: 16px; height: 16px; border: 1.5px solid var(--border-strong); border-radius: 4px; margin-top: 1px; background: #fff; }
.check strong { color: var(--text-bright); }
.callout { margin-top: 12px; padding: 11px 14px; border-radius: 8px; font-size: 0.84rem; line-height: 1.45; }
.callout.blue { background: var(--accent-soft); border: 1px solid #b6e3ff; color: #0a4b8c; }
.callout.green { background: var(--green-soft); border: 1px solid #aceebb; color: #0b4f22; }
.callout.orange { background: var(--orange-soft); border: 1px solid #ffd8a8; color: #6b3a00; }
.callout.red { background: var(--red-soft); border: 1px solid #ffcecb; color: #7a1a12; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 999px; font-family: var(--mono); font-size: 0.7rem; font-weight: 800; }
.badge.get { background: #ddf4ff; color: #0550ae; } .badge.post { background: #dafbe1; color: #116329; }
.badge.put { background: #fff8c5; color: #7d4e00; } .badge.delete { background: #ffebe9; color: #a40e26; }
.badge.patch { background: #fbefff; color: #8250df; }
.buttons { display: flex; gap: 9px; flex-wrap: wrap; margin-top: 12px; }
.btn {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 9px 14px; border-radius: 8px; border: 1px solid var(--border);
  background: #fff; color: var(--text-bright); font-size: 0.82rem; font-weight: 700;
  text-decoration: none;
}
.btn.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
.btn:hover { filter: brightness(0.98); }
.footer-note { margin-top: 12px; font-size: 0.76rem; color: var(--silver); }
.layout-result { display: grid; grid-template-columns: 1.18fr 0.82fr; gap: 16px; align-items: start; }
.criteria-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 14px 15px; }
.criteria-card h3 { margin-bottom: 8px; }
.criteria-card ul { padding-left: 18px; }
.criteria-card li { font-size: 0.8rem; line-height: 1.42; margin-bottom: 6px; }
footer {
  flex: 0 0 auto;
  height: 52px;
  padding: 0 28px;
  background: rgba(255, 255, 255, 0.9);
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.progress { font-size: 0.8rem; font-family: var(--mono); color: var(--accent); font-weight: 800; }
.progress span { color: var(--silver); font-weight: 500; }
.controls { display: flex; gap: 8px; }
button {
  background: #fff; color: var(--text-bright); border: 1px solid var(--border);
  padding: 7px 15px; border-radius: 7px; cursor: pointer; font-weight: 700; font-size: 0.8rem;
  font-family: var(--sans);
}
button:hover { background: #f8fafc; }
button:disabled { opacity: 0.38; cursor: not-allowed; }
code { font-family: var(--mono); font-size: 0.86em; background: #eef4fa; padding: 1px 5px; border-radius: 4px; color: #0a3069; }
pre code { background: none; padding: 0; color: inherit; }
ul.clean { list-style: none; padding: 0; }
ul.clean li { position: relative; padding-left: 18px; margin-bottom: 6px; font-size: 0.84rem; line-height: 1.42; }
ul.clean li::before { content: "→"; position: absolute; left: 0; color: var(--accent); font-weight: 800; }
@media (max-width: 1180px) {
  .slide { padding: 20px 26px 16px; }
  h1 { font-size: 2rem; } h2 { font-size: 1.45rem; }
  .grid-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .timeline { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .layout-result { grid-template-columns: 1fr; }
}
@media print {
  body { overflow: visible; height: auto; }
  header, footer, .controls { display: none; }
  main { display: block; }
  .slide { position: relative; opacity: 1; visibility: visible; transform: none; page-break-after: always; min-height: 100vh; }
}
"""

JS = r"""
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const indicator = document.getElementById('slideIndicator');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

function updateSlides() {
  slides.forEach((slide, index) => slide.classList.toggle('active', index === currentSlide));
  indicator.textContent = `SLIDE ${currentSlide + 1} / ${slides.length}`;
  prevBtn.disabled = currentSlide === 0;
  nextBtn.disabled = currentSlide === slides.length - 1;
  if (location.hash !== `#${currentSlide + 1}`) {
    history.replaceState(null, '', `#${currentSlide + 1}`);
  }
}
function nextSlide() { if (currentSlide < slides.length - 1) { currentSlide++; updateSlides(); } }
function prevSlide() { if (currentSlide > 0) { currentSlide--; updateSlides(); } }
function toggleCard(card) {
  card.classList.toggle('expanded');
  const hint = card.querySelector('.expand-hint');
  if (hint) hint.textContent = card.classList.contains('expanded') ? '[-]' : '[+]';
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); nextSlide(); }
  if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prevSlide(); }
  if (e.key === 'Home') { currentSlide = 0; updateSlides(); }
  if (e.key === 'End') { currentSlide = slides.length - 1; updateSlides(); }
});
const inicial = parseInt(location.hash.replace('#', ''), 10);
if (!Number.isNaN(inicial) && inicial >= 1 && inicial <= slides.length) currentSlide = inicial - 1;
updateSlides();
"""


def e(texto: object) -> str:
    """Escapa HTML y convierte `código` en <code>."""
    crudo = html.escape(str(texto))
    crudo = re.sub(r"`([^`]+)`", r"<code>\1</code>", crudo)
    crudo = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", crudo)
    return crudo.replace("\n", "<br>")


def codigo(texto: str) -> str:
    return html.escape(str(texto))


def cargar_sesiones() -> dict[int, dict]:
    sesiones: dict[int, dict] = {}
    for numero, teoria in TEORIA.items():
        if numero not in ENRIQUECIMIENTO:
            raise SystemExit(f"Falta el contenido enriquecido de la sesión {numero:02d}")
        datos = dict(teoria)
        datos.update(ENRIQUECIMIENTO[numero])
        datos["numero"] = numero
        faltantes = CAMPOS_OBLIGATORIOS - set(datos)
        if faltantes:
            raise SystemExit(f"Sesión {numero:02d}: faltan campos {sorted(faltantes)}")
        sesiones[numero] = datos
    if sorted(sesiones) != list(range(1, 41)):
        raise SystemExit("El curso debe tener exactamente las sesiones 01 a 40")
    return sesiones


def enlace_colab(numero: int) -> str:
    n = f"{numero:02d}"
    return f"https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/sesion{n}/sesion{n}_laboratorio.ipynb"


def enlace_slides(numero: int) -> str:
    return f"{SITIO}/presentaciones/sesion{numero:02d}.html"


def tarjetas_teoria(tarjetas: list) -> str:
    salida = []
    for titulo, descripcion, detalle in tarjetas:
        salida.append(
            f"""
      <div class="card">
        <div class="card-head"><h3>{e(titulo)}</h3></div>
        <p>{e(descripcion)}</p>
        <p class="theory-detail">{e(detalle)}</p>
      </div>"""
        )
    return "".join(salida)


def tarjetas_arquitectura(tarjetas: list) -> str:
    salida = []
    for titulo, descripcion, detalle in tarjetas:
        salida.append(
            f"""
      <div class="card">
        <div class="card-head"><h3>{e(titulo)}</h3></div>
        <p>{e(descripcion)}</p>
        <div class="small" style="margin-top:7px; border-top:1px dashed var(--border); padding-top:7px;">{e(detalle)}</div>
      </div>"""
        )
    return "".join(salida)


def tarjetas_conceptos(conceptos: list[dict]) -> str:
    salida = []
    for indice, concepto in enumerate(conceptos, start=1):
        salida.append(
            f"""
      <div class="card">
        <div class="term"><span class="num">{indice:02d}</span>{e(concepto["termino"])}</div>
        <p>{e(concepto["definicion"])}</p>
        <div class="analogy">{e(concepto["analogia"])}</div>
      </div>"""
        )
    return "".join(salida)


def tabla_casos(casos: list[dict], limite: int | None = None) -> str:
    filas = []
    for caso in casos[:limite] if limite else casos:
        metodo = caso.get("metodo", "GET").upper()
        ruta = caso.get("ruta", "—")
        estado = caso.get("estado", "—")
        descripcion = caso.get("descripcion", "")
        filas.append(
            f"<tr><td><span class='badge {metodo.lower()}'>{metodo}</span></td>"
            f"<td><code>{e(ruta)}</code></td><td>{e(estado)}</td><td>{e(descripcion)}</td></tr>"
        )
    return (
        "<table class='cases'><thead><tr><th>Método</th><th>Ruta</th><th>HTTP</th>"
        "<th>Qué demuestra</th></tr></thead><tbody>"
        + "".join(filas)
        + "</tbody></table>"
    )


def casos_http(datos: dict) -> list[dict]:
    for bloque in datos["verificacion"]:
        if bloque.get("tipo") == "http":
            return bloque.get("casos", [])
    return []


def criterios_aceptacion(datos: dict) -> list[tuple[str, object]]:
    """Devuelve (descripción, estado HTTP o None) para casos y comprobaciones."""
    criterios: list[tuple[str, object]] = []
    for bloque in datos["verificacion"]:
        if bloque.get("tipo") == "http":
            for caso in bloque.get("casos", []):
                criterios.append((caso.get("descripcion", "Caso HTTP"), caso.get("estado")))
        else:
            for check in bloque.get("checks", []):
                criterios.append((check.get("descripcion") or check.get("ruta", "Comprobación"), None))
    return criterios


def cabecera_html(numero: int, tema: str, unidad: str) -> str:
    n = f"{numero:02d}"
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sesión {n}: {e(tema)} | Desarrollo de Aplicaciones Web</title>
  <style>{CSS}</style>
</head>
<body>
  <header>
    <div class="brand">TecNM Cancún <span>·</span> DAB-2201</div>
    <div class="tag">SESIÓN {n} / 40 &bull; {e(tema)}</div>
  </header>
  <main>
"""


def pie_html() -> str:
    return f"""  </main>
  <footer>
    <div class="progress" id="slideIndicator">SLIDE 1 / 1</div>
    <div class="controls">
      <button id="prevBtn" onclick="prevSlide()" disabled>&larr; Anterior</button>
      <button id="nextBtn" onclick="nextSlide()">Siguiente &rarr;</button>
    </div>
  </footer>
  <script>{JS}</script>
</body>
</html>
"""


def diapositiva(contenido: str, activa: bool = False) -> str:
    clase = "slide active" if activa else "slide"
    return f'    <section class="{clase}"><div class="slide-inner">{contenido}</div></section>\n'


def botones_sesion(numero: int) -> str:
    return f"""<div class="buttons">
      <a class="btn primary" href="{enlace_colab(numero)}" target="_blank" rel="noopener">Abrir el cuaderno en Colab &rarr;</a>
      <a class="btn" href="{enlace_slides(numero)}" target="_blank" rel="noopener">Ver esta presentación en línea</a>
      <a class="btn" href="{REPO}" target="_blank" rel="noopener">Repositorio del curso</a>
    </div>"""


def presentacion_encuadre(datos: dict) -> str:
    n = datos["numero"]
    tema = datos["tema"]
    conceptos = tarjetas_conceptos(datos["conceptos"])
    objetivos = "".join(
        f'<div class="card objective"><div class="term"><span class="num">{i:02d}</span>Objetivo</div><p>{e(o)}</p></div>'
        for i, o in enumerate(datos["objetivos"], start=1)
    )
    casos = casos_http(datos)
    criterios = "".join(
        f"<li>{e(descripcion)}" + (f" <code>HTTP {estado}</code>" if estado is not None else "") + "</li>"
        for descripcion, estado in criterios_aceptacion(datos)
    )

    html_partes = [cabecera_html(n, tema, datos["unidad"])]
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker">Sesión 01 &bull; Bienvenida y encuadre del curso</div>
      <h1>{e(tema)}</h1>
      <p class="lead">No vas a memorizar plantillas: vas a <strong>diseñar, construir y auditar</strong> servicios web reales. Hoy empieza tu portafolio profesional en GitHub.</p>
      <p class="small" style="margin-bottom:8px;"><strong>Al finalizar la clase podrás:</strong></p>
      <div class="grid-3">{objetivos}</div>
      <div class="callout blue"><strong>La pregunta que guía el curso:</strong> ¿cómo viaja una petición desde el navegador hasta una base de datos y vuelve convertida en una respuesta segura?</div>
      <div class="small" style="margin-top:10px;">Sesión 01 de 40 &bull; Docente: MCC. Iván Márquez Larios (<code>ijmarquezl</code>)</div>
""",
            activa=True,
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker">Cómo funciona cada clase</div>
      <h2>60 minutos, tres momentos, un resultado</h2>
      <p class="lead">La clase no es una demostración del profesor: es un ciclo de práctica con evidencia.</p>
      <div class="timeline">
        <div class="step"><div class="time">00–20 min</div><strong>Conceptos y teoría</strong><p>Entiendes el problema y el modelo mental antes de tocar código.</p></div>
        <div class="step"><div class="time">20–35 min</div><strong>El Artesano</strong><p>Implementas el resultado sin asistencia de IA. Forjas intuición técnica.</p></div>
        <div class="step"><div class="time">35–50 min</div><strong>El Científico</strong><p>Formulas el contrato C-R-E-O y contrastas tu solución con la IA.</p></div>
        <div class="step"><div class="time">50–60 min</div><strong>El Auditor</strong><p>Ejecutas la verificación, documentas y haces commit en GitHub.</p></div>
      </div>
      <div class="callout green"><strong>Resultado de cada sesión:</strong> un cuaderno ejecutado, una bitácora en <code>auditorias/</code> y un commit en tu fork.</div>
""",
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker">Conceptos desde cero</div>
      <h2>Las cuatro palabras que necesitas hoy</h2>
      <p class="lead">Si entiendes estas cuatro ideas, el resto de la sesión se sostiene solo.</p>
      <div class="grid-2">{conceptos}</div>
""",
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker orange">Herramientas y evaluación</div>
      <h2>Con qué trabajamos y cómo se evalúa</h2>
      <div class="grid-2">
        <div class="card">
          <h3>Herramientas del curso</h3>
          <ul class="clean">
            <li><strong>Google Colab:</strong> servidores y pruebas en el navegador.</li>
            <li><strong>GitHub Web:</strong> portafolio, bitácoras y control de versiones.</li>
            <li><strong>MS Teams:</strong> clase sincrónica y grabaciones.</li>
            <li><strong>Moodle TecNM:</strong> registro de calificaciones y entregas.</li>
          </ul>
        </div>
        <div class="card">
          <h3>Ponderación oficial</h3>
          <ul class="clean">
            <li><strong>40%</strong> Laboratorios diarios: cuadernos y bitácoras.</li>
            <li><strong>30%</strong> Proyecto integrador: 4 hitos full-stack.</li>
            <li><strong>20%</strong> Evaluaciones prácticas por unidad.</li>
            <li><strong>10%</strong> Participación activa en MS Teams.</li>
          </ul>
        </div>
      </div>
      <div class="interactive-box"><strong>Regla de oro:</strong> tu repositorio de GitHub es tu portafolio y tu evidencia. Si no está en GitHub, no existe.</div>
""",
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker red">Reglas del juego</div>
      <h2>Rigor, IA auditada y trazabilidad</h2>
      <div class="grid-3">
        <div class="card"><h3>IA como copiloto</h3><p>Puedes usar IA, pero no puedes hacer copy-paste ciego. Todo código generado debe probarse y justificarse.</p></div>
        <div class="card"><h3>Trazabilidad</h3><p>Cada sesión termina con un commit. La bitácora documenta tu proceso, no solo el resultado.</p></div>
        <div class="card"><h3>Constancia</h3><p>40 sesiones, una evidencia diaria. El portafolio se construye sesión por sesión.</p></div>
      </div>
      <div class="callout orange"><strong>Estándar de calidad:</strong> no basta con que funcione; debes demostrar por qué es seguro y mantenible.</div>
""",
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker green">El reto de hoy &bull; resultado final</div>
      <h2>{e(datos["resultado"]["titulo"])}</h2>
      <div class="layout-result">
        <div class="terminal"><div class="terminal-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="terminal-title">resultado esperado</span></div>
          <pre class="code">{codigo(datos["resultado"]["codigo"])}</pre>
        </div>
        <div class="criteria-card">
          <h3>El verificador comprobará</h3>
          <ul>{criterios}</ul>
          <div class="callout blue" style="margin-top:10px;"><strong>Sin pasos intermedios:</strong> el cuaderno te muestra el resultado y tú decides cómo llegar.</div>
        </div>
      </div>
      {botones_sesion(n)}
""",
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker">Checklist de la sesión</div>
      <h2>Tu evidencia de hoy</h2>
      <div class="grid-2">
        <div class="card">
          <h3>Antes de cerrar</h3>
          <div class="checklist">
            <div class="check"><span class="box"></span><div><strong>Fork creado</strong> y README con tu nombre, matrícula y track.</div></div>
            <div class="check"><span class="box"></span><div><strong>Cuaderno ejecutado</strong> de la primera a la última celda.</div></div>
            <div class="check"><span class="box"></span><div><strong>Verificación en verde</strong>: {len(casos)} de {len(casos)} casos.</div></div>
            <div class="check"><span class="box"></span><div><strong>Bitácora</strong> en <code>auditorias/auditoria_sesion01.md</code>.</div></div>
            <div class="check"><span class="box"></span><div><strong>Commit</strong> con tus evidencias en tu fork.</div></div>
          </div>
        </div>
        <div class="card">
          <h3>Entregable</h3>
          <p>{e(datos["entrega"])}</p>
          <div class="callout green" style="margin-top:10px;">El resultado de hoy es tu primer ladrillo del proyecto integrador: una API que responde JSON y no se cae ante un error.</div>
        </div>
      </div>
      {botones_sesion(n)}
""",
        )
    )
    html_partes.append(pie_html())
    return "".join(html_partes)


def presentacion(numero: int, datos: dict) -> str:
    if numero == 1:
        return presentacion_encuadre(datos)

    n = f"{numero:02d}"
    tema = datos["tema"]
    unidad = datos["unidad"]
    tp = datos["teoria_principal"]
    am = datos["arquitectura_memoria"]
    cb = datos["casos_borde"]

    objetivos = "".join(
        f'<div class="card objective"><div class="term"><span class="num">{i:02d}</span>Objetivo</div><p>{e(o)}</p></div>'
        for i, o in enumerate(datos["objetivos"], start=1)
    )
    prerrequisitos = "".join(f"<li>{e(p)}</li>" for p in datos["prerrequisitos"])
    conceptos = tarjetas_conceptos(datos["conceptos"])
    teoria = tarjetas_teoria(tp["tarjetas"])
    arquitectura = tarjetas_arquitectura(am["tarjetas"])
    errores = "".join(f"<li>{e(item)}</li>" for item in cb["items"])
    casos = casos_http(datos)
    criterios = "".join(
        f"<li>{e(descripcion)}" + (f" <code>HTTP {estado}</code>" if estado is not None else "") + "</li>"
        for descripcion, estado in criterios_aceptacion(datos)[:6]
    )
    comprobaciones = [
        check
        for bloque in datos["verificacion"]
        if bloque.get("tipo") != "http"
        for check in bloque.get("checks", [])
    ]
    partes_conteo = []
    if casos:
        partes_conteo.append(f"{len(casos)} caso" if len(casos) == 1 else f"{len(casos)} casos")
    if comprobaciones:
        partes_conteo.append(
            f"{len(comprobaciones)} comprobación" if len(comprobaciones) == 1 else f"{len(comprobaciones)} comprobaciones"
        )
    conteo = " + ".join(partes_conteo)
    requisitos = "".join(f"<li>{e(r)}</li>" for r in datos["reto"]["requisitos"])

    html_partes = [cabecera_html(numero, tema, unidad)]
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker">Sesión {n} / 40 &bull; {e(unidad)}</div>
      <h1>{e(tema)}</h1>
      <p class="lead"><strong>La pregunta de hoy:</strong> {e(datos["pregunta"])}</p>
      <p class="small" style="margin-bottom:8px;"><strong>Al finalizar la clase podrás:</strong></p>
      <div class="grid-3">{objetivos}</div>
      <div class="callout blue" style="margin-top:12px;">
        <strong>El resultado de la clase:</strong> {e(datos["resultado"]["titulo"])}. Lo verás completo en la última diapositiva y lo comprobarás en el cuaderno.
      </div>
      <div class="small" style="margin-top:9px;">Docente: MCC. Iván Márquez Larios (<code>ijmarquezl</code>) &bull; TecNM Cancún</div>
""",
            activa=True,
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker">Mapa de la sesión</div>
      <h2>Qué vamos a hacer y en qué orden</h2>
      <div class="timeline">
        <div class="step"><div class="time">00–15 min</div><strong>Conceptos desde cero</strong><p>Las palabras que necesitas para entender el problema.</p></div>
        <div class="step"><div class="time">15–30 min</div><strong>Teoría y arquitectura</strong><p>Cómo funciona por dentro y por qué está diseñado así.</p></div>
        <div class="step"><div class="time">30–50 min</div><strong>El reto</strong><p>Implementas el resultado final sin pasos intermedios.</p></div>
        <div class="step"><div class="time">50–60 min</div><strong>Verificación</strong><p>El verificador compara tu resultado con el esperado.</p></div>
      </div>
      <div class="grid-2" style="margin-top:6px;">
        <div class="card">
          <h3>Lo que ya deberías saber</h3>
          <ul class="clean">{prerrequisitos}</ul>
        </div>
        <div class="card">
          <h3>La pregunta que responde la sesión</h3>
          <p>{e(datos["pregunta"])}</p>
          <div class="small" style="margin-top:8px;">Si al final puedes responderla con un ejemplo propio, la sesión cumplió su objetivo.</div>
        </div>
      </div>
""",
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker green">Conceptos desde cero</div>
      <h2>Cuatro ideas que sostienen toda la sesión</h2>
      <p class="lead">No son definiciones para memorizar: son modelos mentales para decidir mejor frente al código.</p>
      <div class="grid-2">{conceptos}</div>
""",
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker">Fundamentos</div>
      <h2>{e(tp["titulo"])}</h2>
      <p class="lead">{e(tp["lead"])}</p>
      <div class="grid-3">{teoria}</div>
""",
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker">Cómo funciona por dentro</div>
      <h2>{e(am["titulo"])}</h2>
      <p class="lead">{e(am["descripcion"])}</p>
      <div class="grid-2">{arquitectura}</div>
""",
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker red">Errores comunes</div>
      <h2>{e(cb["titulo"])}</h2>
      <p class="lead">Estos son los puntos de falla que la verificación de hoy está diseñada para detectar.</p>
      <div class="grid-2">
        <div class="card" style="border-left:4px solid var(--red);">
          <h3>Antipatrones que debes evitar</h3>
          <ul class="clean">{errores}</ul>
        </div>
        <div class="card">
          <h3>Cómo lo comprueba el cuaderno</h3>
          <ul class="clean">{criterios or "<li>La celda de verificación ejecuta los casos del contrato.</li>"}</ul>
          <div class="small" style="margin-top:8px;">No se evalúa cómo escribes el código: se evalúa el comportamiento que el cliente observa.</div>
        </div>
      </div>
""",
        )
    )
    html_partes.append(
        diapositiva(
            f"""
      <div class="kicker green">El reto de hoy: resultado final</div>
      <h2>{e(datos["resultado"]["titulo"])}</h2>
      <div class="layout-result">
        <div class="terminal"><div class="terminal-bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span><span class="terminal-title">así se verá el resultado</span></div>
          <pre class="code">{codigo(datos["resultado"]["codigo"])}</pre>
        </div>
        <div class="criteria-card">
          <h3>Lo que debe cumplirse</h3>
          <ul>{requisitos}</ul>
          <div class="callout green" style="margin-top:10px;"><strong>{conteo}</strong> en el verificador. Sin pasos intermedios: tú decides la estructura.</div>
          <div class="small" style="margin-top:8px;">{e(datos["resultado"]["nota"])}</div>
        </div>
      </div>
      {botones_sesion(numero)}
""",
        )
    )
    html_partes.append(pie_html())
    return "".join(html_partes)


def _fuente(lineas: list[str] | str) -> list[str]:
    if isinstance(lineas, str):
        lineas = lineas.splitlines(keepends=True)
    return lineas


def celda_markdown(texto: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": _fuente(texto),
    }


def celda_codigo(texto: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _fuente(texto),
    }


def _bloque_verificacion(bloque: dict) -> str:
    tipo = bloque.get("tipo")
    if tipo == "http":
        casos = pprint.pformat(bloque.get("casos", []), width=118, sort_dicts=False)
        limpiar = repr(bloque.get("limpiar", []))
        archivo = bloque.get("archivo", "app.py")
        env = repr(bloque.get("env", {}))
        return (
            "from verificar import probar_http\n\n"
            f"casos = {casos}\n\n"
            f'probar_http(casos, archivo="{archivo}", limpiar={limpiar}, env={env})\n'
        )
    if tipo == "archivos":
        lineas = ["from verificar import revisar_archivo, resumen", "", "resultados = []"]
        for check in bloque.get("checks", []):
            argumentos = [f'"{check["ruta"]}"']
            if check.get("exigir"):
                argumentos.append(f"exigir={json.dumps(check['exigir'], ensure_ascii=False)}")
            if check.get("prohibir"):
                argumentos.append(f"prohibir={json.dumps(check['prohibir'], ensure_ascii=False)}")
            if check.get("regex"):
                argumentos.append(f"regex={json.dumps(check['regex'], ensure_ascii=False)}")
            if check.get("descripcion"):
                argumentos.append(f"descripcion={json.dumps(check['descripcion'], ensure_ascii=False)}")
            lineas.append(f"resultados.append(revisar_archivo({', '.join(argumentos)}))")
        lineas.append("resumen(resultados)")
        return "\n".join(lineas) + "\n"
    if tipo == "json":
        lineas = ["from verificar import revisar_json, resumen", "", "resultados = []"]
        for check in bloque.get("checks", []):
            argumentos = [f'"{check["ruta"]}"']
            if check.get("claves"):
                argumentos.append(f"claves={json.dumps(check['claves'], ensure_ascii=False)}")
            if check.get("contiene"):
                argumentos.append(f"contiene={json.dumps(check['contiene'], ensure_ascii=False)}")
            if check.get("descripcion"):
                argumentos.append(f"descripcion={json.dumps(check['descripcion'], ensure_ascii=False)}")
            lineas.append(f"resultados.append(revisar_json({', '.join(argumentos)}))")
        lineas.append("resumen(resultados)")
        return "\n".join(lineas) + "\n"
    if tipo == "python":
        lineas = ["from verificar import revisar_python, resumen", "", "resultados = []"]
        for check in bloque.get("checks", []):
            codigo_check = check["codigo"]
            descripcion = check.get("descripcion", "Comprobación")
            lineas.append(
                f"resultados.append(revisar_python({json.dumps(codigo_check, ensure_ascii=False)}, "
                f"{json.dumps(descripcion, ensure_ascii=False)}))"
            )
        lineas.append("resumen(resultados)")
        return "\n".join(lineas) + "\n"
    raise SystemExit(f"Tipo de verificación desconocido: {tipo}")


def _esqueleto_http(datos: dict) -> str:
    titulo = datos.get("resultado", {}).get("titulo", "API")
    return (
        "%%writefile app.py\n"
        "from fastapi import FastAPI\n\n"
        f'app = FastAPI(title="{titulo.replace(chr(34), "")}")\n\n'
        "# Implementa aquí el contrato declarado en el reto.\n"
        "# Tú decides los modelos, las rutas, las validaciones y el manejo de errores.\n"
    )


def laboratorio(numero: int, datos: dict) -> str:
    n = f"{numero:02d}"
    tema = datos["tema"]
    resultado = datos["resultado"]
    casos = casos_http(datos)
    criterios = "\n".join(
        f"- [ ] {descripcion}" + (f" → HTTP {estado}" if estado is not None else "")
        for descripcion, estado in criterios_aceptacion(datos)
    )
    if not criterios:
        criterios = "\n".join(f"- [ ] {r}" for r in datos["reto"]["requisitos"])
    objetivos = "\n".join(f"- {o}" for o in datos["objetivos"])
    requisitos = "\n".join(f"- {r}" for r in datos["reto"]["requisitos"])
    hay_http = bool(casos)
    hay_checks = any(bloque.get("tipo") != "http" for bloque in datos["verificacion"])
    if hay_http and hay_checks:
        intro_criterios = "El verificador ejecutará los casos HTTP y comprobará los archivos del contrato. Todo debe quedar en verde:"
    elif hay_http:
        intro_criterios = "El verificador ejecutará estos casos. Cada uno debe quedar en verde:"
    else:
        intro_criterios = "El verificador comprobará estos criterios sobre los archivos que produzcas:"

    archivos = datos["reto"].get("archivos")
    if not archivos:
        archivos = [
            {
                "ruta": datos["reto"].get("archivo", "app.py"),
                "esqueleto": datos["reto"].get("esqueleto") or _esqueleto_http(datos),
                "descripcion": "Archivo principal de la implementación.",
            }
        ]

    celdas: list[dict] = []
    celdas.append(
        celda_markdown(
            f"""# 🧪 Sesión {n} · {tema}

**Desarrollo de Aplicaciones Web (DAB-2201)** · TecNM Cancún  
**Docente:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Repositorio:** {REPO}

> **La pregunta de hoy:** {datos["pregunta"]}

---

## 🖥️ Así se verá el resultado final

```{resultado.get("lenguaje", "text")}
{resultado["codigo"]}
```

_{resultado.get("nota", "")}_

**No hay pasos intermedios.** El cuaderno declara el resultado que debe existir al final; tú decides la estructura, los modelos y el orden de tu implementación. La celda de verificación compara tu resultado con este contrato.

---

## 🎯 Al finalizar podrás

{objetivos}

## ✅ Criterios de aceptación

{intro_criterios}

{criterios}

## 🧩 El reto

{datos["reto"]["enunciado"]}

**Requisitos del contrato**

{requisitos}

> **Pista conceptual:** {datos["reto"]["pista"]}

## 📦 Entregable

{datos["entrega"]}
"""
        )
    )
    celdas.append(
        celda_markdown(
            """## ⚙️ Preparación del entorno

Ejecuta esta celda una sola vez. Instala las herramientas del track **Python / FastAPI** y descarga el motor de verificación del repositorio. No necesitas instalar nada en tu computadora: todo corre en Colab.
"""
        )
    )
    celdas.append(
        celda_codigo(
            """import os, sys
print("⏳ Preparando el entorno de Desarrollo Web...")
!pip install -q fastapi uvicorn httpx pydantic "passlib[bcrypt]" bcrypt python-jose[cryptography] PyJWT "sqlalchemy[asyncio]" greenlet aiosqlite alembic python-multipart
!wget -q -O verificar.py https://raw.githubusercontent.com/ijmarquezl/tecnm-desarrollo-web/main/laboratorios/verificar.py
if not os.path.exists("verificar.py") or os.path.getsize("verificar.py") < 1000:
    raise RuntimeError("No se pudo descargar verificar.py. Revisa tu conexión o abre el cuaderno desde el repositorio del curso.")
print("✅ Entorno listo")
print("Python:", sys.version.split()[0])
print("Motor de verificación:", os.path.getsize("verificar.py"), "bytes")
"""
        )
    )
    celdas.append(
        celda_markdown(
            f"""## 🧩 El reto: escribe el resultado

Crea el o los archivos del contrato. No hay una plantilla de pasos: el esqueleto solo te da el punto de partida. Todo lo que sigue lo decides tú.

**Archivos que debes producir:** {", ".join(f"`{a['ruta']}`" for a in archivos)}
"""
        )
    )
    if datos["reto"].get("preparacion"):
        celdas.append(celda_codigo(datos["reto"]["preparacion"]))
    for archivo in archivos:
        celdas.append(
            celda_markdown(
                f"### 📄 `{archivo['ruta']}`\n\n{archivo.get('descripcion', '')}"
            )
        )
        celdas.append(celda_codigo(archivo["esqueleto"]))
    celdas.append(
        celda_markdown(
            """## 🧪 Tu contrato C-R-E-O

Antes de pedir ayuda a la IA, escribe el contrato que describe el resultado. Esto alimenta tu bitácora y te obliga a pensar como arquitecto:

| Elemento | Tu definición |
| :--- | :--- |
| **Contexto** | Framework, versión y restricciones del entorno. |
| **Rol** | Qué papel técnico debe asumir el modelo. |
| **Especificación** | Rutas, entradas, salidas, validaciones y códigos HTTP. |
| **Output** | Qué formato exacto esperas de vuelta. |

> No pegues código de la IA sin auditarlo. La responsabilidad técnica del resultado es tuya.
"""
        )
    )
    celdas.append(
        celda_markdown(
            """## 🔍 Verificación del resultado

Ejecuta esta celda cuando tu implementación esté lista. La verificación no modifica tu código: solo observa el comportamiento y compara con el contrato. Si algo falla, el mensaje te dice **qué esperaba** y **qué recibió**.
"""
        )
    )
    for bloque in datos["verificacion"]:
        celdas.append(celda_codigo(_bloque_verificacion(bloque)))
    celdas.append(
        celda_markdown(
            f"""## 📝 Cierre y bitácora

1. Copia la plantilla `plantillas/auditoria_sesion{n}.md` a `auditorias/auditoria_sesion{n}.md` en tu fork.
2. Responde con tus palabras:
   - ¿Qué resultado te costó más alcanzar y por qué?
   - ¿Qué decisión de diseño tomaste que no estaba escrita en el contrato?
   - ¿Qué error detectó la verificación que tú no habías previsto?
3. Haz commit de tu cuaderno ejecutado y de tu bitácora.

**La sesión termina cuando el resultado está en verde, no cuando el código "parece funcionar".**
"""
        )
    )

    notebook = {
        "cells": celdas,
        "metadata": {
            "colab": {"name": f"sesion{n}_laboratorio.ipynb", "provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }
    return json.dumps(notebook, ensure_ascii=False, indent=1)


def bitacora(numero: int, datos: dict) -> str:
    n = f"{numero:02d}"
    criterios = "\n".join(
        f"- [ ] {descripcion}" + (f" → HTTP {estado}" if estado is not None else "")
        for descripcion, estado in criterios_aceptacion(datos)
    )
    if not criterios:
        criterios = "\n".join(f"- [ ] {r}" for r in datos["reto"]["requisitos"])
    return f"""# Bitácora de la Sesión {n} — {datos["tema"]}

**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Nombre completo]  
**Matrícula:** [Número de control]  
**Track:** [Python/FastAPI | PHP 8+]  
**Fecha:** [DD/MM/AAAA]

---

## 1. Resultado al que llegué

**Resultado esperado:** {datos["resultado"]["titulo"]}

> Pega aquí la salida de la celda de verificación (los casos en verde) o describe exactamente qué obtuviste.

```text
[Pega aquí la salida de la verificación]
```

## 2. Criterios de aceptación

{criterios}

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
- **Presentación:** {enlace_slides(numero)}

---
**Firma digital:** [Usuario de GitHub]
"""


def leerme(sesiones: dict[int, dict]) -> str:
    filas = []
    for numero in range(1, 41):
        datos = sesiones[numero]
        n = f"{numero:02d}"
        filas.append(
            f"| **{n}** | {datos['tema']} | [Presentación]({enlace_slides(numero)}) | "
            f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({enlace_colab(numero)}) |"
        )
    filas_txt = "\n".join(filas)
    return f"""# Desarrollo de Aplicaciones Web (DAB-2201)

Repositorio oficial y entorno de laboratorio interactivo del curso de **Desarrollo de Aplicaciones Web** del Tecnológico Nacional de México / Instituto Tecnológico de Cancún.

**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Sitio del curso:** [ijmarquezl.github.io/tecnm-desarrollo-web]({SITIO}/)

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

- [Presentación: Git, Codespaces y primer commit]({SITIO}/presentaciones/lab00-git-codespaces.html)
- [Guía del Laboratorio 00]({REPO}/blob/main/laboratorios/lab00-git-codespaces.md)

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
{filas_txt}

---

## 🛠️ Mantenimiento del curso

El contenido se genera desde una sola fuente de verdad:

- `datos_teoria.py`: teoría de las 40 sesiones.
- `datos_sesiones_b1.py` … `datos_sesiones_b4.py`: objetivos, conceptos, resultado final, reto y casos de verificación.
- `generar_curso.py`: regenera las 40 presentaciones, los 40 cuadernos, las 40 bitácoras y este README.
- `laboratorios/verificar.py`: motor compartido que descargan los cuadernos.

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
"""


def portada_sitio(sesiones: dict[int, dict]) -> str:
    bloques = [
        ("Bloque 1", "Arquitectura web, HTTP y REST APIs", range(1, 11)),
        ("Bloque 2", "Lógica de negocio y autenticación segura", range(11, 21)),
        ("Bloque 3", "Persistencia relacional y OWASP", range(21, 31)),
        ("Bloque 4", "Despliegue, SPA y pruebas E2E", range(31, 41)),
    ]
    tarjetas = []
    for bloque, descripcion, numeros in bloques:
        sesiones_html = []
        for numero in numeros:
            datos = sesiones[numero]
            n = f"{numero:02d}"
            sesiones_html.append(
                f'<a class="session" href="presentaciones/sesion{n}.html">'
                f'<span class="num">{n}</span>'
                f'<span class="session-body"><strong>{e(datos["tema"])}</strong>'
                f'<small>{e(datos["pregunta"])}</small></span></a>'
            )
        tarjetas.append(
            f'<section class="block"><div class="block-head"><span class="kicker">{bloque}</span>'
            f'<h2>{e(descripcion)}</h2></div><div class="sessions">{"".join(sesiones_html)}</div></section>'
        )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Desarrollo de Aplicaciones Web (DAB-2201) | TecNM Cancún</title>
  <style>
    :root {{
      --bg: #f3f7fb; --card: #ffffff; --border: #d3dfea; --accent: #0969da;
      --text: #334155; --bright: #0f172a; --muted: #5b6b7c;
      --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: radial-gradient(1000px 500px at 10% -10%, #e3f0fb, transparent 60%), var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.5; }}
    .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 22px; }}
    header {{ border-bottom: 1px solid var(--border); background: rgba(255,255,255,.85); backdrop-filter: blur(10px); }}
    header .wrap {{ display: flex; justify-content: space-between; align-items: center; gap: 14px; padding-top: 14px; padding-bottom: 14px; }}
    .brand {{ font-weight: 800; color: var(--bright); }}
    .brand span {{ color: var(--accent); }}
    .hero {{ padding: 64px 0 34px; }}
    .kicker {{ display: inline-block; background: #ddf4ff; color: var(--accent); border: 1px solid #b6e3ff; border-radius: 999px; padding: 5px 12px; font-family: var(--mono); font-size: .72rem; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }}
    h1 {{ font-size: clamp(2rem, 5vw, 3.4rem); line-height: 1.05; color: var(--bright); margin: 14px 0 12px; letter-spacing: -.03em; }}
    .lead {{ font-size: 1.08rem; color: #475569; max-width: 820px; }}
    .buttons {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 22px; }}
    .btn {{ display: inline-flex; align-items: center; gap: 7px; padding: 10px 15px; border-radius: 8px; border: 1px solid var(--border); background: #fff; color: var(--bright); text-decoration: none; font-weight: 700; font-size: .88rem; }}
    .btn.primary {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
    .block {{ padding: 26px 0 8px; }}
    .block-head h2 {{ font-size: 1.35rem; color: var(--bright); margin-top: 6px; }}
    .sessions {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 10px; margin-top: 14px; }}
    .session {{ display: flex; gap: 11px; align-items: flex-start; background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 12px 13px; text-decoration: none; color: inherit; transition: border-color .2s, transform .2s, box-shadow .2s; }}
    .session:hover {{ border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(9,105,218,.10); }}
    .num {{ flex: 0 0 auto; display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; background: #ddf4ff; color: var(--accent); font-family: var(--mono); font-weight: 800; font-size: .78rem; }}
    .session-body {{ display: flex; flex-direction: column; gap: 3px; }}
    .session-body strong {{ color: var(--bright); font-size: .9rem; line-height: 1.3; }}
    .session-body small {{ color: var(--muted); font-size: .78rem; line-height: 1.35; }}
    .note {{ margin: 24px 0 10px; padding: 14px 16px; background: #fff; border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 8px; font-size: .88rem; }}
    footer {{ margin-top: 42px; border-top: 1px solid var(--border); padding: 24px 0 40px; font-size: .82rem; color: var(--muted); }}
    code {{ font-family: var(--mono); background: #eef4fa; padding: 1px 5px; border-radius: 4px; }}
  </style>
</head>
<body>
  <header><div class="wrap"><div class="brand">TecNM Cancún <span>·</span> DAB-2201</div>
    <div class="kicker">Curso 2026</div></div></header>
  <main class="wrap">
    <section class="hero">
      <span class="kicker">Desarrollo de Aplicaciones Web</span>
      <h1>Construye, verifica y despliega APIs reales.</h1>
      <p class="lead">40 sesiones con presentaciones claras, conceptos desde cero y laboratorios de <strong>resultado primero</strong>: ves exactamente qué debe producir tu API y un verificador te dice qué falta. Sin pasos intermedios.</p>
      <div class="buttons">
        <a class="btn primary" href="presentaciones/lab00-git-codespaces.html">Empezar con Git y Codespaces &rarr;</a>
        <a class="btn" href="presentaciones/sesion01.html">Ver la Sesión 01</a>
        <a class="btn" href="https://github.com/ijmarquezl/tecnm-desarrollo-web">Repositorio en GitHub</a>
      </div>
    </section>
    <div class="note"><strong>Antes de la sesión 01:</strong> abre tu fork, ejecuta tu primer script y publica tu primer commit. La guía está en <a href="https://github.com/ijmarquezl/tecnm-desarrollo-web/blob/main/laboratorios/lab00-git-codespaces.md">Laboratorio 00</a>.</div>
    {"".join(tarjetas)}
    <footer>MCC. Iván Márquez Larios (<code>ijmarquezl</code>) · Tecnológico Nacional de México — Campus Cancún<br>
      El contenido se genera desde <code>datos_sesiones_b*.py</code> con <code>python3 generar_curso.py</code>.</footer>
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera el curso completo de Desarrollo Web")
    parser.add_argument("--solo", nargs="*", type=int, default=None, help="Sesiones específicas a generar")
    parser.add_argument("--sin-readme", action="store_true", help="No reescribir el README")
    args = parser.parse_args()

    sesiones = cargar_sesiones()
    numeros = sorted(sesiones) if not args.solo else sorted(set(args.solo))
    for numero in numeros:
        if numero not in sesiones:
            raise SystemExit(f"Sesión inexistente: {numero}")

    (RAIZ / "presentaciones").mkdir(exist_ok=True)
    (RAIZ / "plantillas").mkdir(exist_ok=True)
    (RAIZ / "proyecto_integrador" / "docs").mkdir(parents=True, exist_ok=True)
    (RAIZ / "proyecto_integrador" / "src").mkdir(parents=True, exist_ok=True)
    (RAIZ / "proyecto_integrador" / "tests").mkdir(parents=True, exist_ok=True)

    for numero in numeros:
        datos = sesiones[numero]
        n = f"{numero:02d}"
        carpeta_lab = RAIZ / "laboratorios" / f"sesion{n}"
        carpeta_lab.mkdir(parents=True, exist_ok=True)

        (RAIZ / "presentaciones" / f"sesion{n}.html").write_text(
            presentacion(numero, datos), encoding="utf-8"
        )
        (carpeta_lab / f"sesion{n}_laboratorio.ipynb").write_text(
            laboratorio(numero, datos), encoding="utf-8"
        )
        (RAIZ / "plantillas" / f"auditoria_sesion{n}.md").write_text(
            bitacora(numero, datos), encoding="utf-8"
        )
        print(f"✅ Sesión {n}: presentación, cuaderno y bitácora")

    (RAIZ / "index.html").write_text(portada_sitio(sesiones), encoding="utf-8")
    print("✅ Portada del sitio (index.html)")

    if not args.sin_readme:
        (RAIZ / "README.md").write_text(leerme(sesiones), encoding="utf-8")
        print("✅ README actualizado")

    print(f"\n🎉 Generación completa: {len(numeros)} sesión(es).")


if __name__ == "__main__":
    main()
