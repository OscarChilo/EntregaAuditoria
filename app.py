"""Interfaz web de PIMS Privacy Assistant.

Pestañas:
  1. Evaluar política (SK-01)  — una solicitud a Gemini por evaluación
  2. Auditoría (agente)        — SK-02 a SK-04, unas 11 solicitudes por auditoría; revisión humana de hallazgos
  3. Chat                      — preguntas sobre una ejecución guardada; una solicitud por pregunta
  4. Acerca de

Ejecutar en local:  .\\.venv\\Scripts\\python.exe -m streamlit run app.py
La clave se lee de GEMINI_API_KEY (variable de entorno o, en la nube, secretos de Streamlit).
Si se define APP_PASSWORD, la aplicación pide esa contraseña antes de mostrar nada.
"""

import csv
import hmac
import io
import json
import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent
DIR_RES_SK01 = RAIZ / "resultados"
DIR_RES_AGENTE = RAIZ / "resultados_agente"
DIR_SIMULACION = RAIZ / "simulacion" / "documentos"
PLAN_SIMULACION = RAIZ / "simulacion" / "plan_AUD-2026-001.json"
POLITICAS_EJEMPLO = ["Protección de Datos Personales - UNSA.pdf", "Política de Privacidad - Infounsa.pdf"]
REVISION = ["Pendiente", "Confirmado", "Reclasificado a N", "Reclasificado a O", "Reclasificado a M", "Descartado"]

st.set_page_config(page_title="PIMS Privacy Assistant", page_icon="🛡️", layout="wide")


# ---------- configuración y acceso ----------

def _secreto(nombre: str) -> str | None:
    if os.environ.get(nombre):
        return os.environ[nombre]
    rutas = [RAIZ / ".streamlit" / "secrets.toml", Path.home() / ".streamlit" / "secrets.toml"]
    if not any(r.exists() for r in rutas) and not os.environ.get("STREAMLIT_SHARING_MODE"):
        return None  # en local sin secrets.toml: evita el aviso «No secrets found»
    try:
        return st.secrets.get(nombre)
    except Exception:  # sin secrets.toml en local
        return None


clave = _secreto("GEMINI_API_KEY")
if clave:
    os.environ["GEMINI_API_KEY"] = clave
password = _secreto("APP_PASSWORD")
if password and not st.session_state.get("autenticado"):
    st.title("🛡️ PIMS — acceso")
    intento = st.text_input("Contraseña de la aplicación", type="password")
    if intento and hmac.compare_digest(intento, password):
        st.session_state["autenticado"] = True
        st.rerun()
    elif intento:
        st.error("Contraseña incorrecta.")
    st.stop()

from agente import chat, medir  # noqa: E402
from agente.auditar import auditar  # noqa: E402
from conexion.config import MODELOS, MODELO_ACTIVO  # noqa: E402
from motor.evaluar import evaluar  # noqa: E402


# ---------- utilidades ----------

def carpetas(base: Path, excluir_prefijos=("seco",)) -> list[Path]:
    if not base.exists():
        return []
    return sorted([p for p in base.iterdir() if p.is_dir() and not p.name.startswith(excluir_prefijos)
                   and (p / "metadatos.json").exists()], key=lambda p: p.stat().st_mtime, reverse=True)


def zip_de(carpeta: Path) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in carpeta.rglob("*"):
            if f.is_file():
                z.write(f, f.relative_to(carpeta.parent))
    return buf.getvalue()


def leer_csv(ruta: Path) -> list[dict]:
    if not ruta.exists():
        return []
    with ruta.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def guardar_subidos(archivos, destino: Path) -> Path:
    destino.mkdir(parents=True, exist_ok=True)
    for a in archivos:
        (destino / Path(a.name).name).write_bytes(a.getbuffer())
    return destino


def ruta_politica(nombre: str) -> Path | None:
    for base in (RAIZ / "politicas", RAIZ):
        if (base / nombre).exists():
            return base / nombre
    return None


def selector_modelo(clave_widget: str) -> str:
    opciones = {f"{v} ({k})": v for k, v in MODELOS.items()}
    defecto = next(i for i, v in enumerate(opciones.values()) if v == MODELO_ACTIVO)
    return opciones[st.selectbox("Modelo", list(opciones), index=defecto, key=clave_widget)]


# ---------- encabezado ----------

st.title("🛡️ PIMS Privacy Assistant")
st.caption("Evaluación de privacidad y auditoría interna del PIMS con IA · ISO/IEC 27701:2025 · Los resultados son "
           "propuestas que el equipo auditor debe revisar: **no certifican cumplimiento**.")
