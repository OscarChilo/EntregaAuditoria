# SK-01 — Elementos por control (metodología del equipo)

> **Qué es:** la descomposición de cada control en elementos verificables, derivada de las paráfrasis del catálogo (`catalogo_iso27701.md` §4) y de sus orientaciones (§5).
> **Aclaraciones marcadas con †:** responden a errores observados en las pruebas con las dos políticas actuales (SisacApp + y UNSA general). Precisan lo que ya dice la paráfrasis, pero pueden favorecer el resultado en esos mismos documentos. Para medir si generalizan, hace falta un documento nuevo que no se haya usado para ajustar la Skill.
> **Qué no es:** no es texto de la ISO ni un requisito adicional. Es metodología del equipo, igual que la clasificación E / C / INT-i / INT (catálogo §2).
> **Estado:** borrador v0.3 (2026-10-21), **pendiente de revisión humana**. Copias anteriores en `historial/skill_v0.4/` y `historial/skill_v0.5/`.

## Cómo se usa

- Cada elemento tiene un código (E1, E2…) y una etiqueta:
  - **[aviso]**: puede evidenciarse en una política pública.
  - **[interno]**: solo se evidencia con documentos internos.
- **Cumple** (solo E, o C con aplicabilidad *Aplica*): **todos** los elementos [aviso] están respaldados por una cita pertinente y ninguno está contradicho. Los [interno] no se exigen para *Cumple*, pero se listan como "Falta (interno)".
- **Cumple parcialmente:**
  - en E y C: al menos un elemento [aviso] respaldado y al menos otro [aviso] faltante o contradicho;
  - en INT-i: basta **un** elemento [aviso] respaldado con una cita que trate ese elemento **específico**, porque los [interno] siempre faltan en una política pública. (En v0.1 esta regla estaba mal formulada para los controles internos.)
- **Dependencias:** "(depende de E1)" significa que el elemento **no** puede quedar respaldado si E1 falta. Por ejemplo, no hay mecanismo para ejercer un derecho que el documento no declara.
- **Sugerencias:** lo que aparece como "Sugerencia (O-xx)" **no** es un elemento: no cuenta para el estado y se recomienda aparte (`criterios.md` §5).
- La justificación recorre **todos** los elementos de la fila, en orden, con este formato:
  `E1 Respalda ← "cita" · E2 Falta · E3 Falta (interno) · E4 Contradicho ← "cita"`
- No se agregan, quitan ni fusionan elementos.

## Tabla A.1 (controles con fila propia; los INT no tienen elementos)

