"""Presentación de la verificación (verificacion.md), aviso inicial y leyenda del informe."""

import re
from pathlib import Path

from motor import documento, skill
from motor.verificacion import CIERRE, DESDE, ESTADOS, HASTA_ANTES_DE, RE_ID, _v

CATEGORIAS = ["Cobertura", "Plantilla", "Conteos", "Estados", "Citas", "Formato"]
DONDE = {"aviso": "Política pública", "interno": "Documento interno"}


def etiqueta(v: dict) -> str:
    partes = [
        "TRUNCADA" if v["truncada"] else "no truncada",
        "cobertura completa" if v["cobertura_completa"] else "COBERTURA INCOMPLETA",
        f"{v['n_exigibles']} observaciones exigibles",
    ]
    return " · ".join(partes)


def aviso(v: dict, con_leyenda: bool = False) -> str:
    texto = f"> **Verificación automática:** {etiqueta(v)} (ver `verificacion.md`)."
    if v["truncada"] or not v["cobertura_completa"]:
        texto += "\n> ⚠️ **No presentar como evaluación completa.**"
    texto += ("\n> Las comprobaciones son de forma: no confirman que los estados sean correctos. "
              "El texto siguiente es la respuesta original del modelo, sin cambios.")
    if con_leyenda:
        texto += ("\n> Los códigos E1, E2… de la justificación se explican en la **Leyenda de elementos**, "
                  "al final del informe.")
    return texto


def informe(v: dict, texto: str, ruta_elementos: Path | None = None) -> str:
    """informe.md: aviso + resumen generado + respuesta original sin cambios (+ leyenda de elementos)."""
    cuerpo = aviso(v, con_leyenda=ruta_elementos is not None) + "\n\n" + resumen_generado(v) + texto
    if ruta_elementos is not None:
        cuerpo += "\n\n---\n\n" + leyenda_elementos(ruta_elementos)
    return cuerpo


def leyenda_elementos(ruta: Path) -> str:
    """Significado de los códigos E1, E2… tomado de elementos.md (lo genera la aplicación, no el modelo)."""
    texto = ruta.read_text(encoding="utf-8")
    m = re.search(r"\*\*Estado:\*\*\s*borrador\s+(v[\d.]+)", texto)
    try:
        nombre = ruta.resolve().relative_to(skill.RAIZ).as_posix()
    except ValueError:
        nombre = ruta.name
    l = ["## Leyenda de elementos (generada por la aplicación, no por el modelo)", "",
         f"Fuente: `{nombre}`{' ' + m.group(1) if m else ''}. Es metodología del equipo, no texto de la ISO, "
         "y está pendiente de revisión humana.", "",
         "**Cómo leer la justificación:**", "",
         "- `E1 Respalda ← \"cita\"`: el documento contiene ese elemento; la cita es la evidencia.",
         "- `E2 Falta`: el documento no contiene ese elemento.",
         "- `E2 Falta (interno)`: solo puede evidenciarse con documentos internos; no se exige a una política pública.",
         "- `E2 Contradicho ← \"cita\"`: el documento dice algo contrario al elemento.",
         "- *(depende de E1)*: el elemento no puede quedar respaldado si E1 falta.",
         "- †: aclaración del equipo agregada por errores observados en las pruebas.",
         "- Los controles INT y las filas agrupadas no tienen elementos.", "",
         "| Control | Elemento | Qué significa | Dónde puede evidenciarse |", "|---|---|---|---|"]
    for linea in texto.splitlines():
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if not (c and RE_ID.fullmatch(c[0])):
            continue
        for seg in (s.strip() for s in c[-1].split("·")):
            e = re.match(r"(E\d+)\s+(.*?)\s*\[(aviso|interno)\]$", seg)
            if e:
                l.append(f"| {c[0]} | {e.group(1)} | {e.group(2)} | {DONDE[e.group(3)]} |")
            elif seg.startswith("Sugerencia"):
                l.append(f"| {c[0]} | — | {seg} (no cuenta para el estado) | Política pública |")
    return "\n".join(l) + "\n"


def resumen_generado(v: dict) -> str:
    """Resumen calculado por la aplicación a partir de la matriz (no lo escribe el modelo)."""
    l = ["## Resumen generado por la aplicación (no por el modelo)", ""]
    if _v(v["version_skill"]) >= _v("0.5"):
        l += ["Clasificación de los controles: metodología del equipo (no una obligación de la norma). "
              "Cobertura: 78 controles del Anexo A, con orientaciones seleccionadas del Anexo B.", "",
              "**1. Información esencial o condicional aplicable que la política no documenta por completo**", ""]
        l += [f"- **{i}** ({e}): {vac}" for i, e, vac in v.get("vacios", [])] or ["- Ninguno"]
        l += ["", "**2. Aplicabilidad por determinar** (límite del documento, no un vacío)", ""]
        l += [f"- **{i}**: {nec}" for i, nec in v.get("por_determinar", [])] or ["- Ninguno"]
        l += ["", "**3. Evidencia interna a solicitar** (no es contenido obligatorio de la política)", ""]
        ids_int = [i for i, _ in v.get("evidencia_interna", [])]
        l += [f"- {', '.join(ids_int)} (qué pedir en cada caso: columna «Información faltante o necesaria» "
              "de la matriz)"] if ids_int else ["- Ninguno"]
    else:
        l += ["Posibles vacíos documentales en controles D / D* activado, según los estados de la matriz:", ""]
        l += [f"- **{i}** ({e}): {vac}" for i, e, vac in v.get("vacios", [])] or ["- Ninguno"]
    l += ["", "| Estado | Filas | IDs |", "|---|---|---|"]
    l += [f"| {e} | {v['conteo_filas'][e]} | {v['conteo_ids'][e]} |" for e in ESTADOS]
    l += ["", "---", ""]
    return "\n".join(l)


