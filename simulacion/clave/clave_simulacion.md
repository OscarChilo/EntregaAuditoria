# Clave de la simulación — vacíos sembrados en los documentos sintéticos

> **No se envía al modelo.** Este archivo sirve solo para medir al agente después de cada ejecución. El código del agente no debe leer la carpeta `simulacion/clave/`.
>
> **Sesgo declarado:** la misma IA (Claude) redactó los documentos, esta clave y las skills SK-02 a SK-04. Los vacíos son deliberadamente claros; un auditor humano podría clasificar algunos casos de otra manera. Las métricas que se calculen con esta clave miden la detección de vacíos sembrados, no la calidad general de una auditoría real.
>
> Para reducir el sesgo, los ejemplos de `skill/sk02/criterios.md` y `skill/sk03/SKILL.md` se cambiaron por ejemplos neutros que **no** coinciden con ningún vacío sembrado (una primera redacción sí coincidía con S-02, S-03, S-06 y S-09). Aun así, reglas generales como «una falta en el lugar esperable es N» o «buscar estados provisionales y datos en blanco» se escribieron conociendo la simulación.

**Versión:** 1.0 · **Fecha:** 2026-10-27 · **Documentos:** `simulacion/documentos/SIM-PIMS-01` a `SIM-PIMS-14`

## 1. Vacíos sembrados (hallazgos esperados)

Cada fila es un hallazgo que el agente debería proponer. «Aceptable» indica otra clasificación que también se considera correcta, porque el caso admite interpretación.

| ID | Documento | Requisito | Elemento ausente o contradicho | Esperado | Aceptable | Dónde se nota |
|---|---|---|---|---|---|---|
| S-01 | SIM-PIMS-01 Contexto y alcance | 4.1 | E2: no se determina si el cambio climático es una cuestión relevante | N | O | Secciones 2 y 3: no hay ninguna mención |
| S-02 | SIM-PIMS-02 Política de privacidad | 5.2 | E4: falta el compromiso de mejora continua del PIMS | N | — | Sección 4 «Compromisos»: cumplir requisitos, objetivos, recursos e integración, pero no mejora continua |
| S-03 | SIM-PIMS-03 Roles | 5.3 | E3: nadie tiene asignada la responsabilidad de informar a la alta dirección sobre el desempeño del PIMS | N | O | Sección 2: el CPSI «supervisa» y hace seguimiento, pero no se asigna el informe a la dirección |
| S-04 | SIM-PIMS-05 Tratamiento y SoA | 6.1.3 | E7: el plan no está aprobado por los dueños del riesgo ni se aceptó el riesgo residual | N | — | Encabezado «pendiente de aprobación» y nota de la sección 6 |
| S-05 | SIM-PIMS-06 Objetivos | 6.2 | E8: OBJ-3 y OBJ-4 no tienen responsable | O | N | Tabla de la sección 2, columna «Responsable» con «—» |
| S-06 | SIM-PIMS-07 Capacitación | 7.2 | E4: no se evalúa la eficacia de las acciones de capacitación | N | — | Sección 3: «no se toman exámenes ni se evalúa después…» |
| S-07 | SIM-PIMS-08 Control documental | 7.5.2 | E3: el propio procedimiento no está revisado ni aprobado, y se usa como borrador | N | — | Encabezado: «Aprobado por: — (pendiente de firma)», «Borrador — en uso desde marzo de 2026» |
| S-08 | SIM-PIMS-09 Registro de tratamientos | A.1.4.8 | E1: RAT-06 (bolsa de trabajo) no tiene plazo de conservación | N | O | Tabla, fila RAT-06, columna «Conservación» con «—» |
| S-09 | SIM-PIMS-10 ARCO-P | A.1.3.9 | E1: no se prevé entregar al titular una copia de sus datos (el acceso solo «informa»; la portabilidad transmite a otra institución) | N | O | Sección 5 |
| S-10 | SIM-PIMS-11 Incidentes | A.3.11 | E1: el proceso no asigna roles ni responsables a cada etapa, y la atención depende de «la disponibilidad del personal» | N | — | Sección 4 |
| S-11 | SIM-PIMS-12 Programa de auditoría | 9.2.2 | E4: el auditor líder es el jefe de la OPDP, que administra el PIMS: no se asegura la imparcialidad | N | — | Tabla de la sección 3 y SIM-PIMS-03 |
| S-12 | SIM-PIMS-13 Revisión por la dirección | 9.3.2 | E3: no se revisan los cambios en las necesidades y expectativas de las partes interesadas | N | O | Sección 3: hay cuestiones (3.2) y desempeño (3.3), pero no partes interesadas |
| S-13 | SIM-PIMS-14 No conformidades | 10.2 | E6: las acciones cerradas no tienen verificación de eficacia | N | — | Columna «Verificación de eficacia» con «—» en NC-2026-01 y NC-2026-02 |

