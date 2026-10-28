# Metodología de evaluación de riesgos de privacidad

> **DOCUMENTO SINTÉTICO — SIMULACIÓN ACADÉMICA.** Elaborado para el TIF de Auditoría de Sistemas (UNSA, 2026-B). No es un documento oficial de la Universidad Nacional de San Agustín de Arequipa. Unidades, personas, cargos, correos y cifras son ficticios.

| Campo | Valor |
|---|---|
| Código | SIM-PIMS-04 |
| Versión | 1.0 |
| Fecha de aprobación | 2026-04-06 |
| Elaborado por | Oficina de Protección de Datos Personales (OPDP) |
| Aprobado por | Comité de Privacidad y Seguridad de la Información — Acta simulada N.° 03-2026-CPSI |
| Clasificación | Uso interno |

## 1. Propósito

Definir cómo se identifican, analizan y evalúan los riesgos de privacidad de los tratamientos de datos personales de la Universidad, según la cláusula 6.1.2 de ISO/IEC 27701:2025.

## 2. Cuándo se evalúa

- Una vez al año, en el periodo de riesgos definido en la plataforma PIMS (periodo 2026: abril a junio).
- Cuando se planifique un tratamiento nuevo o un cambio significativo en uno existente.
- Después de un incidente de seguridad o privacidad de nivel alto.

## 3. Identificación

1. Para cada actividad del registro de tratamientos (SIM-PIMS-09) se identifican los riesgos para la **privacidad de los titulares** y los riesgos de **seguridad de la información**.
2. Se usan como referencia los catálogos de amenazas y vulnerabilidades de la plataforma PIMS.
3. Cada riesgo tiene un **dueño**: el dueño del proceso al que pertenece el tratamiento (ver SIM-PIMS-03).

## 4. Análisis

Cada riesgo se analiza con dos dimensiones, en la escala de 1 a 4 de la matriz 4×4 activa en la plataforma PIMS:

**Consecuencia:** se valora el mayor de dos efectos:

| Nivel | Para la Universidad | Para los titulares |
|---|---|---|
| 1 Leve | Sin impacto legal ni reputacional | Molestia menor, reversible |
| 2 Moderada | Reclamo individual; costo menor | Pérdida de tiempo o de control sobre sus datos |
| 3 Grave | Procedimiento sancionador posible; impacto reputacional local | Daño económico, discriminación o exposición de datos sensibles |
| 4 Muy grave | Sanción probable; impacto nacional | Daño a la integridad física, psicológica o patrimonial difícil de revertir |

**Probabilidad:** 1 Rara (menos de una vez en 5 años), 2 Posible (una vez en 2 a 5 años), 3 Probable (una vez al año), 4 Casi segura (varias veces al año). Se estima con datos de incidentes previos y la opinión del dueño del proceso, no con supuestos del peor caso.

**Nivel de riesgo** = Consecuencia × Probabilidad (1 a 16).

## 5. Evaluación y criterios de aceptación

| Nivel | Rango | Criterio | Quién acepta |
|---|---|---|---|
| Bajo | 1–3 | Aceptable sin tratamiento adicional | Dueño del proceso |
| Medio | 4–6 | Aceptable con controles existentes y seguimiento | Dueño del proceso |
| Alto | 8–9 | Requiere tratamiento en el periodo | CPSI |
| Extremo | 12–16 | Requiere tratamiento inmediato; puede suspenderse el tratamiento | CPSI y Rectorado |

Los riesgos se comparan con estos criterios y se **priorizan** por nivel; ante el mismo nivel, primero los que afectan datos sensibles.

## 6. Coherencia de los resultados

Para que evaluaciones repetidas den resultados coherentes y comparables:

- se usan siempre la misma escala, la misma matriz y las mismas definiciones;
- la OPDP revisa en una sesión de calibración las valoraciones de todos los dueños de proceso antes de cerrar el periodo;
- los cambios a esta metodología se aplican al periodo siguiente, nunca a uno en curso.

## 7. Registros

Los resultados de cada periodo se conservan en el módulo de Riesgos de la plataforma PIMS (evaluación, matriz y tratamiento) y en el informe de evaluación de riesgos del periodo, firmado por la OPDP.
