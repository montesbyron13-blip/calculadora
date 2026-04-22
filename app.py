import streamlit as st
import io
import base64
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cierre de Caja", page_icon="💰", layout="centered")

# --- INICIALIZACIÓN SEGURA DE CADA CLAVE ---
# Local
if 'local_com_fisicas' not in st.session_state:
    st.session_state.local_com_fisicas = 0.0
if 'local_pos' not in st.session_state:
    st.session_state.local_pos = 0.0
if 'local_caja_ini' not in st.session_state:
    st.session_state.local_caja_ini = 0.0
if 'local_salidas' not in st.session_state:
    st.session_state.local_salidas = 0.0
if 'local_efectivo_cont' not in st.session_state:
    st.session_state.local_efectivo_cont = 0.0
if 'local_depositos' not in st.session_state:
    st.session_state.local_depositos = 0.0

# Total
if 'total_pos_ventas' not in st.session_state:
    st.session_state.total_pos_ventas = 0.0
if 'total_fondo_ini' not in st.session_state:
    st.session_state.total_fondo_ini = 0.0
if 'total_salidas' not in st.session_state:
    st.session_state.total_salidas = 0.0
if 'total_caja_contada' not in st.session_state:
    st.session_state.total_caja_contada = 0.0
if 'total_pedidos_ya' not in st.session_state:
    st.session_state.total_pedidos_ya = 0.0
if 'total_depositos' not in st.session_state:
    st.session_state.total_depositos = 0.0

# Banderas de reset
if 'reset_local_flag' not in st.session_state:
    st.session_state.reset_local_flag = False
if 'reset_total_flag' not in st.session_state:
    st.session_state.reset_total_flag = False

# --- PROCESAR RESETS ---
if st.session_state.reset_local_flag:
    st.session_state.local_com_fisicas = 0.0
    st.session_state.local_pos = 0.0
    st.session_state.local_caja_ini = 0.0
    st.session_state.local_salidas = 0.0
    st.session_state.local_efectivo_cont = 0.0
    st.session_state.local_depositos = 0.0
    st.session_state.reset_local_flag = False
    st.rerun()

if st.session_state.reset_total_flag:
    st.session_state.total_pos_ventas = 0.0
    st.session_state.total_fondo_ini = 0.0
    st.session_state.total_salidas = 0.0
    st.session_state.total_caja_contada = 0.0
    st.session_state.total_pedidos_ya = 0.0
    st.session_state.total_depositos = 0.0
    st.session_state.reset_total_flag = False
    st.rerun()

