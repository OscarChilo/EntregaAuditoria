"""Archivos de salida del agente, en los formatos de plantillas/ (campos de GESTITEL)."""

import csv
from pathlib import Path

from agente.verificar import RESULTADOS

NORMA = "ISO/IEC 27701:2025"


def _csv(ruta: Path, cabecera: list[str], filas: list[list]) -> None:
    with ruta.open("w", encoding="utf-8-sig", newline="") as f:  # utf-8-sig: Excel lee bien las tildes
        w = csv.writer(f)
        w.writerow(cabecera)
        w.writerows(filas)


def _tabla(cabecera: list[str], filas: list[list]) -> str:
    l = ["| " + " | ".join(cabecera) + " |", "|" + "---|" * len(cabecera)]
    l += ["| " + " | ".join(str(x).replace("|", "/") for x in f) + " |" for f in filas]
    return "\n".join(l)


def conteos(resultados: list[dict]) -> dict[str, int]:
    return {r: sum(1 for x in resultados if x["resultado"] == r) for r in RESULTADOS}


def lista_verificacion(carpeta: Path, plan: dict, resultados: list[dict]) -> None:
    cab = ["N.°", "Código de requisito", "Proceso", "Norma", "Requisito", "Evidencia encontrada",
           "Resultado propuesto", "Alerta del verificador", "Elementos (detalle)"]
    filas = [[n, r["id"], r["proceso"], NORMA, r["requisito"], r["evidencia"], r["resultado"],
              " / ".join(r.get("alertas", [])) or "—", r["elementos_texto"]]
             for n, r in enumerate(resultados, start=1)]
    _csv(carpeta / "lista_verificacion.csv", cab, filas)
    (carpeta / "lista_verificacion.md").write_text(
        f"# Lista de verificación — {plan['codigo']}\n\n> Propuesta del agente: el equipo auditor revisa cada "
        "resultado antes de cargarlo en GESTITEL (columnas 1 a 6).\n\n" + _tabla(cab, filas) + "\n", encoding="utf-8")


def hallazgos_y_planes(carpeta: Path, plan: dict, hallazgos: list[dict], planes: dict) -> None:
    cab_h = ["N.°", "Clasificación", "Requisitos", "Descripción", "Evidencia", "Revisión del auditor"]
    fh = [[h["id"], h["clasificacion"], h["requisitos"], h["descripcion"], h["evidencia"], ""] for h in hallazgos]
    cab_p = ["Hallazgo", "Corrección inmediata", "Acción correctiva", "Responsable", "Fecha compromiso",
             "Verificación de eficacia", "Estado", "Avance"]
    fp = [[p["id"], p["correccion"], p["accion"], p["responsable"], p["fecha"], p["eficacia"], p["estado"], p["avance"]]
          for p in planes.values()]
    _csv(carpeta / "hallazgos.csv", cab_h, fh)
    _csv(carpeta / "plan_accion.csv", cab_p, fp)
    aviso = "> Propuesta del agente: clasificación, responsables y fechas los confirma el equipo auditor.\n\n"
    (carpeta / "hallazgos.md").write_text(f"# Hallazgos — {plan['codigo']}\n\n{aviso}{_tabla(cab_h, fh)}\n", encoding="utf-8")
    (carpeta / "plan_accion.md").write_text(f"# Planes de acción — {plan['codigo']}\n\n{aviso}{_tabla(cab_p, fp)}\n",
                                            encoding="utf-8")


def informe(carpeta: Path, plan: dict, resultados: list[dict], hallazgos: list[dict], planes: dict,
            conclusiones: str, n_obs: int) -> None:
    c = conteos(resultados)
    cl = {k: sum(1 for h in hallazgos if h["clasificacion"] == k) for k in "NOM"}
    l = [f"# Informe de auditoría interna del PIMS — {plan['codigo']}", "",
         "> **Borrador generado por el agente de evidencias y auditoría.** Debe revisarlo y aprobarlo el auditor "
         f"líder. Verificación automática: {n_obs} observaciones (ver `verificacion.md`).", "",
         "| | |", "|---|---|",
         f"| Auditoría | {plan['codigo']} — {plan['nombre']} |", f"| Tipo | {'Interna' if plan['tipo'] == 'I' else 'Externa'} |",
         f"| Fechas | {plan['inicio']} a {plan['fin']} |", f"| Auditor líder | {plan['auditor_lider']} |",
         f"| Equipo auditor | {plan['equipo']} |", f"| Destinatarios | {plan['destinatarios']} |", "",
         "## 1. Objetivo, alcance y criterios", "", f"- **Objetivo:** {plan['objetivo']}",
         f"- **Alcance:** {plan['alcance']}", f"- **Criterios:** {plan['criterios']}", "",
         "## 2. Metodología", "",
         "Revisión documental de las evidencias entregadas, con apoyo del agente de IA (skills SK-02 a SK-04, "
         "modelo de Gemini). El agente propuso los resultados; el equipo auditor los revisa.", "",
         "## 3. Resumen de resultados", "", "| Resultado | Cantidad |", "|---|---|",
         f"| Requisitos verificados | {len(resultados)} |", f"| Conformes | {c['Conforme']} |",
         f"| Ítems con resultado N / O / M | {c['N']} / {c['O']} / {c['M']} |",
         f"| Sin evidencia suficiente | {c['Sin evidencia']} |",
         f"| Hallazgos redactados N / O / M | {cl['N']} / {cl['O']} / {cl['M']} |", "",
         "## 4. Hallazgos", "",
         _tabla(["N.°", "Clasificación", "Requisitos", "Descripción", "Evidencia"],
                [[h["id"], h["clasificacion"], h["requisitos"], h["descripcion"], h["evidencia"]] for h in hallazgos]), "",
         "## 5. Planes de acción propuestos", "",
         _tabla(["Hallazgo", "Acción correctiva", "Responsable", "Fecha compromiso", "Verificación de eficacia"],
                [[p["id"], p["accion"], p["responsable"], p["fecha"], p["eficacia"]] for p in planes.values()]), "",
         "## 6. Resumen ejecutivo, conclusiones y limitaciones (redactados por SK-04)", "", conclusiones, "",
         "## 7. Aprobación", "", "| Rol | Nombre | Fecha |", "|---|---|---|", "| Auditor líder | | |", ""]
    (carpeta / "informe_auditoria.md").write_text("\n".join(l), encoding="utf-8")


def verificacion(carpeta: Path, observaciones: list[dict], citas: list[dict]) -> None:
    l = ["# Verificación automática del agente", "",
         "Comprobaciones de forma: no confirman que los resultados sean correctos.", "",
         f"**Observaciones:** {len(observaciones)}", ""]
    pasos = sorted({o["paso"] for o in observaciones})
    for p in pasos:
        l += [f"## {p}", ""] + [f"- [{o['regla']}] {o['detalle']}" for o in observaciones if o["paso"] == p] + [""]
    cats = {}
    for c in citas:
        cats[c["categoria"]] = cats.get(c["categoria"], 0) + 1
    l += ["## Citas de SK-02", "", ", ".join(f"{k}: {v}" for k, v in cats.items()) or "sin citas", ""]
    (carpeta / "verificacion.md").write_text("\n".join(l), encoding="utf-8")
