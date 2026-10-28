# Catálogo de referencia ISO/IEC 27701:2025 — SK-01 Evaluación de Cumplimiento de Privacidad

**Versión:** 0.6.2 · **Estado:** comprobación humana completa: 18 de 18 (V-01 a V-18; ver §6). El catálogo está validado por el equipo en las referencias y paráfrasis registradas en §6; `elementos.md` sigue pendiente de revisión humana.

> **Fuente:** ISO/IEC 27701:2025(en), 2.ª edición (reemplaza a la de 2019; redactada como norma de sistema de gestión autónoma).
> **Naturaleza del texto:** paráfrasis en español elaboradas por el equipo con apoyo de IA. No son traducciones oficiales. Para citar literalmente, usar el PDF original.
> **Paginación:** "Pág. norma" = número impreso al pie; "Pág. PDF" = página del archivo `ISO 27701-2025.pdf`. **Pág. PDF = Pág. norma + 6.**
> **Cómo se transcribió:** a partir de la lectura de las imágenes de las páginas indicadas (el PDF no tiene capa de texto y el OCR automático altera los identificadores, p. ej. "A.13.2" en lugar de "A.1.3.2"). La validación humana está en curso; ver §6.

---

## 0. Cobertura declarada

| Parte de ISO/IEC 27701:2025 | Uso en la Skill |
|---|---|
| **Anexo A**: 78 controles (Tablas A.1: 31, A.2: 18, A.3: 29) | **Criterios evaluados.** Todos se recorren en cada evaluación. |
| **Anexo B**: guía seleccionada (B.1.2.2–B.1.2.5, B.1.3.2–B.1.3.11, B.1.4.2–B.1.4.10, B.1.5.2–B.1.5.3) | **Orientaciones** para interpretar los controles y redactar recomendaciones (§5). No reciben estado ni son obligaciones. |
| Anexo B: B.1.2.6–B.1.2.9, B.1.5.4–B.1.5.5, B.2 (encargados) y la guía de la Tabla A.3 | No catalogados |
| Cláusulas 1–11 (incluido el sistema de gestión, cl. 4–10) | No evaluadas; la cl. 5.2 figura solo como referencia (§4.4) |
| Anexos C–F (correspondencias) | No incluidos |

**Forma correcta de presentarlo:** "evaluación documental de políticas de privacidad frente a los 78 controles del Anexo A de ISO/IEC 27701:2025, con orientaciones seleccionadas del Anexo B". **No** es una evaluación de toda la norma ni del sistema de gestión.

---

## 1. Tipos de referencia: controles vs. orientaciones

El catálogo distingue dos tipos de referencia. **Solo los controles reciben estado.**

| Tipo | Origen en la norma | Redacción en la norma | Uso en la Skill |
|---|---|---|---|
| **Control** (criterio de evaluación) | Anexo A (normativo), Tablas A.1, A.2 y A.3 | "The organization **shall**…" | Se evalúa y recibe uno de los estados definidos en `criterios.md`. |
| **Orientación de implementación** | Anexo B (normativo), apartados "Implementation guidance" | "should…" | Sirve para **interpretar** el control y redactar **recomendaciones**. **No recibe estado propio** ni se reporta como incumplimiento por sí sola. |
| **Ejemplo o posibilidad** | Anexo B: listas de ejemplos (p. ej., B.1.3.3), "can…", "some jurisdictions…" | "can…" / "examples…" | Solo para **sugerencias**. Nunca se convierte en obligación ni en incumplimiento automático. |

Notas:
- Cada control A.x.y.z tiene su guía en B.x.y.z (nota del Anexo A, Pág. norma 15 / PDF 21).
- En particular, la lista de B.1.3.3 se presenta en la norma como **ejemplos** de información que *puede* darse al titular, y esa información "puede tomar la forma de un aviso". Que un elemento de esa lista falte en la política se reporta como **observación** dentro del control relacionado (A.1.3.3 / A.1.3.4 u otro), no como un requisito incumplido.
- Por el Anexo A, la organización puede excluir controles justificándolo en su Declaración de Aplicabilidad (cl. 6.1.3 e). La Skill no conoce esa declaración, salvo que se la entreguen.

---

## 2. Clasificación metodológica de los controles (metodología del equipo)

> **Importante:** esta clasificación es una **selección metodológica del equipo** para evaluar **políticas de privacidad públicas**. **No figura en ISO/IEC 27701** y **no es una obligación universal de publicación**. Una organización puede documentar esa información en otros medios (formularios, avisos al recolectar los datos, contratos) o haber excluido controles en su Declaración de Aplicabilidad (cl. 6.1.3 e). Por eso un vacío en la política es un **vacío documental de ese documento**, no un incumplimiento de la organización.
> Reemplaza a la clasificación D / I / N (v0.2–v0.5) con la misma pertenencia: D → E, D\* → C, I → INT-i, N → INT; la Tabla A.2 (rol) pasa a C.

