"""Prueba mínima de conexión con la API de Gemini (nivel gratuito).

No usa la Skill SK-01 ni tiene interfaz. Solo comprueba que la clave funciona:
  1. Lista los modelos que la clave puede usar con generateContent.
  2. Envía una única consulta corta al modelo elegido.

La clave se lee de la variable de entorno GEMINI_API_KEY y nunca se imprime.

Uso:
  python conexion/prueba_gemini.py --solo-listar
  python conexion/prueba_gemini.py --modelo gemini-3.5-flash-lite
"""

import argparse
import os
import sys

from google import genai
from google.genai import errors

MODELO_POR_DEFECTO = "gemini-3.5-flash-lite"
PREGUNTA_DE_PRUEBA = "Responde solo con la palabra: conectado"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--modelo", default=MODELO_POR_DEFECTO)
    parser.add_argument("--solo-listar", action="store_true",
                        help="lista los modelos sin enviar ninguna consulta")
    args = parser.parse_args()

    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY no está definida en este proceso.")
        return 1
    if os.environ.get("GOOGLE_API_KEY"):
        print("Aviso: GOOGLE_API_KEY también está definida y el SDK le da prioridad.")

    client = genai.Client()  # toma GEMINI_API_KEY del entorno

    try:
        modelos = sorted(
            m.name.removeprefix("models/")
            for m in client.models.list()
            if "generateContent" in (m.supported_actions or [])
        )
    except errors.APIError as e:
        print(f"Error al listar modelos: {e.code} {e.status} - {e.message}")
        return 1

    print(f"Modelos con generateContent ({len(modelos)}):")
    for nombre in modelos:
        print(f"  {nombre}")

    if args.solo_listar:
        return 0

    if args.modelo not in modelos:
        print(f"\nEl modelo '{args.modelo}' no está en la lista; no se envía la consulta.")
        return 1

    print(f"\nConsulta única a {args.modelo} ...")
    try:
        respuesta = client.models.generate_content(
            model=args.modelo, contents=PREGUNTA_DE_PRUEBA
        )
    except errors.APIError as e:
        print(f"Error en la consulta: {e.code} {e.status} - {e.message}")
        return 1

    uso = respuesta.usage_metadata
    print(f"Respuesta: {(respuesta.text or '').strip()}")
    print(f"Tokens: entrada={uso.prompt_token_count} salida={uso.candidates_token_count} "
          f"total={uso.total_token_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
