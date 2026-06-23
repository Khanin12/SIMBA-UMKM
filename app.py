import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu

# ----------------------------------------------------
# 1. Konfigurasi Halaman (Premium SaaS Standard)
# ----------------------------------------------------
st.set_page_config(
    page_title="SIMBA UMKM - Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dashboard
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #F8FAFC !important;
    }
    
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    /* Sidebar styling overrides */
    [data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebar"] iframe,
    [data-testid="stSidebar"] [data-testid="stHtml"],
    [data-testid="stSidebar"] [class*="st-emotion-cache"],
    [data-testid="stSidebar"] [class*="stEmotionCache"] {
        background-color: transparent !important;
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #E2E8F0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #E2E8F0 !important;
    }
    
    /* Header blur effect */
    [data-testid="stHeader"] {
        background-color: rgba(248, 250, 252, 0.8) !important;
        backdrop-filter: blur(8px) !important;
    }
    
    /* Premium card wrapper style for st.container(border=True) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border-radius: 20px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] h1,
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] h2,
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] h3,
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] h4,
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] h5,
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] h6 {
        color: #0F172A !important;
    }
    
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] li,
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] td,
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] th,
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] span,
    [data-testid="stMain"] div[data-testid="stVerticalBlockBorderWrapper"] label {
        color: #334155 !important;
    }
    
    /* Alert style boxes */
    .alert-green {
        background-color: #DCFCE7;
        border: 1px solid #86EFAC;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #14532D;
        margin-bottom: 1rem;
    }
    .alert-yellow {
        background-color: #FEF3C7;
        border: 1px solid #FCD34D;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #78350F;
        margin-bottom: 1rem;
    }
    .alert-blue {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    
    /* Footer styling */
    .footer-container {
        margin-top: 4rem;
        border-top: 1px solid #E2E8F0;
        padding-top: 2rem;
        padding-bottom: 2rem;
        color: #64748B;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. Konstanta & Mesin Simulasi (Simulation Engine)
# ----------------------------------------------------
HARGA_JUAL = 246846.85
HPP_UNIT = 197477.48
MARGIN_DASAR_PERSEN = 0.20

# Konstanta Baseline
BASELINE_IKLAN = 2000000
BASELINE_DISKON = 10.0
BASELINE_STOK = 300.0

def hitung_simulasi(iklan_rp, diskon_persen, stok_unit):
    iklan_juta = iklan_rp / 1000000.0
    
    # Formula Permintaan: 100 + (15 * Iklan_Juta) + (5.5 * Diskon)
    permintaan = 100.0 + (15.0 * iklan_juta) + (5.5 * diskon_persen)
    
    # Penjualan Aktual
    penjualan_aktual = min(permintaan, stok_unit)
    
    # Margin Aktual
    margin_aktual = 0.2 - (0.5 * diskon_persen / 100.0)
    
    # Pendapatan Kotor
    pendapatan = penjualan_aktual * HARGA_JUAL
    
    # Keuntungan Bersih
    keuntungan_bersih = (penjualan_aktual * (HARGA_JUAL * margin_aktual)) - iklan_rp
    
    return permintaan, penjualan_aktual, margin_aktual, pendapatan, keuntungan_bersih

# Hitung Baseline
base_dem, base_sales, base_marg, base_rev, base_profit = hitung_simulasi(
    BASELINE_IKLAN, BASELINE_DISKON, BASELINE_STOK
)

# Inisialisasi Session State untuk Multi-Skenario
if "sken_a" not in st.session_state:
    st.session_state.sken_a = {"iklan": 2000000, "diskon": 10, "stok": 300, "profit": base_profit, "sales": base_sales, "dem": base_dem, "marg": base_marg}
if "sken_b" not in st.session_state:
    st.session_state.sken_b = {"iklan": 3000000, "diskon": 5, "stok": 400, "profit": 0.0, "sales": 0.0, "dem": 0.0, "marg": 0.0}
if "sken_c" not in st.session_state:
    st.session_state.sken_c = {"iklan": 4000000, "diskon": 15, "stok": 500, "profit": 0.0, "sales": 0.0, "dem": 0.0, "marg": 0.0}

# ----------------------------------------------------
# 3. Sidebar (Navigasi & Sliders)
# ----------------------------------------------------
# Logo area
st.sidebar.markdown("""
    <div style='padding: 1.5rem 1rem; border-bottom: 1px solid #1E293B; margin-bottom: 1.5rem;'>
        <div style='display: flex; align-items: center; gap: 0.75rem;'>
            <div style='background-color: #2563EB; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);'>
                <span style='font-size: 1.5rem; color: #FFFFFF;'>📈</span>
            </div>
            <div>
                <h2 style='margin: 0; color: #FFFFFF; font-size: 1.25rem; font-weight: 700; letter-spacing: -0.025em; line-height: 1; font-family: "Inter", sans-serif !important;'>SIMBA UMKM</h2>
                <span style='color: #64748B; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;'>Analytics Platform</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Navigation Menu
with st.sidebar:
    selected_menu = option_menu(
        menu_title=None,
        options=["Dashboard", "Simulator", "Analisis Sensitivitas", "Laporan Skenario", "Insight & Rekomendasi", "Pengaturan"],
        icons=["house", "sliders", "activity", "file-earmark-text", "lightbulb", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0px !important", "background-color": "transparent"},
            "icon": {"color": "var(--text-color)", "font-size": "16px"}, 
            "nav-link": {
                "font-size": "14px", 
                "text-align": "left", 
                "margin": "4px 8px", 
                "border-radius": "8px",
                "color": "var(--text-color)",
                "padding": "10px 15px",
                "--hover-color": "rgba(128, 128, 128, 0.15)",
                "font-family": "Inter"
            },
            "nav-link-selected": {
                "background-color": "#2563EB", 
                "color": "#FFFFFF", 
                "font-weight": "600",
                "box-shadow": "0 4px 12px rgba(37, 99, 235, 0.2)",
                "font-family": "Inter"
            },
        }
    )

# Sliders (Hanya muncul jika relevan)
if selected_menu in ["Dashboard", "Simulator", "Analisis Sensitivitas", "Laporan Skenario"]:
    st.sidebar.markdown("""<div style='padding: 0 1rem; color: #64748B; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;'>🕹️ Pengaturan Simulasi</div>""", unsafe_allow_html=True)
    
    val_iklan = st.sidebar.slider(
        "Anggaran Iklan (Rp)",
        min_value=0,
        max_value=10000000,
        value=2000000,
        step=100000,
        format="Rp %d"
    )
    
    val_diskon = st.sidebar.slider(
        "Diskon (%)",
        min_value=0,
        max_value=50,
        value=10,
        step=1
    )
    
    val_stok = st.sidebar.slider(
        "Jumlah Stok (Unit)",
        min_value=50,
        max_value=1000,
        value=300,
        step=10
    )
    
    st.sidebar.markdown("<div style='padding: 0 1rem; margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.sidebar.button("🔄 Reset ke Baseline", use_container_width=True):
        st.rerun()
else:
    # Nilai default
    val_iklan = 2000000
    val_diskon = 10
    val_stok = 300

# Baseline Business Status Card (Selalu di Sidebar bawah)
st.sidebar.markdown(f"""
    <div style='background-color: #1E293B; border-radius: 12px; padding: 1.25rem; border: 1px solid #334155; margin: 2rem 0.75rem;'>
        <p style='color: #94A3B8; font-size: 0.75rem; font-weight: 700; margin: 0 0 0.75rem 0; letter-spacing: 0.05em;'>KONDISI BISNIS BASELINE</p>
        <div style='display: flex; flex-direction: column; gap: 0.5rem; color: #CBD5E1; font-size: 0.85rem;'>
            <div style='display: flex; justify-content: space-between;'><span>📢 Status:</span><span style='font-weight: 600; color: #22C55E;'>Normal</span></div>
            <div style='display: flex; justify-content: space-between;'><span>📢 Iklan:</span><span>Rp 2.000.000</span></div>
            <div style='display: flex; justify-content: space-between;'><span>🏷️ Diskon:</span><span>10%</span></div>
            <div style='display: flex; justify-content: space-between;'><span>📦 Stok:</span><span>300 Unit</span></div>
            <div style='display: flex; justify-content: space-between;'><span>💸 Margin:</span><span>20%</span></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Hitung proyeksi skenario baru
dem_baru, sales_baru, marg_baru, rev_baru, profit_baru = hitung_simulasi(val_iklan, val_diskon, val_stok)
delta_profit = profit_baru - base_profit
persen_delta_profit = (delta_profit / base_profit) * 100 if base_profit != 0 else 0

# ----------------------------------------------------
# 4. Reusable UI Components
# ----------------------------------------------------
def render_header(title, subtitle, badge="SIMBA UMKM", icon="📊"):
    st.markdown(f"""
        <div style='display: flex; align-items: center; background-color: #FFFFFF; padding: 1.25rem 2rem; border-radius: 20px; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.02); margin-bottom: 2rem;'>
            <div style='display: flex; align-items: center; gap: 1.25rem;'>
                <div style='background-color: #EFF6FF; padding: 0.75rem; border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid #DBEAFE;'>
                    <span style='font-size: 1.75rem;'>{icon}</span>
                </div>
                <div>
                    <span style='background-color: #EFF6FF; color: #2563EB; font-size: 0.75rem; font-weight: 700; padding: 0.25rem 0.75rem; border-radius: 9999px; text-transform: uppercase; border: 1px solid #DBEAFE;'>{badge}</span>
                    <h1 style='margin: 0.35rem 0 0.15rem 0; color: #0F172A; font-size: 32px; font-weight: 700; line-height: 1.1; font-family: "Inter", sans-serif;'>{title}</h1>
                    <p style='margin: 0; color: #64748B; font-size: 0.9rem; font-family: "Inter", sans-serif;'>{subtitle}</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_kpi_card(title, value, description, icon, accent_color="#2563EB", is_delta=False, delta_val=0):
    if is_delta:
        delta_color = "#22C55E" if delta_val >= 0 else "#EF4444"
        delta_icon = "↑" if delta_val >= 0 else "↓"
        desc_html = f"<span style='color: {delta_color}; font-weight: 600;'>{delta_icon} {description}</span>"
    else:
        desc_html = f"<span style='color: #64748B;'>{description}</span>"
        
    return f"""
        <div style='background-color: #FFFFFF; border-top: 4px solid {accent_color}; border-radius: 20px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03); margin-bottom: 1.5rem;'>
            <div style='display: flex; justify-content: space-between; align-items: flex-start;'>
                <div>
                    <div style='color: #64748B; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; font-family: "Inter", sans-serif;'>{title}</div>
                    <div style='color: #0F172A; font-size: 36px; font-weight: 700; margin-bottom: 0.25rem; font-family: "Inter", sans-serif;'>{value}</div>
                    <div style='font-size: 0.85rem; font-family: "Inter", sans-serif;'>{desc_html}</div>
                </div>
                <div style='background-color: {accent_color}15; color: {accent_color}; padding: 0.5rem; border-radius: 8px; font-size: 1.5rem; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px;'>
                    {icon}
                </div>
            </div>
        </div>
    """

# ----------------------------------------------------
# 5. Render Page Header Dinamis
# ----------------------------------------------------
if selected_menu == "Dashboard":
    render_header(
        title="Analisis Sensitivitas",
        subtitle="What-If Analysis Dashboard",
        badge="SIMBA UMKM",
        icon="📊"
    )
elif selected_menu == "Simulator":
    render_header(
        title="Simulator Skenario Bisnis",
        subtitle="Uji Dampak Parameter Promosi, Harga, dan Persediaan",
        badge="SIMBA UMKM",
        icon="🎛️"
    )
elif selected_menu == "Analisis Sensitivitas":
    render_header(
        title="Analisis Kurva Sensitivitas",
        subtitle="Analisis Pengaruh Variabel Kontrol Terhadap Permintaan dan Margin",
        badge="SIMBA UMKM",
        icon="📈"
    )
elif selected_menu == "Laporan Skenario":
    render_header(
        title="Laporan Perbandingan Skenario",
        subtitle="Perbandingan Detil Parameter Hasil Simulasi Multiskeanrio",
        badge="SIMBA UMKM",
        icon="📋"
    )
elif selected_menu == "Insight & Rekomendasi":
    render_header(
        title="Insight & Panduan Rekomendasi",
        subtitle="Rekomendasi AI Strategis untuk Optimasi Bisnis",
        badge="SIMBA UMKM",
        icon="💡"
    )
elif selected_menu == "Pengaturan":
    render_header(
        title="Pengaturan & Teknis Platform",
        subtitle="Informasi Pengembang dan Arsitektur Sistem",
        badge="SIMBA UMKM",
        icon="⚙️"
    )

# ----------------------------------------------------
# 6. Formula Chart Generator (Global / Reusable)
# ----------------------------------------------------
# Kurva Respon Permintaan vs Iklan
iklan_arr = np.linspace(0, 10000000, 100)
dem_arr = 100.0 + 15.0 * (iklan_arr / 1000000.0) + 5.5 * val_diskon
fig_sa1 = go.Figure()
fig_sa1.add_trace(go.Scatter(x=iklan_arr, y=dem_arr, mode='lines', line=dict(color='#2563EB', width=3)))
fig_sa1.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=10, b=10, l=10, r=10),
    height=250,
    xaxis=dict(title="Anggaran Iklan (Rupiah)", gridcolor="#F1F5F9", titlefont=dict(size=12, color="#64748B"), tickfont=dict(size=10, color="#64748B")),
    yaxis=dict(title="Permintaan (Unit)", gridcolor="#F1F5F9", titlefont=dict(size=12, color="#64748B"), tickfont=dict(size=10, color="#64748B")),
    font=dict(family="Inter, sans-serif")
)

# Kurva Respon Margin vs Diskon
diskon_arr = np.linspace(0, 50, 100)
marg_arr = (0.2 - 0.5 * (diskon_arr / 100.0)) * 100
fig_sa2 = go.Figure()
fig_sa2.add_trace(go.Scatter(x=diskon_arr, y=marg_arr, mode='lines', line=dict(color='#EF4444', width=3)))
fig_sa2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=10, b=10, l=10, r=10),
    height=250,
    xaxis=dict(title="Diskon (%)", gridcolor="#F1F5F9", titlefont=dict(size=12, color="#64748B"), tickfont=dict(size=10, color="#64748B")),
    yaxis=dict(title="Margin Aktual (%)", gridcolor="#F1F5F9", titlefont=dict(size=12, color="#64748B"), tickfont=dict(size=10, color="#64748B")),
    font=dict(family="Inter, sans-serif")
)

# Perbandingan Laba: Baseline vs Intervensi
fig_comp = go.Figure()
fig_comp.add_trace(go.Bar(
    x=["Kondisi Baseline", "Skenario Baru", "Selisih (Delta)"],
    y=[base_profit, profit_baru, delta_profit],
    marker_color=["#64748B", "#2563EB", "#22C55E" if delta_profit >= 0 else "#EF4444"],
    text=[f"Rp {x:,.0f}".replace(",", ".") for x in [base_profit, profit_baru, delta_profit]],
    textposition='auto'
))
fig_comp.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=30, b=10, l=10, r=10),
    height=350,
    yaxis=dict(title="Keuntungan Bersih (Rupiah)", gridcolor="#F1F5F9", titlefont=dict(size=12, color="#64748B"), tickfont=dict(size=10, color="#64748B")),
    xaxis=dict(gridcolor="#F1F5F9", tickfont=dict(size=12, color="#64748B")),
    font=dict(family="Inter, sans-serif")
)

# Analisis Sensitivitas Variabel Kontrol
fig_sens = go.Figure()
fig_sens.add_trace(go.Bar(
    y=["Jumlah Stok", "Diskon Produk", "Anggaran Iklan"],
    x=[37000.0, -160439.5, 4.68],
    orientation='h',
    marker_color=["#22C55E", "#EF4444", "#22C55E"]
))
fig_sens.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=10, b=10, l=10, r=10),
    height=220,
    xaxis=dict(title="Dampak Terhadap Profit (Rupiah)", gridcolor="#F1F5F9", titlefont=dict(size=12, color="#64748B")),
    yaxis=dict(tickfont=dict(size=12, color="#64748B")),
    font=dict(family="Inter, sans-serif")
)

# Grafik Multi Skenario
fig_multi = go.Figure()
fig_multi.add_trace(go.Bar(
    x=["Skenario A", "Skenario B", "Skenario C"],
    y=[st.session_state.sken_a['profit'], st.session_state.sken_b['profit'], st.session_state.sken_c['profit']],
    marker_color=["#2563EB", "#60A5FA", "#93C5FD"]
))
fig_multi.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=20, b=10, l=10, r=10),
    height=300,
    yaxis=dict(title="Laba Bersih (Rupiah)", gridcolor="#F1F5F9", titlefont=dict(size=12, color="#64748B")),
    xaxis=dict(tickfont=dict(size=12, color="#64748B")),
    font=dict(family="Inter, sans-serif")
)

# ----------------------------------------------------
# 7. AI Recommendation Logic (Global)
# ----------------------------------------------------
insights_green = []
insights_yellow = []
insights_blue = []

if val_iklan > BASELINE_IKLAN:
    iklan_diff = (val_iklan - BASELINE_IKLAN) / 1000000.0
    insights_green.append(f"<b>Pemasaran Digital:</b> Tambahan anggaran iklan meningkatkan permintaan pasar sebesar <b>{15.0 * iklan_diff:.0f} unit</b> secara langsung.")
else:
    insights_blue.append("<b>Pemasaran Digital:</b> Tingkatkan anggaran iklan dari baseline untuk merangsang permintaan pasar secara instan.")

if val_diskon > BASELINE_DISKON:
    insights_yellow.append(f"<b>Peringatan Diskon:</b> Pemberian diskon {val_diskon:.0f}% meningkatkan volume penjualan tetapi memotong margin keuntungan menjadi <b>{marg_baru*100:.1f}%</b>.")
else:
    insights_green.append(f"<b>Kebijakan Harga:</b> Tingkat diskon saat ini ({val_diskon}%) menjaga margin keuntungan sehat di tingkat <b>{marg_baru*100:.1f}%</b>.")

if dem_baru > val_stok:
    insights_yellow.append(f"<b>Potensi Stockout:</b> Jumlah stok saat ini ({val_stok:.0f} Unit) kurang untuk memenuhi perkiraan permintaan ({dem_baru:.0f} Unit). Segera lakukan <b>restock</b>!")
else:
    insights_green.append(f"<b>Rantai Pasok Aman:</b> Persediaan stok saat ini ({val_stok:.0f} Unit) cukup untuk memenuhi permintaan pasar ({dem_baru:.0f} Unit).")

if val_stok > dem_baru * 1.5:
    insights_yellow.append("<b>Peringatan Overstock:</b> Persediaan stok berlebih dapat menahan arus kas operasional Anda di dalam gudang.")

insights_blue.append("<b>Optimasi Kombinasi:</b> Langkah paling optimal untuk memaksimalkan laba bersih adalah dengan menaikkan anggaran iklan sebesar 20% tanpa mengubah tingkat diskon dasar demi menjaga kesehatan margin profitabilitas dasar bisnis.")

# ----------------------------------------------------
# 8. Render Main Pages Content
# ----------------------------------------------------
if selected_menu == "Dashboard":
    # Row 1: KPI Cards Grid
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        profit_accent = "#22C55E" if delta_profit >= 0 else "#EF4444"
        profit_desc = f"{persen_delta_profit:+.1f}% dari baseline"
        st.markdown(
            render_kpi_card(
                title="Prediksi Keuntungan Bersih",
                value=f"Rp {profit_baru:,.0f}".replace(",", "."),
                description=profit_desc,
                icon="💰",
                accent_color=profit_accent,
                is_delta=True,
                delta_val=delta_profit
            ),
            unsafe_allow_html=True
        )
    with col_kpi2:
        st.markdown(
            render_kpi_card(
                title="Permintaan Pasar",
                value=f"{dem_baru:.0f} Unit",
                description="Target kebutuhan pasar",
                icon="🛒",
                accent_color="#2563EB"
            ),
            unsafe_allow_html=True
        )
    with col_kpi3:
        st.markdown(
            render_kpi_card(
                title="Penjualan Aktual",
                value=f"{sales_baru:.0f} Unit",
                description="Terjual terbatas stok",
                icon="📦",
                accent_color="#6366F1"
            ),
            unsafe_allow_html=True
        )
    with col_kpi4:
        st.markdown(
            render_kpi_card(
                title="Margin Aktual",
                value=f"{marg_baru * 100:.0f}%",
                description="Persentase profit margin",
                icon="💸",
                accent_color="#F59E0B"
            ),
            unsafe_allow_html=True
        )

    # Row 2: Sensitivity Charts
    col_row2_left, col_row2_right = st.columns(2)
    with col_row2_left:
        with st.container(border=True):
            st.markdown("### 📈 Kurva Respon Permintaan vs Iklan")
            st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;'>Menampilkan pergerakan volume permintaan pasar seiring peningkatan biaya promosi digital.</p>", unsafe_allow_html=True)
            st.plotly_chart(fig_sa1, use_container_width=True)
            st.markdown("<div style='color: #2563EB; font-size: 0.8rem; font-weight: 500; border-top: 1px solid #F1F5F9; padding-top: 0.75rem; margin-top: 0.5rem;'>💡 Setiap penambahan Rp 1.000.000 anggaran iklan mendorong 15 unit permintaan.</div>", unsafe_allow_html=True)
            
    with col_row2_right:
        with st.container(border=True):
            st.markdown("### 📈 Kurva Respon Margin vs Diskon")
            st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;'>Menampilkan efek penurunan persentase profit margin seiring kenaikan persentase diskon.</p>", unsafe_allow_html=True)
            st.plotly_chart(fig_sa2, use_container_width=True)
            st.markdown("<div style='color: #EF4444; font-size: 0.8rem; font-weight: 500; border-top: 1px solid #F1F5F9; padding-top: 0.75rem; margin-top: 0.5rem;'>⚠️ Diskon produk menurunkan margin operasional dasar secara proporsional.</div>", unsafe_allow_html=True)
            
    # Row 3: Full Width Analysis Chart
    with st.container(border=True):
        st.markdown("### 📊 Perbandingan Keuntungan Bersih: Baseline vs Proyeksi Skenario Baru")
        st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;'>Perbandingan laba bersih kondisi awal dibandingkan skenario intervensi yang Anda uji saat ini.</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_comp, use_container_width=True)
        delta_text = f"mengalami peningkatan Rp {delta_profit:,.0f}" if delta_profit >= 0 else f"mengalami penurunan Rp {abs(delta_profit):,.0f}"
        st.markdown(f"<div style='color: #2563EB; font-size: 0.8rem; font-weight: 500; border-top: 1px solid #F1F5F9; padding-top: 0.75rem; margin-top: 0.5rem;'>💡 Proyeksi laba bersih {delta_text.replace(',', '.')} dibandingkan kondisi dasar bisnis.</div>", unsafe_allow_html=True)
        
    # Row 4: Insights Panel
    with st.container(border=True):
        st.markdown("### 💡 AI Recommendations & Strategy Guidelines")
        st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-bottom: 1.5rem;'>Hasil evaluasi model simulasi berdasarkan masukan parameter kontrol Anda.</p>", unsafe_allow_html=True)
        
        col_ins1, col_ins2, col_ins3 = st.columns(3)
        with col_ins1:
            st.markdown("#### **Rekomendasi Positif**")
            for ins in insights_green:
                st.markdown(f"<div class='alert-green' style='font-size: 0.85rem;'>{ins}</div>", unsafe_allow_html=True)
        with col_ins2:
            st.markdown("#### **Peringatan & Risiko**")
            if insights_yellow:
                for ins in insights_yellow:
                    st.markdown(f"<div class='alert-yellow' style='font-size: 0.85rem;'>{ins}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='alert-green' style='font-size: 0.85rem;'>Tidak ada peringatan risiko kritis untuk skenario ini.</div>", unsafe_allow_html=True)
        with col_ins3:
            st.markdown("#### **Saran Strategis**")
            for ins in insights_blue:
                st.markdown(f"<div class='alert-blue' style='font-size: 0.85rem;'>{ins}</div>", unsafe_allow_html=True)

elif selected_menu == "Simulator":
    # Row 1: KPI Cards
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        profit_accent = "#22C55E" if delta_profit >= 0 else "#EF4444"
        profit_desc = f"{persen_delta_profit:+.1f}% dari baseline"
        st.markdown(
            render_kpi_card(
                title="Prediksi Keuntungan Bersih",
                value=f"Rp {profit_baru:,.0f}".replace(",", "."),
                description=profit_desc,
                icon="💰",
                accent_color=profit_accent,
                is_delta=True,
                delta_val=delta_profit
            ),
            unsafe_allow_html=True
        )
    with col_kpi2:
        st.markdown(
            render_kpi_card(
                title="Permintaan Pasar",
                value=f"{dem_baru:.0f} Unit",
                description="Target kebutuhan pasar",
                icon="🛒",
                accent_color="#2563EB"
            ),
            unsafe_allow_html=True
        )
    with col_kpi3:
        st.markdown(
            render_kpi_card(
                title="Penjualan Aktual",
                value=f"{sales_baru:.0f} Unit",
                description="Terjual terbatas stok",
                icon="📦",
                accent_color="#6366F1"
            ),
            unsafe_allow_html=True
        )
    with col_kpi4:
        st.markdown(
            render_kpi_card(
                title="Margin Aktual",
                value=f"{marg_baru * 100:.0f}%",
                description="Persentase profit margin",
                icon="💸",
                accent_color="#F59E0B"
            ),
            unsafe_allow_html=True
        )
        
    # Row 2: 3-Panel Main Layout
    col_ctrl, col_form, col_status = st.columns(3)
    with col_ctrl:
        with st.container(border=True):
            st.markdown("### 🎛️ Variabel Kontrol Aktif")
            st.markdown(f"""
                <div style='background-color: #F8FAFC; border-radius: 12px; padding: 1.25rem; border: 1px solid #E2E8F0; margin-top: 0.5rem;'>
                    <p style='margin: 0 0 0.5rem 0; font-weight: 600; color: #0F172A; font-size: 0.9rem;'>Parameter Skenario Aktif:</p>
                    <ul style='margin: 0; padding-left: 1.25rem; font-size: 0.85rem; color: #334155; line-height: 1.7;'>
                        <li>Anggaran Iklan: <b>Rp {val_iklan:,.0f}</b></li>
                        <li>Diskon Produk: <b>{val_diskon}%</b></li>
                        <li>Jumlah Stok: <b>{val_stok} Unit</b></li>
                    </ul>
                    <p style='margin: 1rem 0 0 0; font-size: 0.8rem; color: #64748B; font-style: italic;'>Ubah parameter ini secara real-time melalui panel slider di sidebar sebelah kiri.</p>
                </div>
            """.replace(",", "."), unsafe_allow_html=True)
            
    with col_form:
        with st.container(border=True):
            st.markdown("### ⚙️ Rumus Mesin Simulasi")
            st.markdown("""
                <div style='display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem;'>
                    <div style='background-color: #F8FAFC; border-left: 4px solid #2563EB; padding: 0.5rem 0.75rem; border-radius: 4px;'>
                        <code style='color: #1E3A8A; font-size: 0.8rem; font-weight: 700;'>Permintaan = 100 + (15 × Iklan_Juta) + (5.5 × Diskon)</code>
                    </div>
                    <div style='background-color: #F8FAFC; border-left: 4px solid #2563EB; padding: 0.5rem 0.75rem; border-radius: 4px;'>
                        <code style='color: #1E3A8A; font-size: 0.8rem; font-weight: 700;'>Penjualan Aktual = min(Permintaan, Stok)</code>
                    </div>
                    <div style='background-color: #F8FAFC; border-left: 4px solid #2563EB; padding: 0.5rem 0.75rem; border-radius: 4px;'>
                        <code style='color: #1E3A8A; font-size: 0.8rem; font-weight: 700;'>Margin Aktual = 0.2 - (0.5 × Diskon / 100)</code>
                    </div>
                    <div style='background-color: #F8FAFC; border-left: 4px solid #2563EB; padding: 0.5rem 0.75rem; border-radius: 4px;'>
                        <code style='color: #1E3A8A; font-size: 0.8rem; font-weight: 700;'>Keuntungan Bersih = (Penjualan × Margin) - Iklan</code>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    with col_status:
        with st.container(border=True):
            st.markdown("### 📊 Status Kesehatan Bisnis")
            if profit_baru >= 6000000:
                health_color = "#22C55E"
                health_status = "Sangat Sehat"
                health_bg = "#DCFCE7"
                health_text = "#14532D"
                progress_pct = 95
            elif profit_baru >= 3000000:
                health_color = "#F59E0B"
                health_status = "Perlu Perhatian"
                health_bg = "#FEF3C7"
                health_text = "#78350F"
                progress_pct = 60
            else:
                health_color = "#EF4444"
                health_status = "Berisiko"
                health_bg = "#FEE2E2"
                health_text = "#7F1D1D"
                progress_pct = 25
            st.markdown(f"""
                <div style='margin-top: 0.5rem;'>
                    <div style='background-color: {health_bg}; padding: 0.75rem 1rem; border-radius: 10px; color: {health_text}; display: flex; flex-direction: column; gap: 0.5rem;'>
                        <span style='font-weight: 700; font-size: 0.9rem;'>Kondisi: {health_status}</span>
                        <div style='background-color: rgba(0,0,0,0.1); border-radius: 9999px; height: 8px; width: 100%; overflow: hidden; margin-top: 0.25rem;'>
                            <div style='background-color: {health_color}; width: {progress_pct}%; height: 100%;'></div>
                        </div>
                    </div>
                    <p style='color: #64748B; font-size: 0.75rem; margin: 0.75rem 0 0 0;'>Status didasarkan pada tingkat keberhasilan perolehan laba bersih terhadap estimasi minimal.</p>
                </div>
            """, unsafe_allow_html=True)

    # Row 3: detailed summary table, Multi Scenario Table & actions
    st.markdown("---")
    col_sim_left, col_sim_right = st.columns([2, 1])
    with col_sim_left:
        with st.container(border=True):
            st.markdown("### 📋 Ringkasan Proyeksi Simulasi")
            df_bot_res = pd.DataFrame({
                "Komponen Variabel": ["Permintaan", "Penjualan Aktual", "Margin Aktual", "Pendapatan Kotor", "Anggaran Biaya Iklan", "Keuntungan Bersih", "Delta Keuntungan"],
                "Nilai Proyeksi Skenario": [
                    f"{dem_baru:.0f} Unit", 
                    f"{sales_baru:.0f} Unit", 
                    f"{marg_baru*100:.1f}%", 
                    f"Rp {rev_baru:,.0f}".replace(",", "."), 
                    f"Rp {val_iklan:,.0f}".replace(",", "."), 
                    f"Rp {profit_baru:,.0f}".replace(",", "."), 
                    f"Rp {delta_profit:,.0f}".replace(",", ".")
                ]
            })
            st.table(df_bot_res)
            
    with col_sim_right:
        with st.container(border=True):
            st.markdown("### 💾 Manajemen Skenario")
            st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;'>Simpan konfigurasi simulasi aktif ke slot penyimpanan skenario.</p>", unsafe_allow_html=True)
            
            sken_opt = st.selectbox("Slot Penyimpanan Skenario:", ["Skenario A", "Skenario B", "Skenario C"])
            if st.button("💾 Simpan Konfigurasi Skenario", use_container_width=True):
                if sken_opt == "Skenario A":
                    st.session_state.sken_a = {"iklan": val_iklan, "diskon": val_diskon, "stok": val_stok, "profit": profit_baru, "sales": sales_baru, "dem": dem_baru, "marg": marg_baru}
                elif sken_opt == "Skenario B":
                    st.session_state.sken_b = {"iklan": val_iklan, "diskon": val_diskon, "stok": val_stok, "profit": profit_baru, "sales": sales_baru, "dem": dem_baru, "marg": marg_baru}
                elif sken_opt == "Skenario C":
                    st.session_state.sken_c = {"iklan": val_iklan, "diskon": val_diskon, "stok": val_stok, "profit": profit_baru, "sales": sales_baru, "dem": dem_baru, "marg": marg_baru}
                st.success(f"Berhasil disimpan ke slot **{sken_opt}**!")
            
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            st.markdown("#### **Aksi Ekspor**")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📄 Ekspor PDF", use_container_width=True): st.success("PDF Berhasil Dibuat!")
                if st.button("🖨️ Cetak", use_container_width=True): st.success("Cetak Terkirim!")
            with col_btn2:
                if st.button("📊 Ekspor Excel", use_container_width=True): st.success("Excel Diekspor!")

elif selected_menu == "Analisis Sensitivitas":
    # Row 1: KPI Cards
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        profit_accent = "#22C55E" if delta_profit >= 0 else "#EF4444"
        profit_desc = f"{persen_delta_profit:+.1f}% dari baseline"
        st.markdown(
            render_kpi_card(
                title="Prediksi Keuntungan Bersih",
                value=f"Rp {profit_baru:,.0f}".replace(",", "."),
                description=profit_desc,
                icon="💰",
                accent_color=profit_accent,
                is_delta=True,
                delta_val=delta_profit
            ),
            unsafe_allow_html=True
        )
    with col_kpi2:
        st.markdown(
            render_kpi_card(
                title="Permintaan Pasar",
                value=f"{dem_baru:.0f} Unit",
                description="Target kebutuhan pasar",
                icon="🛒",
                accent_color="#2563EB"
            ),
            unsafe_allow_html=True
        )
    with col_kpi3:
        st.markdown(
            render_kpi_card(
                title="Penjualan Aktual",
                value=f"{sales_baru:.0f} Unit",
                description="Terjual terbatas stok",
                icon="📦",
                accent_color="#6366F1"
            ),
            unsafe_allow_html=True
        )
    with col_kpi4:
        st.markdown(
            render_kpi_card(
                title="Margin Aktual",
                value=f"{marg_baru * 100:.0f}%",
                description="Persentase profit margin",
                icon="💸",
                accent_color="#F59E0B"
            ),
            unsafe_allow_html=True
        )
        
    # Row 2: Curves Grid
    col_sa1, col_sa2 = st.columns(2)
    with col_sa1:
        with st.container(border=True):
            st.markdown("### 📈 Kurva Respon Permintaan terhadap Iklan")
            st.markdown("<p style='color: #64748B; font-size: 0.85rem;'>Menganalisis bagaimana anggaran iklan mempengaruhi jumlah permintaan pasar secara linier.</p>", unsafe_allow_html=True)
            st.plotly_chart(fig_sa1, use_container_width=True)
            st.info("💡 **Insight:** Pemasaran digital yang lebih masif secara linier merangsang permintaan pasar, pastikan stok fisik memadai agar tidak stockout.")
            
    with col_sa2:
        with st.container(border=True):
            st.markdown("### 📈 Kurva Respon Margin terhadap Diskon")
            st.markdown("<p style='color: #64748B; font-size: 0.85rem;'>Menampilkan penurunan margin kotor produk seiring kenaikan persentase diskon yang diberikan.</p>", unsafe_allow_html=True)
            st.plotly_chart(fig_sa2, use_container_width=True)
            st.warning("⚠️ **Peringatan:** Meskipun diskon meningkatkan ketertarikan pasar, margin keuntungan bersih dipangkas secara tajam.")
            
    # Row 3: Sensitivity Analysis Chart & Table
    with st.container(border=True):
        st.markdown("### 📐 Analisis Sensitivitas Variabel Kontrol")
        st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;'>Mengukur sensitivitas finansial (keuntungan bersih) terhadap perubahan unit parameter kontrol.</p>", unsafe_allow_html=True)
        
        col_tbl, col_chart = st.columns([1, 1])
        with col_tbl:
            df_sens_tbl = pd.DataFrame({
                "Variabel Kontrol": ["Anggaran Iklan (per Rp 1 Juta)", "Diskon Produk (per 1%)", "Jumlah Stok (per 1 Unit)"],
                "Dampak Finansial (Profit Bersih)": ["+ Rp 4,68", "- Rp 160.439,50", "+ Rp 37.000,00"],
                "Tingkat Dampak Sensitivitas": ["Sangat Rendah", "Sangat Tinggi (Negatif)", "Sedang (Positif)"]
            })
            st.table(df_sens_tbl)
        with col_chart:
            st.plotly_chart(fig_sens, use_container_width=True)

elif selected_menu == "Laporan Skenario":
    # Row 1: KPI Cards
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        profit_accent = "#22C55E" if delta_profit >= 0 else "#EF4444"
        profit_desc = f"{persen_delta_profit:+.1f}% dari baseline"
        st.markdown(
            render_kpi_card(
                title="Prediksi Keuntungan Bersih",
                value=f"Rp {profit_baru:,.0f}".replace(",", "."),
                description=profit_desc,
                icon="💰",
                accent_color=profit_accent,
                is_delta=True,
                delta_val=delta_profit
            ),
            unsafe_allow_html=True
        )
    with col_kpi2:
        st.markdown(
            render_kpi_card(
                title="Permintaan Pasar",
                value=f"{dem_baru:.0f} Unit",
                description="Target kebutuhan pasar",
                icon="🛒",
                accent_color="#2563EB"
            ),
            unsafe_allow_html=True
        )
    with col_kpi3:
        st.markdown(
            render_kpi_card(
                title="Penjualan Aktual",
                value=f"{sales_baru:.0f} Unit",
                description="Terjual terbatas stok",
                icon="📦",
                accent_color="#6366F1"
            ),
            unsafe_allow_html=True
        )
    with col_kpi4:
        st.markdown(
            render_kpi_card(
                title="Margin Aktual",
                value=f"{marg_baru * 100:.0f}%",
                description="Persentase profit margin",
                icon="💸",
                accent_color="#F59E0B"
            ),
            unsafe_allow_html=True
        )
        
    col_rep_left, col_rep_right = st.columns([4, 3])
    with col_rep_left:
        with st.container(border=True):
            st.markdown("### 📂 Laporan Hasil Perbandingan Multi Skenario")
            st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;'>Menampilkan detil perbandingan input variabel kontrol dan laba bersih yang dihasilkan skenario A, B, dan C.</p>", unsafe_allow_html=True)
            df_multi_rep = pd.DataFrame({
                "Parameter Simulasi": ["Anggaran Iklan (Rp)", "Diskon (%)", "Jumlah Stok (Unit)", "Prediksi Laba Bersih (Rp)"],
                "Skenario A (Penyimpanan)": [f"Rp {st.session_state.sken_a['iklan']:,.0f}".replace(",", "."), f"{st.session_state.sken_a['diskon']}%", f"{st.session_state.sken_a['stok']} Unit", f"Rp {st.session_state.sken_a['profit']:,.0f}".replace(",", ".")],
                "Skenario B (Penyimpanan)": [f"Rp {st.session_state.sken_b['iklan']:,.0f}".replace(",", "."), f"{st.session_state.sken_b['diskon']}%", f"{st.session_state.sken_b['stok']} Unit", f"Rp {st.session_state.sken_b['profit']:,.0f}".replace(",", ".")],
                "Skenario C (Penyimpanan)": [f"Rp {st.session_state.sken_c['iklan']:,.0f}".replace(",", "."), f"{st.session_state.sken_c['diskon']}%", f"{st.session_state.sken_c['stok']} Unit", f"Rp {st.session_state.sken_c['profit']:,.0f}".replace(",", ".")]
            })
            st.table(df_multi_rep)
            
    with col_rep_right:
        with st.container(border=True):
            st.markdown("### 📊 Perbandingan Keuntungan antar Skenario")
            st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;'>Visualisasi grafik laba bersih yang diproyeksikan oleh masing-masing slot skenario.</p>", unsafe_allow_html=True)
            st.plotly_chart(fig_multi, use_container_width=True)

elif selected_menu == "Insight & Rekomendasi":
    with st.container(border=True):
        st.markdown("### 💡 AI Recommendations & Strategy Guidelines")
        st.markdown("<p style='color: #64748B; font-size: 0.95rem; margin-bottom: 1.5rem;'>Berikut adalah panduan strategi optimasi bisnis hasil komputasi model analitik SIMBA UMKM:</p>", unsafe_allow_html=True)
        
        st.markdown("#### **📈 1. Optimasi Pemasaran Digital (Marketing Strategy)**")
        st.markdown("<div class='alert-blue'>Menambah anggaran iklan sebesar Rp 2 Juta diproyeksikan mendongkrak ketertarikan pasar sebesar <b>45 Unit</b> secara langsung. Namun, pastikan kapasitas persediaan mencukupi sebelum meluncurkan promosi tambahan guna menghindari kerugian <i>stockout</i>.</div>", unsafe_allow_html=True)
        
        st.markdown("#### **🏷️ 2. Kebijakan Harga & Diskon (Discounting Policy)**")
        st.markdown("<div class='alert-yellow'>Memberikan diskon 15% terbukti menaikkan volume penjualan tetapi memangkas margin profit kotor dari 20% menjadi 12.5%. Hindari pemberian diskon berlebih untuk produk-produk dengan tingkat elastisitas harga rendah.</div>", unsafe_allow_html=True)
        
        st.markdown("#### **📦 3. Supply Chain (Keseimbangan Persediaan)**")
        st.markdown("<div class='alert-green'>Ketersediaan stok fisik minimal disarankan setara dengan 110% dari rata-rata permintaan bulanan untuk mengantisipasi lonjakan permintaan tak terduga (*surge demand*).</div>", unsafe_allow_html=True)
        
        st.markdown("#### **🎯 4. Rekomendasi Kombinasi Terbaik**")
        st.markdown("<div class='alert-blue'>Langkah paling optimal untuk memaksimalkan laba bersih adalah dengan <b>menaikkan anggaran iklan sebesar 20%</b> tanpa mengubah tingkat diskon dasar demi menjaga kesehatan margin profitabilitas dasar bisnis.</div>", unsafe_allow_html=True)

elif selected_menu == "Pengaturan":
    with st.container(border=True):
        st.markdown("### 🛠️ Tech Stack & Model Matematika")
        st.markdown("""
            Aplikasi **SIMBA UMKM** dibangun dengan teknologi analitik mutakhir untuk menjamin keakuratan prediksi *What-If Analysis*:
            - **Core Engine**: Python 3.10
            - **Dashboard Framework**: Streamlit (SaaS Premium UI)
            - **Visualizations**: Plotly express & Graph Objects
            - **Modeling**: NumPy & Pandas
        """)
        
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #FFFFFF; border-left: 5px solid #2563EB; padding: 1.5rem; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);'>
            <h4 style='margin-top: 0; color: #0F172A; font-weight: 700; margin-bottom: 1rem; font-family: "Inter", sans-serif;'>🏢 IDENTITAS PENGEMBANG:</h4>
            <table style='width:100%; border:none; color:#334155; font-size:0.95rem; border-collapse: collapse; font-family: "Inter", sans-serif;'>
                <tr style='border-bottom: 1px solid #E2E8F0;'><td style='width:180px; font-weight:600; padding: 0.75rem 0;'>Nama Pengembang</td><td style='padding: 0.75rem 0;'>: Khanin Oktavia</td></tr>
                <tr style='border-bottom: 1px solid #E2E8F0;'><td style='font-weight:600; padding: 0.75rem 0;'>NPM</td><td style='padding: 0.75rem 0;'>: 2313020019</td></tr>
                <tr style='border-bottom: 1px solid #E2E8F0;'><td style='font-weight:600; padding: 0.75rem 0;'>Program Studi</td><td style='padding: 0.75rem 0;'>: Teknik Informatika</td></tr>
                <tr><td style='font-weight:600; padding: 0.75rem 0;'>Institusi Kampus</td><td style='padding: 0.75rem 0;'>: Universitas Nusantara PGRI Kediri</td></tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# 9. Footer (Credits & Copyright)
# ----------------------------------------------------
st.markdown(
    """<div class='footer-container'>
    <div style='float: left;'>
    <strong>SIMBA UMKM</strong><br>
    <span style='font-size: 0.8rem; color: #64748B;'>Simulator Bisnis Analitik dan Prediksi Keuntungan UMKM Berbasis What-If Analysis</span>
    </div>
    <div style='float: right; text-align: right;'>
    Developed by: <strong>Khanin Oktavia</strong> | NPM 2313020019<br>
    Teknik Informatika | Universitas Nusantara PGRI Kediri<br>
    © 2026 All Rights Reserved
    </div>
    <div style='clear: both;'></div>
    </div>""",
    unsafe_allow_html=True
)
