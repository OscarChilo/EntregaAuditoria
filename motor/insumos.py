"""Insumos de verificación según la versión de la Skill con que se generó una respuesta.

Permite volver a verificar ejecuciones antiguas con los mismos elementos y reglas que tenían,
sin cambiar sus resultados, y verificar las nuevas con todo lo vigente.
"""

from pathlib import Path

from motor import plantilla, reporte, skill, verificacion


def ruta_elementos(version: str, dir_instrucciones: Path | None = None) -> Path:
    if dir_instrucciones is not None and (dir_instrucciones / "elementos.md").exists():
        return dir_instrucciones / "elementos.md"
    archivada = skill.DIR_SKILL / "historial" / f"skill_v{version}" / "elementos.md"
    if version != skill.version_skill() and archivada.exists():
        return archivada                                                        # p. ej., v0.5 → elementos v0.2
    if verificacion._v(version) < verificacion._v("0.5"):
        return skill.DIR_SKILL / "historial" / "skill_v0.4" / "elementos.md"   # elementos v0.1 (Skill v0.4)
    return skill.DIR_SKILL / "elementos.md"


def verificar(texto: str, finish_reason: str | None, paginas: list[str], estado_cat: str,
              version: str, con_plantilla: bool, dir_instrucciones: Path | None = None) -> dict:
    exig = lambda regla: verificacion.exigible(regla, version)  # noqa: E731
    ruta_el = ruta_elementos(version, dir_instrucciones)
    return verificacion.verificar(
        texto, finish_reason, paginas,
        verificacion.catalogo_detallado(skill.ARCHIVO_CATALOGO), estado_cat, version,
        plantilla.ids_plantilla(skill.ARCHIVO_CATALOGO) if con_plantilla else None,
        verificacion.elementos_por_control(ruta_el) if exig("elementos") else None,
        verificacion.dependencias_por_control(ruta_el) if exig("dependencias") else None,
        verificacion.lista_titular(skill.ARCHIVO_CATALOGO) if exig("lista_titular") else None,
    )


def informe(v: dict, texto: str, dir_instrucciones: Path | None = None) -> str:
    """informe.md con la leyenda de los elementos de la misma versión con que se verificó
    (sin leyenda en las versiones anteriores a los elementos)."""
    version = v["version_skill"]
    ruta = ruta_elementos(version, dir_instrucciones) if verificacion.exigible("elementos", version) else None
    return reporte.informe(v, texto, ruta if ruta and ruta.exists() else None)
