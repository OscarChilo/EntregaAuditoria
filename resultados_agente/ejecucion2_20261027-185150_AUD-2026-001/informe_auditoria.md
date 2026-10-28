# Informe de auditoría interna del PIMS — AUD-2026-001

> **Borrador generado por el agente de evidencias y auditoría.** Debe revisarlo y aprobarlo el auditor líder. Verificación automática: 60 observaciones (ver `verificacion.md`).

| | |
|---|---|
| Auditoría | AUD-2026-001 — Auditoría interna del PIMS 2026 |
| Tipo | Interna |
| Fechas | 2026-11-09 a 2026-11-20 |
| Auditor líder | Auditor líder (por designar) |
| Equipo auditor | Equipo auditor interno, con apoyo del agente de evidencias y auditoría |
| Destinatarios | Comité de Privacidad y Seguridad de la Información y dueños de proceso |

## 1. Objetivo, alcance y criterios

- **Objetivo:** Verificar la conformidad del PIMS con ISO/IEC 27701:2025 antes de la revisión por la dirección
- **Alcance:** Procesos del alcance del PIMS (SIM-PIMS-01): admisión, matrícula, bienestar, personal, biblioteca, bolsa de trabajo y Centro de Idiomas; revisión documental
- **Criterios:** Cláusulas 4 a 10 y controles del Anexo A de ISO/IEC 27701:2025 (los 78 controles); política SIM-PIMS-02

## 2. Metodología

Revisión documental de las evidencias entregadas, con apoyo del agente de IA (skills SK-02 a SK-04, modelo de Gemini). El agente propuso los resultados; el equipo auditor los revisa.

## 3. Resumen de resultados

| Resultado | Cantidad |
|---|---|
| Requisitos verificados | 57 |
| Conformes | 44 |
| Ítems con resultado N / O / M | 4 / 6 / 0 |
| Sin evidencia suficiente | 3 |
| Hallazgos redactados N / O / M | 2 / 4 / 0 |

## 4. Hallazgos

| N.° | Clasificación | Requisitos | Descripción | Evidencia |
|---|---|---|---|---|
| H-01 | N | 7.2 E4 | En SIM-PIMS-07 se observó que no se evalúa la eficacia de las acciones de capacitación sino solo la asistencia. El requisito 7.2 exige determinar y asegurar la competencia del personal que influye en el desempeño de privacidad. | "En 2026 no se toman exámenes ni se evalúa después si la capacitación mejoró el desempeño: se considera suficiente la asistencia completa al curso." [SIM-PIMS-07 §3] |
| H-02 | O | 8.3 E1 | En SIM-PIMS-05 se observó que el plan de tratamiento se encuentra pendiente de aprobación y varios tratamientos de riesgos presentan avances parciales. El requisito 8.3 exige implementar el plan de tratamiento de riesgos de privacidad. | "Ejecutar el plan de tratamiento SIM-PIMS-05" [SIM-PIMS-06 §2] |
| H-03 | N | 9.3.2 E3 | En SIM-PIMS-13 se observó que el acta de revisión por la dirección omite los cambios en las necesidades de las partes interesadas. El requisito 9.3.2 exige que la revisión por la dirección incluya entradas mínimas. | SIM-PIMS-13 §3 no menciona los cambios en las necesidades de las partes interesadas. |
| H-04 | O | 10.2 E6 | En SIM-PIMS-14 se observó que no se registra la verificación de eficacia de las acciones correctivas implementadas en los registros de no conformidades. El requisito 10.2 exige ante una no conformidad, reaccionar, analizar causas, actuar y verificar la eficacia. | SIM-PIMS-14 §2 no registra la verificación de eficacia de las acciones correctivas implementadas. |
| H-05 | O | A.1.4.9 E2 | En SIM-PIMS-08 se observó que falta una política o procedimiento documentado específico para la eliminación de datos personales en los procesos de negocio. El control A.1.4.9 exige tener políticas, procedimientos o mecanismos documentados para la eliminación. | SIM-PIMS-08 §4 no menciona políticas o procedimientos específicos para la eliminación de datos personales en los procesos de negocio. |
| H-06 | O | A.3.26 E2 | En SIM-PIMS-05 se observó que el documento omite la descripción de las reglas de criptografía y gestión de claves asociadas al control A.3.26. El control A.3.26 exige establecer reglas para el uso de criptografía. | SIM-PIMS-05 §3 no describe las reglas de criptografía y gestión de claves asociadas al control A.3.26. |

