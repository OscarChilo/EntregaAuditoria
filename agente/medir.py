"""Mide una ejecución del agente contra la clave de la simulación. No llama a Gemini.

Uso: python -m agente.medir resultados_agente/<carpeta> [--clave simulacion/clave/clave_simulacion.md]

La medición es por requisito: un vacío sembrado cuenta como detectado si el resultado de SK-02 para su
requisito es la clasificación esperada o la aceptable. No comprueba que el hallazgo describa el mismo
elemento: eso lo revisa el equipo con medicion.md.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from agente.verificar import celdas  # noqa: E402

RE_ID = re.compile(r"A\.[123]\.\d+(?:\.\d+)?|(?:[4-9]|10)(?:\.\d+)+")


def leer_clave(ruta: Path) -> tuple[list[dict], set[str]]:
    sembrados, aceptables = [], set()
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        c = celdas(linea) if linea.startswith("|") else []
        if c and re.fullmatch(r"S-\d+", c[0]):
            sembrados.append({"id": c[0], "doc": c[1], "req": c[2], "elemento": c[3], "esperado": c[4],
                              "aceptable": c[5] if c[5] != "—" else ""})
        elif c and re.fullmatch(r"A-\d+", c[0]):
            aceptables |= set(RE_ID.findall(c[2]))
    return sembrados, aceptables


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--clave", default=str(RAIZ / "simulacion" / "clave" / "clave_simulacion.md"))
    a = ap.parse_args()
    carpeta = Path(a.carpeta)
    with (carpeta / "lista_verificacion.csv").open(encoding="utf-8-sig") as f:
        res = {row["Código de requisito"]: row for row in csv.DictReader(f)}
    sembrados, aceptables = leer_clave(Path(a.clave))

    l = ["# Medición contra la clave de la simulación", "", f"Ejecución: `{carpeta.name}`", "",
         "> Sesgo declarado: la misma IA redactó los documentos, la clave y las skills. Medición por requisito.", "",
         "## 1. Vacíos sembrados", "", "| Clave | Requisito | Esperado | Resultado del agente | Detectado | Clasificación exacta | Alerta del verificador | Evidencia encontrada (agente) |",
         "|---|---|---|---|---|---|---|---|"]
    det = exacta = alertados = 0
    for s in sembrados:
        r = res.get(s["req"], {})
        obt = r.get("Resultado propuesto", "(sin fila)")
        ok = obt in (s["esperado"], s["aceptable"])
        det += ok
        exacta += obt == s["esperado"]
        alerta = r.get("Alerta del verificador", "—")
        alertados += (not ok) and alerta not in ("—", "")
        l.append(f"| {s['id']} | {s['req']} | {s['esperado']}{' (o ' + s['aceptable'] + ')' if s['aceptable'] else ''} "
                 f"| {obt} | {'sí' if ok else 'no'} | {'sí' if obt == s['esperado'] else 'no'} | {alerta} "
                 f"| {(r.get('Evidencia encontrada') or '')[:160]} |")
    reqs_sembrados = {s["req"] for s in sembrados}
    posibles_fp = [(i, r["Resultado propuesto"], r["Evidencia encontrada"]) for i, r in res.items()
                   if r["Resultado propuesto"] in ("N", "O") and i not in reqs_sembrados and i not in aceptables]
    l += ["", f"**Detectados:** {det} de {len(sembrados)} · **Clasificación exacta:** {exacta} de {len(sembrados)} · "
          f"**No detectados pero con alerta para el revisor:** {alertados} de {len(sembrados) - det}", "",
          "## 2. Posibles falsos positivos (N u O fuera de los vacíos sembrados y aceptables)", "",
          "Hay que revisarlos a mano: algunos pueden ser hallazgos reales que la clave no previó.", ""]
    l += [f"- **{i}** ({c}): {e[:200]}" for i, c, e in posibles_fp] or ["- Ninguno"]
    cont = {}
    for r in res.values():
        cont[r["Resultado propuesto"]] = cont.get(r["Resultado propuesto"], 0) + 1
    l += ["", "## 3. Distribución de resultados", "", ", ".join(f"{k}: {v}" for k, v in cont.items()), ""]
    (carpeta / "medicion.md").write_text("\n".join(l), encoding="utf-8")
    print(f"Detectados {det}/{len(sembrados)} · exactos {exacta}/{len(sembrados)} · no detectados con alerta "
          f"{alertados}/{len(sembrados) - det} · posibles falsos positivos "
          f"{len(posibles_fp)} — {carpeta / 'medicion.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
