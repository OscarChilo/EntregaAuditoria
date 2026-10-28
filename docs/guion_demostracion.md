# Guion de demostración (10–12 minutos)

**Antes de empezar:** abrir la aplicación (local: `.\.venv\Scripts\python.exe -m streamlit run app.py`; o el enlace de Streamlit Cloud) y comprobar que no aparece el aviso «No hay clave». Tener a mano la carpeta `simulacion/documentos/`.

| Min. | Qué mostrar | Qué decir | Cuota |
|---|---|---|---|
| 0–1 | Pestaña **Acerca de** | Qué hace la herramienta, sobre qué norma (ISO/IEC 27701:2025) y que sus resultados son propuestas que el equipo revisa | 0 |
| 1–3 | **Evaluar política** → ejecución guardada de la política de la UNSA | Cada fila: criterio ISO con página, cita literal con página, estado y recomendación. El aviso de verificación es automático | 0 |
| 3–4 | (Opcional) **Evaluar** la política de Infounsa | Una sola llamada; se guarda todo lo enviado y la respuesta original | 1 |
| 4–7 | **Auditoría** → ejecución 3 | 108 requisitos (cláusulas 4–10 y 78 controles del Anexo A). Lista de verificación con **alertas** del verificador; filtrar «solo filas con alerta» | 0 |
| 7–8 | **Hallazgos y revisión** | Hallazgos N / O / M con evidencia y planes de acción con responsable y fecha. Marcar uno como «Confirmado» y guardar: eso es la revisión humana | 0 |
| 8–9 | **Medir la precisión del agente** | Conjunto de prueba con 13 vacíos sembrados: 7 detectados; las alertas guían al revisor. Explicar por qué no es un auditor autónomo | 0 |
| 9–10 | **Descargar** los CSV | Formato del módulo Auditorías de GESTITEL: se cargan en unsa.27k.pe | 0 |
| 10–11 | **Chat**: «¿Por qué 7.2 es una no conformidad?» | Respuesta con cita literal verificada | 1 |
| 11–12 | Cierre | Cobertura, límites (catálogos de A.2/A.3 y elementos pendientes de revisión humana) y próximos pasos | 0 |

**Si falla la conexión:** todo lo marcado con cuota 0 funciona sin internet a Gemini (las ejecuciones guardadas están en el repositorio).

**No ejecutar una auditoría nueva en vivo:** tarda varios minutos y usa unas 11 solicitudes. Mostrar la ejecución guardada.