## 5. Planes de acción propuestos

| Hallazgo | Acción correctiva | Responsable | Fecha compromiso | Verificación de eficacia |
|---|---|---|---|---|
| H-01 | Definir e implementar una metodología de evaluación de eficacia posterior a las capacitaciones. | Jefe de Recursos Humanos | 2026-01-19 | Revisar los registros de capacitación para comprobar la inclusión de evaluaciones de eficacia. |
| H-02 | Realizar seguimiento semanal al avance de los planes de tratamiento hasta alcanzar el 100 %. | Jefe de la OPDP | 2026-01-19 | Verificar el estado de implementación de las acciones en el módulo de Riesgos de la plataforma PIMS. |
| H-03 | Actualizar el procedimiento de revisión por la dirección para asegurar el registro de todas las entradas obligatorias. | Jefe de la OPDP | 2026-01-19 | Revisar la siguiente acta de revisión por la dirección para confirmar la inclusión de todas las entradas. |
| H-04 | Establecer un campo obligatorio y un procedimiento para registrar la verificación de eficacia en SIM-PIMS-14. | Jefe de la OPDP | 2026-01-19 | Auditar el registro de no conformidades para verificar que todas las acciones lleven constancia de su eficacia. |
| H-05 | Elaborar y aprobar un procedimiento documentado específico para la eliminación de datos personales. | Dueño del proceso | 2026-03-21 | Revisar el procedimiento aprobado y su difusión en la lista maestra de documentos. |
| H-06 | Incluir formalmente las reglas de criptografía y gestión de claves en el plan de tratamiento y SoA (SIM-PIMS-05). | Jefe OUIS | 2026-03-21 | Inspeccionar el documento SIM-PIMS-05 actualizado para constatar la inclusión del control A.3.26. |

## 6. Resumen ejecutivo, conclusiones y limitaciones (redactados por SK-04)

## Resumen ejecutivo

Durante la auditoría interna del PIMS (AUD-2026-001) de la Universidad Nacional de San Agustín de Arequipa, se verificaron 57 requisitos y controles de la norma ISO/IEC 27701:2025 mediante una revisión documental que abarcó los procesos del alcance del PIMS (admisión, matrícula, bienestar, personal, biblioteca, bolsa de trabajo y Centro de Idiomas). Como resultado de la evaluación, se determinaron 32 conformidades, 2 no conformidades (H-01, H-03), 4 oportunidades de mejora (H-02, H-04, H-05, H-06) y 3 requisitos sin evidencia (7.4, A.1.3.3, A.1.3.9). Los temas más importantes que requieren atención se centran en la evaluación de la eficacia de la capacitación del personal, la completitud de las entradas mínimas en la revisión por la dirección y la formalización de procedimientos específicos de eliminación de datos personales.

## Conclusiones

- Sobre la base de la evidencia documental revisada, el PIMS demuestra un nivel general de cumplimiento operativo y documental en la mayoría de sus procesos; sin embargo, no cumple de manera íntegra con todos los criterios de auditoría evaluados debido a las no conformidades detectadas.
- El requisito 7.2 no se cumple en su totalidad, toda vez que se identificó que no se evalúa la eficacia de las acciones de capacitación del personal, limitándose al registro de asistencia (H-01).
- El requisito 9.3.2 no se cumple plenamente, ya que el acta de revisión por la dirección omite los cambios en las necesidades de las partes interesadas exigidos como entradas mínimas (H-03).
- Se identificaron áreas de mejora significativas relativas a la implementación del plan de tratamiento de riesgos de privacidad (H-02), la verificación de eficacia en las acciones correctivas (H-04), la documentación para la eliminación de datos personales (H-05) y la descripción de reglas de criptografía y gestión de claves (H-06).

## Limitaciones

- Se identificaron tres requisitos sin evidencia documental aportada: 7.4, A.1.3.3 y A.1.3.9.
- No se entregaron ni revisaron documentos adicionales a los especificados en el alcance de la simulación.
- No se realizaron entrevistas a personal de los procesos ni se efectuó muestreo en campo, basándose la auditoría estrictamente en la revisión documental.
- Los resultados, hallazgos, conclusiones y propuestas presentados fueron generados por un Agente de Evidencias y Auditoría basado en IA y constituyen una propuesta que debe ser revisada, validada y aprobada formalmente por el equipo auditor interno.

## 7. Aprobación

| Rol | Nombre | Fecha |
|---|---|---|
| Auditor líder | | |