| Categoría | Qué significa para una política pública | Si la política no dice nada | Recomendación permitida |
|---|---|---|---|
| **E — Información esencial** | El control es incondicional en el Anexo A ("shall") y su guía lo vincula con la información al titular (A.1.3.3, A.1.3.4 y los ejemplos de B.1.3.3) | *No evidenciado* + información faltante | "Completar la política: …" (requisito del control) |
| **C — Información condicional según el tratamiento** | Solo aplica si existe la situación: consentimiento, decisiones automatizadas, transferencias entre jurisdicciones o rol de encargado | Aplicabilidad **por determinar** → *No determinado* + información necesaria. **No es un vacío.** | "Aclarar aplicabilidad: …"; si aplica, "Completar la política: …" |
| **INT-i — Evidencia interna, con posibles indicios** | Se cumple con documentos internos; la política solo puede dar indicios | *No determinado* | "Solicitar evidencia interna: …". **Nunca** "Completar la política". |
| **INT — Evidencia interna** | Control interno; no se espera en una política pública | *No determinado* | "Solicitar evidencia interna: …" |

**Aplicabilidad de C:** *Aplica* si el documento declara la situación (con cita). *No aplica* solo si el documento la descarta expresamente (con cita). En cualquier otro caso, incluidos el silencio y los indicios, queda *Por determinar*.

### 2.1 Fundamento de la clasificación (referencias leídas en el PDF; ver §6)

- **E:** A.1.3.3 y A.1.3.4 (pág. 16 / PDF 22) piden determinar y entregar al titular información clara. B.1.3.3 (25–26 / 31–32) da **ejemplos** de esa información: finalidad, contacto, base legal, derechos (acceso, rectificación, supresión, copia, oposición), conservación, entre otros. Los controles A.1.3.6 y A.1.3.9 son incondicionales en el Anexo A. B.1.3.6 y B.1.3.9 mencionan jurisdicciones solo para el alcance legal o la portabilidad, que se tratan como orientaciones.
- **C:** el propio control o su guía depende de una situación: consentimiento (A.1.3.5; B.1.2.3), decisiones automatizadas (A.1.3.11; B.1.3.11), transferencias entre jurisdicciones (A.1.5.2–A.1.5.3; B.1.5.2–B.1.5.3) y rol de encargado (Tabla A.2; nota del Anexo A).
- **INT-i / INT:** los controles piden documentar procesos, mantener registros o contratos, o aplicar mecanismos internos (Anexo A, 15–20 / 21–26; B.1.3.8, B.1.4.2–B.1.4.10, B.1.5.4–B.1.5.5).

### 2.2 Referencias de guía por control (las usa la plantilla de la matriz)

| ID | Cat. | Guía del Anexo B | Nota |
|---|---|---|---|
| A.1.2.2 | E | B.1.2.2, B.1.3.3 | — |
| A.1.2.3 | E | B.1.2.3, B.1.3.3 | La demostración del cumplimiento es interna |
| A.1.3.2 | E | B.1.3.2 | — |
| A.1.3.3 | E | B.1.3.3 | Los ejemplos de B.1.3.3 se revisan en la lista "Información al titular" |
| A.1.3.4 | E | B.1.3.3, B.1.3.4 | — |
| A.1.3.6 | E | B.1.3.3, B.1.3.6 | — |
| A.1.3.7 | E | B.1.3.3, B.1.3.7 | — |
| A.1.3.9 | E | B.1.3.3, B.1.3.9 | La portabilidad es solo una orientación (B.1.3.9: «some jurisdictions») |
| A.1.3.10 | E | B.1.3.2, B.1.3.10 | El plazo de respuesta es una recomendación, no un elemento esencial |
| A.1.4.8 | E | B.1.3.3, B.1.4.8 | Los calendarios de conservación (B.1.4.8) son internos |
| A.1.3.5 | C | B.1.3.3, B.1.3.5 | Condición: algún tratamiento se basa en el consentimiento |
| A.1.3.11 | C | B.1.3.3, B.1.3.11 | Condición: existen decisiones basadas solo en tratamiento automatizado |
| A.1.5.2 | C | B.1.3.3, B.1.5.2 | Condición: hay transferencias a otra jurisdicción |
| A.1.5.3 | C | B.1.3.3, B.1.5.3 | Ídem |
| A.1.2.4 | INT-i | B.1.2.4 | — |
| A.1.2.5 | INT-i | B.1.2.5 | — |
| A.1.3.8 | INT-i | B.1.3.8 | — |
| A.1.4.2 | INT-i | B.1.4.2 | — |
| A.1.4.3 | INT-i | B.1.4.3 | — |
| A.1.4.4 | INT-i | B.1.4.4 | — |
| A.1.4.6 | INT-i | B.1.4.6 | — |
| A.1.4.9 | INT-i | B.1.4.9 | — |
| A.1.4.10 | INT-i | B.1.4.10 | — |

Los controles sin fila en esta tabla no tienen guía del Anexo B catalogada: A.1.2.7, A.1.2.8, los INT, la Tabla A.3 y la Tabla A.2.

---

## 3. Estados y reglas de asignación

Desde la v0.4, los estados y las reglas de decisión están en **`criterios.md`**, que es su única fuente. Estados: *Cumple*, *Cumple parcialmente*, *No evidenciado*, *Incumplimiento documental sustentado*, *No determinado* y *No aplica*. Este catálogo conserva las referencias ISO, la clasificación metodológica (§2) y las orientaciones (§5).

---

## 4. Criterios basados en controles (Anexo A)

### 4.1 Tabla A.1 — Controles para responsables del tratamiento (PII controllers)

La UNSA aparece como **responsable** en las políticas de prueba; esta es la tabla principal.