def informe_verificacion(v: dict, meta: dict) -> str:
    ok = lambda b: "✅" if b else "❌"  # noqa: E731
    l = ["# Verificación automática — SK-01", "",
         f"Skill evaluada: v{v['version_skill']} · Modelo: {meta['modelo']} · "
         f"Catálogo: v{meta.get('catalogo_version', '?')}", "",
         f"**Resultado:** {etiqueta(v)}", ""]

    # Resumen por categoría
    l += ["## 0. Resumen por categoría", "", "| Categoría | Observaciones exigibles | No exigibles en esta versión |", "|---|---|---|"]
    l.append(f"| Truncamiento | {'1' if v['truncada'] else '0'} | — |")
    for c in CATEGORIAS:
        ex = sum(1 for o in v["observaciones"] if o["categoria"] == c and o["exigible"])
        nx = sum(1 for o in v["observaciones"] if o["categoria"] == c and not o["exigible"])
        l.append(f"| {c} | {ex} | {nx or '—'} |")

    # 1. Truncamiento
    u = meta["uso"]
    l += ["", "## 1. Truncamiento", "",
          f"- {ok(v['finish_reason'] == 'STOP')} Motivo de fin de la API: `{v['finish_reason']}`",
          f"- {ok(v['tiene_bloque_de_cierre'])} Bloque de cierre `{CIERRE}` presente",
          f"- Tokens: entrada {u['entrada']}, salida {u['salida']}, razonamiento {u['razonamiento']}, "
          f"límite de salida {meta['max_output_tokens']}"]

    # 2. Cobertura calculada
    l += ["", "## 2. Cobertura (calculada por el programa con los IDs del catálogo)", "",
          "| Grupo | IDs con fila explícita | Esperados |", "|---|---|---|"]
    for g, (n, t) in v["por_tabla"].items():
        l.append(f"| {g} | {ok(n == t)} {n} | {t} |")
    l.append(f"\nFilas de la matriz: {v['filas']} ({v['filas_individuales']} con un solo ID).")

    # 4. Conteos calculados
    l += ["", "## 3. Conteos calculados por el programa", "",
          "| Estado | Filas | IDs | Declarado por el modelo (filas) |", "|---|---|---|---|"]
    dec = v["declarados"]["por_estado"]
    for e in ESTADOS:
        l.append(f"| {e} | {v['conteo_filas'][e]} | {v['conteo_ids'][e]} | {dec.get(e, '—')} |")
    for k in ("(estado no válido)", "(sin fila explícita)"):
        if v["conteo_ids"][k]:
            l.append(f"| {k} | — | {v['conteo_ids'][k]} | — |")
    l.append(f"| **Total** | {v['filas']} | {sum(v['conteo_ids'].values())} | {v['declarados']['total'] or '—'} |")

    # Observaciones por categoría
    l += ["", "## 4. Observaciones exigibles en esta versión", ""]
    for c in CATEGORIAS:
        obs = [o for o in v["observaciones"] if o["categoria"] == c and o["exigible"]]
        l.append(f"### {c}")
        l += [f"- ❌ {o['detalle']}" for o in obs] or ["- ✅ Sin observaciones"]
        l.append("")

    # Citas
    l += ["## 5. Citas", ""]
    cats = {}
    for c in v["citas"]:
        cats[c["categoria"]] = cats.get(c["categoria"], 0) + 1
    l.append("Por categoría: " + (", ".join(f"{k}: {n}" for k, n in cats.items()) or "sin citas"))
    l += ["", "| IDs | Cita | Pág. indicada | Categoría | Encontrada en |", "|---|---|---|---|---|"]
    for c in v["citas"]:
        marca = "✅" if c["categoria"] == "literal" else "⚠️" if c["categoria"].startswith("literal") else "❌"
        l.append(f"| {', '.join(c['ids'][:3])} | «{c['cita'].replace('|', '/')}» | "
                 f"{c['paginas_indicadas'] or '—'} | {marca} {c['categoria']} | {c['encontrada_en'] or '—'} |")

    # Reglas no exigibles
    nx = [o for o in v["observaciones"] if not o["exigible"]]
    l += ["", f"## 6. Reglas no exigibles en la Skill v{v['version_skill']} (informativo)", ""]
    l += [f"- {o['detalle']} — regla «{o['regla']}» exigible desde v{DESDE[o['regla']]}"
          + (f" y deja de exigirse desde v{HASTA_ANTES_DE[o['regla']]}" if o["regla"] in HASTA_ANTES_DE else "") for o in nx] or ["- Ninguna"]

    l += ["", "## 7. Redacciones aplicadas antes del envío", ""]
    l += [f"- Pág. {r['pagina']}: {r['ocurrencias']} ocurrencia(s) reemplazada(s) por `{documento.MARCA_REDACCION}`"
          for r in meta.get("redacciones", [])] or ["- Ninguna"]
    l += ["", "> Comprobaciones automáticas de forma. La pertinencia de cada estado la revisa el equipo."]
    return "\n".join(l) + "\n"
