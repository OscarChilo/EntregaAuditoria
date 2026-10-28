---
id: SK-04
nombre: Conclusiones del informe de auditoría
version: 0.1
marco_de_referencia: ISO/IEC 27701:2025, 9.2
archivos:
  plantilla: ../../plantillas/informe_auditoria.md
---

# SK-04 — Conclusiones del informe de auditoría

## 1. Propósito

Redactar el resumen ejecutivo, las conclusiones y las limitaciones del informe de auditoría. El resto del informe (datos de la auditoría, conteos, hallazgos y planes de acción) lo arma el programa del agente a partir de las salidas de SK-02 y SK-03, para que no dependa del modelo.

## 2. Activación

Se usa al final de una auditoría, cuando el agente entrega:

- los datos del plan (objetivo, alcance, criterios);
- los conteos de resultados (calculados por el programa);
- la tabla de hallazgos de SK-03;
- la lista de requisitos «Sin evidencia».

## 3. Pasos

1. **Resumen ejecutivo** (3 a 5 frases): qué se auditó, cuántos requisitos, cuántos hallazgos por clasificación y los dos o tres temas más importantes.
2. **Conclusiones** (9.2.1): si, según la evidencia revisada, el PIMS cumple los criterios y si está implementado y se mantiene eficazmente. Fundamenta cada conclusión en hallazgos concretos (cita su N.°).
3. **Limitaciones:** requisitos sin evidencia, documentos no entregados, que no hubo entrevistas ni muestreo en campo (si así fue) y que los resultados los propuso un agente de IA y deben ser revisados por el equipo auditor.

## 4. Restricciones

- Usa solo los conteos y hallazgos recibidos: no recalcules ni agregues hallazgos.
- No afirmes que la organización «está certificada», «cumple la norma» o «es conforme» en general: habla de la evidencia revisada.
- No inventes riesgos, cifras ni personas.

## 5. Formato del resultado

```
## Resumen ejecutivo

...

## Conclusiones

- ...

## Limitaciones

- ...

--- FIN SK-04 ---
```

## 6. Historial

- **v0.1** (2026-10-27): primera versión.
