---
id: SK-03
nombre: Redacción de hallazgos y planes de acción
version: 0.1
marco_de_referencia: ISO/IEC 27701:2025, 10.2
archivos:
  plantillas:
    - ../../plantillas/hallazgos.md
    - ../../plantillas/plan_accion.md
---

# SK-03 — Redacción de hallazgos y planes de acción

## 1. Propósito

Convertir los resultados N, O y M de SK-02 en hallazgos redactados para el módulo Auditorías de GESTITEL y proponer un plan de acción para cada uno.

## 2. Activación

Se usa cuando el agente entrega la lista de resultados N, O o M de una auditoría, cada uno con su requisito, sus elementos y sus citas, y la lista de roles que figuran en los documentos (dueños de proceso, responsables).

## 3. Pasos

1. **Agrupa** los resultados que describen el mismo problema en el mismo documento (p. ej., dos elementos del mismo requisito en DOC-01) en un solo hallazgo, citando todos los requisitos. No agrupes problemas de documentos distintos.
2. **Clasificación:** conserva la de SK-02 (N, O o M). Si al agrupar hay clasificaciones distintas, usa la más grave.
3. **Descripción:** «En {{documento}} se observó que {{hecho}}. El requisito {{ID}} exige {{elemento, parafraseado}}.» Sin juicios sobre personas.
4. **Evidencia:** una cita literal breve con su documento y sección, copiada de los elementos de SK-02. Si el hallazgo es una falta, indica dónde se buscó («DOC-01 §3 no menciona…»).
5. **Plan de acción** (uno por hallazgo):
   - **Corrección inmediata:** qué hacer ya para contener el problema.
   - **Acción correctiva:** qué hacer para eliminar la causa. Si la causa no consta en la evidencia, escribe «Causa por determinar con el dueño del proceso» y propone primero ese análisis.
   - **Responsable:** un **rol** que figure en los documentos recibidos (p. ej., «Jefe del área responsable»). Si no consta, «Por designar».
   - **Fecha compromiso:** la fecha base recibida más 60 días (N), 90 días (O) o 120 días (M). Es una propuesta.
   - **Verificación de eficacia:** cómo se comprobará que la acción funcionó.
   - **Estado:** O · **Avance:** 0.

## 4. Restricciones

- No crees hallazgos nuevos ni cambies los requisitos: trabaja solo con los resultados recibidos.
- No inventes nombres de personas, causas ni fechas fuera de la regla del paso 5.
- Copia las citas sin modificarlas.

## 5. Formato del resultado

```
# SK-03 — Hallazgos y planes de acción

## Hallazgos

| N.° | Clasificación | Requisitos | Descripción | Evidencia |
|---|---|---|---|---|
| H-01 | N | X.Y E2 | ... | "cita" [DOC-01 §3] |

## Planes de acción

| Hallazgo | Corrección inmediata | Acción correctiva | Responsable | Fecha compromiso | Verificación de eficacia | Estado | Avance |
|---|---|---|---|---|---|---|---|
| H-01 | ... | ... | Jefe del área responsable | AAAA-MM-DD | ... | O | 0 |

--- FIN SK-03 ---
```

Sin el carácter `|` dentro de las celdas ni saltos de línea.

## 6. Historial

- **v0.1** (2026-10-27): primera versión.
