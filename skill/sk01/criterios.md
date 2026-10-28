# SK-01 — Criterios de evaluación

Este archivo es la **única fuente** de los estados y las reglas de decisión de la Skill SK-01. El catálogo (`catalogo_iso27701.md`) aporta las referencias ISO, la **clasificación metodológica** de cada control (E / C / INT-i / INT, catálogo §2) y las orientaciones del Anexo B (catálogo §5).

> **Recordatorio:** la clasificación es una **selección metodológica del equipo**, no una clasificación de ISO/IEC 27701 ni una obligación universal de publicación. Un vacío en la política es un **vacío documental de ese documento**: la organización puede tener la información en otros medios o haber excluido el control en su Declaración de Aplicabilidad.

---

## 1. Qué se evalúa

- **Objeto evaluado:** el documento entregado (p. ej., una política de privacidad pública), **no** la organización.
- **Cobertura:** los **78 controles del Anexo A** (catálogo §0). Todos se recorren en cada evaluación, aunque el documento no los mencione. Solo los controles reciben estado.
- **Orientaciones del Anexo B:** se usan para **interpretar** y para **sugerir** (catálogo §5). No reciben estado ni son obligaciones:
  - **O-01 a O-16:** lista "Información al titular" (ejemplos de B.1.3.3 y B.1.3.4). Se recorre completa.
  - **O-17 y O-18:** solo para interpretar la base legal y el consentimiento.
  - **O-19 a O-30:** para interpretar y para redactar sugerencias o pedidos de evidencia interna.
- La cl. 5.2 no se evalúa sobre un aviso público (catálogo §4.4).

## 2. Estados

| Estado | Definición | Requisitos para asignarlo | Equivalencia con la propuesta del TIF (§2.6) |
|---|---|---|---|
| **Cumple** | El documento contiene evidencia específica que cubre todos los elementos del control que pueden evidenciarse en un aviso. Se refiere **solo al criterio documental**: no significa que la organización cumpla el control en la práctica. | Solo E, o C con aplicabilidad *Aplica*. Cita literal y ubicación de cada elemento. | Cumple |
| **Cumple parcialmente** | Hay evidencia específica que cubre algunos elementos del control. | Cita literal y ubicación. Nombrar el elemento cubierto y el faltante. | Cumple parcialmente |
| **No evidenciado** | El control es E (o C con *Aplica*): el documento es un lugar esperable para esa información, según la metodología del equipo, pero no la contiene. | Indicar qué se buscó y que no se encontró. **No hay cita**, porque la evidencia es la ausencia. | Refina "No cumple" |
| **Incumplimiento documental sustentado** | El propio texto del documento contradice el control o muestra una deficiencia concreta frente a él. | Cita literal y ubicación **obligatorias**. Explicar qué elemento del control contradice. | Refina "No cumple" |
| **No determinado** | La información del documento no alcanza para concluir, o la aplicabilidad está por determinar. | Indicar qué evidencia o información haría falta. Puede incluir una cita si el texto es un indicio insuficiente. | No determinado |
| **No aplica** | El control queda fuera del alcance de esta evaluación, por una razón explícita. | Cita del documento que **contenga la razón**. En controles C, solo un **descarte expreso** (§3.1); en la Tabla A.2, el rol justificado (regla 8). El silencio **nunca** basta. | (añadido por el equipo) |

### 2.1 Diferencias clave

- **Cumple = criterio documental.** No es una conclusión sobre la implementación real del control.
- **No evidenciado ≠ incumplimiento.** Significa que *la política no documenta* el elemento. Es un **posible vacío documental**.
- **Incumplimiento documental sustentado** solo existe con un **texto citado** que lo demuestre. Aun así, describe una deficiencia **del documento**, no una conclusión de auditoría sobre la organización.
- **No determinado ≠ No aplica.** La falta de indicios **nunca** es razón para *No aplica*.
- **No evidenciado ≠ No determinado.** *No evidenciado* solo para E, o C con *Aplica*. En INT-i e INT, y en C *Por determinar*, el silencio da *No determinado*.

## 3. Categoría, aplicabilidad y estados permitidos

| Categoría (catálogo §2) | Aplicabilidad | Estados permitidos | Si el documento no dice nada |
|---|---|---|---|
| **E** | *Aplica* (siempre, salvo exclusión declarada por la organización, con cita) | Todos | No evidenciado |
| **C** | *Aplica* (situación declarada, con cita) | Todos | No evidenciado |
| **C** | *No aplica* (descarte expreso, con cita) | No aplica | — |
| **C** | *Por determinar* (silencio o solo indicios) | No determinado | No determinado; anotar la información necesaria |
| **INT-i** | — | Cumple parcialmente (solo con evidencia específica), Incumplimiento documental sustentado (solo con cita), No determinado, No aplica | No determinado |
| **INT** | — | Incumplimiento documental sustentado (solo con cita), No determinado, No aplica | No determinado |