**Condiciones para la recolección y el tratamiento** — Pág. norma 15 / PDF 21
Objetivo: demostrar que el tratamiento es lícito, con base legal y finalidades definidas y legítimas.

| ID | Título (en) | Paráfrasis del control | Cat. | Orientación relacionada (§5) |
|---|---|---|---|---|
| A.1.2.2 | Identify and document purpose | Identificar y documentar las finalidades específicas del tratamiento. | E | O-01 |
| A.1.2.3 | Identify lawful basis | Determinar y documentar la base legal pertinente del tratamiento para las finalidades identificadas, y poder demostrar su cumplimiento. | E | O-03, O-17 |
| A.1.2.4 | Determine when and how consent is to be obtained | Documentar un proceso que permita demostrar si, cuándo y cómo se obtuvo el consentimiento. | INT-i | O-18 |
| A.1.2.5 | Obtain and record consent | Obtener y registrar el consentimiento según los procesos documentados. | INT-i | O-18 |
| A.1.2.6 | Privacy impact assessment | Evaluar la necesidad de una evaluación de impacto en la privacidad siempre que se planifique un tratamiento nuevo o un cambio en uno existente, y realizarla cuando corresponda. | INT | — |
| A.1.2.7 | Contracts with PII processors | Tener un contrato escrito con cada encargado que utilice y asegurar que esos contratos aborden la implementación de los controles apropiados del Anexo A (ver Tabla A.2). | INT-i | — |
| A.1.2.8 | Joint PII controller | Determinar los roles y responsabilidades respectivos en el tratamiento (incluidos los requisitos de protección y seguridad de los datos) con cualquier corresponsable. | INT-i | — |
| A.1.2.9 | Records related to processing PII | Determinar y mantener de forma segura los registros necesarios para respaldar sus obligaciones en el tratamiento de datos personales. | INT | — |

**Obligaciones con los titulares** — Pág. norma 16 / PDF 22
Objetivo: que los titulares reciban información adecuada sobre el tratamiento y que se cumplan las demás obligaciones aplicables.

| ID | Título (en) | Paráfrasis del control | Cat. | Orientación relacionada |
|---|---|---|---|---|
| A.1.3.2 | Determining and fulfilling obligations to PII principals | Determinar y documentar las obligaciones legales, regulatorias y de negocio con los titulares, y ofrecer los medios para cumplirlas. | E | O-06, O-16 |
| A.1.3.3 | Determining information for PII principals | Determinar y documentar qué información se entrega a los titulares y en qué momento. | E | O-01 a O-14 |
| A.1.3.4 | Providing information to PII principals | Dar a los titulares información clara y fácilmente accesible que identifique al responsable y describa el tratamiento. | E | O-02, O-15 |
| A.1.3.5 | Providing mechanism to modify or withdraw consent | Ofrecer un mecanismo para modificar o retirar el consentimiento. | C (si algún tratamiento se basa en el consentimiento) | O-07 |
| A.1.3.6 | Providing mechanism to object to PII processing | Ofrecer un mecanismo para oponerse al tratamiento. | E | O-06 |
| A.1.3.7 | Access, correction or erasure | Implementar políticas, procedimientos o mecanismos para el acceso, la rectificación o la supresión. | E | O-06 |
| A.1.3.8 | PII controllers' obligations to inform third parties | Informar a los terceros con quienes se compartieron datos sobre cualquier modificación, retiro u oposición relativa a esos datos, e implementar políticas, procedimientos o mecanismos apropiados para hacerlo. | INT-i | — |
| A.1.3.9 | Providing copy of PII processed | Poder entregar al titular una copia de sus datos cuando la solicite. | E | O-06 |
| A.1.3.10 | Handling requests | Definir y documentar políticas y procedimientos para atender solicitudes legítimas de los titulares. | E | O-16 |
| A.1.3.11 | Automated decision making | Identificar las obligaciones derivadas de decisiones basadas solo en tratamiento automatizado y demostrar cómo se atienden. | C (si existen decisiones automatizadas) | O-11 |

**Privacidad desde el diseño y por defecto** — Pág. norma 16–17 / PDF 22–23
Objetivo: limitar la recolección y el tratamiento (uso, divulgación, conservación, transmisión y eliminación) a lo necesario para la finalidad.

| ID | Título (en) | Paráfrasis del control | Cat. | Pág. norma / PDF |
|---|---|---|---|---|
| A.1.4.2 | Limit collection | Limitar la recolección al mínimo relevante, proporcional y necesario. | INT-i | 16 / 22 |
| A.1.4.3 | Limit processing | Limitar el tratamiento a lo adecuado, relevante y necesario. | INT-i | 16 / 22 |
| A.1.4.4 | Accuracy and quality | Asegurar y documentar que los datos sean exactos, completos y actualizados durante su ciclo de vida. | INT-i | 16 / 22 |
| A.1.4.5 | PII minimization objectives | Definir objetivos de minimización y los mecanismos para cumplirlos (p. ej., desidentificación). | INT | 16 / 22 |
| A.1.4.6 | PII de-identification and deletion at the end of processing | Eliminar los datos o transformarlos de modo que no permitan identificar ni reidentificar a los titulares, tan pronto como dejen de ser necesarios para las finalidades identificadas. | INT-i | 16 / 22 |
| A.1.4.7 | Temporary files | Eliminar los archivos temporales según procedimientos y plazos documentados. | INT | 16 / 22 |
| A.1.4.8 | Retention | No conservar los datos más tiempo del necesario para la finalidad. | E | 17 / 23 |
| A.1.4.9 | Disposal | Tener políticas, procedimientos o mecanismos documentados para la eliminación. | INT-i | 17 / 23 |
| A.1.4.10 | PII transmission controls | Aplicar controles a la transmisión por redes para que los datos lleguen a su destino previsto. | INT-i | 17 / 23 |

