# PIMS Privacy Assistant

Aplicación con IA para la gestión de privacidad según **ISO/IEC 27701:2025**:

- **Evaluar política:** revisa una política de privacidad publicada frente a los 78 controles del Anexo A e identifica posibles vacíos documentales, con cita y página de cada evidencia (skill SK-01).
- **Auditoría:** el agente de evidencias y auditoría verifica los documentos del PIMS frente a las cláusulas 4–10 y los 78 controles del Anexo A, propone hallazgos (N / O / M) y planes de acción en el formato del módulo Auditorías de GESTITEL, y redacta las conclusiones del informe (skills SK-02 a SK-04). El equipo registra su revisión de cada hallazgo.
- **Chat:** preguntas sobre una ejecución guardada, con citas verificadas automáticamente.

Modelo: `gemini-3.5-flash-lite` (API de Gemini, nivel gratuito). Los resultados son **propuestas que el equipo auditor revisa**: no certifican cumplimiento.

## Estructura

```
app.py                     interfaz web (Streamlit)
requirements.txt           dependencias
.streamlit/                configuración y ejemplo de secretos (la clave nunca va al repositorio)
conexion/                  conexión con Gemini y modelos configurables
motor/                     SK-01: lectura, armado del mensaje, verificación y reporte
agente/                    agente de auditoría: alcance, lotes, verificación, salidas, medición y chat
skill/sk01 … sk04, comun/  skills (instrucciones, criterios, formatos) y catálogos ISO (paráfrasis)
asistente/                 identidad del PIMS Privacy Assistant
plantillas/                formatos alineados con GESTITEL
simulacion/                14 documentos de demostración simulados, plan de auditoría y conjunto de prueba
politicas/                 políticas públicas de ejemplo
resultados/, resultados_agente/   ejecuciones guardadas para demostración
docs/                      diseño del agente, uso local y despliegue en la nube
```

## Cobertura normativa

| Parte de ISO/IEC 27701:2025 | Catálogo | Comprobación humana |
|---|---|---|
| Cláusulas 4–10 (30 requisitos) | `skill/comun/clausulas_iso27701.md` | 4 de 4 |
| Anexo A, Tabla A.1 (31) y guías seleccionadas del Anexo B | `skill/sk01/catalogo_iso27701.md` | 18 de 18 |
| Anexo A, Tablas A.2 (18) y A.3 (29) | `skill/comun/anexo_a_tablas_a2_a3.md` | Pendiente (V-23, V-24) |
| Elementos verificables de los controles | `skill/sk01/elementos.md` y los catálogos anteriores | Pendiente |

No se cubren las cláusulas 1–3 ni los Anexos C–F; el Anexo B está cubierto solo en las guías seleccionadas de B.1.

## Uso en Windows

En VS Code, abra esta carpeta y use una terminal **PowerShell**.

Crear el entorno e instalar (una vez):

```powershell
py -3.13 -m venv .venv
```

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Clave de Gemini (variable de entorno; en esta computadora ya existe a nivel de sistema):

```powershell
$env:GEMINI_API_KEY = [Environment]::GetEnvironmentVariable("GEMINI_API_KEY", "Machine"); $env:PYTHONIOENCODING = "utf-8"
```

Iniciar la aplicación (se abre en `http://localhost:8501`):

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Sin clave, la aplicación permite revisar las ejecuciones guardadas, pero no ejecutar evaluaciones nuevas.

### Comandos sin interfaz

```powershell
.\.venv\Scripts\python.exe -m motor.evaluar "politicas\Protección de Datos Personales - UNSA.pdf" --fuente "https://www.unsa.edu.pe/servicios/politica-proteccion-datos.html"
```

```powershell
.\.venv\Scripts\python.exe -m agente.auditar simulacion\plan_AUD-2026-001.json simulacion\documentos
```

```powershell
.\.venv\Scripts\python.exe -m agente.auditar simulacion\plan_AUD-2026-001.json simulacion\documentos --seco
```

(`--seco` prepara las llamadas sin enviarlas a Gemini.)

## Publicar en la nube

Ver `docs/despliegue_nube.md` (Streamlit Community Cloud, gratuito). La clave y la contraseña de la aplicación se configuran como secretos de la plataforma.

## Cuota y datos

- Evaluar una política: 1 solicitud · Auditoría completa: unas 11 · Chat: 1 por pregunta.
- En el nivel gratuito, Google puede usar el contenido enviado: envíe solo documentos públicos o de prueba y oculte los nombres de personas.

## Resultados de las pruebas

`resultados_agente/README.md` resume las tres ejecuciones del agente sobre el conjunto de prueba: en la más reciente detectó 7 de 13 vacíos sembrados (7 de 10 en las cláusulas 4–10, 0 de 3 en el Anexo A). Por eso la lista de verificación marca con una **alerta** los resultados favorables apoyados en citas que no están en el documento, para que el revisor los compruebe.
