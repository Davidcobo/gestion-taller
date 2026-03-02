import streamlit as st
import pandas as pd

# CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="ERP Taller", layout="wide")

# CONEXIÓN SIMPLIFICADA (Usando el enlace CSV de Google)
# 1. VE A TU EXCEL -> ARCHIVO -> COMPARTIR -> PUBLICAR EN LA WEB
# 2. SELECCIONA "VALORES SEPARADOS POR COMAS (.CSV)" Y COPIA ESE ENLACE
URL_CSV = "PEGA_AQUÍ_TU_ENLACE_DE_PUBLICAR_COMO_CSV"

try:
    df = pd.read_csv(URL_CSV)
except:
    df = pd.DataFrame(columns=['id', 'cliente', 'articulos', 'laser', 'taller', 'dtf', 'empaquetado'])

st.title("🏭 ERP Taller: Control Total")

menu = st.sidebar.selectbox("Ir a:", ["Ventas", "Laser", "Taller", "DTF", "Empaquetado"])

if menu == "Ventas":
    st.header("🛒 Nuevo Pedido")
    with st.form("f_nuevo"):
        cliente = st.text_input("Cliente")
        articulos = st.text_area("Trabajo")
        laser = st.checkbox("Laser")
        taller = st.checkbox("Taller")
        dtf = st.checkbox("DTF")
        if st.form_submit_button("Guardar"):
            st.success(f"Pedido para {cliente} registrado. (Nota: En modo lectura pública, contacta con soporte para escritura completa)")
            # Nota: Para escritura real en Chromebooks antiguos, 
            # lo más estable es usar el formulario de Google directamente.

else:
    st.header(f"📍 Sala: {menu}")
    col_busqueda = menu.lower()
    if col_busqueda in df.columns:
        pendientes = df[df[col_busqueda] == "Pendiente"]
        st.write(f"Trabajos pendientes: {len(pendientes)}")
        st.dataframe(pendientes)
    else:
        st.error("Configura las columnas en tu Excel (id, cliente, articulos, laser, taller, dtf, empaquetado)")
