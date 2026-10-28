# Ejecuciones del agente de evidencias y auditoría — punto de control 2

**Fecha:** 2026-10-27 · **Modelo:** `gemini-3.5-flash-lite` · **Auditoría simulada:** AUD-2026-001 sobre los 14 documentos sintéticos (`simulacion/`) · **Requisitos:** 57 (30 cláusulas 4–10 + 27 controles del Anexo A)

> Revisión: medición automática contra la clave de la simulación y lectura de la IA (Claude). **El equipo indicó el 27-10-2026 que revisó los resultados de las ejecuciones 1 y 2 y está de acuerdo**; la decisión sobre cada hallazgo se registra en la aplicación (Auditoría → Hallazgos y revisión → `revision_equipo.csv`), que aún no tiene registros. Dos ejecuciones no bastan para estimar la variabilidad, y entre ellas cambió la plantilla de filas: no son repeticiones puras.

## 1. Las ejecuciones

| | Ejecución 1 | Ejecución 2 |
|---|---|---|
| Carpeta | `ejecucion1_20261027-184804_AUD-2026-001` | `ejecucion2_20261027-185150_AUD-2026-001` |
| SK-02 | v0.1 | v0.1.1 (plantilla con «E1 ? · E2 ?») |
| Llamadas | 8, todas completas, sin errores 503 | 8, todas completas, sin errores 503 |
| Tokens por llamada de SK-02 | ≈ 17 600–19 200 de entrada, 900–2 800 de salida | similar |
| Resultados (Conforme / N / O / M / Sin evidencia) | 36 / 9 / 11 / 0 / 1 | 44 / 4 / 6 / 0 / 3 |
| Hallazgos redactados (N / O / M) | 9 / 11 / 0 | 2 / 4 / 0 |
| **Vacíos sembrados detectados** | **9 de 13** (6 con la clasificación exacta) | **4 de 13** (3 exactos) |
| No detectados, pero con alerta para el revisor | 4 de 4 | 6 de 9 |
| Posibles falsos positivos (por revisar) | 9 | 5 |
| Filas con alerta del verificador | 36 de 57 | 18 de 57 |

## 2. Qué funcionó

- **Orquestación completa:** el programa armó el alcance, dividió en 6 lotes, llamó a SK-02, SK-03 y SK-04, verificó cada paso y generó la lista de verificación, los hallazgos, los planes de acción y el informe en los formatos de GESTITEL (también en CSV).
- **Detecciones estables en las dos ejecuciones:** 6.1.3 (plan sin aprobar), 7.2 (no se evalúa la eficacia de la capacitación), A.1.4.8 (bolsa de trabajo sin plazo de conservación) y 9.3.2 (sin partes interesadas en la revisión por la dirección).
- **La clave nunca se envió al modelo** (comprobado en lo enviado).

## 3. Problemas encontrados

1. **Formato de los elementos (ejecución 1):** en los lotes del Anexo A y de las cláusulas 9–10, el modelo escribió la definición de cada elemento en lugar de su estado. Corregido con la plantilla v0.1.1; en la ejecución 2 ya no ocurrió.
2. **Carácter «|» dentro de las citas (ejecución 2):** desplazó columnas. El lector reconstruye la fila y lo registra como observación de formato.
3. **«Conforme» apoyado en citas inventadas o recortadas (ejecución 2):** por ejemplo, en 5.2 se cita «…mejora continua del PIMS», que la política no dice, y en 4.1 «Sección 3. Cuestiones internas» como prueba de que se evaluó el cambio climático. Es el error más grave, porque oculta no conformidades.
4. **Variabilidad alta:** de 9 a 4 detecciones. Con solo dos ejecuciones, y con un cambio de plantilla entre ellas, no se puede separar el efecto de la plantilla del azar del modelo.
5. **SK-04 confunde la clasificación (ejecución 1):** escribe «11 oportunidades de mejora (O)» cuando O son observaciones. El verificador de SK-04 no lo detecta; hay que revisarlo en el informe.
6. **«Sin evidencia» incoherente:** el modelo marca «Sin evidencia» aunque indica dónde buscó (A.1.3.9, 7.4); por la regla, debería ser N. El verificador lo alerta.

## 4. Mitigación aplicada (sin cambiar resultados del modelo)

Se agregó una **alerta del verificador** en la lista de verificación: «Revisar: Conforme apoyado en cita no literal» y «Revisar: resultado incoherente con sus elementos». Con ella, el revisor humano ve **10 de los 13 vacíos** en la ejecución 2 (4 detectados + 6 alertados) y **13 de 13** en la ejecución 1. El costo: revisar 18 a 36 filas de 57.

Las respuestas originales (`llamadas/*_respuesta.md`) no se modificaron: las dos ejecuciones se volvieron a procesar sin llamar a Gemini (`--reprocesar`) después de corregir el lector y agregar las alertas.

## 5. Lectura

- El agente **sirve como asistente con revisión obligatoria**, no como auditor autónomo: deja pasar no conformidades con citas inventadas, y la detección cambia mucho entre ejecuciones.
- El valor está en la combinación de **propuesta del modelo + verificación de citas + revisión humana guiada por alertas**.
- Opciones para mejorar (no aplicadas): una segunda pasada de SK-02 solo sobre las filas con alerta; comparar con `gemini-3.8-flash`; repetir 3 ejecuciones con la misma versión para medir la variabilidad.

## 6. Ejecución 3 — verificación con el Anexo A completo (agente v0.2)

| | Ejecución 3 (`ejecucion3_20261027-193724_AUD-2026-001`) |
|---|---|
| Alcance | 108 requisitos: cláusulas 4–10 (30) y los 78 controles del Anexo A, con A.2 y A.3 parafraseados (`skill/comun/anexo_a_tablas_a2_a3.md`) |
| Llamadas | 11 (9 de SK-02, 1 de SK-03, 1 de SK-04), todas completas, sin errores 503 |
| Vacíos sembrados detectados | **7 de 13** (6 con la clasificación exacta); no detectados con alerta: 4 de 6 |
| Por zona | Cláusulas 4–10: 7 de 10 · Anexo A: 0 de 3 (A.1.4.8, A.1.3.9 y A.3.11 salieron «Conforme») |
| Posibles falsos positivos | 21, por revisar. Muchos parecen hallazgos reales que la clave no previó porque el alcance ahora incluye controles que los documentos no tratan (p. ej., A.1.5.3 países de destino no documentados; A.3.24 copias de seguridad no probadas; A.1.2.4 proceso de consentimiento no documentado) |
| Citas de SK-02 | 169 literales, 40 no literales, 5 en otro documento |

**Lectura:** el agente es más fiable en las cláusulas del sistema de gestión que en los controles del Anexo A, donde tiende a aceptar evidencia general como suficiente. La revisión humana guiada por las alertas sigue siendo necesaria. Las ejecuciones 1 y 2 se conservan con su alcance original (57 requisitos) y se reprocesan sin cambios.

