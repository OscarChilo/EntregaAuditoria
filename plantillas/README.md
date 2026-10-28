# Plantillas del agente de evidencias y auditoría

Formatos que usa el agente para entregar sus resultados. Están **calcados de los campos del módulo Auditorías de GESTITEL** (Anexo 02, tablas `core_audit`, `core_auditchecklistitem`, `core_auditfinding` y `core_auditactionplan`) y de lo que pide la cláusula 9.2.2 de ISO/IEC 27701:2025, para que lo producido se pueda cargar en unsa.27k.pe campo por campo.

> **Provisionales:** si el docente entrega plantillas propias para este tipo de agente, reemplazan a estas. Basta con ajustar los archivos de esta carpeta y el formato de las skills.

| Plantilla | Para qué | Campos de GESTITEL que alimenta |
|---|---|---|
| `programa_auditoria.md` | Programa anual (9.2.2) | — (documento; se sube a Gestión Documental) |
| `plan_auditoria.md` | Plan de una auditoría | `core_audit`: código, tipo, nombre, alcance, objetivo, fechas, auditor líder, equipo, áreas, estado |
| `lista_verificacion.md` | Requisitos a verificar y evidencia encontrada | `core_auditchecklistitem`: proceso, norma, requisito, evidencia textual, código de requisito de origen |
| `hallazgos.md` | Hallazgos clasificados | `core_auditfinding`: clasificación N / O / M, descripción, evidencia |
| `plan_accion.md` | Acciones correctivas por hallazgo | `core_auditactionplan`: acción, responsable, fecha compromiso, estado, avance |
| `informe_auditoria.md` | Informe final para la dirección | — (documento; se sube a Gestión Documental) |

Valores permitidos (según el Anexo 02):

- Tipo de auditoría: **I** Interna · **E** Externa.
- Estado de la auditoría: **P** Planificada · **R** En curso · **C** Cerrada.
- Clasificación del hallazgo: **N** No conformidad · **O** Observación · **M** Oportunidad de mejora.
- Estado de la acción: **O** Abierta · **P** En progreso · **C** Cerrada. Avance de 0 a 100.