if not clave:
    st.warning("No hay clave de Gemini (GEMINI_API_KEY). Puede revisar ejecuciones guardadas, pero no ejecutar "
               "evaluaciones nuevas ni usar el chat.")

tab1, tab2, tab3, tab4 = st.tabs(["📄 Evaluar política", "🔎 Auditoría", "💬 Chat", "ℹ️ Acerca de"])

# ---------- 1. SK-01 ----------

with tab1:
    st.subheader("Evaluar una política de privacidad frente al Anexo A de ISO/IEC 27701:2025")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        origen = st.radio("Documento", ["Política de ejemplo", "Subir un archivo"], horizontal=True, key="sk01_origen")
        archivo = None
        if origen == "Política de ejemplo":
            disponibles = [n for n in POLITICAS_EJEMPLO if ruta_politica(n)]
            elegido = st.selectbox("Política", disponibles) if disponibles else None
            archivo = ruta_politica(elegido) if elegido else None
        else:
            subido = st.file_uploader("PDF con texto, .txt o .md", type=["pdf", "txt", "md"], key="sk01_subida")
            if subido:
                tmp = Path(tempfile.mkdtemp())
                archivo = guardar_subidos([subido], tmp) / subido.name
        nombre = st.text_input("Nombre del documento (opcional)")
        fuente = st.text_input("Fuente (URL o procedencia)", value="no indicada")
        redactar = st.text_area("Texto a ocultar antes del envío (uno por línea; p. ej., nombres de personas)")
        modelo1 = selector_modelo("modelo_sk01")
        st.info("Envíe solo políticas públicas: en el nivel gratuito, Google puede usar el contenido enviado.")
        if st.button("Evaluar (1 solicitud a Gemini)", disabled=not (clave and archivo), type="primary"):
            with st.spinner("Evaluando…"):
                r = evaluar(str(archivo), nombre or None, fuente, modelo1, redactar.splitlines(), "app")
            (st.success if r["ok"] else st.error)(r["mensaje"])
            if r["ok"]:
                st.session_state["sk01_ver"] = r["carpeta"].name
    with col_b:
        ejec = carpetas(DIR_RES_SK01)
        nombres = [p.name for p in ejec]
        if nombres:
            idx = nombres.index(st.session_state["sk01_ver"]) if st.session_state.get("sk01_ver") in nombres else 0
            ver = st.selectbox("Ejecución guardada", nombres, index=idx, key="sk01_sel")
            c = DIR_RES_SK01 / ver
            meta = json.loads((c / "metadatos.json").read_text(encoding="utf-8"))
            st.caption(f"{meta.get('documento')} · Skill v{meta.get('skill_version', '0.1')} · {meta.get('modelo')} · "
                       f"{meta.get('fecha', '')}")
            st.download_button("Descargar carpeta (.zip)", zip_de(c), f"{ver}.zip", key="sk01_zip")
    if nombres:
        c = DIR_RES_SK01 / st.session_state.get("sk01_sel", nombres[0])
        with st.expander("Informe", expanded=True):
            st.markdown((c / "informe.md").read_text(encoding="utf-8"))
        with st.expander("Verificación automática"):
            st.markdown((c / "verificacion.md").read_text(encoding="utf-8"))

# ---------- 2. Agente de auditoría ----------