*Cumple* y *No evidenciado* nunca se asignan a INT-i ni a INT: su evidencia completa está fuera de la política, y los controles internos **no son contenido obligatorio** de una política pública.

### 3.1 Aplicabilidad de los controles C

**No supongas que un control C aplica ni que no aplica por la sola ausencia de información.**
- **Aplica:** el documento **declara afirmativamente** la situación, y se cita.
- **No aplica:** el documento **descarta expresamente** esa misma situación, con una negación clara sobre ella (p. ej., "no realizamos…", "no se toman…", "los datos no salen de…"), y se cita esa negación. La justificación debe **reproducir la negación** y decir qué situación descarta.
- **Por determinar:** cualquier otro caso, incluidos el silencio y los indicios. Es una **limitación del documento**, no un vacío. Se escribe qué información haría falta para determinarlo.

**El silencio nunca es "No aplica".** Si tu propia justificación dice que el documento "no menciona", "no declara", "no contempla", "no especifica" o "no identifica" la situación, la aplicabilidad es *Por determinar* y el estado es *No determinado*. **Ante la duda entre *No aplica* y *Por determinar*, elegir *Por determinar*.**

| Control | Aplica si el documento declara… | No basta para "Aplica" | No basta para "No aplica" | Información necesaria si está por determinar |
|---|---|---|---|---|
| A.1.3.5 | que algún tratamiento se basa en el consentimiento, o que el consentimiento puede retirarse o modificarse | la sola mención de "aceptar" una política o unos términos | que no se mencione el consentimiento; mencionar otras bases legales | ¿Qué tratamientos se basan en el consentimiento? |
| A.1.3.11 | que se toman decisiones basadas únicamente en tratamiento automatizado que afectan al titular | negar marketing o perfilado; describir procesos técnicos automáticos | que no se mencionen decisiones automatizadas; negar otra cosa (p. ej., perfilado publicitario); describir finalidades generales | ¿Se toman decisiones automatizadas sobre los titulares? |
| A.1.5.2, A.1.5.3 | que se transfieren datos a otra jurisdicción, país u organismo internacional | la ubicación de los servidores propios; un proveedor extranjero sin decir que recibe datos; **fuentes** de datos ubicadas en el exterior | que no se mencionen transferencias internacionales; compromisos condicionados sobre transferencias a terceros en general (p. ej., "no transferiremos sin su consentimiento"); indicar dónde están los servidores propios | ¿Se transfieren datos fuera del país (proveedores, servicios en la nube, socios)? ¿A dónde? |
| Tabla A.2 | que la organización trata datos por encargo de un cliente | — | — (se decide por el rol justificado, regla 8) | ¿La organización actúa como encargada en el servicio evaluado? |

### 3.2 Procedimiento obligatorio para cada fila

1. **Categoría y aplicabilidad:** copiar la categoría de la plantilla. En C, decidir la aplicabilidad con §3.1 y escribirla en la columna Aplicabilidad. En E, escribir *Aplica*. En INT-i e INT, escribir "—".
2. **Estados permitidos:** tomar de la tabla §3 la lista que corresponde a la categoría y la aplicabilidad. **El estado final debe estar en esa lista.**
3. **Elementos del control:** usar **exactamente** los elementos E1, E2… de `elementos.md`, con su etiqueta [aviso] o [interno]. No reformular el control como un único elemento.
4. **Evidencia pertinente, elemento por elemento:** para **cada** elemento [aviso], buscar texto del documento que lo afirme y aplicar la **prueba de pertinencia** (§3.3). Una cita sobre un tema relacionado **no basta**.
5. **Búsqueda de evidencia contraria:** antes de dar un elemento por respaldado, revisar el documento completo en busca de texto que lo **amplíe, limite o contradiga** (p. ej., cláusulas abiertas, excepciones amplias, "entre otros", "cualquier otro fin", "de manera indefinida"). Si existe, el elemento queda **Contradicho** (con cita) o, como mucho, parcialmente respaldado.
6. **Dependencias:** si `elementos.md` indica que un elemento depende de otro (p. ej., "mecanismo para ejercer el derecho" depende de "derecho declarado"), el dependiente **no** puede quedar respaldado si el elemento del que depende falta.
7. **Decisión** (solo con los elementos [aviso]):
   - *Cumple*: los estados permitidos lo admiten, **todos** los elementos [aviso] están respaldados y ninguno contradicho.
   - *Cumple parcialmente*: al menos un elemento [aviso] respaldado y otro faltante o contradicho. En INT-i basta un elemento [aviso] respaldado con evidencia específica, porque los [interno] siempre faltan en una política.
   - *Incumplimiento documental sustentado*: un elemento está contradicho por una cita y esa contradicción es el hallazgo principal.
   - Ningún elemento respaldado: el estado de la columna "Si el documento no dice nada" de §3.