# --- FUNCIONES DE GENERACIÓN DE IMAGEN Y TICKET (sin cambios, pero las incluyo completas) ---
def generar_imagen_resultados(datos_local, datos_total):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.axis('off')
    ax.set_facecolor('#f0f0f0')
    fig.patch.set_facecolor('#f0f0f0')
    ax.text(0.5, 0.98, "💰 CIERRE DE CAJA", transform=ax.transAxes, fontsize=16, fontweight='bold', ha='center')
    ax.text(0.5, 0.94, now, transform=ax.transAxes, fontsize=10, ha='center')
    y = 0.88
    ax.text(0.05, y, "🏪 CIERRE LOCAL", transform=ax.transAxes, fontsize=12, fontweight='bold')
    y -= 0.04
    ax.text(0.05, y, f"Comandas físicas: {datos_local['com_fisicas']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.03
    ax.text(0.05, y, f"POS: {datos_local['pos']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.03
    ax.text(0.05, y, f"Caja inicial: {datos_local['caja_ini']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.03
    ax.text(0.05, y, f"Salidas dinero: {datos_local['salidas']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.03
    ax.text(0.05, y, f"Efectivo contado: {datos_local['efectivo_cont']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.03
    ax.text(0.05, y, f"Depósitos: {datos_local['depositos']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.04
    ax.text(0.05, y, f"📊 Ventas efectivo: {datos_local['ventas_efectivo']:,.2f}", transform=ax.transAxes, fontsize=10, fontweight='bold')
    y -= 0.03
    ax.text(0.05, y, f"📊 Efectivo ideal: {datos_local['efectivo_ideal']:,.2f}", transform=ax.transAxes, fontsize=10, fontweight='bold')
    y -= 0.03
    diferencia_color = 'red' if datos_local['diferencia'] != 0 else 'green'
    ax.text(0.05, y, f"⚠️ Diferencia: {datos_local['diferencia']:,.2f}", transform=ax.transAxes, fontsize=10, fontweight='bold', color=diferencia_color)
    y -= 0.03
    ax.text(0.05, y, f"💵 Estado final caja: {datos_local['estado_final']:,.2f}", transform=ax.transAxes, fontsize=10, fontweight='bold')
    y -= 0.05
    ax.text(0.05, y, "─"*50, transform=ax.transAxes, fontsize=10)
    y -= 0.05
    ax.text(0.05, y, "💳 CIERRE TOTAL", transform=ax.transAxes, fontsize=12, fontweight='bold')
    y -= 0.04
    ax.text(0.05, y, f"POS + ventas efectivo: {datos_total['pos_ventas']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.03
    ax.text(0.05, y, f"Fondo inicial: {datos_total['fondo_ini']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.03
    ax.text(0.05, y, f"Salidas totales: {datos_total['salidas']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.03
    ax.text(0.05, y, f"Caja contada: {datos_total['caja_contada']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.03
    ax.text(0.05, y, f"Pedidos Ya: {datos_total['pedidos_ya']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.03
    ax.text(0.05, y, f"Depósitos: {datos_total['depositos']:,.2f}", transform=ax.transAxes, fontsize=10)
    y -= 0.04
    ax.text(0.05, y, f"📊 Ventas totales: {datos_total['ventas_totales']:,.2f}", transform=ax.transAxes, fontsize=10, fontweight='bold')
    y -= 0.03
    ax.text(0.05, y, f"📊 Caja ideal: {datos_total['caja_ideal']:,.2f}", transform=ax.transAxes, fontsize=10, fontweight='bold')
    y -= 0.03
    dif_total_color = 'red' if datos_total['diferencia'] != 0 else 'green'
    ax.text(0.05, y, f"⚠️ Diferencia: {datos_total['diferencia']:,.2f}", transform=ax.transAxes, fontsize=10, fontweight='bold', color=dif_total_color)
    y -= 0.03
    ax.text(0.05, y, f"🏦 Estado cuentas: {datos_total['estado_cuentas']:,.2f}", transform=ax.transAxes, fontsize=10, fontweight='bold')
    y -= 0.06
    ax.text(0.5, y, "✅ Cierre de Caja App", transform=ax.transAxes, fontsize=9, ha='center', style='italic')
    plt.tight_layout()
    return fig

def generar_html_ticket(datos_local, datos_total):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    html = f"""
    <html>
    <head><meta charset="UTF-8"><style>
        @media print {{ body {{ margin: 0; padding: 0; }} }}
        body {{ font-family: monospace; font-size: 12px; width: 80mm; padding: 5mm; margin: 0 auto; }}
        .center {{ text-align: center; }}
        .line {{ border-top: 1px dashed #000; margin: 5px 0; }}
        table {{ width: 100%; }}
        td {{ padding: 2px 0; }}
        .right {{ text-align: right; }}
        .title {{ font-weight: bold; font-size: 14px; margin: 5px 0; }}
    </style></head>
    <body>
        <div class="center"><b>💰 CIERRE DE CAJA</b><br/>{now}</div>
        <div class="line"></div>
        <div class="title">🏪 CIERRE LOCAL</div>
        <table>
            <tr><td>Comandas físicas:</td><td class="right">{datos_local['com_fisicas']:,.2f}</td></tr>
            <tr><td>POS:</td><td class="right">{datos_local['pos']:,.2f}</td></tr>
            <tr><td>Caja inicial:</td><td class="right">{datos_local['caja_ini']:,.2f}</td></tr>
            <tr><td>Salidas dinero:</td><td class="right">{datos_local['salidas']:,.2f}</td></tr>
            <tr><td>Efectivo contado:</td><td class="right">{datos_local['efectivo_cont']:,.2f}</td></tr>
            <tr><td>Depósitos:</td><td class="right">{datos_local['depositos']:,.2f}</td></tr>
        </table>
        <div class="line"></div>
        <table>
            <tr><td><b>Ventas efectivo:</b></td><td class="right"><b>{datos_local['ventas_efectivo']:,.2f}</b></td></tr>
            <tr><td><b>Efectivo ideal:</b></td><td class="right"><b>{datos_local['efectivo_ideal']:,.2f}</b></td></tr>
            <tr><td><b>Diferencia:</b></td><td class="right"><b>{datos_local['diferencia']:,.2f}</b></td></tr>
            <tr><td><b>Estado final caja:</b></td><td class="right"><b>{datos_local['estado_final']:,.2f}</b></td></tr>
        </table>
        <div class="line"></div>
        <div class="title">💳 CIERRE TOTAL</div>
        <table>
            <tr><td>POS + ventas efectivo:</td><td class="right">{datos_total['pos_ventas']:,.2f}</td></tr>
            <tr><td>Fondo inicial:</td><td class="right">{datos_total['fondo_ini']:,.2f}</td></tr>
            <tr><td>Salidas totales:</td><td class="right">{datos_total['salidas']:,.2f}</td></tr>
            <tr><td>Caja contada:</td><td class="right">{datos_total['caja_contada']:,.2f}</td></tr>
            <tr><td>Pedidos Ya:</td><td class="right">{datos_total['pedidos_ya']:,.2f}</td></tr>
            <tr><td>Depósitos:</td><td class="right">{datos_total['depositos']:,.2f}</td></tr>
        </table>
        <div class="line"></div>
        <tr>
            <tr><td><b>Ventas totales:</b></td><td class="right"><b>{datos_total['ventas_totales']:,.2f}</b></td></tr>
            <tr><td><b>Caja ideal:</b></td><td class="right"><b>{datos_total['caja_ideal']:,.2f}</b></td></tr>
            <tr><td><b>Diferencia:</b></td><td class="right"><b>{datos_total['diferencia']:,.2f}</b></td></tr>
            <tr><td><b>Estado cuentas:</b></td><td class="right"><b>{datos_total['estado_cuentas']:,.2f}</b></td></tr>
        </table>
        <div class="line"></div>
        <div class="center">✅ Cierre de Caja App</div>
    </body>
    </html>
    """
    return html

# --- INTERFAZ DE USUARIO ---
st.title("💰 Cierre de Caja")
st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# SECCIÓN LOCAL
st.subheader("🏪 Cierre de Caja Local")
col1, col2 = st.columns(2)

with col1:
    com_fisicas = st.number_input("Comandas físicas", value=st.session_state.local_com_fisicas, step=0.01, format="%.2f", key="local_com_fisicas")
    caja_ini = st.number_input("Caja inicial", value=st.session_state.local_caja_ini, step=0.01, format="%.2f", key="local_caja_ini")
    efectivo_cont = st.number_input("Efectivo contado (real)", value=st.session_state.local_efectivo_cont, step=0.01, format="%.2f", key="local_efectivo_cont")
    depositos = st.number_input("Depósitos", value=st.session_state.local_depositos, step=0.01, format="%.2f", key="local_depositos")
with col2:
    pos = st.number_input("POS", value=st.session_state.local_pos, step=0.01, format="%.2f", key="local_pos")
    salidas = st.number_input("Salidas de dinero", value=st.session_state.local_salidas, step=0.01, format="%.2f", key="local_salidas")

if st.button("🔄 Resetear Local", key="reset_local_btn"):
    st.session_state.reset_local_flag = True
    st.rerun()

ventas_efectivo = com_fisicas - pos
efectivo_ideal = ventas_efectivo + caja_ini - salidas
diferencia = efectivo_cont - efectivo_ideal
estado_final = efectivo_cont - depositos

st.markdown("### 📊 Resultados Locales")
r1, r2 = st.columns(2)
r1.metric("Ventas en efectivo", f"{ventas_efectivo:,.2f}")
r1.metric("Efectivo final (ideal)", f"{efectivo_ideal:,.2f}")
r2.metric("Diferencia", f"{diferencia:,.2f}", delta_color="inverse")
r2.metric("Estado final en caja", f"{estado_final:,.2f}")

st.divider()

# SECCIÓN TOTAL
st.subheader("💳 Cierre de Caja Total (Físico + Digital)")
col3, col4 = st.columns(2)

with col3:
    pos_ventas = st.number_input("POS y ventas en efectivo", value=st.session_state.total_pos_ventas, step=0.01, format="%.2f", key="total_pos_ventas")
    fondo_ini = st.number_input("Fondo inicial", value=st.session_state.total_fondo_ini, step=0.01, format="%.2f", key="total_fondo_ini")
    caja_contada = st.number_input("Caja contada (real)", value=st.session_state.total_caja_contada, step=0.01, format="%.2f", key="total_caja_contada")
    depositos_total = st.number_input("Depósitos", value=st.session_state.total_depositos, step=0.01, format="%.2f", key="total_depositos")
with col4:
    salidas_total = st.number_input("Salidas de dinero (total)", value=st.session_state.total_salidas, step=0.01, format="%.2f", key="total_salidas")
    pedidos_ya = st.number_input("Pedidos Ya", value=st.session_state.total_pedidos_ya, step=0.01, format="%.2f", key="total_pedidos_ya")

if st.button("🔄 Resetear Total", key="reset_total_btn"):
    st.session_state.reset_total_flag = True
    st.rerun()

ventas_totales = pos_ventas + pedidos_ya
caja_ideal = pos_ventas + fondo_ini + pedidos_ya - salidas_total
diferencia_total = caja_contada - caja_ideal
estado_cuentas = caja_contada - depositos_total

st.markdown("### 📊 Resultados Totales")
r3, r4 = st.columns(2)
r3.metric("Ventas totales", f"{ventas_totales:,.2f}")
r3.metric("Caja ideal", f"{caja_ideal:,.2f}")
r4.metric("Diferencia", f"{diferencia_total:,.2f}", delta_color="inverse")
r4.metric("Estado final de cuentas", f"{estado_cuentas:,.2f}")

st.divider()

# EXPORTAR
st.subheader("📤 Exportar datos")

datos_local = {
    'com_fisicas': com_fisicas, 'pos': pos, 'caja_ini': caja_ini, 'salidas': salidas,
    'efectivo_cont': efectivo_cont, 'depositos': depositos,
    'ventas_efectivo': ventas_efectivo, 'efectivo_ideal': efectivo_ideal,
    'diferencia': diferencia, 'estado_final': estado_final
}
datos_total = {
    'pos_ventas': pos_ventas, 'fondo_ini': fondo_ini, 'salidas': salidas_total,
    'caja_contada': caja_contada, 'pedidos_ya': pedidos_ya, 'depositos': depositos_total,
    'ventas_totales': ventas_totales, 'caja_ideal': caja_ideal,
    'diferencia': diferencia_total, 'estado_cuentas': estado_cuentas
}

fig = generar_imagen_resultados(datos_local, datos_total)
buf = io.BytesIO()
fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
buf.seek(0)
st.download_button(label="📸 Descargar imagen PNG (para WhatsApp)", data=buf,
                   file_name=f"cierre_caja_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", mime="image/png")
plt.close(fig)

st.subheader("🖨️ Imprimir ticket térmico")
html_ticket = generar_html_ticket(datos_local, datos_total)
b64 = base64.b64encode(html_ticket.encode()).decode()
st.markdown(f'<a href="data:text/html;base64,{b64}" download="ticket_cierre.html">📄 Descargar HTML (para imprimir después)</a>', unsafe_allow_html=True)
st.components.v1.html(f"""
<button onclick="window.print()" style="padding:10px; background-color:#4CAF50; color:white; border:none; border-radius:5px; cursor:pointer; margin-top:10px;">
    🖨️ Imprimir ticket ahora
</button>
<div style="display:none;">{html_ticket}</div>
""", height=100)
st.info("💡 Al hacer clic en 'Imprimir ticket ahora', el navegador abrirá la vista previa. Selecciona tu impresora térmica Bluetooth/WiFi desde allí.")
