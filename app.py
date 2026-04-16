import streamlit as st
from datetime import datetime

# Configuración de página (ancho centrado tipo móvil)
st.set_page_config(page_title="Cierre de Caja", page_icon="💰", layout="centered")

# Título y fecha
st.title("💰 Cierre de Caja")
st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ================== LOCAL ==================
st.subheader("🏪 Cierre de Caja Local")

col1, col2 = st.columns(2)

with col1:
    com_fisicas = st.number_input("Comandas físicas", value=0.0, step=0.01, format="%.2f")
    caja_ini = st.number_input("Caja inicial", value=0.0, step=0.01, format="%.2f")
    efectivo_cont = st.number_input("Efectivo contado (real)", value=0.0, step=0.01, format="%.2f")
    depositos = st.number_input("Depósitos", value=0.0, step=0.01, format="%.2f")

with col2:
    pos = st.number_input("POS", value=0.0, step=0.01, format="%.2f")
    salidas = st.number_input("Salidas de dinero", value=0.0, step=0.01, format="%.2f")

# Cálculos
ventas_efectivo = com_fisicas - pos
efectivo_ideal = ventas_efectivo + caja_ini - salidas
diferencia = efectivo_cont - efectivo_ideal
estado_final = efectivo_cont - depositos

st.markdown("### 📊 Resultados")
r1, r2 = st.columns(2)
r1.metric("Ventas en efectivo", f"{ventas_efectivo:,.2f}")
r1.metric("Efectivo final (ideal)", f"{efectivo_ideal:,.2f}")
r2.metric("Diferencia", f"{diferencia:,.2f}", delta_color="inverse")
r2.metric("Estado final en caja", f"{estado_final:,.2f}")

st.divider()

# ================== TOTAL ==================
st.subheader("💳 Cierre de Caja Total (Físico + Digital)")

col3, col4 = st.columns(2)

with col3:
    pos_ventas = st.number_input("POS y ventas en efectivo", value=0.0, step=0.01, format="%.2f", key="pos_total")
    fondo_ini = st.number_input("Fondo inicial", value=0.0, step=0.01, format="%.2f")
    caja_contada = st.number_input("Caja contada (real)", value=0.0, step=0.01, format="%.2f")
    depositos_total = st.number_input("Depósitos", value=0.0, step=0.01, format="%.2f", key="dep_total")

with col4:
    salidas_total = st.number_input("Salidas de dinero (total)", value=0.0, step=0.01, format="%.2f")
    pedidos_ya = st.number_input("Pedidos Ya", value=0.0, step=0.01, format="%.2f")

ventas_totales = pos_ventas + pedidos_ya
caja_ideal = pos_ventas + fondo_ini + pedidos_ya - salidas_total
diferencia_total = caja_contada - caja_ideal
estado_cuentas = caja_contada - depositos_total

st.markdown("### 📊 Resultados")
r3, r4 = st.columns(2)
r3.metric("Ventas totales", f"{ventas_totales:,.2f}")
r3.metric("Caja ideal", f"{caja_ideal:,.2f}")
r4.metric("Diferencia", f"{diferencia_total:,.2f}", delta_color="inverse")
r4.metric("Estado final de cuentas", f"{estado_cuentas:,.2f}")

st.caption("✅ Datos en tiempo real - Cierre de caja")