with tab2:
    st.subheader("Agente de evidencias y auditoría")
    with st.expander("▶ Ejecutar una auditoría nueva", expanded=False):
        plan = json.loads(PLAN_SIMULACION.read_text(encoding="utf-8"))
        origen2 = st.radio("Evidencias", ["Evidencias de demostración (14 documentos simulados)", "Subir documentos"],
                           horizontal=True)
        evid = DIR_SIMULACION
        if origen2 == "Subir documentos":
            subidos = st.file_uploader("Documentos de evidencia (.md, .txt, .pdf con texto)", type=["pdf", "txt", "md"],
                                       accept_multiple_files=True)
            evid = guardar_subidos(subidos, Path(tempfile.mkdtemp())) if subidos else None
        c1, c2 = st.columns(2)
        plan["codigo"] = c1.text_input("Código", plan["codigo"])
        plan["nombre"] = c2.text_input("Nombre", plan["nombre"])
        plan["objetivo"] = st.text_input("Objetivo", plan["objetivo"])
        plan["alcance"] = st.text_area("Alcance", plan["alcance"])
        plan["criterios"] = st.text_area("Criterios", plan["criterios"])
        c3, c4 = st.columns(2)
        plan["inicio"] = str(c3.date_input("Inicio", datetime.fromisoformat(plan["inicio"])))
        plan["fin"] = str(c4.date_input("Fin (base de las fechas compromiso)", datetime.fromisoformat(plan["fin"])))
        modelo2 = selector_modelo("modelo_agente")
        st.caption("Cada auditoría hace unas 11 solicitudes a Gemini (9 de SK-02, 1 de SK-03 y 1 de SK-04) y tarda "
                   "unos minutos.")
        if st.button("Ejecutar auditoría", disabled=not (clave and evid), type="primary"):
            with st.status("Ejecutando el agente…", expanded=True) as estado:
                r = auditar(plan, evid, "app", modelo2, aviso=st.write)
                estado.update(label=r["mensaje"], state="complete" if r["ok"] else "error")
            if r["ok"]:
                if evid != DIR_SIMULACION:  # guardar las evidencias subidas junto a la ejecución
                    shutil.copytree(evid, r["carpeta"] / "evidencias", dirs_exist_ok=True)
                st.session_state["agente_ver"] = r["carpeta"].name

    ejec = carpetas(DIR_RES_AGENTE)
    nombres = [p.name for p in ejec]
    if not nombres:
        st.info("Aún no hay ejecuciones del agente.")
    else:
        idx = nombres.index(st.session_state["agente_ver"]) if st.session_state.get("agente_ver") in nombres else 0
        ver = st.selectbox("Ejecución", nombres, index=idx, key="agente_sel")
        c = DIR_RES_AGENTE / ver
        meta = json.loads((c / "metadatos.json").read_text(encoding="utf-8"))
        st.caption(f"{meta['plan']['codigo']} · {meta.get('modelo')} · {meta.get('fecha', '')} · "
                   f"versiones {meta.get('versiones', {})}")
        filas = leer_csv(c / "lista_verificacion.csv")
        cont = meta.get("conteos", {})
        m = st.columns(6)
        for col, (k, etiqueta) in zip(m, [("Conforme", "Conformes"), ("N", "No conformidades"), ("O", "Observaciones"),
                                          ("M", "Oport. de mejora"), ("Sin evidencia", "Sin evidencia")]):
            col.metric(etiqueta, cont.get(k, 0))
        m[5].metric("Con alerta", sum(f.get("Alerta del verificador", "—") != "—" for f in filas))

        sub1, sub2, sub3, sub4 = st.tabs(["Lista de verificación", "Hallazgos y revisión", "Planes de acción", "Informe"])
        with sub1:
            solo_alertas = st.checkbox("Mostrar solo filas con alerta del verificador")
            vista = [f for f in filas if not solo_alertas or f.get("Alerta del verificador", "—") != "—"]
            st.dataframe([{k: f[k] for k in ("Código de requisito", "Requisito", "Resultado propuesto",
                                              "Alerta del verificador", "Evidencia encontrada")} for f in vista],
                         use_container_width=True, hide_index=True)
            with st.expander("Detalle de elementos y citas"):
                st.dataframe([{k: f[k] for k in ("Código de requisito", "Elementos (detalle)")} for f in vista],
                             use_container_width=True, hide_index=True)
        with sub2:
            hall = leer_csv(c / "hallazgos.csv")
            previa = {r["N.°"]: r for r in leer_csv(c / "revision_equipo.csv")}
            st.caption("Propuestas del agente. Registre la decisión del equipo para cada hallazgo; solo esto cuenta "
                       "como revisión humana.")
            datos = [{"N.°": h["N.°"], "Clasificación": h["Clasificación"], "Requisitos": h["Requisitos"],
                      "Descripción": h["Descripción"], "Evidencia": h["Evidencia"],
                      "Revisión del equipo": previa.get(h["N.°"], {}).get("Revisión del equipo", "Pendiente"),
                      "Nota": previa.get(h["N.°"], {}).get("Nota", "")} for h in hall]
            editado = st.data_editor(
                datos, use_container_width=True, hide_index=True, key=f"rev_{ver}",
                disabled=["N.°", "Clasificación", "Requisitos", "Descripción", "Evidencia"],
                column_config={"Revisión del equipo": st.column_config.SelectboxColumn(options=REVISION, required=True)})
            revisor = st.text_input("Nombre de quien revisa")
            if st.button("Guardar revisión del equipo", disabled=not revisor):
                with (c / "revision_equipo.csv").open("w", encoding="utf-8-sig", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=["N.°", "Clasificación", "Revisión del equipo", "Nota", "Revisor",
                                                      "Fecha"])
                    w.writeheader()
                    for e in editado:
                        w.writerow({"N.°": e["N.°"], "Clasificación": e["Clasificación"],
                                    "Revisión del equipo": e["Revisión del equipo"], "Nota": e["Nota"],
                                    "Revisor": revisor, "Fecha": datetime.now().isoformat(timespec="minutes")})
                st.success("Revisión guardada en revision_equipo.csv (las propuestas del agente no se modifican).")
        with sub3:
            st.dataframe(leer_csv(c / "plan_accion.csv"), use_container_width=True, hide_index=True)
        with sub4:
            st.markdown((c / "informe_auditoria.md").read_text(encoding="utf-8"))
            with st.expander("Verificación automática"):
                st.markdown((c / "verificacion.md").read_text(encoding="utf-8"))

        d1, d2, d3 = st.columns(3)
        d1.download_button("Descargar todo (.zip)", zip_de(c), f"{ver}.zip")
        d2.download_button("Lista de verificación (CSV para GESTITEL)", (c / "lista_verificacion.csv").read_bytes(),
                           "lista_verificacion.csv")
        d3.download_button("Hallazgos (CSV para GESTITEL)", (c / "hallazgos.csv").read_bytes(), "hallazgos.csv")
        if (RAIZ / "simulacion" / "clave" / "clave_simulacion.md").exists() and \
                meta.get("documentos") and meta["documentos"][0]["codigo"].startswith("SIM-PIMS"):
            if st.button("Medir la precisión del agente con el conjunto de prueba"):
                import sys
                sys.argv = ["medir", str(c)]
                medir.main()
            if (c / "medicion.md").exists():
                with st.expander("Precisión del agente (conjunto de prueba)", expanded=True):
                    st.markdown((c / "medicion.md").read_text(encoding="utf-8"))

