# Aplicación web en local

Interfaz del proyecto (`app.py`, Streamlit) con cuatro pestañas: **Evaluar política (SK-01)**, **Auditoría (agente)**, **Chat** y **Acerca de**.

## Abrirla (Windows, terminal de VS Code en PowerShell)

Desde la carpeta `TIF_AS2`. La primera vez, instala Streamlit:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Carga la clave y la codificación (en cada terminal nueva):

```powershell
$env:GEMINI_API_KEY = [Environment]::GetEnvironmentVariable("GEMINI_API_KEY", "Machine"); $env:PYTHONIOENCODING = "utf-8"
```

Inicia la aplicación:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Se abre en el navegador en `http://localhost:8501`. Para detenerla: `Ctrl+C` en la terminal.

## Qué gasta cuota de Gemini

| Acción | Solicitudes |
|---|---|
| Ver ejecuciones guardadas, tablas, informe, descargas | 0 |
| Registrar la revisión del equipo | 0 |
| «Medir contra la clave de la simulación» | 0 |
| «Evaluar» una política (SK-01) | 1 |
| «Ejecutar auditoría» (78 controles + cláusulas 4–10) | ≈ 11 |
| Cada pregunta del chat | 1 |

## Revisión humana

En **Auditoría → Hallazgos y revisión**, el equipo marca cada hallazgo como Confirmado, Reclasificado o Descartado, escribe su nombre y pulsa **Guardar revisión del equipo**. Se guarda en `revision_equipo.csv` dentro de la carpeta de la ejecución; las propuestas del agente no se modifican.

## Contraseña (opcional en local, obligatoria en la nube)

Si se define la variable `APP_PASSWORD`, la aplicación la pide antes de mostrar nada. En la nube se configurará como secreto de la plataforma, junto con `GEMINI_API_KEY`.
