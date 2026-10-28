"""Vuelve a verificar una respuesta guardada con el verificador actual, sin llamar a la API.

Uso: python -m motor.reverificar resultados/<carpeta>
- Lee respuesta_original.md (nunca la modifica).
- Usa la versión de la Skill con que se generó la respuesta (metadatos; v0.1 si no consta),
  para separar las reglas que no eran exigibles en esa versión.
- Usa la plantilla solo si la ejecución la envió, y los elementos de la versión correspondiente
  (motor/insumos.py), para no cambiar retrospectivamente sus resultados.
- Conserva la verificación anterior como verificacion_anterior_<hora>.md.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from motor import insumos, reporte  # noqa: E402


def main() -> int:
    carpeta = Path(sys.argv[1])
    meta = json.loads((carpeta / "metadatos.json").read_text(encoding="utf-8"))
    texto = (carpeta / "respuesta_original.md").read_text(encoding="utf-8")
    enviado = (carpeta / "documento_enviado.txt").read_text(encoding="utf-8")
    cuerpo = enviado.split("<<<DOCUMENTO>>>\n", 1)[1].rsplit("\n<<<FIN DEL DOCUMENTO>>>", 1)[0]
    paginas = [p for p in re.split(r"\[Página \d+\]\n", cuerpo) if p.strip()]

    version = meta.get("skill_version", "0.1")
    instr = meta.get("instrucciones", "vigentes")
    dir_instr = (RAIZ / instr) if instr not in ("vigentes", None) and (RAIZ / instr).exists() else None
    v = insumos.verificar(texto, meta["finish_reason"], paginas, meta["catalogo_estado"], version,
                          con_plantilla=bool(meta.get("plantilla")), dir_instrucciones=dir_instr)

    anterior = carpeta / "verificacion.md"
    if anterior.exists():
        anterior.rename(carpeta / f"verificacion_anterior_{datetime.now():%H%M%S}.md")
    (carpeta / "verificacion.md").write_text(reporte.informe_verificacion(v, meta), encoding="utf-8")
    (carpeta / "informe.md").write_text(insumos.informe(v, texto, dir_instr), encoding="utf-8")
    print(f"{carpeta.name}: Skill v{version} — {reporte.etiqueta(v)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
