# Plan de tratamiento de riesgos de privacidad y declaración de aplicabilidad 2026

> **DOCUMENTO SINTÉTICO — SIMULACIÓN ACADÉMICA.** Elaborado para el TIF de Auditoría de Sistemas (UNSA, 2026-B). No es un documento oficial de la Universidad Nacional de San Agustín de Arequipa. Unidades, personas, cargos, correos y cifras son ficticios.

| Campo | Valor |
|---|---|
| Código | SIM-PIMS-05 |
| Versión | 0.9 |
| Fecha | 2026-07-15 |
| Elaborado por | Oficina de Protección de Datos Personales (OPDP) |
| Estado | Presentado al CPSI; **pendiente de aprobación** |
| Clasificación | Uso interno |

## 1. Propósito

Documentar el tratamiento de los riesgos de privacidad del periodo 2026, los controles seleccionados y la declaración de aplicabilidad, según las cláusulas 6.1.3 y 8.3 de ISO/IEC 27701:2025.

## 2. Resultado de la evaluación (periodo 2026)

La evaluación del periodo abril–junio 2026 (SIM-PIMS-04) identificó 24 riesgos: 2 extremos, 6 altos, 10 medios y 6 bajos.

## 3. Opciones de tratamiento y controles

| Riesgo | Nivel | Dueño | Opción | Controles seleccionados (ISO/IEC 27701:2025) | Responsable | Plazo | Avance al 2026-10-15 |
|---|---|---|---|---|---|---|---|
| R-01 Acceso no autorizado al sistema académico por credenciales robadas | Extremo (12) | Dir. Registro Académico | Mitigar | A.3.8 Gestión de identidades, A.3.23 Autenticación segura (doble factor) | Jefe OUIS | 2026-09-30 | 100 % |
| R-02 Fichas socioeconómicas en papel sin resguardo en Bienestar | Extremo (12) | Dir. Bienestar | Mitigar | A.3.14 Protección de registros, A.1.4.9 Eliminación | Dir. Bienestar | 2026-12-15 | 40 % |
| R-03 Proveedor de la plataforma de aulas virtuales sin contrato de encargo | Alto (9) | Dir. Académico | Mitigar | A.1.2.7 Contratos con encargados, A.3.10 Seguridad en acuerdos con proveedores | Asesoría Jurídica | 2026-11-30 | 60 % |
| R-04 Conservación indefinida de datos de la bolsa de trabajo | Alto (8) | Dir. Bolsa de Trabajo | Mitigar | A.1.4.8 Conservación, A.1.4.6 Eliminación al final del tratamiento | Dir. Bolsa de Trabajo | 2026-12-31 | 10 % |
| R-05 Envío de listas de notas por correo sin cifrar | Alto (8) | Decanos | Mitigar | A.1.4.10 Controles de transmisión, A.3.26 Criptografía | Jefe OUIS | 2026-10-31 | 75 % |
| R-06 Publicación de resultados de admisión con DNI completo | Alto (9) | Dir. Admisión | Mitigar | A.1.4.2 Limitar la recolección, A.1.4.3 Limitar el tratamiento | Dir. Admisión | 2026-08-31 | 100 % |
| R-07 a R-24 | Medio o bajo | Varios | Aceptar con seguimiento | Controles existentes | Dueños de proceso | — | — |

Los controles se determinaron a partir de la evaluación de riesgos y se compararon con el Anexo A de ISO/IEC 27701:2025 para verificar que no se omitiera ninguno necesario. Para implementarlos se consideró la guía del Anexo B.

## 4. Programa de seguridad de la información

La Universidad aplica el programa de seguridad de la información de la OUIS («Plan de seguridad de TI 2026», simulado), que abarca la gestión de riesgos de seguridad, políticas, organización, seguridad del personal, gestión de activos, control de acceso, seguridad de las operaciones y de las redes, desarrollo seguro, proveedores, incidentes, continuidad, revisiones de seguridad, criptografía y seguridad física.

## 5. Declaración de aplicabilidad (extracto)

| Control | ¿Aplica? | Justificación | ¿Implementado? |
|---|---|---|---|
| A.1.2.2 Identificar y documentar la finalidad | Sí | Requisito legal y del registro de tratamientos | Sí |
| A.1.2.6 Evaluación de impacto en la privacidad | Sí | Tratamientos de datos sensibles en Bienestar | Parcial |
| A.1.2.7 Contratos con encargados | Sí | Uso de proveedores en la nube (R-03) | Parcial |
| A.1.3.11 Decisiones automatizadas | No | La Universidad no toma decisiones basadas únicamente en tratamiento automatizado; la admisión incluye revisión humana de resultados | — |
| A.1.5.2 Base para transferencias entre jurisdicciones | Sí | El proveedor de aulas virtuales aloja datos fuera del país | Parcial |
| A.2.x Controles para encargados | Sí | Rol de encargado en el Centro de Idiomas (ver SIM-PIMS-01) | Parcial |
| A.3.23 Autenticación segura | Sí | Riesgo R-01 | Sí |

La declaración completa, con los controles restantes, se mantiene en la pestaña «Anexo A» de la Matriz de Brecha de la plataforma PIMS.

## 6. Riesgo residual

Después del tratamiento se estima que R-01, R-05 y R-06 quedan en nivel medio, y R-02, R-03 y R-04 en nivel alto hasta completar sus acciones.

> Nota de la OPDP: el plan se presentó al CPSI el 2026-07-20. La firma de los dueños de riesgo y la aceptación del riesgo residual se programaron para la siguiente sesión del comité.

## 7. Seguimiento

La OPDP actualiza el avance de cada acción en el módulo de Riesgos de la plataforma PIMS y lo informa al CPSI cada trimestre.
