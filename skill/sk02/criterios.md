# SK-02 — Criterios de evaluación de evidencias

Metodología del equipo. Los requisitos vienen de ISO/IEC 27701:2025; la forma de decidir el resultado es nuestra.

## 1. Qué cuenta como evidencia

- Un texto de un documento entregado que trata **el mismo elemento** del requisito.
- Un encabezado o metadato del documento (fecha, versión, estado, aprobación) también es evidencia sobre ese documento.
- Una tabla es evidencia de lo que dice cada celda, fila por fila.

## 2. Prueba de pertinencia

Antes de usar una cita, pregúntate: ¿este texto trata **exactamente** el elemento, o solo un tema vecino?

- «Se hacen copias de seguridad» no es lo mismo que «se prueban las restauraciones».
- «Existe un formulario de quejas» no es lo mismo que «las quejas se responden en un plazo definido».
- «Se elaboró un inventario» no es lo mismo que «el inventario se mantiene actualizado».
- Una intención futura («se programó», «se considerará») no demuestra que algo se hizo.
- Un anuncio («este documento describe…») no es el contenido.

Si la cita no pasa la prueba, el elemento queda como **Falta**.

## 3. Estado de cada elemento

| Estado | Cuándo | Formato |
|---|---|---|
| **Respalda** | Un texto pertinente lo demuestra | `E1 Respalda ← "cita literal" [CÓDIGO §sección]` |
| **Falta** | No hay texto pertinente. Si buscaste en el lugar esperable, indícalo | `E2 Falta [CÓDIGO §sección]` o, si ningún documento trata el requisito, `E2 Falta` |
| **Contradicho** | Un texto dice lo contrario o deja el elemento sin efecto | `E3 Contradicho ← "cita literal" [CÓDIGO §sección]` |

Los elementos marcados **[recomendación]** («should» en la norma) nunca producen una N.

## 4. Resultado del requisito

| Resultado | Regla |
|---|---|
| **Conforme** | Todos los elementos están en **Respalda** (los [recomendación] pueden faltar) |
| **N — No conformidad** | Al menos un elemento obligatorio está en **Contradicho**, o en **Falta** con lugar esperable indicado (el documento que debía contenerlo existe y no lo contiene) |
| **O — Observación** | Todos los elementos tienen algo de evidencia, pero al menos uno es débil, incompleto o parcial (p. ej., la tabla tiene el dato en unas filas y no en otras), o hay un riesgo concreto de incumplir |
| **M — Oportunidad de mejora** | El requisito es conforme, pero hay una mejora clara, o falta solo un elemento [recomendación] |
| **Sin evidencia** | Ningún documento entregado trata el requisito: todos los elementos en **Falta** sin lugar esperable. No es un hallazgo: se pide evidencia |

Reglas adicionales:

- **Una falta en el lugar esperable es N, no «Sin evidencia».** Ejemplo: el documento que trata el requisito existe y omite un elemento que el requisito exige → N.
- **Entre N y O, decide por el elemento:** si el elemento obligatorio no aparece en absoluto → N; si aparece de forma incompleta → O.
- **Contradicción entre documentos:** si dos documentos dicen cosas incompatibles sobre el mismo elemento, cita ambos y marca **O** (salvo que uno de ellos sea claramente el vigente).
- **No compenses:** un elemento respaldado no cubre a otro que falta.

## 5. Evidencia encontrada (columna para GESTITEL)

- Una o dos frases, en tercera persona, con el código de los documentos: «DOC-01 §3 define el procedimiento y sus responsables; no indica la frecuencia de revisión.»
- No repitas las citas completas: ya están en la columna de elementos.

## 6. Hallazgo propuesto

- Solo para N, O o M. Para Conforme o Sin evidencia, escribe «—».
- Una frase: «{{documento}}: {{qué falta o qué está mal}} ({{ID}} {{elemento}}).»
