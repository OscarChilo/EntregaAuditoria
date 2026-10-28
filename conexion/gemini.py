"""Conexión con la API de Gemini. No contiene lógica de la Skill.

La clave se lee de GEMINI_API_KEY y nunca se imprime ni se guarda.
"""

import time

from google import genai
from google.genai import errors, types

ESPERAS_503 = [30, 60, 120]  # segundos entre reintentos ante "503 UNAVAILABLE"


def generar(instrucciones: str, contenido: str | list[str], modelo: str) -> dict:
    """Una única llamada a generate_content. `contenido` puede ser una lista de bloques
    (p. ej., conocimiento y documento), que se envían como partes separadas del mismo mensaje.
    Devuelve texto, motivo de fin y uso de tokens."""
    client = genai.Client()

    limite_salida = client.models.get(model=modelo).output_token_limit
    config = types.GenerateContentConfig(
        system_instruction=instrucciones,
        max_output_tokens=limite_salida,
    )
    intentos = []
    for espera in ESPERAS_503 + [None]:
        try:
            r = client.models.generate_content(model=modelo, contents=contenido, config=config)
            break
        except errors.APIError as e:
            intentos.append(f"{e.code} {e.status}")
            # Solo se reintenta la saturación temporal (503); una cuota agotada (429) no.
            if e.code != 503 or espera is None:
                return {"error": f"{e.code} {e.status} - {e.message}", "modelo": modelo,
                        "intentos": intentos}
            time.sleep(espera)

    cand = r.candidates[0] if r.candidates else None
    uso = r.usage_metadata
    return {
        "modelo": modelo,
        "intentos_fallidos": intentos,
        "texto": r.text or "",
        "finish_reason": cand.finish_reason.name if cand and cand.finish_reason else None,
        "max_output_tokens": limite_salida,
        "uso": {
            "entrada": uso.prompt_token_count,
            "salida": uso.candidates_token_count,
            "razonamiento": uso.thoughts_token_count,
            "total": uso.total_token_count,
        },
    }
