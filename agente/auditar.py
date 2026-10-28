"""Agente de evidencias y auditoría del PIMS: orquesta SK-02, SK-03 y SK-04 sobre un conjunto de evidencias.

Uso (desde la raíz del proyecto):
  python -m agente.auditar <plan.json> <carpeta de evidencias> [--etiqueta ...] [--modelo ...] [--seco]

  --seco   arma y guarda todo lo que se enviaría, sin llamar a Gemini.

Guarda en resultados_agente/<etiqueta>_<fecha>_<código>/:
  lista_verificacion.md/.csv, hallazgos.md/.csv, plan_accion.md/.csv, informe_auditoria.md,
  verificacion.md, metadatos.json y llamadas/ (lo enviado y la respuesta original de cada llamada).
La clave de la simulación (simulacion/clave/) nunca se lee aquí.
"""

import argparse
import json
import sys
import time
from datetime import date, datetime
from pathlib import Path
from types import SimpleNamespace

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from agente import evidencias, requisitos, salidas, verificar  # noqa: E402
from conexion.config import MODELOS, MODELO_ACTIVO  # noqa: E402

DIR_SKILL = RAIZ / "skill"
ARCH_AGENTE = RAIZ / "agente" / "agente_auditoria_pims.md"
PAUSA = 4  # segundos entre llamadas (límite de 15 solicitudes por minuto)
AGENTE_VERSION = "0.2"  # 0.2: Anexo A completo (78 controles, con A.2 y A.3 parafraseados) y 9 lotes


def _leer(*rutas: Path) -> str:
    return "\n\n".join(f"===== ARCHIVO: {r.relative_to(RAIZ).as_posix()} =====\n{r.read_text(encoding='utf-8')}"
                       for r in rutas)


def instrucciones(skill: str) -> str:
    d = DIR_SKILL / skill
    return "Eres el Agente de Evidencias y Auditoría del PIMS.\n\n" + _leer(
        ARCH_AGENTE, *[d / n for n in ("SKILL.md", "criterios.md", "formato_resultado.md") if (d / n).exists()])


def contexto(plan: dict) -> str:
    return ("<<<CONTEXTO DE LA AUDITORÍA>>>\n"
            f"Organización: {plan['organizacion']}\nAuditoría: {plan['codigo']} — {plan['nombre']}\n"
            f"Objetivo: {plan['objetivo']}\nAlcance: {plan['alcance']}\nCriterios: {plan['criterios']}\n"
            "<<<FIN DEL CONTEXTO>>>")


def _elementos(r: dict) -> str:
    return " · ".join(f"{e['codigo']} {'[recomendación] ' if e['recomendacion'] else ''}{e['texto']}"
                      for e in r["elementos"])


def mensaje_sk02(plan: dict, nombre: str, lote: list[dict], bloque_docs: str) -> list[str]:
    tabla = ["<<<REQUISITOS DEL LOTE>>>", f"Lote: {nombre}", "",
             "| ID | Requisito | Elementos a evaluar | Información documentada exigida |", "|---|---|---|---|"]
    tabla += [f"| {r['id']} | {r['requisito']} | {_elementos(r)} | {r['id_r']} |" for r in lote]
    tabla.append("<<<FIN DE LOS REQUISITOS>>>")
    filas = ["<<<PLANTILLA DE FILAS (cópiala y completa las columnas vacías)>>>",
             "| ID | Requisito | Elementos | Resultado | Evidencia encontrada | Hallazgo propuesto |",
             "|---|---|---|---|---|---|"] + [
        f"| {r['id']} | {r['requisito']} | {' · '.join(e['codigo'] + ' ?' for e in r['elementos'])} |  |  |  |"
        for r in lote]
    filas.append("<<<FIN DE LA PLANTILLA>>>")
    return [contexto(plan), "\n".join(tabla), "\n".join(filas),
            f"Aplica SK-02 al lote «{nombre}» con las evidencias siguientes.\n\n{bloque_docs}"]


def mensaje_sk03(plan: dict, fecha_base: date, nmo: list[dict], bloque_docs: str) -> list[str]:
    t = ["<<<RESULTADOS N, O y M DE SK-02>>>", "| ID | Requisito | Resultado | Elementos | Hallazgo propuesto |",
         "|---|---|---|---|---|"]
    t += [f"| {r['id']} | {r['requisito']} | {r['resultado']} | {r['elementos_texto']} | {r['hallazgo']} |" for r in nmo]
    t.append("<<<FIN DE LOS RESULTADOS>>>")
    return [contexto(plan), f"Fecha base para las fechas compromiso: {fecha_base.isoformat()}", "\n".join(t),
            f"Aplica SK-03. Toma los roles responsables de estos documentos:\n\n{bloque_docs}"]