Orientación relacionada: A.1.4.8 → O-10.

**Compartición, transferencia y divulgación** — Pág. norma 17 / PDF 23
Objetivo: determinar si los datos se comparten, se transfieren a otras jurisdicciones o a terceros, o se divulgan, y documentar cuándo ocurre, de acuerdo con las obligaciones aplicables.

| ID | Título (en) | Paráfrasis del control | Cat. | Orientación relacionada |
|---|---|---|---|---|
| A.1.5.2 | Identify basis for PII transfer between jurisdictions | Identificar y documentar la base para transferencias entre jurisdicciones. | C (si hay transferencias a otra jurisdicción) | O-08 |
| A.1.5.3 | Countries and international organizations to which PII can be transferred | Especificar y documentar los países y organismos internacionales a los que pueden transferirse los datos. | C (ídem) | O-08 |
| A.1.5.4 | Records of transfer of PII | Registrar las transferencias hacia y desde terceros y cooperar con ellos para atender a los titulares. | INT | — |
| A.1.5.5 | Records of PII disclosures to third parties | Registrar las divulgaciones a terceros: qué datos, a quién y cuándo. | INT | O-09 (solo como contexto) |

### 4.2 Tabla A.2 — Controles para encargados del tratamiento (PII processors)

Pág. norma 17–18 / PDF 23–24. **Sin estado por defecto.** El estado de la Tabla A.2 depende del **rol de la organización justificado con el propio documento** (regla 8 de `criterios.md`): *No aplica* solo si una cita identifica a la organización como responsable del tratamiento evaluado y nada indica que trate datos por encargo de un cliente; *No determinado* si el documento no permite establecer el rol. Si el documento describe a la organización actuando como encargada, la tabla se activa y sus controles son **INT**. **Categoría: C (según el rol).**

| ID | Título (en) | ID | Título (en) |
|---|---|---|---|
| A.2.2.2 | Customer agreement | A.2.4.4 | PII transmission controls |
| A.2.2.3 | Organization's purposes | A.2.5.2 | Basis for PII transfer between jurisdictions |
| A.2.2.4 | Marketing and advertising use | A.2.5.3 | Countries and international organizations to which PII can be transferred |
| A.2.2.5 | Infringing instruction | A.2.5.4 | Records of PII disclosures to third parties |
| A.2.2.6 | Customer obligations | A.2.5.5 | Notification of PII disclosure requests |
| A.2.2.7 | Records related to processing PII | A.2.5.6 | Legally binding PII disclosures |
| A.2.3.2 | Comply with obligations to PII principals | A.2.5.7 | Disclosure of subcontractors used to process PII |
| A.2.4.2 | Temporary files | A.2.5.8 | Engagement of a subcontractor to process PII |
| A.2.4.3 | Return, transfer or disposal of PII | A.2.5.9 | Change of subcontractor to process PII |

### 4.3 Tabla A.3 — Controles de seguridad para responsables y encargados

Pág. norma 18–20 / PDF 24–26. Objetivo: asegurar la seguridad del tratamiento de datos personales.
Una mención genérica de seguridad se registra como evidencia, pero **no** fija un estado por sí sola (regla 4 de `criterios.md`). Un control **INT-i** de esta tabla puede llegar a *Cumple parcialmente* solo si la política describe una medida concreta vinculada a ese control (p. ej., un método de autenticación específico para A.3.23).

| ID | Título (en) | Cat. | Pág. norma / PDF |
|---|---|---|---|
| A.3.3 | Policies for information security | INT-i | 18 / 24 |
| A.3.4 | Information security roles and responsibilities | INT | 18 / 24 |
| A.3.5 | Classification of information | INT | 19 / 25 |
| A.3.6 | Labelling of information | INT | 19 / 25 |
| A.3.7 | Information transfer | INT-i | 19 / 25 |
| A.3.8 | Identity management | INT | 19 / 25 |
| A.3.9 | Access rights | INT-i | 19 / 25 |
| A.3.10 | Addressing information security within supplier agreements | INT-i | 19 / 25 |
| A.3.11 | Information security incident management planning and preparation | INT-i | 19 / 25 |
| A.3.12 | Response to information security incidents | INT | 19 / 25 |
| A.3.13 | Legal, statutory, regulatory and contractual requirements | INT-i | 19 / 25 |
| A.3.14 | Protection of records | INT | 19 / 25 |
| A.3.15 | Independent review of information security | INT | 19 / 25 |
| A.3.16 | Compliance with policies, rules and standards for information security | INT | 19 / 25 |
| A.3.17 | Information security awareness, education and training | INT | 19 / 25 |
| A.3.18 | Confidentiality or non-disclosure agreements | INT-i | 19 / 25 |
| A.3.19 | Clear desk and clear screen | INT | 19 / 25 |
| A.3.20 | Storage media | INT | 19 / 25 |
| A.3.21 | Secure disposal or re-use of equipment | INT | 20 / 26 |
| A.3.22 | User endpoint devices | INT | 20 / 26 |
| A.3.23 | Secure authentication | INT-i | 20 / 26 |
| A.3.24 | Information backup | INT | 20 / 26 |
| A.3.25 | Logging | INT | 20 / 26 |
| A.3.26 | Use of cryptography | INT-i | 20 / 26 |
| A.3.27 | Secure development life cycle | INT | 20 / 26 |
| A.3.28 | Application security requirements | INT | 20 / 26 |
| A.3.29 | Secure system architecture and engineering principles | INT | 20 / 26 |
| A.3.30 | Outsourced development | INT | 20 / 26 |
| A.3.31 | Test information | INT | 20 / 26 |

