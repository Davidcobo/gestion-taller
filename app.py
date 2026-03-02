import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="ERP Taller", layout="wide")

# CONEXIÓN CON GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# LEER DATOS ACTUALES
df = conn.read(ttl="0s") # ttl=0 para que refresque al instante

st.title("🏭 Gestión Taller Sincronizada")

menu = st.sidebar.selectbox("Ir a:", ["Ventas", "Laser", "Taller", "DTF", "Empaquetado"])

if menu == "Ventas":
    st.header("🛒 Nuevo Pedido")
    with st.form("f_nuevo"):
        cliente = st.text_input("Cliente")
        articulos = st.text_area("Trabajo a realizar")
        laser = st.checkbox("Laser")
        taller = st.checkbox("Taller")
        dtf = st.checkbox("DTF")
        if st.form_submit_button("Guardar"):
            # Crear nueva fila
            nueva_fila = pd.DataFrame([{
                "id": len(df) + 1,
                "cliente": cliente,
                "articulos": articulos,
                "laser": "Pendiente" if laser else "N/A",
                "taller": "Pendiente" if taller else "N/A",
                "dtf": "Pendiente" if dtf else "N/A",
                "empaquetado": "Pendiente"
            }])
            # Unir con los datos viejos y guardar
            df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
            conn.update(data=df_actualizado)
            st.success("¡Pedido guardado en la nube!")
            st.rerun()

# PANTALLAS DE SALAS (Láser, DTF, etc)
else:
    sala_col = menu.lower()
    st.header(f"📍 Sala: {menu}")
    # Filtrar solo los pendientes de esa sala
    pendientes = df[df[sala_col] == "Pendiente"]
    
    for index, row in pendientes.iterrows():
        with st.expander(f"Pedido #{row['id']} - {row['cliente']}"):
            st.write(row['articulos'])
            if st.button("TERMINAR TRABAJO", key=f"btn_{index}"):
                df.at[index, sala_col] = "Listo"
                conn.update(data=df)
                st.rerun()
