"""Verificaciones automáticas de una respuesta de SK-01.

Comprueba la FORMA de la respuesta, no la corrección de fondo (eso lo revisa el equipo).
Las comprobaciones se separan por categoría:
  1. Truncamiento            motivo de fin de la API y bloque de cierre
  2. Cobertura               calculada por el programa a partir de los IDs del catálogo
  3. Plantilla               filas e IDs iguales a la plantilla enviada (desde la Skill v0.3)
  4. Conteos                 calculados por el programa; se contrastan con lo que declara el modelo
  5. Estados                 válidos y compatibles con la categoría y la aplicabilidad
  6. Citas                   literalidad y página
  7. Formato y coherencia    justificación, elementos, aplicabilidad, recomendaciones, listas

Cada comprobación indica desde qué versión de la Skill es exigible. Las que no eran
exigibles en la versión evaluada se informan aparte y no cuentan como observaciones.
Lee los formatos de matriz de todas las versiones (v0.1: 8 columnas; v0.2–v0.4: 9; v0.5: 10).
Nunca se modifica la respuesta del modelo.
"""

import re
import unicodedata
from pathlib import Path

RE_ID = re.compile(r"A\.[123]\.\d+(?:\.\d+)?")
RE_RANGO = re.compile(
    r"(A\.[123]\.\d+(?:\.\d+)?)\s*(?:to|a|al|hasta|–|—|-)\s*(A\.[123]\.\d+(?:\.\d+)?)", re.IGNORECASE)
RE_PAGINA = re.compile(r"P[áa]g(?:ina)?s?\.?\s*(\d+)(?:\s*(?:-|–|y|a)\s*(\d+))?", re.IGNORECASE)
RE_MARCA = re.compile(r"\[P[áa]gina\s*\d+\]\s*", re.IGNORECASE)
RE_CITAS = [re.compile(p) for p in (r'"([^"]{3,}?)"', r"“([^”]{3,}?)”", r"«([^»]{3,}?)»")]
RE_ELEM = re.compile(r"\b(E\d+)\s+(Respalda|Falta|Contradicho)", re.IGNORECASE)
CIERRE = "--- FIN SK-01 ---"

ESTADOS = [
    "Cumple",
    "Cumple parcialmente",
    "No evidenciado",
    "Incumplimiento documental sustentado",
    "No determinado",
    "No aplica",
]
REQUIEREN_CITA = {"Cumple", "Cumple parcialmente", "Incumplimiento documental sustentado"}
ESTADOS_DE_VACIO = {"No evidenciado", "Cumple parcialmente", "Incumplimiento documental sustentado"}

# Categorías metodológicas (catálogo v0.6). Equivalencias con la clasificación anterior:
# D → E, D* → C, I → INT-i, N → INT; la Tabla A.2 se identifica como "A2" (C según el rol).
EQUIVALENCIAS = {"D": "E", "D*": "C", "I": "INT-i", "N": "INT"}
PERMITIDOS = {
    "E": set(ESTADOS),
    "C": set(ESTADOS),                       # C con aplicabilidad «Aplica»
    "C-por-determinar": {"No determinado"},
    "C-no-aplica": {"No aplica"},
    "INT-i": {"Cumple parcialmente", "Incumplimiento documental sustentado", "No determinado", "No aplica"},
    "INT": {"Incumplimiento documental sustentado", "No determinado", "No aplica"},
}
APLICABILIDADES = {"aplica": "Aplica", "no aplica": "No aplica", "por determinar": "Por determinar"}
ROTULOS = ("completar la política", "corregir el texto", "aclarar aplicabilidad",
           "solicitar evidencia interna", "mantener", "ninguna")
SITUACIONES = {"presente", "parcial", "ausente", "no aplica", "por determinar"}
# Expresiones que describen silencio del documento. Si justifican un «No aplica» en un control C,
# probablemente se confundió el silencio con un descarte expreso (heurística: la revisa una persona).
RE_SILENCIO = re.compile(
    r"\bno (se )?(menciona|mencionan|identifica|identifican|declara|declaran|contempla|contemplan|"
    r"especifica|especifican|indica|indican|detalla|detallan|describe|describen|hace referencia)|"
    r"\bal no haber\b|\bsin menci[oó]n\b|\bno hay (menci[oó]n|referencia|indicios?)", re.IGNORECASE)