8. **Justificación** recorriendo **todos** los elementos del control, en orden:
   `E1 Respalda ← "<cita>" · E2 Falta · E3 Falta (interno) · E4 Contradicho ← "<cita>"`
   Cada "Respalda" y cada "Contradicho" llevan su cita literal.
9. **Información faltante o necesaria:**
   - E, o C con *Aplica*, sin *Cumple*: **qué información falta** en la política, en concreto.
   - C *Por determinar*: **qué información se necesita** para determinar la aplicabilidad.
   - INT-i e INT: qué evidencia interna haría falta.
10. **Recomendación** según §5.
11. **Control final:** confirmar que el estado está en la lista del paso 2 y que es coherente con los elementos del paso 8. Si no lo es, se rehace la decisión. **No** se elige otro estado al azar.

### 3.3 Prueba de pertinencia de la evidencia

Una cita respalda un elemento del control solo si se cumplen estas condiciones:

1. **Mismo objeto:** la cita trata exactamente lo que pide el elemento, no un tema relacionado, una consecuencia ni un medio genérico. Ejemplos ilustrativos, que no se aplican de forma mecánica: describir copias de seguridad no evidencia un plazo de conservación; mencionar un comité no evidencia una evaluación de impacto.
2. **Afirmación directa:** leída sola, o junto con el texto al que el documento la vincula (condición 4), permite afirmar el elemento **sin suponer** nada que no esté escrito. Si hace falta conocimiento externo (sobre una ley, una práctica habitual o el proveedor), no lo respalda.
3. **Sin extensión por enumeración:** cuando el documento enumera derechos, medios o datos, solo cuenta lo enumerado. Invocar una ley no incorpora su contenido al documento.
4. **Contenido, no anuncio:** una frase que anuncia que algo *se informará* (p. ej., "en cada formulario se indicará la finalidad") no es el contenido mismo. Respalda, como mucho, el **momento o medio** de la información, no su contenido.

**Párrafos y canales comunes:** un párrafo o canal respalda un elemento de otro párrafo **cuando el propio documento establece el vínculo**. Ejemplos: "para ejercer estos derechos…" o "para ejercer cualquiera de sus derechos…" inmediatamente después de enumerarlos, o un título de sección que los agrupa. En ese caso:
- el canal respalda el mecanismo de **cada derecho que el documento declara**, y de ninguno que no declare;
- la justificación cita **ambos textos**, el del derecho y el del canal, y explica el vínculo en una frase.

Si el vínculo no está en el documento (solo se infiere por cercanía o por costumbre), no se usa.

**Expresiones equivalentes:** no se exigen palabras exactas. Una frase distinta respalda el elemento si describe el mismo objeto (p. ej., "pedir que dejen de usar sus datos" puede expresar oposición). La justificación explica la equivalencia en una frase. Si la equivalencia es dudosa, el elemento se considera **no respaldado** y la duda se anota.

## 4. Reglas de decisión

1. **No inventar.** Solo se citan IDs del catálogo y textos que estén literalmente en el documento evaluado. Un aspecto sin correspondencia en el catálogo se reporta como "sin correspondencia en el catálogo".
2. **Citas literales.** Toda cita se copia **exactamente** del documento, sin corregir ortografía ni parafrasear, y entre comillas dobles. Máximo unas 40 palabras por cita; si se necesita más, se usan dos citas. Las marcas `[Página N]` **no** son texto del documento y nunca van dentro de una cita. Si el texto ocupa varias líneas, se unen con un espacio, sin insertar "/" ni otros separadores. Para omitir texto intermedio se usa `[...]`. Si no puedes reproducir el texto exacto, no uses comillas: en ese caso no hay evidencia citada.
3. **Ubicación obligatoria** para cada cita: página (según las marcas `[Página N]`) y sección o título más cercano. Si no hay título, se escribe "sin título de sección".
4. **Una mención genérica no fija el estado.** Frases como "se aplican medidas de seguridad" o "conforme a la Ley 29733" se registran como evidencia, pero el estado se decide comparándolas con los elementos concretos del control. Si no cubren ningún elemento específico: *No evidenciado* (E, o C con *Aplica*) o *No determinado* (INT-i, INT).
   - **Seguridad (Tabla A.3 y A.1.4.10):** una frase general sobre "medidas de seguridad", "confidencialidad", "protección adecuada" o "cumplimiento de la norma" **no demuestra** una política, un procedimiento ni un control interno. Para *Cumple parcialmente* en estos controles, la cita debe identificar algo **concreto** del control: una política nombrada, un alcance, una tecnología, un proceso o un responsable. Si no, el estado es *No determinado* y la frase se anota como indicio insuficiente.
