"""Genera fichas de revisión humana para controles de una ejecución, sin modificar la respuesta.

Uso:
  python -m motor.hoja_revision resultados/<carpeta> --propuestas <archivo.json> [--salida <archivo.md>]

<archivo.json>:
  {"A.1.3.9": {"problema": "...", "propuesta_ia": "No evidenciado", "tipo_error": "Extensión por enumeración"}, ...}
  ("tipo_error" es opcional.)

Cada ficha tiene los campos acordados con el equipo:
  Criterio ISO · Categoría y aplicabilidad · Elementos · Documento · Evidencia del documento ·
  Resultado del modelo · Corrección propuesta (IA) · Tipo de error · Revisión del equipo
Los campos del modelo se copian textualmente de respuesta_original.md. La revisión del equipo
queda vacía: solo la completan las personas que revisan.
"""

import argparse
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from motor import insumos, skill, verificacion  # noqa: E402

NOMBRES_CAT = {"E": "E — información esencial (metodología del equipo)",
               "C": "C — información condicional según el tratamiento",
               "INT-i": "INT-i — evidencia interna, con posibles indicios",
               "INT": "INT — evidencia interna", "A2": "C — según el rol (Tabla A.2)"}


def _pagina_control(id_control: str) -> str:
    """Página (norma / PDF) del control en el Anexo A, según el catálogo."""
    p = [int(x) for x in id_control.split(".")[1:]]
    if id_control.startswith("A.1."):
        if p[1] == 2:
            return "15 / 21"
        if p[1] == 3 or (p[1] == 4 and p[2] <= 7):
            return "16 / 22"
        return "17 / 23"
    if id_control.startswith("A.3."):
        return "18 / 24" if p[1] <= 4 else ("19 / 25" if p[1] <= 20 else "20 / 26")
    return "17–18 / 23–24"


def _criterio(id_control: str) -> tuple[str, str]:
    texto = skill.ARCHIVO_CATALOGO.read_text(encoding="utf-8")
    for linea in texto[texto.index("## 4."):texto.index("## 5.")].splitlines():
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if c and c[0] == id_control:
            return c[1], (c[2] if id_control.startswith("A.1.") else "")
    return "?", ""


def _elementos_texto(ruta: Path, id_control: str) -> str:
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if c and c[0] == id_control:
            return c[-1]
    return "— (sin elementos definidos: control INT o agrupado)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--propuestas", required=True)
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()

    carpeta = Path(a.carpeta)
    propuestas = json.loads(Path(a.propuestas).read_text(encoding="utf-8"))
    meta = json.loads((carpeta / "metadatos.json").read_text(encoding="utf-8"))
    version = meta.get("skill_version", "0.1")
    filas = {f["ids"][0]: f for f in
             verificacion.filas_de_la_matriz((carpeta / "respuesta_original.md").read_text(encoding="utf-8"))
             if len(f["ids"]) == 1}
    categorias = verificacion.controles_del_catalogo(skill.ARCHIVO_CATALOGO)
    guia = verificacion.guia_por_control(skill.ARCHIVO_CATALOGO)
    ruta_el = insumos.ruta_elementos(version)

    l = [f"# Fichas de revisión humana — {meta['documento']}", "",
         f"Ejecución: `{carpeta.name}` · Modelo: {meta['modelo']} · Skill v{version} · "
         f"Catálogo de la ejecución: v{meta.get('catalogo_version', '?')}", "",
         "- **Resultado del modelo:** copiado textualmente de `respuesta_original.md`, que no se modifica.",
         "- **Corrección propuesta (IA):** revisión asistida por IA, **no validada**.",
         "- **Revisión del equipo:** la completa solo el equipo: `confirma la propuesta de la IA` · "
         "`confirma el resultado del modelo` · `otro estado`, con el motivo, el revisor y la fecha.", "",
         "## Tabla de decisiones", "",
         "| # | ID | Estado del modelo | Propuesta IA (no validada) | Revisión del equipo | Estado final (equipo) | Revisor | Fecha |",
         "|---|---|---|---|---|---|---|---|"]
    for n, (i, p) in enumerate(propuestas.items(), 1):
        f = filas.get(i)
        l.append(f"| {n} | {i} | {f['estado_texto'] if f else '(sin fila)'} | {p['propuesta_ia']} |  |  |  |  |")

    l += ["", "## Fichas", ""]
    for n, (i, p) in enumerate(propuestas.items(), 1):
        f = filas.get(i)
        titulo, parafrasis = _criterio(i)
        cat = categorias.get(i, "?")
        aplic = (f.get("aplicabilidad_texto") or "(no consta en esta versión)") if f else "—"
        l += [f"### {n}. {i} — {titulo}", "",
              "| Campo | Contenido |", "|---|---|",
              f"| Criterio ISO | {i} *{titulo}*" + (f": {parafrasis}" if parafrasis else "")
              + " (ISO/IEC 27701:2025, pág. norma {} / PDF {})".format(*_pagina_control(i).split(" / "))
              + (f". Guía del Anexo B: {guia[i]}" if i in guia else "") + " |",
              f"| Categoría y aplicabilidad | {NOMBRES_CAT.get(cat, cat)} · Aplicabilidad según el modelo: {aplic} |",
              f"| Elementos | {_elementos_texto(ruta_el, i)} (`{ruta_el.relative_to(RAIZ).as_posix()}`) |",
              f"| Documento | {meta['documento']} — {f['ubicacion'] if f else '—'} |",
              f"| Evidencia del documento | {f['evidencia'] if f else '—'} |",
              f"| Resultado del modelo | Skill v{version}: **{f['estado_texto'] if f else '—'}**. "
              f"Justificación: {(f.get('justificacion') or '—') if f else '—'} |",
              f"| Corrección propuesta (IA) | **{p['propuesta_ia']}**. {p['problema']} |",
              f"| Tipo de error | {p.get('tipo_error', '—')} |",
              "| **Revisión del equipo** | Decisión: ______ · Estado final: ______ · Motivo: ______ · Revisor: ______ · Fecha: ______ |",
              ""]

    salida = Path(a.salida) if a.salida else carpeta / "fichas_revision.md"
    salida.write_text("\n".join(l), encoding="utf-8")
    print(f"Fichas creadas: {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