### 4.4 Requisito del sistema de gestión relacionado: cláusula 5.2

| ID | Título | Paráfrasis | Pág. norma / PDF | Cat. |
|---|---|---|---|---|
| 5.2 | Privacy policy | La alta dirección establece una política de privacidad que: a) es adecuada al propósito de la organización; b) da un marco para fijar objetivos de privacidad; c) incluye un compromiso de cumplir los requisitos aplicables; d) incluye un compromiso de mejora continua del PIMS. Esa política debe estar disponible como información documentada, comunicarse dentro de la organización y estar disponible para las partes interesadas, según corresponda. | 6–7 / 12–13 | — (no se evalúa) |

**Nota:** la cl. 5.2 se refiere a la política *interna* del PIMS, aprobada por la alta dirección. Un aviso público de privacidad **no** es necesariamente ese documento. Por eso la Skill no evalúa la cl. 5.2 sobre un aviso. Si el aviso contiene un compromiso de cumplir la normativa, se registra como observación, sin asignar estado a 5.2.

---

## 5. Orientaciones de implementación (Anexo B) — sin estado propio

Sirven para **interpretar** los controles, saber **qué buscar** y redactar **recomendaciones**. **Ninguna orientación es un requisito ni genera un incumplimiento automático.** Las recomendaciones que se basan en orientaciones se rotulan "Sugerencia (orientación)", separadas de los requisitos del control.

| Grupo | Uso en el informe |
|---|---|
| O-01 a O-16 (§5.1) | Lista **"Información al titular"**: se recorre completa en cada informe, aunque la política no mencione el punto. Son **ejemplos** de B.1.3.3 y B.1.3.4; su resultado (Presente / Parcial / Ausente / No aplica / Por determinar) alimenta la justificación de A.1.3.3 y A.1.3.4, pero **no genera estados propios**. |
| O-17 y O-18 (§5.2) | **No** forman parte de esa lista: no son información al titular, sino orientaciones para **interpretar** la base legal y el consentimiento (A.1.2.3–A.1.2.5). Se usan en las justificaciones y sugerencias; no generan estados ni observaciones obligatorias. |
| O-19 a O-30 (§5.3) | Orientaciones nuevas (v0.6) para interpretar los controles y redactar recomendaciones o pedidos de evidencia interna. |

### 5.1 Información para el titular — B.1.3.3 y B.1.3.4

La columna "Cat. en la lista" es metodología del equipo: indica si el punto se espera siempre (E) o solo según el tratamiento (C). Un punto ausente es una **sugerencia**, no un incumplimiento, salvo que coincida con un elemento [aviso] de un control E o C aplicable.

B.1.3.3 (Pág. norma 25–26 / PDF 31–32) los presenta como *ejemplos* de información que puede entregarse. La misma guía indica que la organización debería determinar los requisitos legales, regulatorios o de negocio para entregar información al titular (p. ej., antes del tratamiento) y para el tipo de información a entregar.

| ID | Qué buscar en la política | Fuente | Control al que aporta | Pág. norma / PDF | Cat. en la lista |
|---|---|---|---|---|---|
| O-01 | Finalidad(es) del tratamiento | B.1.3.3 (remite a B.1.2.2) | A.1.2.2, A.1.3.3 | 25 / 31 | E |
| O-02 | Datos de contacto del responsable o su representante | B.1.3.3 | A.1.3.4 | 25 / 31 | E |
| O-03 | Base legal del tratamiento | B.1.3.3 (remite a B.1.2.3) | A.1.2.3, A.1.3.3 | 25 / 31 | E |
| O-04 | Origen de los datos, si no se obtienen del titular | B.1.3.3 | A.1.3.3 | 25 / 31 | C (si hay datos no obtenidos del titular) |
| O-05 | Si entregar los datos es requisito legal o contractual y qué pasa si no se entregan | B.1.3.3 | A.1.3.3 | 25 / 31 | E |
| O-06 | Derechos y cómo ejercerlos: acceso, modificación, rectificación, supresión, copia y oposición | B.1.3.3 (remite a B.1.3.2) | A.1.3.2, A.1.3.6, A.1.3.7, A.1.3.9 | 25 / 31 | E |
| O-07 | Cómo retirar el consentimiento | B.1.3.3 (remite a B.1.3.5) | A.1.3.5 | 25 / 31 | C (si hay tratamientos basados en el consentimiento) |
| O-08 | Transferencias de datos | B.1.3.3 | A.1.5.2, A.1.5.3 | 25 / 31 | C (si hay transferencias) |
| O-09 | Destinatarios o categorías de destinatarios | B.1.3.3 | A.1.3.3 | 25 / 31 | E |
| O-10 | Plazo de conservación | B.1.3.3 | A.1.4.8, A.1.3.3 | 26 / 32 | E |
| O-11 | Uso de decisiones automatizadas | B.1.3.3 | A.1.3.11 | 26 / 32 | C (si hay decisiones automatizadas) |
| O-12 | Derecho a presentar una reclamación y cómo hacerlo | B.1.3.3 | A.1.3.3 | 26 / 32 | E |
| O-13 | Frecuencia o momento en que se entrega la información (p. ej., *just in time*) | B.1.3.3 | A.1.3.3 | 26 / 32 | E |
| O-14 | Actualización de la información si cambian o se amplían las finalidades | B.1.3.3 | A.1.3.3 | 26 / 32 | E |
| O-15 | Forma: oportuna, concisa, completa, transparente, inteligible, en lenguaje claro y fácilmente accesible, adecuada al público destinatario; entregada al recolectar los datos cuando corresponda y accesible de forma permanente | B.1.3.4 | A.1.3.4 | 26 / 32 | E |
| O-16 | Punto de contacto actualizado para solicitudes, por un medio similar al usado para recolectar los datos (p. ej., web o correo, no teléfono o fax) | B.1.3.2 | A.1.3.2, A.1.3.10 | 25 / 31 | E |

