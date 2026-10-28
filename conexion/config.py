"""Configuración de modelos de Gemini (nivel gratuito, sin facturación).

Ambos identificadores fueron comprobados con la API el 2026-10-21 (models.list).
Se empieza con el de desarrollo, que respondió correctamente a la prueba de conexión.
No se asume que el modelo "final" produzca mejores evaluaciones: eso se comparará en las pruebas.

Límites del nivel gratuito vistos en AI Studio (proyecto tif-auditoria, 2026-10-21):
  gemini-3.5-flash-lite: 15 RPM, 250K TPM, 500 RPD
  gemini-3.8-flash:       5 RPM, 250K TPM,  20 RPD
"""

import os

MODELOS = {
    "desarrollo": "gemini-3.5-flash-lite",
    "final": "gemini-3.8-flash",
}

# Se puede cambiar sin tocar código: SK01_MODELO=final  (o un identificador completo)
_eleccion = os.environ.get("SK01_MODELO", "desarrollo")
MODELO_ACTIVO = MODELOS.get(_eleccion, _eleccion)
