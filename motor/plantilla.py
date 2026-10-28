"""Plantilla de la matriz y lista «Información al titular», generadas desde el catálogo.

Fijan las filas, los IDs, las referencias, la categoría y los puntos esperados para que el modelo
no omita, repita ni agrupe controles de forma distinta a la prevista. El verificador compara la
respuesta con estas mismas plantillas.

Formatos:
  - Skill v0.5 o posterior: 10 columnas (Referencia ISO con la guía del Anexo B, Categoría,
    Aplicabilidad, …) y la lista O-01 a O-16.
  - Skill v0.3–v0.4: 9 columnas, como se enviaron en esas versiones (para ejecutar
    instrucciones archivadas con el mismo formato).
"""

import re
from pathlib import Path

from motor.verificacion import _v, catalogo_detallado, guia_por_control, lista_titular

# ---------- formato v0.5 ----------
ENCABEZADO = ("| Referencia ISO | Control | Cat. | Aplicabilidad | Evidencia (cita literal) | Ubicación | Estado | "
              "Justificación | Información faltante o necesaria | Recomendación |\n"
              "|---|---|---|---|---|---|---|---|---|---|")
APLICABILIDAD_INICIAL = {"E": "Aplica", "C": "(decidir: Aplica / No aplica / Por determinar)",
                         "INT-i": "—", "INT": "—"}
# Desde la Skill v0.5.1 la indicación recuerda que el silencio es «Por determinar».
APLICABILIDAD_C_V051 = ("(decidir: Aplica [situación declarada, con cita] / No aplica [solo con descarte "
                        "expreso citado] / Por determinar [silencio, indicios o duda])")
ENCABEZADO_LISTA = ("| Orientación | Cat. en la lista | Situación | Cita literal | Ubicación | Qué falta | Sugerencia |\n"
                    "|---|---|---|---|---|---|---|")

# ---------- formato v0.3–v0.4 ----------
ENCABEZADO_V03 = ("| ID ISO | Control | Eval. | Evidencia (cita literal) | Ubicación | Estado | "
                  "Justificación | Posible vacío | Recomendación |\n|---|---|---|---|---|---|---|---|---|")
EVAL_V03 = {"E": "D", "C": "D* (escribir: activado / no activado)", "INT-i": "I", "INT": "N"}


def filas_plantilla(ruta_catalogo: Path, version: str = "0.5") -> list[tuple[list[str], str, str, str, str]]:
    """[(ids, referencia, título, categoría, aplicabilidad inicial)] en el orden de la matriz."""
    cat = catalogo_detallado(ruta_catalogo)
    guia = guia_por_control(ruta_catalogo)
    nuevo = _v(version) >= _v("0.5")
    filas = []
    for x in cat:
        if x["grupo"] is not None:
            continue
        ref = f"{x['id']} · {guia[x['id']]}" if nuevo and x["id"] in guia else x["id"]
        categoria = x["eval"] if nuevo else EVAL_V03[x["eval"]]
        aplic = APLICABILIDAD_INICIAL[x["eval"]]
        if x["eval"] == "C" and _v(version) >= _v("0.5.1"):
            aplic = APLICABILIDAD_C_V051
        filas.append(([x["id"]], ref, x["titulo"], categoria, aplic))
    a3n = [x["id"] for x in cat if x["grupo"] == "A.3-N"]
    a2 = [x["id"] for x in cat if x["grupo"] == "A.2"]
    if nuevo:
        filas.append((a3n, ", ".join(a3n), "Controles INT de la Tabla A.3 (agrupados)", "INT", "—"))
        filas.append((a2, ", ".join(a2), "Controles de la Tabla A.2 — encargados (agrupados)", "C (según el rol)",
                      "(decidir según el rol: Aplica / No aplica / Por determinar)"))
    else:
        filas.append((a3n, ", ".join(a3n), "Controles N de la Tabla A.3 (agrupados)", "N", ""))
        filas.append((a2, ", ".join(a2), "Controles de la Tabla A.2 — encargados (agrupados)", "A.2 (según el rol)", ""))
    return filas


def ids_plantilla(ruta_catalogo: Path) -> list[list[str]]:
    return [f[0] for f in filas_plantilla(ruta_catalogo)]


def bloque_plantilla(ruta_catalogo: Path, version: str = "0.5") -> str:
    if _v(version) < _v("0.5"):
        lineas = [ENCABEZADO_V03]
        for ids, ref, titulo, ev, _ in filas_plantilla(ruta_catalogo, version):
            lineas.append(f"| {ref} | {titulo} | {ev} |  |  |  |  |  |  |")
        instruccion = ("Copia TODAS estas filas en este mismo orden y completa sus celdas vacías. "
                       "No cambies la celda ID ISO, no agregues, quites, unas ni dividas filas, y no uses rangos.")
    else:
        lineas = [ENCABEZADO]
        for ids, ref, titulo, categoria, aplic in filas_plantilla(ruta_catalogo, version):
            lineas.append(f"| {ref} | {titulo} | {categoria} | {aplic} |  |  |  |  |  |  |")
        instruccion = ("Copia TODAS estas filas en este mismo orden y completa sus celdas. No cambies las celdas "
                       "Referencia ISO, Control ni Cat.; no agregues, quites, unas ni dividas filas, y no uses rangos. "
                       "En Aplicabilidad, reemplaza «(decidir: …)» por un único valor según criterios.md §3.1.")
    return (
        "<<<PLANTILLA DE LA MATRIZ>>>\n"
        f"Generada desde el catálogo: {len(lineas) - 1} filas.\n"
        f"{instruccion}\n\n"
        + "\n".join(lineas)
        + "\n<<<FIN DE LA PLANTILLA>>>"
    )


def bloque_lista_titular(ruta_catalogo: Path) -> str:
    """Lista O-01 a O-16 que el modelo debe completar entera (desde la Skill v0.5)."""
    lineas = [ENCABEZADO_LISTA]
    for o in lista_titular(ruta_catalogo):
        que = re.sub(r"\s+", " ", o["que"])
        lineas.append(f"| {o['id']} — {que} ({o['fuente']}) | {o['cat']} |  |  |  |  |  |")
    return (
        "<<<LISTA INFORMACIÓN AL TITULAR>>>\n"
        "Ejemplos de B.1.3.3 y B.1.3.4: no son obligaciones. Copia TODAS las filas, en este orden, y "
        "complétalas aunque la política no mencione el punto (formato_resultado.md §3).\n\n"
        + "\n".join(lineas)
        + "\n<<<FIN DE LA LISTA>>>"
    )
