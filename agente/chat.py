"""Chat sobre una ejecución guardada (del agente de auditoría o de SK-01). Una llamada a Gemini por pregunta.

El contexto es completo (resultados + documentos de esa ejecución), no RAG: los tamaños actuales
caben en una llamada (≈ 20–30 mil tokens).
"""

import csv
import re
from pathlib import Path

from agente import evidencias, verificar

RAIZ = Path(__file__).resolve().parent.parent
ARCH_INSTRUCCIONES = Path(__file__).resolve().parent / "chat_instrucciones.md"


def _csv_compacto(ruta: Path, columnas: list[str]) -> str:
    with ruta.open(encoding="utf-8-sig") as f:
        filas = list(csv.DictReader(f))
    l = ["| " + " | ".join(columnas) + " |", "|" + "---|" * len(columnas)]
    l += ["| " + " | ".join((r.get(c) or "").replace("|", "/") for c in columnas) + " |" for r in filas]
    return "\n".join(l)


def contexto(carpeta: Path, carpeta_evidencias: Path | None = None) -> tuple[str, dict[str, str]]:
    """Texto de contexto y {código: texto normalizado} de los documentos, para verificar citas."""
    partes, docs = [], {}
    if (carpeta / "lista_verificacion.csv").exists():  # ejecución del agente
        partes.append("<<<RESULTADOS DE LA AUDITORÍA (propuestos por el agente)>>>\n"
                      + _csv_compacto(carpeta / "lista_verificacion.csv",
                                      ["Código de requisito", "Requisito", "Resultado propuesto", "Alerta del verificador",
                                       "Evidencia encontrada", "Elementos (detalle)"]))
        for nombre in ("hallazgos.csv", "plan_accion.csv", "revision_equipo.csv"):
            if (carpeta / nombre).exists():
                with (carpeta / nombre).open(encoding="utf-8-sig") as f:
                    cab = next(csv.reader(f), [])
                partes.append(f"<<<{nombre}>>>\n" + _csv_compacto(carpeta / nombre, cab))
        if carpeta_evidencias and carpeta_evidencias.exists():
            lista = evidencias.cargar(carpeta_evidencias)
            partes.append(evidencias.bloque(lista))
            docs = {d["codigo"]: verificar.norm(d["texto"]) for d in lista}
    else:  # ejecución de SK-01
        partes.append("<<<INFORME DE SK-01 (respuesta del modelo con aviso de verificación)>>>\n"
                      + (carpeta / "informe.md").read_text(encoding="utf-8"))
        enviado = (carpeta / "documento_enviado.txt").read_text(encoding="utf-8")
        partes.append(enviado)
        docs = {"DOCUMENTO": verificar.norm(enviado)}
    return "\n\n".join(partes), docs


def responder(pregunta: str, carpeta: Path, historial: list[dict], modelo: str,
              carpeta_evidencias: Path | None = None) -> dict:
    from conexion.gemini import generar
    ctx, docs = contexto(carpeta, carpeta_evidencias)
    previas = "\n".join(f"{m['rol']}: {m['texto']}" for m in historial[-6:])
    partes = [ctx, f"Conversación previa (resumen):\n{previas or '—'}", f"Pregunta del usuario: {pregunta}"]
    r = generar(ARCH_INSTRUCCIONES.read_text(encoding="utf-8"), partes, modelo)
    if "error" in r:
        return {"texto": f"Error de la API: {r['error']}", "avisos": [], "uso": None}
    avisos = []
    for m in re.finditer(r"[\"“«]([^\"”»]{12,}?)[\"”»]\s*\[([A-Za-z0-9._-]+)?", r["texto"]):
        cat = verificar.clasificar_cita(m.group(1), m.group(2), docs) if docs else "sin documentos para comparar"
        if cat != "literal":
            avisos.append(f"Cita {cat}: «{m.group(1)[:90]}»")
    return {"texto": r["texto"], "avisos": avisos, "uso": r.get("uso")}