# Versión de la Skill desde la que cada regla es exigible
DESDE = {
    "cobertura": "0.1", "rangos": "0.1", "estados": "0.1", "cita_requerida": "0.1",
    "citas_literales": "0.1", "estado_catalogo": "0.1", "a2_rol": "0.1", "resumen_vacios": "0.1",
    "conteos_declarados": "0.1",
    "d_estrella": "0.2", "marca_pagina": "0.2", "justificacion": "0.2", "recorrido": "0.2",
    "plantilla": "0.3", "separadores": "0.3", "respalda_falta": "0.3",
    "elementos": "0.4",
    "aplicabilidad": "0.5", "info_faltante": "0.5", "recomendacion": "0.5",
    "lista_titular": "0.5", "dependencias": "0.5",
    "no_aplica_silencio": "0.5.1",
}
# Versión a partir de la cual la regla deja de exigirse (exclusiva).
#   conteos: desde v0.3 el modelo no los declara · resumen: desde v0.4 lo genera la aplicación
#   «Respalda / Falta» libre: desde v0.4 es por elemento · activación D*: desde v0.5 es la columna Aplicabilidad
HASTA_ANTES_DE = {"conteos_declarados": "0.3", "resumen_vacios": "0.4", "respalda_falta": "0.4",
                  "d_estrella": "0.5"}