def mensaje_sk04(plan: dict, resultados: list[dict], hallazgos: list[dict]) -> list[str]:
    c = salidas.conteos(resultados)
    h = ["| N.° | Clasificación | Requisitos | Descripción |", "|---|---|---|---|"]
    h += [f"| {x['id']} | {x['clasificacion']} | {x['requisitos']} | {x['descripcion']} |" for x in hallazgos]
    sin = [r["id"] for r in resultados if r["resultado"] == "Sin evidencia"]
    return [contexto(plan),
            "Conteos calculados por el programa: " + ", ".join(f"{k}: {v}" for k, v in c.items())
            + f"; requisitos verificados: {len(resultados)}.",
            "Hallazgos:\n" + "\n".join(h),
            "Requisitos sin evidencia: " + (", ".join(sin) or "ninguno"),
            "Aplica SK-04 y redacta el resumen ejecutivo, las conclusiones y las limitaciones. "
            "En esta auditoría solo hubo revisión documental: no hubo entrevistas ni muestreo en campo."]


def auditar(plan: dict, carpeta_evidencias, etiqueta: str = "", modelo: str | None = None, seco: bool = False,
            reprocesar=None, aviso=print) -> dict:
    """Ejecuta la auditoría completa. Devuelve {"ok", "mensaje", "carpeta"}; la usan el comando y la interfaz."""
    a = SimpleNamespace(etiqueta=etiqueta, modelo=modelo, seco=seco, reprocesar=reprocesar)
    docs = evidencias.cargar(Path(carpeta_evidencias))
    textos = {d["codigo"]: verificar.norm(d["texto"]) for d in docs}
    bloque_docs = evidencias.bloque(docs)
    meta_previa = None
    if a.reprocesar:
        meta_previa = json.loads((Path(a.reprocesar) / "metadatos.json").read_text(encoding="utf-8"))
    # Las ejecuciones anteriores a la v0.2 del agente se reprocesan con su alcance y lotes originales
    # (Anexo A parcial, A.3 solo con título), para no cambiar retrospectivamente sus resultados.
    legado = meta_previa is not None and "agente_version" not in meta_previa
    anexo_a = (meta_previa or {}).get("plan", plan).get("anexo_a", "completo") if legado else plan.get("anexo_a", "completo")
    reqs = requisitos.alcance([d["texto"] for d in docs], anexo_a, con_a2a3=not legado)
    lotes = requisitos.lotes(reqs, requisitos.GRUPOS_V01 if legado else None)
    modelo = MODELOS.get(a.modelo, a.modelo) if a.modelo else MODELO_ACTIVO
    fecha_base = date.fromisoformat(plan["fin"])

    previas = {}
    if a.reprocesar:
        carpeta = Path(a.reprocesar).resolve()
        meta = meta_previa
        previas = {l["n"]: l for l in meta["llamadas"]}
        meta["reprocesado"] = datetime.now().isoformat(timespec="seconds")
    else:
        prefijo = f"{a.etiqueta}_" if a.etiqueta else ""
        carpeta = RAIZ / "resultados_agente" / f"{prefijo}{datetime.now():%Y%m%d-%H%M%S}_{plan['codigo']}"
        (carpeta / "llamadas").mkdir(parents=True)
        meta = {"plan": plan, "modelo": modelo, "documentos": [{k: d[k] for k in ("codigo", "titulo", "archivo")} for d in docs],
                "requisitos": len(reqs), "lotes": [[n, [r["id"] for r in g]] for n, g in lotes], "llamadas": [],
                "seco": a.seco, "fecha": datetime.now().isoformat(timespec="seconds"),
                "agente_version": AGENTE_VERSION, "anexo_a": anexo_a,
                "versiones": {s: requisitos.re.search(r"^version:\s*(\S+)", (DIR_SKILL / s / "SKILL.md").read_text(
                    encoding="utf-8"), requisitos.re.M).group(1) for s in ("sk02", "sk03", "sk04")}}
    n_llamada = 0

    def llamar(skill: str, nombre: str, partes: list[str]) -> dict | None:
        nonlocal n_llamada
        n_llamada += 1
        base = f"{n_llamada:02d}_{skill.lower().replace('-', '')}_{requisitos.re.sub(r'[^a-z0-9]+', '-', nombre.lower()).strip('-')}"
        if a.reprocesar:
            guardada = carpeta / "llamadas" / f"{base}_respuesta.md"
            if not guardada.exists():
                return {"error": f"no hay respuesta guardada {guardada.name}"}
            return {"texto": guardada.read_text(encoding="utf-8"),
                    "finish_reason": previas.get(n_llamada, {}).get("finish_reason")}
        instr = instrucciones(skill.lower().replace("-", ""))
        (carpeta / "llamadas" / f"{base}_enviado.md").write_text(
            f"# Instrucciones\n\n{instr}\n\n# Mensaje\n\n" + "\n\n".join(partes), encoding="utf-8")
        tam = len(instr) + sum(len(p) for p in partes)
        aviso(f"[{n_llamada}] {skill} · {nombre} · ~{tam // 4} tokens de entrada (estimado)")
        if a.seco:
            meta["llamadas"].append({"n": n_llamada, "skill": skill, "lote": nombre, "caracteres": tam})
            return None
        from conexion.gemini import generar
        if n_llamada > 1:
            time.sleep(PAUSA)
        r = generar(instr, partes, modelo)
        meta["llamadas"].append({"n": n_llamada, "skill": skill, "lote": nombre,
                                 **{k: r.get(k) for k in ("finish_reason", "uso", "intentos_fallidos", "error")}})
        if "error" in r:
            aviso(f"    Error de la API: {r['error']}")
            return r
        (carpeta / "llamadas" / f"{base}_respuesta.md").write_text(r["texto"], encoding="utf-8")
        return r

    def guardar_meta():
        (carpeta / "metadatos.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    # 1. SK-02 por lote
    resultados, observaciones, citas = [], [], []
    for nombre, lote in lotes:
        r = llamar("SK-02", nombre, mensaje_sk02(plan, nombre, lote, bloque_docs))
        if r is None:
            continue
        if "error" in r:
            guardar_meta()
            return {"ok": False, "mensaje": f"Error: {r['error']}", "carpeta": carpeta}
        v = verificar.sk02(r["texto"], r["finish_reason"], lote, textos, f"SK-02 · {nombre}")
        resultados += v["resultados"]
        observaciones += v["observaciones"]
        citas += v["citas"]
    if a.seco:
        llamar("SK-03", "hallazgos", mensaje_sk03(plan, fecha_base, [], bloque_docs))
        llamar("SK-04", "conclusiones", mensaje_sk04(plan, [], []))
        guardar_meta()
        return {"ok": True, "mensaje": f"Ensayo en seco: {n_llamada} llamadas preparadas en {carpeta.relative_to(RAIZ)}", "carpeta": carpeta}
    salidas.lista_verificacion(carpeta, plan, resultados)

    # 2. SK-03 con los resultados N, O y M
    nmo = [x for x in resultados if x["resultado"] in ("N", "O", "M")]
    hallazgos, planes = [], {}
    if nmo:
        r = llamar("SK-03", "hallazgos", mensaje_sk03(plan, fecha_base, nmo, bloque_docs))
        if "error" in r:
            guardar_meta()
            return {"ok": False, "mensaje": f"Error: {r['error']}", "carpeta": carpeta}
        v = verificar.sk03(r["texto"], r["finish_reason"], nmo, textos, fecha_base, "SK-03")
        hallazgos, planes = v["hallazgos"], v["planes"]
        observaciones += v["observaciones"]
    salidas.hallazgos_y_planes(carpeta, plan, hallazgos, planes)

    # 3. SK-04: conclusiones
    r = llamar("SK-04", "conclusiones", mensaje_sk04(plan, resultados, hallazgos))
    if "error" in r:
        guardar_meta()
        return {"ok": False, "mensaje": f"Error: {r['error']}", "carpeta": carpeta}
    v = verificar.sk04(r["texto"], r["finish_reason"], {h["id"] for h in hallazgos}, "SK-04")
    observaciones += v["observaciones"]

    salidas.informe(carpeta, plan, resultados, hallazgos, planes, v["texto"], len(observaciones))
    salidas.verificacion(carpeta, observaciones, citas)
    meta["conteos"] = salidas.conteos(resultados)
    meta["hallazgos"] = {k: sum(1 for h in hallazgos if h["clasificacion"] == k) for k in "NOM"}
    meta["observaciones"] = len(observaciones)
    guardar_meta()
    return {"ok": True, "carpeta": carpeta,
            "mensaje": f"Listo: {len(resultados)} requisitos · {meta['conteos']} · hallazgos {meta['hallazgos']} · "
                       f"{len(observaciones)} observaciones — {carpeta.relative_to(RAIZ)}"}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("evidencias")
    ap.add_argument("--etiqueta", default="")
    ap.add_argument("--modelo", default=None, help="desarrollo, final o un identificador")
    ap.add_argument("--seco", action="store_true", help="no llama a Gemini")
    ap.add_argument("--reprocesar", default=None,
                    help="carpeta de una ejecución: vuelve a verificar y armar las salidas con sus respuestas "
                         "guardadas, sin llamar a Gemini (las respuestas originales no se modifican)")
    a = ap.parse_args()
    r = auditar(json.loads(Path(a.plan).read_text(encoding="utf-8")), a.evidencias, a.etiqueta, a.modelo,
                a.seco, a.reprocesar)
    print(r["mensaje"])
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
