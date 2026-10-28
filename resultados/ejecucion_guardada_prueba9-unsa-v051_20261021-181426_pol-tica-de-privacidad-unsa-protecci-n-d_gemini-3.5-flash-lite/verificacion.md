# Verificación automática — SK-01

Skill evaluada: v0.5.1 · Modelo: gemini-3.5-flash-lite · Catálogo: v0.6.1

**Resultado:** no truncada · cobertura completa · 16 observaciones exigibles

## 0. Resumen por categoría

| Categoría | Observaciones exigibles | No exigibles en esta versión |
|---|---|---|
| Truncamiento | 0 | — |
| Cobertura | 0 | — |
| Plantilla | 0 | — |
| Conteos | 0 | — |
| Estados | 5 | — |
| Citas | 5 | — |
| Formato | 6 | 26 |

## 1. Truncamiento

- ✅ Motivo de fin de la API: `STOP`
- ✅ Bloque de cierre `--- FIN SK-01 ---` presente
- Tokens: entrada 34081, salida 10676, razonamiento None, límite de salida 65536

## 2. Cobertura (calculada por el programa con los IDs del catálogo)

| Grupo | IDs con fila explícita | Esperados |
|---|---|---|
| A.1 | ✅ 31 | 31 |
| A.3 (INT-i) | ✅ 9 | 9 |
| A.3 (INT) | ✅ 20 | 20 |
| A.2 | ✅ 18 | 18 |

Filas de la matriz: 42 (40 con un solo ID).

## 3. Conteos calculados por el programa

| Estado | Filas | IDs | Declarado por el modelo (filas) |
|---|---|---|---|
| Cumple | 7 | 7 | — |
| Cumple parcialmente | 19 | 19 | — |
| No evidenciado | 0 | 0 | — |
| Incumplimiento documental sustentado | 0 | 0 | — |
| No determinado | 15 | 34 | — |
| No aplica | 1 | 18 | — |
| **Total** | 42 | 78 | — |

## 4. Observaciones exigibles en esta versión

### Cobertura
- ✅ Sin observaciones

### Plantilla
- ✅ Sin observaciones

### Conteos
- ✅ Sin observaciones

### Estados
- ❌ A.1.2.9: «Cumple parcialmente» no está permitido para INT
- ❌ A.1.2.3: «Cumple parcialmente» sin al menos un elemento respaldado y otro faltante
- ❌ A.1.2.5: «Cumple parcialmente» sin al menos un elemento respaldado y otro faltante
- ❌ A.1.3.3: «Cumple» con elementos [aviso] no respaldados: E2
- ❌ A.1.3.9: «Cumple parcialmente» sin al menos un elemento respaldado y otro faltante

### Citas
- ❌ A.1.2.2: cita no encontrada
- ❌ A.1.3.5: cita no encontrada
- ❌ A.1.3.10: cita no encontrada
- ❌ A.1.4.2: cita no encontrada
- ❌ A.2.2.2: cita no encontrada

### Formato
- ❌ A.1.2.8: la justificación no recorre E1, E2
- ❌ A.1.3.8: la justificación no recorre E1, E2
- ❌ A.3.7: la justificación no recorre E1, E2
- ❌ A.3.11: la justificación no recorre E1, E2
- ❌ A.3.18: la justificación no recorre E1, E2
- ❌ A.3.26: la justificación no recorre E1, E2

## 5. Citas

Por categoría: literal: 32, no encontrada: 5