# ---------- 3. Chat ----------

with tab3:
    st.subheader("Chat sobre una ejecución guardada")
    opciones = {f"Auditoría · {p.name}": p for p in carpetas(DIR_RES_AGENTE)}
    opciones |= {f"Política (SK-01) · {p.name}": p for p in carpetas(DIR_RES_SK01)}
    if not opciones:
        st.info("No hay ejecuciones guardadas.")
    else:
        sel = st.selectbox("Ejecución", list(opciones), key="chat_sel")
        carpeta_chat = opciones[sel]
        evid_chat = carpeta_chat / "evidencias" if (carpeta_chat / "evidencias").exists() else DIR_SIMULACION
        modelo3 = selector_modelo("modelo_chat")
        st.caption("Cada pregunta es una solicitud a Gemini. Las respuestas se basan solo en esta ejecución y sus "
                   "documentos; las citas se comprueban automáticamente.")
        hist = st.session_state.setdefault(f"hist_{sel}", [])
        for msg in hist:
            with st.chat_message("user" if msg["rol"] == "Usuario" else "assistant"):
                st.markdown(msg["texto"])
                for a in msg.get("avisos", []):
                    st.warning(a)
        pregunta = st.chat_input("Pregunte sobre los resultados (p. ej., ¿por qué 7.2 es una no conformidad?)",
                                 disabled=not clave)
        if pregunta:
            hist.append({"rol": "Usuario", "texto": pregunta})
            with st.spinner("Consultando…"):
                r = chat.responder(pregunta, carpeta_chat, hist[:-1], modelo3, evid_chat)
            hist.append({"rol": "Asistente", "texto": r["texto"], "avisos": r["avisos"]})
            st.rerun()

# ---------- 4. Acerca de ----------

with tab4:
    st.markdown("""
**Qué hace**

- **Evaluar política:** revisa una política de privacidad publicada frente a los 78 controles del Anexo A de
  ISO/IEC 27701:2025 e identifica posibles vacíos documentales, con cita y ubicación de cada evidencia.
- **Auditoría:** verifica los documentos de evidencia del PIMS frente a las cláusulas 4–10 y los controles del
  Anexo A, propone hallazgos (no conformidad, observación, oportunidad de mejora) y planes de acción en el formato del
  módulo Auditorías de GESTITEL, y redacta las conclusiones del informe.
- **Chat:** responde preguntas sobre una ejecución guardada, con citas verificadas automáticamente.

**Antes de usar los resultados**

- Son propuestas: el equipo auditor revisa y registra su decisión sobre cada hallazgo.
- La herramienta evalúa documentos; no reemplaza entrevistas ni pruebas en campo. No certifica cumplimiento ni es
  asesoría legal.
- El servicio de IA configurado (`gemini-3.5-flash-lite`, nivel gratuito) puede usar el contenido enviado: envíe solo
  documentos públicos o de prueba, y oculte los nombres de personas.
- Las evidencias de demostración son documentos simulados.
""")