| ID | Cat. | Elementos |
|---|---|---|
| A.1.2.2 | E | E1 finalidades del tratamiento identificadas [aviso] · E2 finalidades específicas y delimitadas, sin finalidades abiertas o indeterminadas† [aviso] |
| A.1.2.3 | E | E1 base legal del tratamiento indicada [aviso] · E2 base legal vinculada a las finalidades identificadas [aviso] · E3 capacidad de demostrar el cumplimiento de la base legal [interno] |
| A.1.2.4 | INT-i | E1 cuándo se requiere el consentimiento [aviso] · E2 cómo se obtiene el consentimiento [aviso] · E3 proceso documentado para demostrar si, cuándo y cómo se obtuvo [interno] |
| A.1.2.5 | INT-i | E1 obtención del consentimiento según un proceso definido [aviso] · E2 registro del consentimiento obtenido [interno] |
| A.1.2.7 | INT-i | E1 identificación de proveedores que tratan datos por cuenta de la organización, calificados así por el documento† [aviso] · E2 contrato escrito con cada encargado [interno] · E3 el contrato aborda los controles de la Tabla A.2 [interno] |
| A.1.2.8 | INT-i | E1 existencia de un corresponsable declarada [aviso] · E2 roles y responsabilidades respectivos, incluidos protección y seguridad [interno] |
| A.1.3.2 | E | E1 obligaciones con los titulares documentadas (qué derechos u obligaciones existen) [aviso] · E2 medio para que el titular las haga efectivas [aviso] · E3 punto de contacto actualizado, por un medio similar al de la recolección [aviso] |
| A.1.3.3 | E | E1 qué información se entrega a los titulares [aviso] · E2 en qué momento o con qué frecuencia se entrega [aviso] |
| A.1.3.4 | E | E1 identificación del responsable [aviso] · E2 descripción del tratamiento [aviso] · E3 información clara y fácilmente accesible para el titular [aviso] |
| A.1.3.5 | C | E1 mecanismo para retirar el consentimiento [aviso] · E2 mecanismo para modificar el consentimiento [aviso] |
| A.1.3.6 | E | E1 posibilidad de oponerse al tratamiento, declarada [aviso] · E2 mecanismo para ejercer la oposición (depende de E1) [aviso] |
| A.1.3.7 | E | E1 acceso a los datos [aviso] · E2 corrección o rectificación [aviso] · E3 supresión o eliminación [aviso] · E4 medio para ejercerlos (depende de E1, E2 o E3) [aviso] |
| A.1.3.8 | INT-i | E1 se informa a los terceros con quienes se compartieron datos sobre modificaciones, retiros u oposiciones [aviso] · E2 políticas, procedimientos o mecanismos para hacerlo [interno] |
| A.1.3.9 | E | E1 entrega de una copia de los datos tratados al titular; el derecho de acceso o una remisión a "otros derechos" no la respaldan (B.1.3.3, B.1.3.9; criterios regla 16)† [aviso] · E2 cómo solicitarla (depende de E1) [aviso] |
| A.1.3.10 | E | E1 canal para presentar solicitudes [aviso] · E2 forma de presentar las solicitudes (requisitos o pasos) [aviso] · Sugerencia (O-23): plazo de respuesta |
| A.1.3.11 | C | E1 decisiones basadas solo en tratamiento automatizado, identificadas [aviso] · E2 obligaciones resultantes y cómo se atienden (depende de E1) [aviso] |
| A.1.4.2 | INT-i | E1 recolección limitada a lo necesario para las finalidades (criterio o declaración específica de minimización) [aviso] · E2 objetivos o mecanismos de limitación documentados [interno] |
| A.1.4.3 | INT-i | E1 tratamiento limitado a lo necesario para las finalidades identificadas [aviso] · E2 mecanismos de limitación documentados [interno] |
| A.1.4.4 | INT-i | E1 medidas para mantener los datos exactos y actualizados [aviso] · E2 aseguramiento documentado durante el ciclo de vida [interno] |
| A.1.4.6 | INT-i | E1 eliminación o anonimización cuando los datos dejan de ser necesarios para la finalidad (no solo a pedido del titular)† [aviso] · E2 procedimiento documentado [interno] |
| A.1.4.8 | E | E1 plazo o criterio de conservación [aviso] · E2 conservación limitada a lo necesario para la finalidad [aviso] |
| A.1.4.9 | INT-i | E1 forma de eliminación de los datos (procedimiento o mecanismo, no el derecho del titular)† [aviso] · E2 políticas o procedimientos de eliminación documentados [interno] |
| A.1.4.10 | INT-i | E1 controles concretos sobre la transmisión de datos por redes (p. ej., una tecnología o un procedimiento nombrado); una mención genérica a seguridad no los respalda† [aviso] · E2 controles documentados que aseguran que los datos llegan a su destino [interno] |
| A.1.5.2 | C | E1 base para las transferencias entre jurisdicciones [aviso] |
| A.1.5.3 | C | E1 países u organismos internacionales de destino [aviso] |

## Tabla A.3 — controles INT-i

| ID | Elementos |
|---|---|
| A.3.3 | E1 existencia de una política de seguridad de la información aplicable a los datos personales, identificada por su nombre, alcance o contenido; una mención genérica a "medidas de seguridad" no la respalda (criterios regla 4)† [aviso] · E2 aprobación, comunicación y revisión de esa política [interno] |
| A.3.7 | E1 reglas, procedimientos o acuerdos para la transferencia de información [aviso] · E2 aplicación a todos los medios de transferencia [interno] |
| A.3.9 | E1 asignación, revisión o retiro de derechos de acceso a los datos [aviso] · E2 política de control de acceso [interno] |
| A.3.10 | E1 requisitos de seguridad acordados con proveedores [aviso] · E2 acuerdos según el tipo de relación [interno] |
| A.3.11 | E1 proceso de gestión de incidentes de seguridad, con roles [aviso] · E2 planificación y comunicación del proceso [interno] |
| A.3.13 | E1 requisitos legales, reglamentarios o contractuales de seguridad identificados; citar una ley de protección de datos en general no los identifica† [aviso] · E2 documentación actualizada del enfoque [interno] |
| A.3.18 | E1 acuerdos de confidencialidad con personal o terceros [aviso] · E2 revisión periódica y firma [interno] |
| A.3.23 | E1 tecnología o procedimiento de autenticación descrito [aviso] · E2 autenticación segura según restricciones de acceso [interno] |
| A.3.26 | E1 uso de criptografía para los datos (medida concreta) [aviso] · E2 reglas de criptografía y gestión de claves [interno] |

## Historial

- **v0.1** (2026-10-21): primera versión (Skill v0.4).
- **v0.2** (2026-10-21):
  - categorías E / C / INT-i en lugar de D / D\* / I;
  - regla de *Cumple parcialmente* corregida para INT-i;
  - dependencias explícitas: A.1.3.6 E2, A.1.3.7 E4, A.1.3.9 E2 y A.1.3.11 E2;
  - en A.1.3.10, E2 pasa a "forma de presentar las solicitudes", y el plazo de respuesta queda como sugerencia (O-23).
- **v0.3** (2026-10-21): aclaraciones generales (marcadas con †) para A.1.3.9 E1 (acceso ≠ copia), A.3.3 E1, A.3.13 E1 y A.1.4.10 E1 (una mención genérica de seguridad no demuestra una política ni un control). No cambian los códigos ni las dependencias.
