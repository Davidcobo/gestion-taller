import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="ERP Taller Multizona", layout="wide")

st.title("🏭 Sistema Integral de Gestión de Taller")

# --- NAVEGACIÓN ---
menu = st.sidebar.selectbox("Ir a:", ["Ventas (Mostrador)", "Láser", "Taller (Serigrafía)", "DTF", "Empaquetado", "Admin"])

# SIMULACIÓN DE BASE DE DATOS (En el siguiente paso la conectaremos a Google Sheets)
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = []

# --- MÓDULO VENTAS ---
if menu == "Ventas (Mostrador)":
    st.header("🛒 Registro de Nuevo Pedido")
    with st.form("nuevo_pedido"):
        cliente = st.text_input("Cliente")
        tel = st.text_input("Teléfono")
        col1, col2, col3 = st.columns(3)
        with col1: laser = st.checkbox("Láser")
        with col2: taller = st.checkbox("Serigrafía/Tampo")
        with col3: dtf = st.checkbox("DTF")
        articulos = st.text_area("Descripción de los artículos")
        total = st.number_input("Total (€)", min_value=0.0)
        senal = st.number_input("Señal (€)", min_value=0.0)
        
        if st.form_submit_button("Guardar Pedido"):
            nuevo = {
                "id": len(st.session_state.pedidos) + 1,
                "cliente": cliente, "tel": tel, "articulos": articulos,
                "laser": "Pendiente" if laser else "N/A",
                "taller": "Pendiente" if taller else "N/A",
                "dtf": "Pendiente" if dtf else "N/A",
                "empaquetado": "Pendiente",
                "total": total, "senal": senal
            }
            st.session_state.pedidos.append(nuevo)
            st.success("✅ Pedido registrado con éxito")

# --- MÓDULOS DE PRODUCCIÓN (LÁSER, TALLER, DTF) ---
def pantalla_produccion(nombre_sala, clave_estado):
    st.header(f"📍 Sala: {nombre_sala}")
    for p in st.session_state.pedidos:
        if p[clave_estado] == "Pendiente":
            with st.expander(f"Pedido #{p['id']} - {p['cliente']}"):
                st.write(f"**Trabajo:** {p['articulos']}")
                if st.button(f"Terminar en {nombre_sala}", key=f"{nombre_sala}_{p['id']}"):
                    p[clave_estado] = "Listo"
                    st.rerun()

if menu == "Láser": pantalla_produccion("Láser", "laser")
if menu == "Taller (Serigrafía)": pantalla_produccion("Serigrafía", "taller")
if menu == "DTF": pantalla_produccion("DTF", "dtf")

# --- MÓDULO EMPAQUETADO ---
if menu == "Empaquetado":
    st.header("📦 Control de Salida")
    for p in st.session_state.pedidos:
        # Solo empaquetamos si todo lo técnico está "Listo" o "N/A"
        if all(p[k] in ["Listo", "N/A"] for k in ["laser", "taller", "dtf"]) and p["empaquetado"] == "Pendiente":
            with st.expander(f"ORDEN LISTA: #{p['id']} - {p['cliente']}"):
                bultos = st.number_input("Número de bultos", min_value=1, key=f"b_{p['id']}")
                if st.button("Finalizar y Etiquetar", key=f"btn_{p['id']}"):
                    p["empaquetado"] = "COMPLETO"
                    st.success(f"Aviso enviado a {p['cliente']}. ¡Pedido cerrado!")

# --- VISTA ADMIN (PRIVADA) ---
if menu == "Admin":
    st.header("📊 Resumen Económico")
    if st.session_state.pedidos:
        df = pd.DataFrame(st.session_state.pedidos)
        st.table(df[["id", "cliente", "total", "senal"]])
        st.metric("Total en Caja", f"{df['total'].sum()} €")
    else:
        st.write("No hay pedidos registrados.")
