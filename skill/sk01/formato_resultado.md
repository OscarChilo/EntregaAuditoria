# SK-01 — Formato del resultado

El resultado se entrega en Markdown, con las secciones siguientes **en este orden**. No se agregan secciones nuevas ni se omiten las existentes. Una sección sin contenido lleva "Ninguno".

Los **conteos**, la **cobertura** y el **resumen** (información esencial faltante, aplicabilidad por determinar, evidencia interna a solicitar) los genera la aplicación a partir de la matriz. **No los escribas.**

---

## 1. Encabezado

```
# Evaluación SK-01 — <nombre del documento>

- Documento: <nombre> (<fuente>, <fecha si se conoce>)
- Páginas recibidas: <N>
- Rol de la organización según el documento: <responsable / encargada / no determinado> — justificación: <cita literal y ubicación, o "el documento no lo indica">
- Marco: ISO/IEC 27701:2025 — catálogo v<versión>
- Cobertura: 78 controles del Anexo A, con orientaciones seleccionadas del Anexo B (no toda la norma ni el sistema de gestión)
- Estado de verificación del catálogo: <copiar exactamente el campo "Estado del catálogo" del mensaje de evaluación>
- Clasificación de los controles: metodología del equipo (esencial, condicional, evidencia interna); no es una clasificación de la norma ni una obligación universal de publicación
- Naturaleza del resultado: apoyo al análisis documental; no es certificación, auditoría de la organización ni opinión legal. "Cumple" se refiere solo al criterio documental evaluado.
```

## 2. Matriz de evaluación

Copia **todas** las filas de la plantilla (bloque `<<<PLANTILLA DE LA MATRIZ>>>`), **en el mismo orden**, y completa sus celdas. Columnas:

| Referencia ISO | Control | Cat. | Aplicabilidad | Evidencia (cita literal) | Ubicación | Estado | Justificación | Información faltante o necesaria | Recomendación |
|---|---|---|---|---|---|---|---|---|---|

Reglas:
- **Referencia ISO, Control y Cat.:** se copian de la plantilla **sin cambios**. No se agregan, quitan, unen ni dividen filas. No se usan rangos.
- **Aplicabilidad:**
  - E: `Aplica`.
  - C: `Aplica` (situación declarada, con cita), `No aplica` (**solo** con una cita que la descarte expresamente; la justificación reproduce la negación) o `Por determinar` (silencio, indicios o duda), según `criterios.md` §3.1. **El silencio nunca es `No aplica`.**
  - INT-i e INT: `—`.
  - Filas agrupadas: como indica la plantilla.
- **Evidencia:** citas literales entre comillas dobles, sin marcas `[Página N]`. Los saltos de línea se unen con un espacio. "—" si no hay. Un carácter `|` se reemplaza por `/`.
- **Ubicación:** `Pág. N — <sección>` para cada cita, o "—".
- **Estado:** uno de los seis de `criterios.md`, escrito exactamente igual y permitido para la categoría y la aplicabilidad.
- **Justificación:** en las filas con elementos (`elementos.md`), recorrer **todos** los elementos en orden: `E1 Respalda ← "<cita>" · E2 Falta · E3 Falta (interno) · E4 Contradicho ← "<cita>"`. Si se usa un párrafo o canal común (`criterios.md` §3.3), citar ambos textos y explicar el vínculo. En las filas agrupadas y en las INT, una frase con la razón.
- **Información faltante o necesaria:**
  - E, o C con *Aplica*, sin *Cumple*: qué información falta, en concreto (p. ej., "el plazo o criterio de conservación por tipo de datos").
  - C *Por determinar*: la pregunta que hay que responder (p. ej., "¿se transfieren datos fuera del país?").
  - INT-i e INT: la evidencia interna que haría falta.
  - En otro caso: "—".
- **Recomendación:** comienza con un rótulo de `criterios.md` §5 ("Completar la política:", "Corregir el texto:", "Aclarar aplicabilidad:", "Solicitar evidencia interna:", "Mantener:", "Ninguna:"). Si se agrega una sugerencia basada en una orientación, va **después** y separada: `Sugerencia (orientación O-xx): …`.
- **Filas agrupadas** (Tabla A.3 INT y Tabla A.2): un solo estado para el grupo. Si hay evidencia específica de un control del grupo, se indica en su Justificación, sin dividir la fila.

## 3. Información al titular (ejemplos de B.1.3.3 y B.1.3.4)

Copia **todas** las filas de la lista (bloque `<<<LISTA INFORMACIÓN AL TITULAR>>>`), en el mismo orden, y complétalas **aunque la política no mencione el punto**. Son **ejemplos de la norma, no obligaciones**: no generan estados.

| Orientación | Cat. en la lista | Situación | Cita literal | Ubicación | Qué falta | Sugerencia |
|---|---|---|---|---|---|---|

- **Situación:** `Presente` · `Parcial` · `Ausente` · `No aplica` (C descartado **expresamente**, con la cita de la negación) · `Por determinar` (C sin información o con solo indicios; nunca `No aplica` por silencio).
- **Sugerencia:** comienza con "Sugerencia (orientación O-xx):". Si el punto coincide con un elemento [aviso] de un control E o C aplicable sin *Cumple*, escribe "Ver <ID del control>"; el faltante ya figura en la matriz.

## 4. Recorrido del documento

| Sección del documento | Pág. | Tratada en |
|---|---|---|

"Tratada en" indica los IDs de control, las orientaciones O-xx o "Sin correspondencia". Ninguna sección que trate datos personales puede quedar sin tratar.

## 5. Evidencias sin correspondencia en el catálogo

Textos del documento relevantes para la privacidad que no corresponden a ningún ID del catálogo. Por ejemplo, una mención a una ley, que se registra pero no se evalúa.

## 6. Limitaciones

Siempre incluir:
- que la evaluación se basa solo en el documento entregado;
- la cobertura (Anexo A, con orientaciones seleccionadas del Anexo B);
- que el catálogo no está validado (si así lo indica su estado);
- los controles C con aplicabilidad *Por determinar*, como límite del documento;
- cualquier problema del texto recibido (páginas ilegibles, texto cortado, partes `[REDACTADO]`, restos de una impresión web, etc.).

## 7. Bloque de cierre (obligatorio)

La respuesta **debe terminar** exactamente con estas líneas, sin encerrarlas en un bloque de código:

--- FIN SK-01 ---
Matriz completada con todas las filas de la plantilla: <sí / no: indicar cuáles faltan>
Lista "Información al titular" completada: <sí / no: indicar cuáles faltan>

Si el bloque falta, la aplicación tratará la respuesta como **truncada**, y no se presentará como una evaluación completa.
