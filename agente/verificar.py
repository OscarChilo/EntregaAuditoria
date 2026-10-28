"""Lectura y verificación de forma de las respuestas de SK-02, SK-03 y SK-04.

Como en la primera entrega, se comprueba la forma (cobertura, citas literales, coherencia entre
elementos y resultado), no si la conclusión es correcta: eso lo decide el equipo auditor.
"""

import re
import unicodedata
from datetime import date, timedelta

RESULTADOS = ["Conforme", "N", "O", "M", "Sin evidencia"]
CIERRE = {"SK-02": "--- FIN SK-02 ---", "SK-03": "--- FIN SK-03 ---", "SK-04": "--- FIN SK-04 ---"}
DIAS = {"N": 60, "O": 90, "M": 120}  # plazo propuesto (metodología del equipo, plantillas/plan_accion.md)
RE_ESTADO = re.compile(r"\b([ER]\d+)\s+(Respalda|Falta|Contradicho)\b", re.I)
RE_CITA = re.compile(r"[\"“«](.+?)[\"”»]")
RE_REF = re.compile(r"\[([A-Za-z0-9._-]+)(?:\s*§\s*([^\]]*))?\]")
PROHIBIDAS = re.compile(r"certificad|cumple (con )?la norma|es conforme con la norma|plenamente conforme", re.I)


def norm(t: str) -> str:
    t = unicodedata.normalize("NFKC", t)
    t = t.replace("“", '"').replace("”", '"').replace("«", '"').replace("»", '"').replace("’", "'")
    t = re.sub(r"[*_`#>]", "", t)          # marcas de Markdown: se quitan sin dejar espacio
    t = re.sub(r"[|:]", " ", t)            # bordes de tabla y «Campo: valor» equivalen a un espacio
    return re.sub(r"\s+", " ", t).strip().lower()


def celdas(linea: str) -> list[str]:
    return [x.strip() for x in linea.strip().strip("|").split("|")]


def filas(texto: str, primera: re.Pattern) -> list[list[str]]:
    return [celdas(l) for l in texto.splitlines() if l.lstrip().startswith("|") and primera.fullmatch(celdas(l)[0])]


def clasificar_cita(cita: str, codigo: str | None, docs: dict[str, str]) -> str:
    """literal · literal en otro documento · no literal · documento inexistente."""
    # «...», «…» y « · » separan fragmentos (p. ej., celdas de una tabla); cada fragmento debe ser literal
    partes = [norm(p) for p in re.split(r"\.\.\.|…|\[\.\.\.\]|\s·\s", cita) if norm(p)]
    en = lambda t: all(p in t for p in partes)  # noqa: E731
    if codigo and codigo in docs and en(docs[codigo]):
        return "literal"
    if any(en(t) for t in docs.values()):
        return "literal en otro documento"
    if codigo and codigo not in docs:
        return "documento inexistente"
    return "no literal"


def elementos_de_celda(celda: str) -> list[dict]:
    marcas = list(RE_ESTADO.finditer(celda))
    out = []
    for n, m in enumerate(marcas):
        resto = celda[m.end():marcas[n + 1].start() if n + 1 < len(marcas) else len(celda)]
        cita = RE_CITA.search(resto)
        ref = RE_REF.search(resto)
        out.append({"codigo": m.group(1).upper(), "estado": m.group(2).capitalize(),
                    "cita": cita.group(1) if cita else None, "doc": ref.group(1) if ref else None,
                    "seccion": (ref.group(2) or "").strip() if ref else ""})
    return out


def _obs(lista, paso, regla, detalle):
    lista.append({"paso": paso, "regla": regla, "detalle": detalle})


