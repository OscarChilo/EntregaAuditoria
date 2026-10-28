# Publicar la aplicación en Streamlit Community Cloud

Servicio gratuito, sin tarjeta. Publica la aplicación desde un repositorio de GitHub. **Usted** crea las cuentas y pega la clave; la clave nunca va al repositorio.

## 0. Antes de empezar

- Pruebe la aplicación en local (`docs/aplicacion_local.md`).
- El repositorio se crea desde la carpeta limpia de entrega (`TIF_AS_Entrega2`), que **no** incluye el PDF de la norma (derechos de autor), la clave ni el historial de desarrollo.
- Decida una contraseña para la aplicación (`APP_PASSWORD`): sin ella, cualquiera con el enlace podría gastar la cuota de Gemini y enviar documentos al nivel gratuito.

## 1. Crear el repositorio en GitHub

1. Entre en https://github.com y cree una cuenta si no tiene.
2. Pulse **New repository**. Nombre sugerido: `pims-privacy-assistant`. Elija **Private** (recomendado) y no agregue README ni .gitignore (ya existen).
3. En la terminal de VS Code, dentro de `TIF_AS_Entrega2`, ejecute (reemplace `<usuario>`):

```powershell
git init
git add .
git commit -m "PIMS Privacy Assistant"
git branch -M main
git remote add origin https://github.com/<usuario>/pims-privacy-assistant.git
git push -u origin main
```

Git le pedirá iniciar sesión en GitHub en una ventana del navegador.

Antes del `git commit`, confirme que la clave no se va a subir:

```powershell
git status
```

No debe aparecer `.streamlit/secrets.toml` ni `.venv`.

## 2. Publicar en Streamlit Community Cloud

1. Entre en https://share.streamlit.io e inicie sesión **con su cuenta de GitHub**.
2. Pulse **Create app** → **Deploy a public app from GitHub** (el repositorio puede ser privado; la aplicación queda protegida por su contraseña).
3. Elija el repositorio `pims-privacy-assistant`, la rama `main` y el archivo `app.py`.
4. En **Advanced settings**:
   - **Python version:** 3.13 (la probada en local).
   - **Secrets:** pegue el contenido de `.streamlit/secrets.toml.example` con sus valores reales:

```toml
GEMINI_API_KEY = "su-clave-de-Gemini"
APP_PASSWORD = "su-contraseña"
```

5. Pulse **Deploy**. La primera instalación tarda unos minutos.

## 3. Comprobar

- Al abrir el enlace, la aplicación debe pedir la contraseña.
- En **Auditoría** y **Evaluar política** se ven las ejecuciones de demostración incluidas en el repositorio.
- Una evaluación nueva consume cuota de Gemini (1 solicitud por política, unas 11 por auditoría, 1 por pregunta del chat).

## 4. Tenga en cuenta

- **Los archivos nuevos no son permanentes:** lo que se genera en la nube (ejecuciones, revisiones del equipo) se borra cuando la aplicación se reinicia o se actualiza. Use los botones **Descargar** para conservarlo.
- **La aplicación se duerme** tras un tiempo sin uso; al abrirla de nuevo tarda unos segundos en despertar.
- **Datos:** envíe solo documentos públicos o de prueba; el nivel gratuito de Gemini puede usar el contenido enviado.
- Para cambiar la clave o la contraseña: **Settings → Secrets** en Streamlit Cloud. Para actualizar el código: `git add .`, `git commit -m "..."` y `git push`; la aplicación se actualiza sola.