### 5.2 Base legal y consentimiento — B.1.2.3, B.1.2.4 y B.1.2.5

| ID | Qué buscar en la política | Fuente | Control al que aporta | Pág. norma / PDF |
|---|---|---|---|---|
| O-17 | Bases legales que pueden servir de fundamento: consentimiento, ejecución de un contrato, cumplimiento de una obligación legal, protección de intereses vitales, misión de interés público o interés legítimo del responsable. La base debería documentarse por cada actividad de tratamiento. Las categorías especiales (p. ej., datos de salud o de menores) deberían incluirse en los esquemas de clasificación y pueden estar sujetas a controles más estrictos. Si se cambian o amplían las finalidades, puede ser necesario revisar la base legal u obtener un nuevo consentimiento. | B.1.2.3 | A.1.2.3 | 21–22 / 27–28 |
| O-18 | Cuándo se requiere el consentimiento y cómo se obtiene. La información previa al consentimiento debería seguir B.1.3.4. | B.1.2.4, B.1.2.5 | A.1.2.4, A.1.2.5 | 22 / 28 |

### 5.3 Orientaciones para interpretar y recomendar (v0.6; leídas por la IA y comprobadas por el equipo: V-15 a V-18)

| ID | Orientación (paráfrasis) | Fuente | Fuerza | Uso | Pág. norma / PDF |
|---|---|---|---|---|---|
| O-19 | Informar sobre la posibilidad de oponerse; mecanismo coherente con el tipo de servicio (p. ej., en línea para servicios en línea). Algunas jurisdicciones otorgan este derecho. | B.1.3.6 | should / some jurisdictions | Interpretar A.1.3.6; sugerencia | 27 / 33 |
| O-20 | Acceso, corrección y supresión sin demora indebida; definir un tiempo de respuesta; informar los cambios o por qué no se corrigió. | B.1.3.7 | should | Sugerencia (A.1.3.7) | 27 / 33 |
| O-21 | Canales de comunicación con terceros y control del acuse de recibo al informarles. | B.1.3.8 | should | Evidencia interna (A.1.3.8) | 27–28 / 33–34 |
| O-22 | Copia en formato estructurado, de uso común y accesible; portabilidad solo en algunas jurisdicciones; informar si los datos ya se eliminaron. | B.1.3.9 | should / some jurisdictions | Interpretar A.1.3.9; sugerencia | 28 / 34 |
| O-23 | Las solicitudes legítimas pueden incluir copia o reclamación; atenderlas en tiempos de respuesta definidos. La guía dice que se definan en la "privacy policy", término que en la norma designa la política del PIMS (cl. 5.2). | B.1.3.10 | should / can | Sugerencia (A.1.3.10); no es un elemento esencial | 28 / 34 |
| O-24 | Algunas jurisdicciones exigen notificar las decisiones automatizadas, permitir oponerse o la intervención humana. | B.1.3.11 | some jurisdictions | Sugerencia si A.1.3.11 aplica | 29 / 35 |
| O-25 | Limitar también la recolección indirecta (p. ej., registros web); opciones desactivadas por defecto. | B.1.4.2 | should | Indicios y evidencia interna (A.1.4.2) | 29 / 35 |
| O-26 | Limitar el tratamiento mediante políticas y procedimientos; mecanismos para minimizar inexactitudes y responder a datos inexactos. | B.1.4.3, B.1.4.4 | should | Evidencia interna (A.1.4.3, A.1.4.4) | 29–30 / 35–36 |
| O-27 | Mecanismos para borrar cuando no se prevé más tratamiento; técnicas de eliminación según el medio. | B.1.4.6, B.1.4.9 | should | Evidencia interna (A.1.4.6, A.1.4.9) | 31–32 / 37–38 |
| O-28 | Calendarios de conservación que consideren requisitos legales, regulatorios y de negocio. | B.1.4.8 | should | Evidencia interna. En la política basta el plazo o criterio (O-10). | 31 / 37 |
| O-29 | Transmisión controlada: acceso autorizado a los sistemas de transmisión y registros de auditoría. | B.1.4.10 | should | Evidencia interna (A.1.4.10) | 32 / 38 |
| O-30 | La base de la transferencia depende de la jurisdicción de destino; países u organismos posibles en la operación normal, incluidos los subcontratados. | B.1.5.2, B.1.5.3 | should / can | Interpretar A.1.5.2–A.1.5.3 si aplican | 32–33 / 38–39 |