| IDs | Cita | Pág. indicada | Categoría | Encontrada en |
|---|---|---|---|---|
| A.1.2.2 | «la presente Política de Privacidad, a fin de informarle acerca de las finalidades para las que se recaba» | [1] | ✅ literal | [1] |
| A.1.2.2 | «La UNSA dará tratamiento a sus Datos Personales en forma directa, para finalidades diversas, dependiendo del caso particular en el que sean recabadas» | [1] | ❌ no encontrada | — |
| A.1.2.3 | «de conformidad con la Ley 29733, Ley de Protección de Datos Personales, y su reglamento (en adelante, norma aplicable).» | [1, 5] | ✅ literal | [1] |
| A.1.2.3 | «No se requiere el consentimiento del titular de datos personales, para los efectos de su tratamiento, en los siguientes casos: 1. Cuando los datos personales se recopilen o transfieran para el ejercicio de las funciones de las entidades públicas en el ámbito de sus competencias.» | [1, 5] | ✅ literal | [5] |
| A.1.2.4 | «Si usted es menor de 14 años, deberá contar con la autorización de sus padres para el registro de su información en nuestro portal o esta deberá ser registrada por sus padres o apoderados debidamente acreditados, motivo por el cual deberá brindarnos los datos de contacto de estos para obtener su consentimiento.» | [3] | ✅ literal | [3] |
| A.1.2.5 | «Sus datos serán almacenados en una base de titularidad y responsabilidad de la UNSA ubicada en la calle Santa Catalina N° 117, cercado de la ciudad de Arequipa» | [3] | ✅ literal | [3] |
| A.1.2.7 | «para lo cual podemos compartir su información, exclusivamente, para las finalidades aquí descritas.» | [1] | ✅ literal | [1] |
| A.1.2.9 | «su información será almacenada en el banco de datos de “Estudiantes”, “Usuarios de Biblioteca”, “Grados y Títulos” y “Convenios, Becas y pasantías”» | [1] | ✅ literal | [1] |
| A.1.2.9 | «Estudiantes» | [1] | ✅ literal | [1] |
| A.1.2.9 | «Usuarios de Biblioteca» | [1] | ✅ literal | [1] |
| A.1.2.9 | «Grados y Títulos» | [1] | ✅ literal | [1] |
| A.1.2.9 | «Convenios, Becas y pasantías» | [1] | ✅ literal | [1] |
| A.1.3.2 | «Como Titular de Datos Personales, Usted tiene derecho a que en cualquier momento se le proporcione Acceso a sus datos; a Rectificarlos o actualizarlos; a Cancelarlos... y a Oponerse al Tratamiento... (derechos ARCO) y otros derechos que la Ley de Protección de Datos Personales y su Reglamento prevé.» | [5] | ✅ literal | [5] |
| A.1.3.2 | «Para facilitar su solicitud alcanzamos el siguiente formato, al correo electrónico odp@unsa.edu.pe. o de manera presencial por Mesa de Partes ubicado en la calle San Agustín N° 115, cercado de la ciudad de Arequipa, dirigido a la oficina de Secretaría General.» | [5] | ✅ literal | [5] |
| A.1.3.3 | «a fin de informarle acerca de las finalidades para las que se recaba, la identidad de los que son o podrían ser los destinatarios, los bancos de datos donde se almacenarán y sus responsables, entre otros» | [1] | ✅ literal | [1] |
| A.1.3.4 | «Para la Universidad Nacional de San Agustín de Arequipa (en adelante, UNSA), con domicilio en calle Santa Catalina N° 117, Cercado de Arequipa... ponemos a su disposición la presente Política de Privacidad» | [1] | ✅ literal | [1] |
| A.1.3.5 | «así como, revocar el Consentimiento que haya otorgado para su Tratamiento.» | [3, 5] | ❌ no encontrada | — |
| A.1.3.5 | «La autorización permite a la UNSA realizar el tratamiento de todos los datos personales que suministre o se generen de manera indefinida o hasta que revoque su consentimiento.» | [3, 5] | ✅ literal | [3] |
| A.1.3.6 | «a Oponerse al Tratamiento de sus Datos Personales (derechos ARCO)» | [5] | ✅ literal | [5] |
| A.1.3.6 | «Para ejercer alguno de sus derechos, puede dirigir su solicitud... al correo electrónico odp@unsa.edu.pe. o de manera presencial por Mesa de Partes...» | [5] | ✅ literal | [5] |
| A.1.3.7 | «Usted tiene derecho a que en cualquier momento se le proporcione Acceso a sus datos; a Rectificarlos o actualizarlos; a Cancelarlos, con lo cual los daríamos de baja en nuestras bases de datos» | [5] | ✅ literal | [5] |
| A.1.3.7 | «Para ejercer alguno de sus derechos, puede dirigir su solicitud... al correo electrónico odp@unsa.edu.pe. o de manera presencial por Mesa de Partes...» | [5] | ✅ literal | [5] |
| A.1.3.9 | «Usted tiene derecho a que en cualquier momento se le proporcione Acceso a sus datos» | [5] | ✅ literal | [5] |
| A.1.3.10 | «Para ejercer alguno de sus derechos, puede dirigir su solicitud, en los términos que establece la norma aplicable (es decir nombres y apellidos, petición concreta que da lugar a la solicitud, domicilio o dirección electrónica para notificar, fecha y firma del solicitante, documentos que sustenten la petición, de ser el caso y pago de la contraprestación, en caso corresponda) Para facilitar su solicitud alcanzamos el siguiente formato, al correo electrónico odp@unsa.edu.pe. o de manera presencial por Mesa de Partes...» | [5] | ❌ no encontrada | — |
| A.1.4.2 | «La UNSA dará tratamiento a sus Datos Personales en forma directa, para finalidades diversas, dependiendo del caso particular en el que sean recabadas» | [1] | ❌ no encontrada | — |
| A.1.4.3 | «será tratada con la finalidad de realizar: i) Gestión de recursos humanos... y, v) En general, sus datos personales serán utilizados para cualquier finalidad conexa con su relación laboral con la UNSA.» | [2, 3] | ✅ literal | [2] |
| A.1.4.4 | «a través de fuentes accesibles al público, con el propósito de validar la veracidad de la información proporcionada por usted.» | [2] | ✅ literal | [2] |
| A.1.4.6 | «a Cancelarlos, con lo cual los daríamos de baja en nuestras bases de datos» | [5] | ✅ literal | [5] |
| A.1.4.8 | «La autorización permite a la UNSA realizar el tratamiento de todos los datos personales que suministre o se generen de manera indefinida o hasta que revoque su consentimiento.» | [3] | ✅ literal | [3] |
| A.1.4.9 | «a Cancelarlos, con lo cual los daríamos de baja en nuestras bases de datos» | [5] | ✅ literal | [5] |
| A.1.4.10 | «teniendo en cuenta además las garantías, principios y medidas de seguridad que reconoce la norma aplicable.» | [1] | ✅ literal | [1] |
| A.3.3 | «teniendo en cuenta además las garantías, principios y medidas de seguridad que reconoce la norma aplicable.» | [1] | ✅ literal | [1] |
| A.3.9 | «Cabe señalar que cada docente y/o auxiliar contará con usuario y contraseña de acceso al aula virtual» | [2] | ✅ literal | [2] |
| A.3.10 | «para lo cual podemos compartir su información, exclusivamente, para las finalidades aquí descritas.» | [1] | ✅ literal | [1] |
| A.3.13 | «de conformidad con la Ley 29733, Ley de Protección de Datos Personales, y su reglamento (en adelante, norma aplicable).» | [1] | ✅ literal | [1] |
| A.3.23 | «Cabe señalar que cada docente y/o auxiliar contará con usuario y contraseña de acceso al aula virtual» | [2] | ✅ literal | [2] |
| A.2.2.2, A.2.2.3, A.2.2.4 | «Para la Universidad Nacional de San Agustín de Arequipa (en adelante, UNSA)... la privacidad y protección de sus datos personales es muy importante. Por ello ponemos a su disposición la presente Política de Privacidad... Sus datos serán almacenados en una base de titularidad y responsabilidad de la UNSA» | [1, 3] | ❌ no encontrada | — |

## 6. Reglas no exigibles en la Skill v0.5.1 (informativo)

- A.1.2.2: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.2.3: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.2.4: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.2.5: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.2.7: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.2.9: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.3.2: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.3.3: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.3.4: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.3.5: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.3.6: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.3.7: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.3.9: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.3.10: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.4.2: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.4.3: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.4.4: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.4.6: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.4.8: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.4.9: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.1.4.10: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.3.3: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.3.9: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.3.10: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.3.13: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4
- A.3.23: justificación sin «Respalda:» y «Falta:» — regla «respalda_falta» exigible desde v0.3 y deja de exigirse desde v0.4

## 7. Redacciones aplicadas antes del envío

- Ninguna

> Comprobaciones automáticas de forma. La pertinencia de cada estado la revisa el equipo.