def _v(s: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", s or "0"))


def exigible(regla: str, version: str) -> bool:
    ok = _v(version) >= _v(DESDE[regla])
    return ok and (regla not in HASTA_ANTES_DE or _v(version) < _v(HASTA_ANTES_DE[regla]))


# ---------- catálogo ----------

def _codigo_cat(celda: str) -> str:
    """Normaliza la categoría del catálogo (acepta la clasificación nueva y la anterior)."""
    c = celda.replace("\\", "").strip()
    for nuevo in ("INT-i", "INT", "E", "C"):
        if c == nuevo or c.startswith(nuevo + " "):
            return nuevo
    if c.startswith("D*"):
        return "C"
    return EQUIVALENCIAS.get(c[:1], c[:1])


def catalogo_detallado(ruta_catalogo: Path) -> list[dict]:
    """Controles en orden de catálogo: id, título, categoría ('E', 'C', 'INT-i', 'INT', 'A2') y grupo.
    (La clave se llama 'eval' por compatibilidad con versiones anteriores del motor.)"""
    texto = ruta_catalogo.read_text(encoding="utf-8")
    seccion = texto[texto.index("## 4."):texto.index("## 5.")]
    controles = []
    for linea in seccion.splitlines():
        if not linea.startswith("| A."):
            continue
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if c[0].startswith("A.2."):
            for i in range(0, len(c) - 1, 2):
                if RE_ID.fullmatch(c[i]):
                    controles.append({"id": c[i], "titulo": c[i + 1], "eval": "A2", "grupo": "A.2"})
        elif c[0].startswith("A.1."):
            controles.append({"id": c[0], "titulo": c[1], "eval": _codigo_cat(c[3]), "grupo": None})
        elif c[0].startswith("A.3."):
            ev = _codigo_cat(c[2])
            controles.append({"id": c[0], "titulo": c[1], "eval": ev, "grupo": "A.3-N" if ev == "INT" else None})
    a2 = sorted((x for x in controles if x["grupo"] == "A.2"), key=lambda x: _v(x["id"]))
    return [x for x in controles if x["grupo"] != "A.2"] + a2


def controles_del_catalogo(ruta_catalogo: Path) -> dict[str, str]:
    return {x["id"]: x["eval"] for x in catalogo_detallado(ruta_catalogo)}


def guia_por_control(ruta_catalogo: Path) -> dict[str, str]:
    """ID -> referencias del Anexo B (catálogo §2.2). Vacío si el catálogo no tiene esa tabla."""
    texto = ruta_catalogo.read_text(encoding="utf-8")
    if "### 2.2" not in texto:
        return {}
    seccion = texto[texto.index("### 2.2"):texto.index("## 3.")]
    out = {}
    for linea in seccion.splitlines():
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if c and RE_ID.fullmatch(c[0]) and len(c) >= 3:
            out[c[0]] = c[2]
    return out


def lista_titular(ruta_catalogo: Path) -> list[dict]:
    """Orientaciones O-01 a O-16 (catálogo §5.1) con su categoría en la lista."""
    texto = ruta_catalogo.read_text(encoding="utf-8")
    if "### 5.1" not in texto:
        return []
    seccion = texto[texto.index("### 5.1"):texto.index("### 5.2")]
    out = []
    for linea in seccion.splitlines():
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if c and re.fullmatch(r"O-\d\d", c[0]):
            out.append({"id": c[0], "que": c[1], "fuente": c[2], "control": c[3],
                        "cat": c[5] if len(c) >= 6 else ""})
    return out


def elementos_por_control(ruta: Path) -> dict[str, list[tuple[str, str]]]:
    """ID -> [(código, etiqueta 'aviso'|'interno')] según elementos.md."""
    out = {}
    if not ruta.exists():
        return out
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if c and RE_ID.fullmatch(c[0]):
            out[c[0]] = [(m.group(1), m.group(2)) for m in re.finditer(r"(E\d+)\b.*?\[(aviso|interno)\]", c[-1])]
    return out


def dependencias_por_control(ruta: Path) -> dict[str, dict[str, list[str]]]:
    """ID -> {elemento: [elementos de los que depende]}, según "(depende de E1, E2 o E3)"."""
    out = {}
    if not ruta.exists():
        return out
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if c and RE_ID.fullmatch(c[0]):
            for seg in c[-1].split("·"):
                m = re.search(r"\b(E\d+)\b.*?\(depende de ([^)]*)\)", seg)
                if m:
                    out.setdefault(c[0], {})[m.group(1)] = re.findall(r"E\d+", m.group(2))
    return out


def _estado_elementos(justificacion: str) -> dict[str, list[str]]:
    """E1 -> [estado, texto que sigue]; toma el primer estado declarado de cada código."""
    out = {}
    marcas = list(RE_ELEM.finditer(justificacion or ""))
    for n, m in enumerate(marcas):
        fin = marcas[n + 1].start() if n + 1 < len(marcas) else len(justificacion)
        out.setdefault(m.group(1).upper(), [m.group(2).capitalize(), justificacion[m.end():fin]])
    return out


# ---------- lectura de la respuesta ----------

def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'"), ("«", '"'), ("»", '"'),
                 ("–", "-"), ("—", "-"), ("­", ""), ("\\", ""), ("**", "")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()


def _estado(celda: str) -> str | None:
    limpio = _norm(celda).strip("*_ .")
    return next((e for e in ESTADOS if limpio == e.lower()), None)


def _aplicabilidad(celda: str | None) -> str | None:
    if celda is None:
        return None
    limpio = _norm(celda).strip("*_ .")
    return APLICABILIDADES.get(limpio)


def filas_de_la_matriz(texto: str) -> list[dict]:
    filas = []
    for linea in texto.splitlines():
        if not linea.lstrip().startswith("|"):
            continue
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if not c or not RE_ID.search(c[0]) or len(c) < 8:
            continue
        if len(c) >= 10:      # v0.5: Ref | Control | Cat. | Aplicabilidad | Evidencia | Ubic. | Estado | Just. | Info | Rec.
            f = {"eval": c[2], "aplicabilidad_texto": c[3], "evidencia": c[4], "ubicacion": c[5],
                 "estado_texto": c[6], "justificacion": c[7], "vacio": c[8], "recomendacion": c[9]}
        elif len(c) >= 9:     # v0.2–v0.4: ID | Control | Eval. | Evidencia | Ubic. | Estado | Just. | Vacío | Rec.
            f = {"eval": c[2], "aplicabilidad_texto": None, "evidencia": c[3], "ubicacion": c[4],
                 "estado_texto": c[5], "justificacion": c[6], "vacio": c[7], "recomendacion": c[8]}
        else:                 # v0.1: ID | Control | Eval. | Evidencia | Ubic. | Estado | Vacío | Rec.
            f = {"eval": c[2], "aplicabilidad_texto": None, "evidencia": c[3], "ubicacion": c[4],
                 "estado_texto": c[5], "justificacion": None, "vacio": c[6], "recomendacion": c[7]}
        f.update({"celda_id": c[0], "ids": RE_ID.findall(c[0]), "rangos": RE_RANGO.findall(c[0]),
                  "estado": _estado(f["estado_texto"]),
                  "aplicabilidad": _aplicabilidad(f["aplicabilidad_texto"])})
        filas.append(f)
    return filas


def filas_lista_titular(texto: str) -> dict[str, dict]:
    """Filas «| O-xx … |» de la sección «Información al titular»."""
    seccion = _seccion(texto, "Información al titular")
    out = {}
    for linea in seccion.splitlines():
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        m = re.match(r"(O-\d\d)", c[0]) if c else None
        if m and len(c) >= 7:
            out[m.group(1)] = {"situacion": c[2], "cita": c[3], "ubicacion": c[4], "falta": c[5], "sugerencia": c[6]}
    return out


def _seccion(texto: str, titulo: str) -> str:
    m = re.search(rf"^#+\s*\d*\.?\s*{titulo}.*?$(.*?)(?=^#+\s|\Z)", texto, re.M | re.S | re.I)
    return m.group(1) if m else ""


def _citas(evidencia: str) -> list[str]:
    return [c for p in RE_CITAS for c in p.findall(evidencia or "")]


def _paginas(ubicacion: str) -> list[int]:
    out = []
    for ini, fin in RE_PAGINA.findall(ubicacion or ""):
        a, b = int(ini), int(fin or ini)
        out += list(range(min(a, b), max(a, b) + 1))
    return out


def _buscar(cita: str, paginas_norm: list[str], indicadas: list[int], separador_extra: bool = False):
    texto = _norm(RE_MARCA.sub("", cita))
    patron = r"\[\s*(?:…|\.\.\.)\s*\]|…|\.\.\."
    if separador_extra:
        patron += r"|\s/\s"
    frags = [f.strip(" .,;:") for f in re.split(patron, texto)]
    frags = [f for f in frags if len(f) >= 4]
    if not frags:
        return "cita demasiado corta", []

    def esta_en(n):
        if not 1 <= n <= len(paginas_norm):
            return False
        t = paginas_norm[n - 1] + (" " + paginas_norm[n] if n < len(paginas_norm) else "")
        return all(f in t for f in frags)

    if any(esta_en(n) for n in indicadas):
        return "en la página indicada", [n for n in indicadas if esta_en(n)]
    otras = [n for n in range(1, len(paginas_norm) + 1) if esta_en(n)]
    return ("en otra página", otras) if otras else ("no encontrada", [])


def _clasificar_cita(cita, paginas_norm, indicadas) -> tuple[str, list[int]]:
    """Categorías: literal · literal con marca de página · literal con separadores añadidos ·
    en otra página · no encontrada."""
    res, en = _buscar(cita, paginas_norm, indicadas)
    con_marca = bool(RE_MARCA.search(cita))
    if res == "en la página indicada":
        return ("literal con marca de página" if con_marca else "literal"), en
    if res == "no encontrada" and " / " in cita:
        res2, en2 = _buscar(cita, paginas_norm, indicadas, separador_extra=True)
        if res2 == "en la página indicada":
            return "literal con separadores añadidos", en2
    return res, en


def _conteos_declarados(texto: str) -> dict:
    resumen = _seccion(texto, "Resumen")
    declarados = {}
    for e in ESTADOS:
        m = re.search(rf"(?:^|\|)\s*-?\s*\**{re.escape(e)}\**\s*(?::|\|)\s*(\d+)", resumen, re.M | re.I)
        if m:
            declarados[e] = int(m.group(1))
    total = re.search(r"Total[^\n:|]*[:|]\s*\**\s*(\d+)", resumen, re.I)
    bloque = texto[texto.find(CIERRE):] if CIERRE in texto else ""
    ind = re.search(r"fila individual:\s*(\d+)", bloque)
    return {"por_estado": declarados, "total": int(total.group(1)) if total else None,
            "individuales_cierre": int(ind.group(1)) if ind else None}


def _categoria_efectiva(f: dict, cat: str) -> str | None:
    """Clave de PERMITIDOS según la categoría y la aplicabilidad declarada en la fila."""
    if cat == "C":
        if f["aplicabilidad"] is not None:                 # formato v0.5
            return {"Aplica": "C", "No aplica": "C-no-aplica",
                    "Por determinar": "C-por-determinar"}[f["aplicabilidad"]]
        t = _norm(f["eval"])                                # formato v0.2–v0.4 (D*)
        if "no activ" in t:
            return "C-por-determinar"
        return "C"
    return cat


# ---------- verificación ----------

def verificar(texto: str, finish_reason: str | None, paginas_enviadas: list[str],
              catalogo: list[dict], estado_catalogo: str, version_skill: str,
              plantilla_ids: list[list[str]] | None = None,
              elementos: dict[str, list[tuple[str, str]]] | None = None,
              dependencias: dict[str, dict[str, list[str]]] | None = None,
              lista_esperada: list[dict] | None = None) -> dict:
    evals = {x["id"]: x["eval"] for x in catalogo}
    filas = filas_de_la_matriz(texto)
    paginas_norm = [_norm(p) for p in paginas_enviadas]
    obs: list[dict] = []

    def anotar(categoria, regla, detalle):
        obs.append({"categoria": categoria, "regla": regla, "detalle": detalle,
                    "exigible": exigible(regla, version_skill)})

    # 1. Truncamiento
    truncada = finish_reason != "STOP" or CIERRE not in texto

    # 2. Cobertura (solo IDs explícitos; los extremos de un rango no cuentan como cobertura)
    apariciones: dict[str, list[int]] = {}
    for n, f in enumerate(filas):
        en_rango = {i for r in f["rangos"] for i in r}
        for r in f["rangos"]:
            anotar("Cobertura", "rangos", f"Fila {n + 1}: rango «{r[0]} … {r[1]}»; los IDs del rango no se cuentan")
        f["ids_explicitos"] = [i for i in f["ids"] if i not in en_rango]
        for i in f["ids_explicitos"]:
            apariciones.setdefault(i, []).append(n)
    faltantes = [x["id"] for x in catalogo if x["id"] not in apariciones]
    repetidos = sorted((i for i, ns in apariciones.items() if len(ns) > 1), key=_v)
    desconocidos = sorted((i for i in apariciones if i not in evals), key=_v)
    individuales = {x["id"] for x in catalogo if x["grupo"] is None}
    mal_agrupados = sorted({i for f in filas if len(f["ids_explicitos"]) > 1
                            for i in f["ids_explicitos"] if i in individuales}, key=_v)
    if faltantes:
        anotar("Cobertura", "cobertura", f"{len(faltantes)} IDs sin fila explícita: {', '.join(faltantes)}")
    for i in repetidos:
        anotar("Cobertura", "cobertura", f"{i} aparece en más de una fila")
    for i in desconocidos:
        anotar("Cobertura", "cobertura", f"{i} no está en el catálogo")
    for i in mal_agrupados:
        anotar("Cobertura", "cobertura", f"{i} debía tener fila propia y está agrupado")
    por_tabla = {}
    for etiqueta, cond in (("A.1", lambda x: x["id"].startswith("A.1.")),
                           ("A.3 (INT-i)", lambda x: x["id"].startswith("A.3.") and x["eval"] == "INT-i"),
                           ("A.3 (INT)", lambda x: x["grupo"] == "A.3-N"),
                           ("A.2", lambda x: x["grupo"] == "A.2")):
        ids = [x["id"] for x in catalogo if cond(x)]
        por_tabla[etiqueta] = (sum(i in apariciones for i in ids), len(ids))

    # 3. Plantilla
    if plantilla_ids is not None:
        esperadas = [frozenset(p) for p in plantilla_ids]
        recibidas = [frozenset(f["ids_explicitos"]) for f in filas]
        for p in esperadas:
            if p not in recibidas:
                ids = sorted(p, key=_v)
                anotar("Plantilla", "plantilla", "Fila de la plantilla ausente o modificada: "
                       + ", ".join(ids[:4]) + (" …" if len(ids) > 4 else ""))
        for r in recibidas:
            if r not in esperadas:
                ids = sorted(r, key=_v)
                anotar("Plantilla", "plantilla", "Fila que no está en la plantilla: "
                       + ", ".join(ids[:4]) + (" …" if len(ids) > 4 else ""))

    # 4. Conteos calculados por el programa
    estado_por_id = {}
    for f in filas:
        for i in f["ids_explicitos"]:
            estado_por_id.setdefault(i, f["estado"])
    conteo_ids = {e: sum(1 for i in evals if estado_por_id.get(i) == e) for e in ESTADOS}
    conteo_ids["(estado no válido)"] = sum(1 for i in evals if i in estado_por_id and estado_por_id[i] is None)
    conteo_ids["(sin fila explícita)"] = len(faltantes)
    conteo_filas = {e: sum(1 for f in filas if f["estado"] == e) for e in ESTADOS}
    n_ind = sum(1 for f in filas if len(f["ids_explicitos"]) == 1)
    declarados = _conteos_declarados(texto)
    for e, n in declarados["por_estado"].items():
        if n != conteo_filas[e]:
            anotar("Conteos", "conteos_declarados", f"El resumen declara {e}: {n}; filas calculadas: {conteo_filas[e]}")
    if declarados["total"] is not None and declarados["total"] != len(filas):
        anotar("Conteos", "conteos_declarados", f"El resumen declara un total de {declarados['total']}; filas calculadas: {len(filas)}")
    if declarados["individuales_cierre"] is not None and declarados["individuales_cierre"] != n_ind:
        anotar("Conteos", "conteos_declarados", f"El cierre declara {declarados['individuales_cierre']} filas individuales; calculadas: {n_ind}")

    # 5. Estados, según categoría y aplicabilidad
    for f in filas:
        cab = ", ".join(f["ids_explicitos"][:3]) or f["celda_id"][:40]
        if f["estado"] is None:
            anotar("Estados", "estados", f"{cab}: estado no reconocido «{f['estado_texto']}»")
            continue
        for i in f["ids_explicitos"]:
            cat = evals.get(i)
            if cat in (None, "A2"):
                continue
            if cat == "C" and f["aplicabilidad"] is None:
                t = _norm(f["eval"])
                if "activ" not in t:
                    anotar("Estados", "d_estrella", f"{i}: D* sin declarar si está activado")
            efectiva = _categoria_efectiva(f, cat)
            if f["estado"] not in PERMITIDOS[efectiva]:
                etiqueta = efectiva if _v(version_skill) >= _v("0.5") else {
                    "E": "D", "C": "D*", "C-por-determinar": "D*-no-activado",
                    "INT-i": "I", "INT": "N"}.get(efectiva, efectiva)
                anotar("Estados", "estados", f"{i}: «{f['estado']}» no está permitido para {etiqueta}")
        if f["estado"] in REQUIEREN_CITA and not _citas(f["evidencia"]):
            anotar("Estados", "cita_requerida", f"{cab}: «{f['estado']}» sin cita literal")

    # 6. Citas
    citas = []
    for f in filas:
        indicadas = _paginas(f["ubicacion"])
        cab = (f["ids_explicitos"] or [f["celda_id"][:30]])[0]
        for c in _citas(f["evidencia"]):
            cat, en = _clasificar_cita(c, paginas_norm, indicadas)
            citas.append({"ids": f["ids_explicitos"] or [f["celda_id"][:30]], "cita": c,
                          "paginas_indicadas": indicadas, "categoria": cat, "encontrada_en": en})
            if cat == "literal con marca de página":
                anotar("Citas", "marca_pagina", f"{cab}: cita con [Página N] dentro de las comillas")
            elif cat == "literal con separadores añadidos":
                anotar("Citas", "separadores", f"{cab}: cita literal con « / » añadidos entre líneas")
            elif cat in ("en otra página", "no encontrada"):
                anotar("Citas", "citas_literales", f"{cab}: cita {cat}")

    # 7. Formato y coherencia
    if _norm(estado_catalogo) not in _norm(texto):
        anotar("Formato", "estado_catalogo", "El estado del catálogo no está copiado literalmente")
    for f in filas:
        if len(f["ids_explicitos"]) != 1:
            continue
        i, j = f["ids_explicitos"][0], f["justificacion"]
        if j is None or _norm(j) in ("", "-"):
            anotar("Formato", "justificacion", f"{i}: fila sin justificación")
            continue
        if f["estado"] in ("Cumple", "Cumple parcialmente"):
            jn = _norm(j)
            if "respalda:" not in jn or "falta:" not in jn:
                anotar("Formato", "respalda_falta", f"{i}: justificación sin «Respalda:» y «Falta:»")
            elif f["estado"] == "Cumple" and not re.search(r"falta:\s*(ninguno|ninguna|nada)", jn):
                anotar("Formato", "respalda_falta", f"{i}: «Cumple», pero la justificación declara elementos faltantes")

    # Elementos (desde v0.4) y dependencias (desde v0.5)
    for f in filas:
        if len(f["ids_explicitos"]) != 1 or not elementos:
            continue
        i = f["ids_explicitos"][0]
        esperados = elementos.get(i)
        if not esperados or f["estado"] is None:
            continue
        cat = evals.get(i)
        if _categoria_efectiva(f, cat) in ("C-por-determinar", "C-no-aplica"):
            continue
        dec = _estado_elementos(f["justificacion"] or "")
        faltan = [c for c, _ in esperados if c not in dec]
        if faltan:
            anotar("Formato", "elementos", f"{i}: la justificación no recorre {', '.join(faltan)}")
        for c, (est, resto) in dec.items():
            if est in ("Respalda", "Contradicho") and not _citas(resto):
                anotar("Formato", "elementos", f"{i}: {c} «{est}» sin cita")
        aviso = [c for c, tag in esperados if tag == "aviso"]
        resp = [c for c in aviso if dec.get(c, [""])[0] == "Respalda"]
        no_resp = [c for c in aviso if dec.get(c, [""])[0] in ("Falta", "Contradicho")]
        if f["estado"] == "Cumple" and (no_resp or len(resp) < len(aviso)):
            anotar("Estados", "elementos", f"{i}: «Cumple» con elementos [aviso] no respaldados: {', '.join(c for c in aviso if c not in resp)}")
        # En los controles internos los elementos [interno] siempre faltan en una política pública:
        # basta con un elemento [aviso] respaldado. En E / C se exige además un [aviso] faltante.
        faltante = no_resp or (cat == "INT-i" and any(tag == "interno" for _, tag in esperados))
        if f["estado"] == "Cumple parcialmente" and (not resp or not faltante):
            anotar("Estados", "elementos", f"{i}: «Cumple parcialmente» sin al menos un elemento respaldado y otro faltante")
        if f["estado"] in ("No evidenciado", "No determinado") and resp:
            anotar("Estados", "elementos", f"{i}: «{f['estado']}» pese a declarar respaldados {', '.join(resp)}")
        for dep, padres in (dependencias or {}).get(i, {}).items():
            if dec.get(dep, [""])[0] == "Respalda" and not any(dec.get(p, [""])[0] == "Respalda" for p in padres):
                anotar("Estados", "dependencias", f"{i}: {dep} respaldado sin {' / '.join(padres)}")

    # Aplicabilidad, información faltante y recomendaciones (desde v0.5)
    for f in filas:
        if not f["ids_explicitos"] or f["aplicabilidad_texto"] is None:
            continue
        i = f["ids_explicitos"][0]
        cat = evals.get(i)
        individual = len(f["ids_explicitos"]) == 1
        rec = _norm(f.get("recomendacion") or "")
        vacio = _norm(f.get("vacio") or "")
        if individual and cat == "E" and f["aplicabilidad"] != "Aplica":
            if not (f["aplicabilidad"] == "No aplica" and _citas(f["evidencia"])):
                anotar("Formato", "aplicabilidad", f"{i}: control E con aplicabilidad «{f['aplicabilidad_texto']}»")
        if individual and cat == "C" and f["aplicabilidad"] == "No aplica":
            motivo = " ".join(x or "" for x in (f["justificacion"], f.get("vacio"), f.get("recomendacion")))
            if RE_SILENCIO.search(motivo):
                anotar("Formato", "no_aplica_silencio",
                       f"{i}: «No aplica» justificado con silencio del documento (debía ser «Por determinar»)")
        if individual and cat == "C":
            if f["aplicabilidad"] is None:
                anotar("Formato", "aplicabilidad", f"{i}: aplicabilidad no reconocida «{f['aplicabilidad_texto']}»")
            elif f["aplicabilidad"] in ("Aplica", "No aplica") and not _citas(f["evidencia"]):
                anotar("Formato", "aplicabilidad", f"{i}: «{f['aplicabilidad']}» sin cita que lo justifique")
        efectiva = _categoria_efectiva(f, cat) if cat not in (None, "A2") else None
        if individual and efectiva in ("E", "C") and f["estado"] not in ("Cumple", "No aplica", None):
            if vacio in ("", "-"):
                anotar("Formato", "info_faltante", f"{i}: falta «Información faltante» en un criterio aplicable sin «Cumple»")
            if not (rec.startswith("completar la política") or rec.startswith("corregir el texto")):
                anotar("Formato", "recomendacion", f"{i}: debía recomendar «Completar la política» o «Corregir el texto»")
        if individual and efectiva == "C-por-determinar":
            if vacio in ("", "-"):
                anotar("Formato", "info_faltante", f"{i}: falta la «Información necesaria» para determinar la aplicabilidad")
            if not rec.startswith("aclarar aplicabilidad"):
                anotar("Formato", "recomendacion", f"{i}: debía recomendar «Aclarar aplicabilidad»")
        if cat in ("INT-i", "INT") and "completar la política" in rec:
            anotar("Formato", "recomendacion", f"{', '.join(f['ids_explicitos'][:3])}: control interno con «Completar la política»")
        if rec and not rec.startswith(ROTULOS):
            anotar("Formato", "recomendacion", f"{', '.join(f['ids_explicitos'][:3])}: recomendación sin rótulo de criterios.md §5")

    # Lista «Información al titular» (desde v0.5)
    if lista_esperada:
        recibida = filas_lista_titular(texto)
        for o in lista_esperada:
            fila = recibida.get(o["id"])
            if fila is None:
                anotar("Formato", "lista_titular", f"{o['id']}: falta en la lista «Información al titular»")
            elif _norm(fila["situacion"]).strip("*_ .") not in SITUACIONES:
                anotar("Formato", "lista_titular", f"{o['id']}: situación no reconocida «{fila['situacion']}»")
            elif (o["cat"].startswith("C") and _norm(fila["situacion"]).strip("*_ .") == "no aplica"
                  and RE_SILENCIO.search(" ".join((fila["falta"], fila["sugerencia"], fila["cita"])))):
                anotar("Formato", "no_aplica_silencio",
                       f"{o['id']}: «No aplica» en la lista justificado con silencio (debía ser «Por determinar»)")

    if not re.search(r"^#+\s*\d*\.?\s*Recorrido del documento", texto, re.M):
        anotar("Formato", "recorrido", "Falta la sección «Recorrido del documento»")
    for i in sorted(set(RE_ID.findall(_seccion(texto, "Resumen"))), key=_v):
        e, ev = estado_por_id.get(i), evals.get(i)
        if ev in ("INT-i", "INT", "A2") or e not in ESTADOS_DE_VACIO:
            anotar("Formato", "resumen_vacios", f"El resumen presenta {i} ({_etiqueta_antigua(ev)}, «{e}») como posible vacío documental")
    a2 = [f for f in filas if any(i.startswith("A.2.") for i in f["ids"])]
    if a2 and any(f["estado"] == "No aplica" for f in a2):
        rol = re.search(r"Rol de la organizaci[oó]n.*", texto)
        if not any(_citas(f["evidencia"] + " " + (f["justificacion"] or "")) for f in a2) \
                and not (rol and _citas(rol.group(0))):
            anotar("Formato", "a2_rol", "Tabla A.2 «No aplica» sin cita que justifique el rol")

    individuales_filas = [f for f in filas if len(f["ids_explicitos"]) == 1]
    return {
        "version_skill": version_skill,
        "finish_reason": finish_reason,
        "tiene_bloque_de_cierre": CIERRE in texto,
        "truncada": truncada,
        "cobertura_completa": not (faltantes or repetidos or mal_agrupados or desconocidos),
        "por_tabla": por_tabla,
        "filas": len(filas),
        "filas_individuales": n_ind,
        "conteo_ids": conteo_ids,
        "conteo_filas": conteo_filas,
        "declarados": declarados,
        "citas": citas,
        "observaciones": obs,
        "n_exigibles": sum(o["exigible"] for o in obs),
        "estado_por_id": estado_por_id,
        "filas_detalle": filas,
        "vacios": [
            (f["ids_explicitos"][0], f["estado"], f["vacio"] or "")
            for f in individuales_filas
            if f["estado"] in ESTADOS_DE_VACIO
            and _categoria_efectiva(f, evals.get(f["ids_explicitos"][0])) in ("E", "C")
        ],
        "por_determinar": [
            (f["ids_explicitos"][0], f["vacio"] or "")
            for f in individuales_filas
            if evals.get(f["ids_explicitos"][0]) == "C" and _categoria_efectiva(f, "C") == "C-por-determinar"
        ],
        "evidencia_interna": [
            (", ".join(f["ids_explicitos"][:3]) + (" …" if len(f["ids_explicitos"]) > 3 else ""), f["vacio"] or "")
            for f in filas
            if f["ids_explicitos"] and evals.get(f["ids_explicitos"][0]) in ("INT-i", "INT")
            and f["vacio"] and _norm(f["vacio"]) not in ("", "-")
        ],
    }


def _etiqueta_antigua(cat: str | None) -> str | None:
    """Mantiene el texto de las observaciones previas (I / N) para que la reverificación de
    ejecuciones antiguas no cambie su redacción."""
    return {"INT-i": "I", "INT": "N", "E": "D", "C": "D*"}.get(cat, cat)