> **Nota de alcance:** la guía menciona como ejemplo a jurisdicciones con requisitos específicos. La Skill no evalúa el cumplimiento de la Ley 29733 ni del RGPD; solo puede señalar que la política *invoca* una norma, como evidencia textual.

---

## 6. Registro de validación humana

**Validación completa (2026-10-27).** Cada casilla se marcó después de que el equipo la comprobara en el PDF.

| # | Qué comprobar | Pág. PDF | Validado por | Fecha |
|---|---|---|---|---|
| V-01 | Desfase de paginación (pág. impresa 2 = PDF 8; 3 = PDF 9) | 8–9 | ☑ Equipo — comprobado: PDF 8→2, 9→3, 21→15, 26→20 | 2026-10-20 |
| V-02 | Nota del Anexo A: exclusiones en 6.1.3 e) y correspondencia A ↔ B | 21 | ☑ Equipo — comprobado: (a)–(e) coinciden, incl. referencia a 6.1.3 e) | 2026-10-21 |
| V-03 | Tabla A.1, A.1.2.2–A.1.2.9: IDs y títulos | 21 | ☑ Equipo — comprobado: bloque, objetivo y 8 controles coinciden | 2026-10-21 |
| V-04 | Tabla A.1, A.1.3.2–A.1.3.11 y A.1.4.2–A.1.4.7 | 22 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-05 | Tabla A.1, A.1.4.8–A.1.4.10 y A.1.5.2–A.1.5.5; Tabla A.2 inicio | 23 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-06 | Tabla A.2 (A.2.4.x, A.2.5.x) y A.3.3–A.3.4 | 24 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-07 | Tabla A.3, A.3.5–A.3.20 | 25 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-08 | Tabla A.3, A.3.21–A.3.31 | 26 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-09 | Cl. 5.2 a)–d) y viñetas de disponibilidad | 12–13 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-10 | B.1.2.3: lista de bases legales y categorías especiales | 27–28 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-11 | B.1.2.4 / B.1.2.5 | 28 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-12 | B.1.3.2 y B.1.3.3: la lista O-01 a O-09 y el carácter de "ejemplos" | 31 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-13 | B.1.3.3 (continuación) y B.1.3.4: O-10 a O-15 | 32 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-14 | Que las paráfrasis no cambien el sentido del control original (revisión de contenido) | 21–26 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-27 |
| V-15 | B.1.3.6–B.1.3.8: O-19, O-20, O-21 | 33–34 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-21 |
| V-16 | B.1.3.9–B.1.3.11: O-22, O-23, O-24 (incluida la frase sobre los tiempos de respuesta en la "privacy policy") | 34–35 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-21 |
| V-17 | B.1.4.2–B.1.4.10: O-25 a O-29 | 35–38 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-21 |
| V-18 | B.1.5.2–B.1.5.5: O-30 y la clasificación INT de A.1.5.4–A.1.5.5 | 38–39 | ☑ Equipo — comprobado en el PDF: coincide | 2026-10-21 |

> En §6 solo se registran comprobaciones **humanas**. La revisión de IA de §6.1 no las reemplaza.

### 6.1 Revisión asistida por IA (Claude), 2026-10-21

Método: comparación del catálogo con las imágenes de las páginas del PDF (renderizadas a 150 ppp y leídas visualmente), sin usar el OCR como fuente. Es una revisión de apoyo, **no** una validación humana.

| # | Págs. PDF revisadas | Resultado | Correcciones aplicadas en v0.3 |
|---|---|---|---|
| V-04 | 22 | IDs y títulos coinciden (A.1.3.2–A.1.3.11, A.1.4.2–A.1.4.7) | — |
| V-05 | 23 | IDs y títulos coinciden (A.1.4.8–A.1.4.10, A.1.5.2–A.1.5.5, A.2.2.2–A.2.2.7, A.2.3.2) | Objetivo del bloque "PII sharing…": se añadió "de acuerdo con las obligaciones aplicables" |
| V-06 | 24 | IDs y títulos coinciden (A.2.4.2–A.2.5.9, A.3.3–A.3.4); la Tabla A.3 empieza en A.3.3 | — |
| V-07 | 25 | IDs y títulos coinciden (A.3.5–A.3.20) | — |
| V-08 | 26 | IDs y títulos coinciden (A.3.21–A.3.31); la tabla termina en A.3.31 | — |
| V-09 | 12–13 | Cl. 5.2 a)–d) y las tres condiciones de disponibilidad coinciden | — |
| V-10 | 27–28 | Las seis bases legales coinciden (la 1.ª, consentimiento, está al final de la pág. 27) | O-17: se añadió que las categorías especiales deberían incluirse en los esquemas de clasificación |
| V-11 | 28 | B.1.2.4 y B.1.2.5 coinciden, incluida la remisión a B.1.3.4 | — |
| V-12 | 31 | Coincide la lista O-01 a O-09, el carácter de "ejemplos" y la orientación del punto de contacto (O-16) | §5.1: se reemplazó "su exigencia depende de…" (inferencia nuestra) por lo que indica la guía |
| V-13 | 32 | O-10 a O-14 y B.1.3.4 coinciden | O-15: se añadió "adecuada al público destinatario" |
| V-14 | 21–23 | 7 paráfrasis omitían o debilitaban elementos del control | Corregidas: A.1.2.3, A.1.2.6, A.1.2.7, A.1.2.8, A.1.2.9, A.1.3.8, A.1.4.6 |
| §7 | 57, 59 | Anexo C empieza en PDF 57 y Anexo D en PDF 59 | — |