def sk02(texto: str, finish: str | None, lote: list[dict], docs: dict[str, str], paso: str) -> dict:
    obs, citas = [], []
    if finish != "STOP" or CIERRE["SK-02"] not in texto:
        _obs(obs, paso, "truncamiento", f"Motivo de fin {finish}; bloque de cierre {'presente' if CIERRE['SK-02'] in texto else 'ausente'}")
    esperados = {r["id"]: r for r in lote}
    rx = re.compile("|".join(re.escape(i) for i in esperados))
    vistas, resultados = {}, []
    for c in filas(texto, rx):
        if len(c) < 6:
            _obs(obs, paso, "formato", f"{c[0]}: la fila tiene {len(c)} columnas en lugar de 6")
            continue
        if len(c) > 6:  # «|» dentro de una cita: las tres últimas columnas siguen siendo resultado, evidencia y hallazgo
            _obs(obs, paso, "formato", f"{c[0]}: carácter «|» dentro de las celdas ({len(c)} columnas); se reconstruye la fila")
            c = [c[0], c[1], " | ".join(c[2:-3]), c[-3], c[-2], c[-1]]
        if c[0] in vistas:
            _obs(obs, paso, "cobertura", f"{c[0]}: fila repetida")
            continue
        vistas[c[0]] = True
        req, res = esperados[c[0]], c[3].strip()
        els = elementos_de_celda(c[2])
        fila = {"id": c[0], "requisito": req["requisito"], "proceso": req["proceso"], "elementos_texto": c[2],
                "elementos": els, "resultado": res, "evidencia": c[4], "hallazgo": c[5], "alertas": []}
        resultados.append(fila)
        if res not in RESULTADOS:
            _obs(obs, paso, "resultado", f"{c[0]}: resultado no permitido «{res}»")
        codigos = [e["codigo"] for e in els]
        faltan = [e["codigo"] for e in req["elementos"] if e["codigo"] not in codigos]
        if faltan:
            _obs(obs, paso, "elementos", f"{c[0]}: no recorre {', '.join(faltan)}")
        rec = {e["codigo"] for e in req["elementos"] if e["recomendacion"]}
        oblig = [e for e in els if e["codigo"] not in rec]
        respalda = any(e["estado"] == "Respalda" for e in els)
        contradicho = any(e["estado"] == "Contradicho" for e in oblig)
        falta_lugar = any(e["estado"] == "Falta" and e["doc"] for e in oblig)
        falta = any(e["estado"] == "Falta" for e in oblig)
        coherente = {"Conforme": not falta and not contradicho and bool(els),
                     "N": contradicho or falta_lugar,
                     "O": respalda,
                     "M": respalda and not contradicho,
                     "Sin evidencia": not respalda and not contradicho and not falta_lugar}.get(res, True)
        if not coherente:
            _obs(obs, paso, "coherencia", f"{c[0]}: «{res}» no es coherente con sus elementos ({c[2][:120]})")
        if res in ("N", "O", "M") and c[5].strip() in ("", "—", "-"):
            _obs(obs, paso, "hallazgo", f"{c[0]}: resultado {res} sin hallazgo propuesto")
        no_literales = []
        for e in els:
            if e["estado"] in ("Respalda", "Contradicho"):
                if not e["cita"]:
                    _obs(obs, paso, "citas", f"{c[0]} {e['codigo']}: {e['estado']} sin cita")
                    no_literales.append(e["codigo"])
                    continue
                cat = clasificar_cita(e["cita"], e["doc"], docs)
                citas.append({"id": c[0], "elemento": e["codigo"], "cita": e["cita"], "doc": e["doc"], "categoria": cat})
                if cat != "literal":
                    _obs(obs, paso, "citas", f"{c[0]} {e['codigo']}: cita {cat} «{e['cita'][:80]}»")
                    if e["estado"] == "Respalda" and cat != "literal en otro documento":
                        no_literales.append(e["codigo"])
        # Alertas para el revisor: un resultado favorable que se apoya en citas que no están en el documento,
        # o un resultado incoherente con sus elementos, no debe aceptarse sin leer la evidencia.
        if res in ("Conforme", "M") and no_literales:
            fila["alertas"].append(f"Revisar: {res} apoyado en cita no literal ({', '.join(no_literales)})")
        if not coherente:
            fila["alertas"].append("Revisar: resultado incoherente con sus elementos")
    for i in esperados:
        if i not in vistas:
            _obs(obs, paso, "cobertura", f"{i}: sin fila en la respuesta")
    return {"resultados": resultados, "observaciones": obs, "citas": citas}


def sk03(texto: str, finish: str | None, hallazgos_sk02: list[dict], docs: dict[str, str],
         fecha_base: date, paso: str) -> dict:
    obs = []
    if finish != "STOP" or CIERRE["SK-03"] not in texto:
        _obs(obs, paso, "truncamiento", f"Motivo de fin {finish}")
    rx = re.compile(r"H-\d+")
    hallazgos, planes = {}, {}
    for c in filas(texto, rx):
        if len(c) == 5 and c[1] in ("N", "O", "M"):
            hallazgos[c[0]] = {"id": c[0], "clasificacion": c[1], "requisitos": c[2], "descripcion": c[3], "evidencia": c[4]}
        elif len(c) >= 8:
            planes[c[0]] = {"id": c[0], "correccion": c[1], "accion": c[2], "responsable": c[3], "fecha": c[4],
                            "eficacia": c[5], "estado": c[6], "avance": c[7]}
        else:
            _obs(obs, paso, "formato", f"{c[0]}: fila con {len(c)} columnas")
    todos = "\n".join(norm(t) for t in docs.values())
    cubiertos = " ".join(h["requisitos"] for h in hallazgos.values())
    for r in hallazgos_sk02:
        if not re.search(rf"(?<![\d.]){re.escape(r['id'])}(?![\d.])", cubiertos):
            _obs(obs, paso, "cobertura", f"{r['id']} ({r['resultado']}) no figura en ningún hallazgo")
    for h in hallazgos.values():
        for cita in [x for x in RE_CITA.findall(h["evidencia"]) if len(x) >= 12]:  # omite rótulos como "Falta"
            ref = RE_REF.search(h["evidencia"])
            cat = clasificar_cita(cita, ref.group(1) if ref else None, docs)
            if cat != "literal":
                _obs(obs, paso, "citas", f"{h['id']}: cita {cat} «{cita[:80]}»")
        p = planes.get(h["id"])
        if not p:
            _obs(obs, paso, "plan", f"{h['id']}: sin plan de acción")
            continue
        esperada = (fecha_base + timedelta(days=DIAS[h["clasificacion"]])).isoformat()
        if p["fecha"] != esperada:
            _obs(obs, paso, "fecha", f"{h['id']}: fecha {p['fecha']} distinta de la regla ({esperada})")
        if p["responsable"] != "Por designar" and norm(p["responsable"]) not in todos:
            _obs(obs, paso, "responsable", f"{h['id']}: «{p['responsable']}» no figura en los documentos")
    return {"hallazgos": list(hallazgos.values()), "planes": planes, "observaciones": obs}


def sk04(texto: str, finish: str | None, ids_hallazgos: set[str], paso: str) -> dict:
    obs = []
    if finish != "STOP" or CIERRE["SK-04"] not in texto:
        _obs(obs, paso, "truncamiento", f"Motivo de fin {finish}")
    for h in sorted(set(re.findall(r"H-\d+", texto)) - ids_hallazgos):
        _obs(obs, paso, "hallazgos", f"menciona {h}, que no existe")
    for m in PROHIBIDAS.finditer(texto):
        _obs(obs, paso, "afirmacion", f"expresión no permitida: «{m.group(0)}»")
    cuerpo = texto.split(CIERRE["SK-04"])[0].strip()
    return {"texto": cuerpo, "observaciones": obs}
