# Diseño del Agente de Evidencias y Auditoría del PIMS (segunda entrega)

**Estado:** diseño v0.1 (2026-10-27), punto de control 1. El código del agente (fase 5) aún no está construido.

## 1. Objetivo

Apoyar la **auditoría interna del PIMS** de la UNSA (ISO/IEC 27701:2025, 9.2) en la plataforma GESTITEL (unsa.27k.pe): a partir de un alcance y de un conjunto de documentos de evidencia, el agente propone la lista de verificación con la evidencia encontrada, los hallazgos clasificados (N / O / M), los planes de acción y las conclusiones del informe. El equipo auditor revisa todo antes de cargarlo.

Corresponde a las tareas del sílabo: **diseño de agente** (objetivo, datos, contexto, herramientas), **orquestación** (coordinación de skills y flujos) y **proyecto agéntico** (solución funcional integrada).

## 2. Datos, contexto y herramientas

| Componente | Qué es en este agente |
|---|---|
| Datos de entrada | Plan de auditoría (objetivo, alcance, criterios, fechas) y carpeta de documentos de evidencia (.md, .txt o .pdf con texto) |
| Contexto | Catálogo de cláusulas 4–10, catálogo y elementos del Anexo A, plantillas de GESTITEL |
| Herramientas (skills) | **SK-02** evalúa evidencias por requisito · **SK-03** redacta hallazgos y planes de acción · **SK-04** redacta conclusiones · **SK-01** (primera entrega) evalúa una política de privacidad pública, si se entrega como evidencia |
| Herramientas (programa) | Lectura de documentos, selección del alcance, armado de lotes, verificación de citas y de formato, conteos, armado del informe y exportación a los campos de GESTITEL |
| Modelo | `gemini-3.5-flash-lite` (nivel gratuito de la API de Gemini) |

## 3. Flujo (orquestación)

```
Plan de auditoría + documentos
        │
 1. Programa: lee los documentos y les asigna código y secciones
 2. Programa: arma la lista de verificación
      · las 30 cláusulas 4–10
      · + los controles del Anexo A que los documentos citan expresamente
 3. Programa: divide la lista en lotes (≈ 5 lotes: 4–5, 6, 7–8, 9–10, Anexo A)
        │
 4. SK-02 (una llamada por lote) ──► verificación: citas literales en su documento,
        │                            una fila por requisito, resultado coherente con elementos
 5. Programa: une los lotes y calcula los conteos
 6. SK-03 (una llamada) ──► verificación: citas, responsables tomados de los documentos, fechas según la regla
 7. SK-04 (una llamada) ──► verificación: no menciona hallazgos inexistentes
 8. Programa: arma el informe, la lista de verificación y las fichas para GESTITEL
        │
 9. Revisión humana: el equipo auditor confirma, reclasifica o descarta cada propuesta
10. Carga manual en GESTITEL (módulo Auditorías)
```

**Llamadas a Gemini por auditoría:** unas 7 (5 de SK-02, 1 de SK-03, 1 de SK-04). Con el límite de 500 solicitudes diarias de `gemini-3.5-flash-lite` visto el 21-10-2026, la cuota no es una restricción.

**Si un documento es una política de privacidad pública**, el agente puede llamar además a SK-01 (una llamada) y adjuntar su resultado como evidencia de los controles A.1.3.x.

## 4. Salidas

| Archivo | Contenido | Destino en GESTITEL |
|---|---|---|
| `lista_verificacion.md` | Una fila por requisito: proceso, norma, requisito, evidencia encontrada, resultado propuesto | Ítems de la lista de verificación de la auditoría |
| `hallazgos.md` | Hallazgos N / O / M con descripción y evidencia | Hallazgos de la auditoría |
| `plan_accion.md` | Acción, responsable (rol), fecha propuesta, estado, avance | Planes de acción |
| `informe_auditoria.md` | Informe completo con conclusiones de SK-04 | Gestión Documental |
| `respuestas_originales/` | Respuestas de cada llamada, sin cambios | Evidencia del proceso (no se carga) |
| `verificacion.md` | Comprobaciones automáticas de cada paso | Evidencia del proceso |

## 5. Supervisión humana (puntos de control)

1. **Antes de ejecutar:** el auditor líder aprueba el plan y el alcance.
2. **Después de SK-02:** el equipo revisa los resultados N, O, M y «Sin evidencia» con sus citas.
3. **Antes de cargar en GESTITEL:** el equipo confirma hallazgos, responsables y fechas.

Nada se carga en la plataforma sin estas revisiones. El agente no tiene credenciales de GESTITEL ni acceso a su API.

## 6. Gobierno del agente

El sílabo menciona ISO/IEC 42001:2023 (sistemas de gestión de inteligencia artificial). No tenemos esa norma, así que no afirmamos cumplirla. Sí aplicamos prácticas de gobierno del uso de IA que el proyecto ya tiene:

- supervisión humana obligatoria y documentada (§5);
- trazabilidad: se guardan lo enviado, las respuestas originales y las verificaciones de cada paso;
- uso solo de datos sintéticos o públicos (el nivel gratuito permite que Google use lo enviado);
- límites declarados (§8) y métricas medidas, no supuestas (§7).

## 7. Cómo se medirá (fase 6)

Con los 14 documentos sintéticos de `simulacion/` y su clave (`simulacion/clave/clave_simulacion.md`, que nunca se envía al modelo):

- **detección** de los 13 vacíos sembrados;
- **clasificación** correcta (N / O / M);
- **falsos positivos** en requisitos que deberían ser conformes;
- **citas literales** (verificador).

Se ejecutará al menos dos veces para observar la variabilidad. Sesgo declarado: la misma IA redactó los documentos, la clave y las skills.

## 8. Límites

- Evalúa **evidencia documental**: no reemplaza entrevistas, observación en campo ni muestreo de registros en la plataforma.
- Catálogos comprobados por el equipo (cláusulas 4–10: 4 de 4; Anexo A y guías B: 18 de 18); `elementos.md` sigue pendiente de revisión humana.
- GESTITEL trae requisitos de ISO/IEC 27001:2022; el agente audita contra ISO/IEC 27701:2025 y no tiene una correspondencia oficial entre ambas.
- La carga en GESTITEL es manual y depende de que la cuenta del grupo tenga permisos en Auditorías.