## 2. Hallazgos secundarios aceptables (no cuentan como falsos positivos)

| ID | Documento | Requisito | Hallazgo | Clasificación razonable |
|---|---|---|---|---|
| A-01 | SIM-PIMS-07 | 7.2 | Solo 12 de 25 trabajadores de la OUIS completaron el curso de seguridad | O |
| A-02 | SIM-PIMS-09 | A.1.5.2 | RAT-05 declara transferencia internacional, pero el registro no indica su base | O |
| A-03 | SIM-PIMS-11 | A.3.11 / A.3.12 | Sin plazos de atención por severidad; la notificación a titulares y autoridad no tiene criterios ni responsable | O (o parte de S-10) |
| A-04 | SIM-PIMS-06 | 6.2 | OBJ-2, OBJ-3 y OBJ-4 «en riesgo» al 2026-09-30 | M u O |
| A-05 | SIM-PIMS-02 | 5.2 | La revisión cada dos años podría ser poco frecuente | M |
| A-06 | SIM-PIMS-01 | 4.2 | La superintendencia queda fuera del PIMS: está justificado, pero podría documentarse mejor | M |
| A-07 | SIM-PIMS-13 | 9.3.3 | AC-04 sin responsable ni plazo | M |
| A-08 | SIM-PIMS-14 | 10.2 | NC-2026-03 abierta sin acción provisional sobre Admisión y Recursos Humanos | O |

## 3. Requisitos cubiertos sin vacío sembrado (esperado: conforme)

Una no conformidad del agente en estos requisitos es un **falso positivo**, salvo que su justificación cite un texto real que lo sostenga (en ese caso se revisa a mano y se anota aquí).

| Documento | Requisitos que deberían salir conformes |
|---|---|
| SIM-PIMS-01 | 4.1 E1, E3, E4 · 4.2 (todos) · 4.3 (todos) · 4.4 |
| SIM-PIMS-02 | 5.2 E1, E2, E3, E5, E6, E7 · 5.1 E1, E3 |
| SIM-PIMS-03 | 5.3 E1, E2 |
| **SIM-PIMS-04** | **6.1.2 completo (E1 a E10): documento de control sin vacíos** |
| SIM-PIMS-05 | 6.1.3 E1 a E6, E8, E9 · 8.3 E1 (parcial, en avance) |
| SIM-PIMS-06 | 6.2 E1 a E7 · 9.1 E1 a E6 |
| SIM-PIMS-07 | 7.2 E1, E3, E5 · 7.3 (todos) |
| SIM-PIMS-08 | 7.5.1 · 7.5.3 (todos) |
| SIM-PIMS-09 | A.1.2.9 · A.1.2.2 · A.1.2.3 |
| SIM-PIMS-10 | A.1.3.7 · A.1.3.10 · A.1.3.8 (sección 6) |
| SIM-PIMS-12 | 9.2.1 · 9.2.2 E1, E2, E3, E5, E6 |
| SIM-PIMS-13 | 9.3.1 · 9.3.2 E1, E2, E4 a E7 · 9.3.3 |
| SIM-PIMS-14 | 10.2 E1 a E5, E7, E9 |

## 4. Cómo medir

Para cada ejecución del agente:

1. **Detección:** de los 13 vacíos sembrados (S-01 a S-13), cuántos aparecen como hallazgo sobre el requisito correcto. Se cuenta como detectado si la clasificación es la esperada o la aceptable.
2. **Clasificación:** de los detectados, cuántos tienen exactamente la clasificación esperada.
3. **Falsos positivos:** hallazgos N u O sobre requisitos de la sección 3 que no se apoyan en un texto real.
4. **Evidencia:** de los hallazgos detectados, cuántos citan literalmente el texto del documento (lo comprueba el verificador).

Con una sola ejecución no se puede estimar la variabilidad del modelo: conviene repetir al menos dos veces.
