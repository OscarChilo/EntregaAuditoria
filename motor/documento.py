"""Extracción del texto del documento evaluado, con marcas de página y redacción opcional.

Formatos admitidos:
  .pdf          una página por página del PDF (debe tener capa de texto; no se hace OCR)
  .txt / .md    el texto completo; si contiene saltos de página (\\f), cada uno inicia una página
"""

from pathlib import Path

import pymupdf

MARCA_REDACCION = "[REDACTADO]"
FORMATOS = (".pdf", ".txt", ".md")


def extraer_paginas(ruta: str) -> list[str]:
    extension = Path(ruta).suffix.lower()
    if extension == ".pdf":
        with pymupdf.open(ruta) as doc:
            paginas = [pagina.get_text() for pagina in doc]
    elif extension in (".txt", ".md"):
        paginas = Path(ruta).read_text(encoding="utf-8").split("\f")
    else:
        raise ValueError(f"Formato no admitido: {extension}. Use {', '.join(FORMATOS)}.")
    if not any(p.strip() for p in paginas):
        raise ValueError("El documento no tiene texto extraíble (¿PDF escaneado sin capa de texto?).")
    return paginas


def redactar(paginas: list[str], textos: list[str]) -> tuple[list[str], list[dict]]:
    """Reemplaza cada texto indicado por MARCA_REDACCION. Devuelve páginas y registro."""
    registro = []
    resultado = []
    for n, texto_pagina in enumerate(paginas, start=1):
        for t in textos:
            veces = texto_pagina.count(t)
            if veces:
                texto_pagina = texto_pagina.replace(t, MARCA_REDACCION)
                registro.append({"pagina": n, "ocurrencias": veces, "longitud": len(t)})
        resultado.append(texto_pagina)
    return resultado, registro


def con_marcas(paginas: list[str]) -> str:
    return "\n".join(f"[Página {n}]\n{texto.strip()}\n" for n, texto in enumerate(paginas, start=1))