No revisado por la IA: **V-03**, comprobada por el equipo (ver §6).

**V-15 a V-18 (2026-10-21):** referencias **leídas por la IA** en las páginas indicadas para redactar O-19 a O-30 y la clasificación de §2 (registro de IA). El mismo día, el equipo las **comprobó en el PDF** y confirmó que coinciden (registro humano en §6). Ambos registros se conservan por separado.

**Decisión del equipo (2026-10-21):** el equipo acepta las siete paráfrasis corregidas en v0.3 (A.1.2.3, A.1.2.6, A.1.2.7, A.1.2.8, A.1.2.9, A.1.3.8, A.1.4.6) para usarlas en el prototipo, apoyándose en esta revisión de IA. **No es una comprobación manual adicional:** V-14 sigue sin marcar en §6. El catálogo seguirá sujeto a correcciones durante las pruebas.

---

## 7. Pendientes diferidos (fuera de la primera entrega)

- Anexo D, mapeo al RGPD (Pág. norma 53 / PDF 59): corresponde al Tema 10 (segunda entrega).
- Anexo C, mapeo a ISO/IEC 29100 (Pág. norma 51 / PDF 57): Tema 9.
- Guía del Anexo B no catalogada: B.1.2.6–B.1.2.9 (no leída), B.1.5.4–B.1.5.5 (leída, sin catalogar), B.2 (encargados) y la guía de la Tabla A.3.
- Cláusulas 4–10 (sistema de gestión): fuera del alcance de la evaluación documental.

## 8. Historial

- **v0.1** (2026-10-19): primera versión, diseñada para un Gem (`historial/catalogo_iso27701_v0.1.md`).
- **v0.2** (2026-10-20): separa controles de orientaciones; aclara que D/I/N es una metodología propia; añade *No aplica* y su diferencia con *No determinado*; elimina la asignación automática de *Cumple parcialmente* por menciones genéricas; incorpora la cl. 5.2 completa y B.1.2.3–B.1.2.5; agrega el registro de validación humana.
- **v0.3** (2026-10-21): registra V-01 y V-02 como comprobadas por el equipo; incorpora la revisión de IA de V-04 a V-14 (§6.1) y corrige 7 paráfrasis de la Tabla A.1, el objetivo de A.1.5, O-15, O-17 y la introducción de §5.1. Copia anterior: `historial/catalogo_iso27701_v0.2.md`. Ese mismo día se registran V-03 (equipo) y la aceptación de las paráfrasis v0.3 para el prototipo (decisión del equipo basada en la revisión de IA, no una comprobación manual).
- **v0.4** (2026-10-21): cambio **solo metodológico**. Los estados y las reglas pasan a `criterios.md`, que distingue *No evidenciado* de *Incumplimiento documental sustentado*. No cambia ninguna referencia ISO, paráfrasis ni el estado de verificación (§6). Copia anterior: `historial/catalogo_iso27701_v0.3.md`.
- **v0.5** (2026-10-21): cambio **solo metodológico** en §4.2: la Tabla A.2 deja de ser *No aplica* por defecto y se decide según el rol justificado con el documento. No cambia ninguna referencia ISO, paráfrasis ni el estado de verificación (§6). Copia anterior: `historial/catalogo_iso27701_v0.4.md`.
- **v0.6** (2026-10-21): agrega la cobertura declarada (§0) y la **clasificación metodológica** E / C / INT-i / INT, que reemplaza a D / I / N con la misma pertenencia y con fundamento y referencias de guía por control (§2). Separa controles, orientaciones y ejemplos (§1). Aclara el uso de O-01 a O-16 (lista "Información al titular") y de O-17 y O-18 (solo interpretación). Agrega O-19 a O-30 desde B.1.3.6–B.1.5.3 (lectura de IA) y las comprobaciones V-15 a V-18, pendientes. No cambian los IDs, los títulos ni las paráfrasis de los controles. Copia anterior: `historial/catalogo_iso27701_v0.5.md`.
- **v0.6.1** (2026-10-21): registra V-15 a V-18 como **comprobadas por el equipo** (confirmación expresa del 21-10-2026). Actualiza el estado: 7 de 18 comprobaciones humanas. **No** implica la validación de V-04 a V-14, de `elementos.md` ni de la calidad de las evaluaciones. No cambian referencias, paráfrasis ni clasificación. Copia anterior: `historial/catalogo_iso27701_v0.6.md`.
- **v0.6.2** (2026-10-27): registra V-04 a V-14 como **comprobadas por el equipo** (confirmación expresa del 27-10-2026). Estado: 18 de 18 comprobaciones humanas. No implica la validación de `elementos.md` ni de la calidad de las evaluaciones. No cambian referencias, paráfrasis ni clasificación. Copia anterior: `historial/catalogo_iso27701_v0.6.1.md`.
