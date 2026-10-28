# Arquitectura del prototipo SK-01

## 1. Componentes (separados a propósito)

| Componente | Ubicación | Contenido | Puede cambiar sin tocar… |
|---|---|---|---|
| Instrucciones de la Skill | `skill/sk01/SKILL.md`, `criterios.md`, `formato_resultado.md` | Activación, pasos, estados, reglas y formato | el conocimiento ISO, el documento y el código |
| Asistente | `asistente/pims_privacy_assistant.md` | Identidad, instrucciones y conocimiento declarado | la Skill |
| Conocimiento ISO | `skill/sk01/catalogo_iso27701.md` | Referencias ISO/IEC 27701:2025 (paráfrasis), evaluabilidad D / I / N y registro de verificación | las instrucciones |
| Documento evaluado | Lo entrega el usuario (PDF) | Texto con marcas `[Página N]` y redacciones | todo lo anterior |
| Motor | `motor/` | Extracción del PDF, armado del mensaje, verificación y guardado de resultados | la Skill |
| Conexión | `conexion/` | Llamada a la API de Gemini y elección de modelo | la Skill y el motor |

## 2. Funcionamiento actual: contexto completo (no es RAG)

En cada evaluación se hace **una sola llamada** a Gemini con tres partes separadas:

1. `system_instruction`: asistente + SKILL.md + criterios.md + formato_resultado.md.
2. Bloque `<<<CONOCIMIENTO ISO>>>`: **el catálogo completo**.
3. Bloque `<<<DOCUMENTO>>>`: metadatos (nombre, fuente, páginas, estado del catálogo) y **el documento completo**.

**No hay recuperación de fragmentos**: no hay búsqueda ni selección del conocimiento, así que este funcionamiento **no es RAG**. Se usa contexto completo porque cabe holgadamente en el límite del nivel gratuito: una evaluación usa unos 15 mil tokens de entrada, y el límite es de 250 mil tokens por minuto.

Cada ejecución guarda en `resultados/<carpeta>/`:
- lo enviado: `instrucciones_enviadas.md` y `documento_enviado.txt`;
- la respuesta: `informe.md`;
- las comprobaciones: `verificacion.md`;
- los metadatos: `metadatos.json`, con el modelo, los tokens, las versiones de la Skill y del catálogo, y las redacciones.

## 3. Requisitos para una futura recuperación de fragmentos (RAG)

El objetivo previsto es recuperar fragmentos relevantes de la ISO para fundamentar las respuestas del **chat**. Cualquier implementación debe respetar estas condiciones:

1. **Ningún criterio aplicable puede omitirse.** El índice completo de controles (IDs, títulos y evaluabilidad D / I / N) se envía **siempre** en una evaluación SK-01. La recuperación solo puede **agregar** detalle (paráfrasis, orientaciones O-xx, texto de apoyo); nunca decide qué controles se evalúan.
2. **Cada fragmento conserva su referencia:** ID ISO, tipo (control u orientación), página de la norma y del PDF, y versión del catálogo. Un fragmento sin referencia no se usa.
3. **El documento evaluado no se fragmenta por relevancia.** Si en algún momento hubiera que dividirlo por tamaño, cada parte conserva sus marcas `[Página N]` y se procesan todas.
4. **La verificación compara con el catálogo completo**, no con lo recuperado. Así, un fallo de la búsqueda se detecta como control faltante.
5. **Se registra qué se recuperó** (IDs de los fragmentos y puntaje) en `metadatos.json`, para poder auditar cada respuesta.
6. **El estado de verificación del catálogo** sigue informándose aunque solo se envíen fragmentos.
7. **La fuente de la recuperación es el catálogo**, no el PDF de la norma completo, salvo que el equipo decida lo contrario y tenga autorización para usar ese material.

El punto de cambio en el código es `motor/skill.py::conocimiento_iso()`. Las instrucciones de la Skill y el bloque del documento no deberían necesitar cambios.

## 4. Cambios de la Skill v0.5 / catálogo v0.6

- La **plantilla de la matriz** se genera desde el catálogo con la referencia ISO (control y guía del Anexo B), la categoría metodológica (E / C / INT-i / INT) y la aplicabilidad inicial.
- La **lista "Información al titular"** (O-01 a O-16) se envía como un bloque más (`<<<LISTA INFORMACIÓN AL TITULAR>>>`).
- La verificación es **sensible a la versión** (`motor/insumos.py`): cada respuesta se verifica con los elementos y las reglas de la versión de la Skill que la generó. Así, volver a verificar una ejecución antigua no cambia sus resultados.
- Formato de la matriz por versión: v0.1, 8 columnas · v0.2–v0.4, 9 · v0.5, 10 (con Aplicabilidad e Información faltante o necesaria).
- **Requisito para una futura recuperación de fragmentos (RAG):** la plantilla (índice completo con categorías y referencias) y la lista de orientaciones se envían siempre completas. La recuperación solo podría agregar texto de apoyo.
