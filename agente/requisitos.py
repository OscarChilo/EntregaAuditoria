"""Requisitos auditables: cláusulas 4–10 y controles del Anexo A de ISO/IEC 27701:2025.

Se leen de los catálogos del proyecto (no del modelo):
  skill/comun/clausulas_iso27701.md   cláusulas 4–10 con sus elementos
  skill/sk01/catalogo_iso27701.md     paráfrasis y categoría de los controles del Anexo A
  skill/sk01/elementos.md             elementos de los controles del Anexo A
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARCH_CLAUSULAS = RAIZ / "skill" / "comun" / "clausulas_iso27701.md"
ARCH_CATALOGO = RAIZ / "skill" / "sk01" / "catalogo_iso27701.md"
ARCH_ELEMENTOS = RAIZ / "skill" / "sk01" / "elementos.md"
ARCH_A2A3 = RAIZ / "skill" / "comun" / "anexo_a_tablas_a2_a3.md"

RE_CLAUSULA = re.compile(r"(?:[4-9]|10)(?:\.\d+)+")
RE_CONTROL = re.compile(r"A\.[12]\.\d+\.\d+|A\.3\.\d+")
GRUPOS = [  # (nombre del lote, prueba de pertenencia)
    ("Cláusulas 4 y 5", lambda i: i.split(".")[0] in ("4", "5")),
    ("Cláusula 6", lambda i: i.split(".")[0] == "6"),
    ("Cláusulas 7 y 8", lambda i: i.split(".")[0] in ("7", "8")),
    ("Cláusulas 9 y 10", lambda i: i.split(".")[0] in ("9", "10")),
    ("Anexo A — Tabla A.1 (2 y 3)", lambda i: i.startswith(("A.1.2.", "A.1.3."))),
    ("Anexo A — Tabla A.1 (4 y 5)", lambda i: i.startswith(("A.1.4.", "A.1.5."))),
    ("Anexo A — Tabla A.2", lambda i: i.startswith("A.2.")),
    ("Anexo A — Tabla A.3 (3 a 17)", lambda i: i.startswith("A.3.") and int(i.split(".")[2]) <= 17),
    ("Anexo A — Tabla A.3 (18 a 31)", lambda i: i.startswith("A.3.") and int(i.split(".")[2]) >= 18),
]
# Lotes de las ejecuciones anteriores a la v0.2 del agente (para reprocesarlas sin cambiar sus resultados)
GRUPOS_V01 = GRUPOS[:4] + [("Anexo A — Tabla A.1", lambda i: i.startswith("A.1.")),
                           ("Anexo A — Tabla A.3", lambda i: i.startswith("A.3."))]
NOMBRE_CLAUSULA = {"4": "Contexto de la organización", "5": "Liderazgo", "6": "Planificación", "7": "Apoyo",
                   "8": "Operación", "9": "Evaluación del desempeño", "10": "Mejora"}


def _celdas(linea: str) -> list[str]:
    return [x.strip() for x in linea.strip().strip("|").split("|")] if linea.lstrip().startswith("|") else []


def elementos_de_texto(texto: str) -> list[dict]:
    """'E1 algo [aviso]† · E2 otra cosa · [recomendación] …' -> [{codigo, texto, recomendacion}]."""
    out, n_rec = [], 0
    for seg in (s.strip() for s in texto.split("·")):
        seg = re.sub(r"\s*\[(aviso|interno)\]", "", seg).replace("†", "").strip()
        m = re.match(r"(E\d+)\s+(.*)", seg)
        if m:
            out.append({"codigo": m.group(1), "texto": m.group(2), "recomendacion": False})
        elif seg.startswith("[recomendación]"):
            n_rec += 1
            out.append({"codigo": f"R{n_rec}", "texto": seg.removeprefix("[recomendación]").strip(),
                        "recomendacion": True})
    return out


def clausulas() -> list[dict]:
    out = []
    for linea in ARCH_CLAUSULAS.read_text(encoding="utf-8").splitlines():
        c = _celdas(linea)
        if len(c) >= 8 and RE_CLAUSULA.fullmatch(c[0]):
            cl = c[0].split(".")[0]
            out.append({"id": c[0], "titulo": c[1], "requisito": c[2], "elementos": elementos_de_texto(c[3]),
                        "id_r": c[4], "proceso": f"{cl}. {NOMBRE_CLAUSULA[cl]}"})
    return out


def controles_anexo_a(con_a2a3: bool = True) -> dict[str, dict]:
    """ID -> {id, titulo, requisito, categoria, elementos, proceso}.
    Tabla A.1: paráfrasis del catálogo de SK-01 y elementos de elementos.md.
    Tablas A.2 y A.3: paráfrasis y elementos de skill/comun/anexo_a_tablas_a2_a3.md.
    con_a2a3=False reproduce la versión anterior (A.3 solo con título; sin A.2), para reprocesar ejecuciones viejas."""
    texto = ARCH_CATALOGO.read_text(encoding="utf-8")
    seccion = texto[texto.index("## 4."):texto.index("## 5.")]
    elementos = {}
    for linea in ARCH_ELEMENTOS.read_text(encoding="utf-8").splitlines():
        c = _celdas(linea)
        if c and RE_CONTROL.fullmatch(c[0]):
            elementos[c[0]] = elementos_de_texto(c[-1])
    out = {}
    for linea in seccion.splitlines():
        c = _celdas(linea)
        if not (c and RE_CONTROL.fullmatch(c[0])) or c[0] in out or c[0].startswith("A.2."):
            continue
        if c[0].startswith("A.1.") and len(c) >= 4:
            requisito, cat = c[2], c[3]
        else:  # A.3 en el catálogo de SK-01: solo título en inglés
            requisito, cat = f"Control «{c[1]}» (Tabla A.3)", c[2] if len(c) > 2 else ""
        out[c[0]] = {"id": c[0], "titulo": c[1], "requisito": requisito, "categoria": cat, "id_r": "—",
                     "elementos": elementos.get(c[0]) or [{"codigo": "E1", "texto": requisito,
                                                           "recomendacion": False}],
                     "proceso": "Anexo A — " + ("Tabla A.1" if c[0].startswith("A.1.") else "Tabla A.3")}
    if con_a2a3:
        for linea in ARCH_A2A3.read_text(encoding="utf-8").splitlines():
            c = _celdas(linea)
            if len(c) >= 5 and RE_CONTROL.fullmatch(c[0]):
                cat = out.get(c[0], {}).get("categoria", "C (según el rol)" if c[0].startswith("A.2.") else "")
                out[c[0]] = {"id": c[0], "titulo": c[1], "requisito": c[2], "categoria": cat, "id_r": "—",
                             "elementos": elementos_de_texto(c[3]),
                             "proceso": "Anexo A — Tabla " + c[0][:3]}
    return out


def alcance(textos_documentos: list[str], anexo_a: str = "completo", con_a2a3: bool = True) -> list[dict]:
    """Cláusulas 4–10 más, del Anexo A:
       "completo"            los 78 controles (A.1, A.2 y A.3);
       "esenciales+citados"  los esenciales (E) de A.1 y los que los documentos citan expresamente;
       "ninguno"             ningún control."""
    reqs = clausulas()
    if anexo_a == "ninguno":
        return reqs
    controles = controles_anexo_a(con_a2a3)
    if anexo_a == "completo":
        elegidos = set(controles)
    else:
        citados = {m for t in textos_documentos for m in RE_CONTROL.findall(t)}
        elegidos = {i for i, c in controles.items() if c["categoria"] == "E"} | (citados & set(controles))
    return reqs + [controles[i] for i in sorted(elegidos, key=lambda i: [int(x) for x in i[2:].split(".")])]


def lotes(reqs: list[dict], grupos=None) -> list[tuple[str, list[dict]]]:
    return [(nombre, grupo) for nombre, prueba in (grupos or GRUPOS)
            if (grupo := [r for r in reqs if prueba(r["id"])])]