5. **Orientaciones ≠ requisitos.** Las orientaciones del Anexo B (O-xx) y sus ejemplos **nunca** generan por sí solos un *No evidenciado* ni un *Incumplimiento*. Ayudan a interpretar los elementos del control y a redactar **sugerencias**, rotuladas como tales (§5).
6. **Lista "Información al titular" (O-01 a O-16):** se recorre completa. Cada punto queda como *Presente*, *Parcial*, *Ausente*, *No aplica* o *Por determinar*. Un punto *Ausente* es una **sugerencia** de mejora, salvo que corresponda a un elemento [aviso] de un control E o C con *Aplica*; en ese caso el faltante ya figura en la fila del control.
7. **"No aplica" del evaluador ≠ exclusión en la Declaración de Aplicabilidad.** La Skill solo delimita su propia evaluación.
8. **Tabla A.2 (encargados): categoría C según el rol, justificado con citas.**
   - El documento identifica a la organización como responsable del tratamiento evaluado (cita) y nada indica que trate datos por encargo de un cliente → *No aplica*, con la cita del rol.
   - El documento no permite establecer el rol, o es ambiguo → *No determinado* (aplicabilidad por determinar).
   - El documento describe a la organización tratando datos por encargo de un cliente → la tabla aplica y sus controles son INT.
9. **Redacción.** Escribir "la política no documenta…" o "el documento no permite determinar…". Nunca "la universidad no cumple…".
10. **Normas externas.** Si el documento invoca una ley, se registra como evidencia textual. La Skill **no** evalúa el cumplimiento de esa ley.
11. **Ante la duda entre dos estados, elegir el más conservador:** en los C, *Por determinar* (*No determinado*) antes que *No aplica*; *No determinado* antes que *No evidenciado*; *No evidenciado* antes que *Incumplimiento documental sustentado*; *Cumple parcialmente* antes que *Cumple*. Siempre dentro de los estados permitidos.
12. **Evidencia pertinente.** Cada conclusión se apoya en evidencia que trate el elemento del control (§3.2 y §3.3). Usar la misma cita para varios controles es válido solo si es pertinente para cada uno.
13. **Inferencias.** No atribuir al documento calificaciones que no hace (p. ej., llamar "encargado" a un proveedor que el documento no califica así, o "transferencia" a una fuente de datos). Si la inferencia es necesaria para el análisis, se escribe como tal.
14. **Recorrido completo del documento.** Toda sección del documento que trate datos personales queda tratada en alguna fila, en la lista "Información al titular" o en "evidencias sin correspondencia".
15. **Esencial ≠ obligación universal.** Al redactar, no decir que la ISO "exige publicar" algo. Decir "la política no documenta…; según la metodología de evaluación, es información esencial para el titular".
16. **Acceso ≠ copia.** El derecho de **acceso** a los datos y la entrega de una **copia** de los datos son elementos distintos: B.1.3.3 los enumera por separado y B.1.3.9 describe la copia (formato estructurado, de uso común y accesible). Por eso:
   - un texto que reconoce el acceso, o que remite a "otros derechos que la ley prevé", **no respalda** la entrega de una copia;
   - solo la respalda un texto que diga que el titular puede **obtener, recibir o descargar sus datos** (una copia, una reproducción o un archivo con ellos), o una expresión equivalente explicada en la justificación;
   - si la copia no se declara, el mecanismo para pedirla tampoco puede darse por respaldado (dependencia de elementos).

## 5. Recomendaciones

Cada recomendación comienza con **uno** de estos rótulos:

| Rótulo | Cuándo | Base |
|---|---|---|
| **"Completar la política: …"** | E, o C con *Aplica*, con estado distinto de *Cumple* y *No aplica* | Elemento [aviso] del control (requisito del control, según la metodología) |
| **"Corregir el texto: …"** | *Incumplimiento documental sustentado* | Texto citado que contradice el control |
| **"Aclarar aplicabilidad: …"** | C *Por determinar* | Condición de §3.1 |
| **"Solicitar evidencia interna: …"** | INT-i, INT (y los elementos [interno] de cualquier control) | Control del Anexo A; nombrar el documento interno |
| **"Mantener: …"** | *Cumple* | — |
| **"Ninguna: …"** | *No aplica* | La justificación explica la razón |

Además, en la misma celda y **separada**, puede agregarse una **"Sugerencia (orientación O-xx): …"** basada en el Anexo B (p. ej., el plazo de respuesta de O-23). Una sugerencia **no** es un requisito del control y **no** cambia el estado.

Nunca se recomienda "Completar la política" para un control INT-i o INT, ni para un elemento [interno].
