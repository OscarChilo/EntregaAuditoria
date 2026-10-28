"""Ejecuta SK-01 sobre un PDF, sin interfaz: una sola llamada a Gemini y verificaciones.

Uso (desde la raíz del proyecto):
  python -m motor.evaluar "<archivo .pdf|.txt|.md>" [--nombre "..."] [--fuente "..."]
      [--modelo desarrollo|final|<id>] [--redactar "texto"]... [--etiqueta pruebaN]

Guarda en resultados/<etiqueta>_<fecha>_<documento>_<modelo>/:
  respuesta_original.md      respuesta del modelo, sin ningún cambio
  informe.md                 la misma respuesta con un aviso inicial de verificación y la leyenda de elementos
  verificacion.md            comprobaciones automáticas por categoría
  instrucciones_enviadas.md  system_instruction enviada
  documento_enviado.txt      bloque del documento (con marcas de página y redacciones)
  plantilla_enviada.md       plantilla de la matriz enviada
  metadatos.json             modelo, tokens, versiones, redacciones (sin la clave)
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from conexion.config import MODELOS, MODELO_ACTIVO  # noqa: E402
from conexion.gemini import generar  # noqa: E402
from motor import documento, insumos, plantilla, reporte, skill, verificacion  # noqa: E402


def _slug(texto: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")[:40]


def evaluar(archivo: str, nombre: str | None = None, fuente: str = "no indicada", modelo: str | None = None,
            redactar: list[str] | tuple = (), etiqueta: str = "", dir_instr: Path | None = None,
            aviso=print) -> dict:
    """Evalúa un documento con SK-01 (una llamada a Gemini) y guarda los resultados.
    Devuelve {"ok", "mensaje", "carpeta"}; la usan el comando y la interfaz."""
    if dir_instr and not (dir_instr / "SKILL.md").is_file():
        return {"ok": False, "mensaje": f"No hay SKILL.md en {dir_instr}", "carpeta": None}
    modelo = MODELOS.get(modelo, modelo) if modelo else MODELO_ACTIVO
    if not Path(archivo).is_file():
        return {"ok": False, "mensaje": f"No existe el archivo: {archivo}", "carpeta": None}
    nombre = nombre or Path(archivo).stem
    redactar = [x for x in redactar if x]
    try:
        paginas, redacciones = documento.redactar(documento.extraer_paginas(archivo), redactar)
    except ValueError as e:
        return {"ok": False, "mensaje": f"No se puede leer el documento: {e}", "carpeta": None}
    if redactar and not redacciones:
        return {"ok": False, "mensaje": "Ningún texto a redactar se encontró en el documento; se detiene sin enviar.",
                "carpeta": None}

    version_cat, estado_cat = skill.estado_catalogo()
    version_sk = skill.version_skill(dir_instr)
    instrucciones = skill.instrucciones_del_sistema(dir_instr)
    conocimiento = skill.conocimiento_iso()
    bloque_plantilla = plantilla.bloque_plantilla(skill.ARCHIVO_CATALOGO, version_sk)
    con_lista = verificacion.exigible("lista_titular", version_sk)
    bloque_lista = plantilla.bloque_lista_titular(skill.ARCHIVO_CATALOGO) if con_lista else None
    mensaje = skill.bloque_documento(nombre, fuente, len(paginas), documento.con_marcas(paginas), estado_cat)

    partes = [conocimiento, bloque_plantilla] + ([bloque_lista] if bloque_lista else []) + [mensaje]
    aviso(f"Enviando {nombre} ({len(paginas)} págs.) a {modelo}, Skill v{version_sk} — una sola llamada ...")
    r = generar(instrucciones, partes, modelo)
    if "error" in r:
        return {"ok": False, "mensaje": f"Error de la API: {r['error']}", "carpeta": None}

    v = insumos.verificar(r["texto"], r["finish_reason"], paginas, estado_cat, version_sk,
                          con_plantilla=True, dir_instrucciones=dir_instr)

    prefijo = f"{etiqueta}_" if etiqueta else ""
    carpeta = RAIZ / "resultados" / f"{prefijo}{datetime.now():%Y%m%d-%H%M%S}_{_slug(nombre)}_{modelo}"
    carpeta.mkdir(parents=True)
    escribir = lambda n, t: (carpeta / n).write_text(t, encoding="utf-8")  # noqa: E731
    escribir("respuesta_original.md", r["texto"])
    escribir("informe.md", insumos.informe(v, r["texto"], dir_instr))
    escribir("instrucciones_enviadas.md", instrucciones)
    escribir("documento_enviado.txt", mensaje)
    escribir("plantilla_enviada.md", bloque_plantilla)
    if bloque_lista:
        escribir("lista_titular_enviada.md", bloque_lista)
    meta = {k: r[k] for k in ("modelo", "finish_reason", "max_output_tokens", "uso", "intentos_fallidos")}
    meta.update({"documento": nombre, "archivo": Path(archivo).name, "fuente": fuente,
                 "etiqueta": etiqueta, "skill_version": version_sk,
                 "instrucciones": str(dir_instr) if dir_instr else "vigentes",
                 "conocimiento": "catálogo completo (contexto completo, sin RAG)",
                 "plantilla": True, "lista_titular": bool(bloque_lista), "paginas": len(paginas), "catalogo_version": version_cat,
                 "catalogo_estado": estado_cat, "redacciones": redacciones,
                 "fecha": datetime.now().isoformat(timespec="seconds")})
    escribir("metadatos.json", json.dumps(meta, ensure_ascii=False, indent=2))
    escribir("verificacion.md", reporte.informe_verificacion(v, meta))
    return {"ok": True, "mensaje": f"Resultado: {reporte.etiqueta(v)} — carpeta: {carpeta.relative_to(RAIZ)}",
            "carpeta": carpeta}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo", help="documento a evaluar: .pdf, .txt o .md")
    ap.add_argument("--nombre", default=None, help="nombre del documento (por defecto, el del archivo)")
    ap.add_argument("--fuente", default="no indicada")
    ap.add_argument("--modelo", default=None, help="desarrollo, final o un identificador")
    ap.add_argument("--redactar", action="append", default=[], help="texto a ocultar antes del envío")
    ap.add_argument("--etiqueta", default="", help="prefijo de la carpeta de resultados (p. ej., prueba3)")
    ap.add_argument("--instrucciones", default=None,
                    help="carpeta de una versión archivada de las instrucciones (para comparar versiones)")
    a = ap.parse_args()
    r = evaluar(a.archivo, a.nombre, a.fuente, a.modelo, a.redactar, a.etiqueta,
                Path(a.instrucciones) if a.instrucciones else None)
    print(r["mensaje"])
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
