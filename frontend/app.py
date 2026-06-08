import streamlit as st
import psycopg2
import psycopg2.extras
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime
from contextlib import contextmanager

# ── 1. ARCHITECTURAL HUD LAYOUT SYSTEM ────────────────────────────────
st.set_page_config(
    page_title="CrimeIQ Pakistan • Command Hub",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Cyber-Grid Dark Mode Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Base Body Reset */
    .stApp {
        background-color: #07090E;
        color: #E2E8F0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Modern Glassmorphic KPI Cards */
    .kpi-container {
        background: linear-gradient(135deg, rgba(20, 30, 55, 0.6) 0%, rgba(10, 15, 30, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 3px solid #3B82F6;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .kpi-container:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.3);
    }
    .kpi-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        font-weight: 600;
    }
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-top: 0.25rem;
    }
    .kpi-subtext {
        font-size: 0.8rem;
        color: #38BDF8;
        margin-top: 0.25rem;
    }
    
    /* Title Treatments */
    .glitch-title {
        font-weight: 800;
        text-transform: uppercase;
        background: linear-gradient(180deg, #FFFFFF 0%, #CBD5E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    
    /* Form elements & Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0A0D14 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Hide native Streamlit UI artifacts */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── DATABASE CONNECTIVITY LAYER (PRODUCTION SECURE) ───────────────────
@st.cache_resource
def get_connection_pool():
    """Generates a cached, pooled database connection matching production cloud handles."""
    if "database" in st.secrets:
        # Use encrypted cloud variables if deployed live
        return psycopg2.connect(
            dbname=st.secrets["database"]["dbname"],
            user=st.secrets["database"]["user"],
            password=st.secrets["database"]["password"],
            host=st.secrets["database"]["host"],
            port=st.secrets["database"]["port"],
            sslmode="require" # Crucial for Render cloud connections
        )
    else:
        # Fallback to your local instance if testing on your laptop
        return psycopg2.connect(
            dbname="CrimeIQ",
            user="postgres",
            password="admin123",
            host="localhost",
            port="5432"
        )

# Global Version Fix: Ensures compatibility across all Pandas 3.0+ execution states
from pandas.io.formats.style import Styler
if not hasattr(Styler, 'applymap'):
    Styler.applymap = Styler.map

@contextmanager
def db_cursor():
    """Safely opens, processes, and immediately recycles connections without resource leaks."""
    conn = get_connection_pool()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        yield cur
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()

def run_query(sql_query, parameters=None):
    """Executes atomic reads cleanly wrapping the safe context router."""
    conn = get_connection_pool()
    return pd.read_sql(sql_query, conn, params=parameters)

# ── 3. RADAR CONTROL INTERFACE (SIDEBAR) ──────────────────────────────
with st.sidebar:
    st.markdown("<div style='text-align: center; padding-top: 1rem;'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/color/96/police-badge.png", width=70)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-top: 0.5rem;'>CrimeIQ Pakistan</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B; font-size: 0.85rem; margin-top:-0.5rem;'>Predictive Crime Analytics Platform</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.selectbox(
        "Select Tactical Deck",
        ["Dashboard", "Crime Map", "COMPSTAT Matrix", "Risk Forecasts", "Active Hotspots"]
    )
    
    st.markdown("---")
    st.caption("⚡ Core Engine Status: Online")
    st.caption("👤 Project Team: Abdul Muqsit Alam & Abdullah Shamim")
    st.caption("🏫 BNU — ADBMS Project 2026")

# ── 4. PAGE 1: EXECUTIVE COMMAND DASHBOARD ────────────────────────────
if page == "Dashboard":
    st.markdown("<h1 class='glitch-title'>🚨 Strategic Command Dashboard</h1>", unsafe_allow_html=True)
    st.caption("COMPSTAT & PredPol-Inspired Real-Time Analytics — Lahore & Greater Punjab")
    st.markdown("---")
    
    # Accelerated Parallel Analytics Processing
    total_crimes = run_query("SELECT COUNT(*) FROM crimes;").iloc[0, 0]
    solved = run_query("SELECT COUNT(*) FROM crimes WHERE status = 'solved';").iloc[0, 0]
    active_hotspots = run_query("SELECT COUNT(*) FROM hotspots WHERE valid_until > NOW();").iloc[0, 0]
    total_districts = run_query("SELECT COUNT(*) FROM districts;").iloc[0, 0]
    solve_rate = round((solved / max(total_crimes, 1) * 100), 1)

    # HTML Custom Metrics Grid Execution
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(f'<div class="kpi-container"><div class="kpi-label">Total Logged Crimes</div><div class="kpi-value">{total_crimes:,}</div><div class="kpi-subtext">Gross Regional Intake</div></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div class="kpi-container" style="border-top-color: #10B981;"><div class="kpi-label">Solved Inquiries</div><div class="kpi-value">{solved:,}</div><div class="kpi-subtext">📈 {solve_rate}% Solve Efficiency</div></div>', unsafe_allow_html=True)
    with m_col3:
        st.markdown(f'<div class="kpi-container" style="border-top-color: #EF4444;"><div class="kpi-label">Active Hotspots</div><div class="kpi-value">{active_hotspots:,}</div><div class="kpi-subtext">Critical Patrolled Clusters</div></div>', unsafe_allow_html=True)
    with m_col4:
        st.markdown(f'<div class="kpi-container" style="border-top-color: #F59E0B;"><div class="kpi-label">Monitored Sectors</div><div class="kpi-value">{total_districts:,}</div><div class="kpi-subtext">Active Police Precincts</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Plotly Visual Grid
    g_col1, g_col2 = st.columns(2)
    
    with g_col1:
        st.markdown("### 📊 Classification Breakdown")
        crime_types = run_query("SELECT crime_type, COUNT(*) AS total FROM crimes GROUP BY crime_type ORDER BY total DESC;")
        fig = px.pie(crime_types, values='total', names='crime_type', hole=0.45, color_discrete_sequence=px.colors.sequential.Cividis)
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
        
    with g_col2:
        st.markdown("### 🏛️ Volume Distribution by Sector")
        by_district = run_query("SELECT d.name AS district, COUNT(*) AS total FROM crimes c JOIN districts d ON c.district_id = d.district_id GROUP BY d.name ORDER BY total DESC;")
        fig2 = px.bar(by_district, x='district', y='total', color='total', color_continuous_scale='Cividis', labels={'total':'Volume', 'district':'Precinct'})
        fig2.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig2, use_container_width=True)

    # Secondary Full Width Visual Grid
    st.markdown("### 🚨 Threat Level Density Vector")
    severity = run_query("SELECT severity, COUNT(*) AS total FROM crimes GROUP BY severity ORDER BY total DESC;")
    fig3 = px.bar(severity, x='severity', y='total', color='severity', color_discrete_map={'high': '#EF4444', 'medium': '#F59E0B', 'low': '#10B981'})
    fig3.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig3, use_container_width=True)

# ── 5. PAGE 2: SPATIAL VECTOR MAP ─────────────────────────────────────
elif page == "Crime Map":
    st.markdown("<h1 class='glitch-title'>🗺️ Geospace Tactical Radar</h1>", unsafe_allow_html=True)
    st.caption("Spatial distribution and automated multi-crime trigger point arrays across Lahore neighborhoods")
    st.markdown("---")
    
    ctrl_col, map_col = st.columns([1, 3])
    
    with ctrl_col:
        st.markdown("### 🎛️ Filter Vectors")
        crime_filter = st.selectbox("Select Target Specification", ["All", "Vehicle Theft", "Snatching", "Burglary", "Homicide", "Armed Robbery", "Cybercrime"])
        severity_filter = st.selectbox("Select Target Intensity", ["All", "high", "medium", "low"])
        
    # Constructing Safe Prepared Filtering Arguments
    where_clauses = ["1=1"]
    params = []
    if crime_filter != "All":
        where_clauses.append("c.crime_type = %s")
        params.append(crime_filter)
    if severity_filter != "All":
        where_clauses.append("c.severity = %s")
        params.append(severity_filter)
        
    where_sql = " AND ".join(where_clauses)
    crimes_df = run_query(f"""
        SELECT c.crime_id, d.name AS district, c.crime_type, c.latitude, c.longitude, 
               c.location_name, c.severity, c.status, c.occurred_at
        FROM crimes c
        JOIN districts d ON c.district_id = d.district_id
        WHERE {where_sql} ORDER BY c.occurred_at DESC LIMIT 300;
    """, params)

    with map_col:
        st.caption(f"Visualizing {len(crimes_df)} Incident Data Points")
        
        # Build Mapbox Dark Grid Base
        m = folium.Map(location=[31.4904, 74.3436], zoom_start=12, tiles='CartoDB dark_matter')
        color_map = {'high': '#EF4444', 'medium': '#F59E0B', 'low': '#10B981'}
        
        for _, row in crimes_df.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                color=color_map.get(row['severity'].lower(), '#3B82F6'),
                fill=True,
                fill_opacity=0.6,
                popup=f"<b>{row['crime_type']}</b><br>Sector: {row['district']}<br>Location: {row['location_name']}"
            ).add_to(m)
            
        # Draw Hotspots Layer safely
        hotspots_layer_df = run_query("SELECT h.*, d.name as district_name FROM hotspots h JOIN districts d ON h.district_id = d.district_id WHERE h.valid_until > NOW();")
        for _, h_spot in hotspots_layer_df.iterrows():
            folium.Marker(
                location=[h_spot['latitude'], h_spot['longitude']],
                popup=f"🔴 ACTIVE HOTSPOT: {h_spot['crime_type']} | Risk Rating: {h_spot['risk_score']}",
                icon=folium.Icon(color='red', icon='exclamation-sign')
            ).add_to(m)
            
        st_folium(m, width="100%", height=550, returned_objects=[])

# ── 6. PAGE 3: COMPSTAT PERFORMANCE MATRIX ────────────────────────────
elif page == "COMPSTAT Matrix":
    st.markdown("<h1 class='glitch-title'>📊 Analytical COMPSTAT Matrix</h1>", unsafe_allow_html=True)
    st.caption("Weekly performance metrics and sector containment targets — inspired by NYPD COMPSTAT Protocols")
    st.markdown("---")
    
    try:
        compstat_data = run_query("""
            SELECT district, crime_type, week::text, total_crimes, solved, solve_rate, moving_avg
            FROM district_weekly_stats ORDER BY week DESC, total_crimes DESC;
        """)
        
        if not compstat_data.empty:
            c_col1, c_col2 = st.columns(2)
            
            with c_col1:
                st.markdown("### 🏛️ Bulk Volumetric Output by District")
                dist_sum = compstat_data.groupby('district')['total_crimes'].sum().reset_index()
                fig_c1 = px.bar(dist_sum, x='district', y='total_crimes', color='total_crimes', color_continuous_scale='Blues')
                fig_c1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig_c1, use_container_width=True)
                
            with c_col2:
                st.markdown("### 🎯 Real Mean Case Enforcement Rates")
                rate_sum = compstat_data.groupby('district')['solve_rate'].mean().reset_index()
                fig_c2 = px.bar(rate_sum, x='district', y='solve_rate', color='solve_rate', color_continuous_scale='Greens')
                fig_c2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig_c2, use_container_width=True)

            st.markdown("### Executive Performance Grid")
            
            def map_compstat_formatting(val):
                try:
                    num = float(str(val).replace('%', ''))
                    if num >= 40.0: return 'background-color: rgba(16, 185, 129, 0.15); color: #10B981; font-weight: bold;'
                    return 'background-color: rgba(239, 68, 68, 0.15); color: #EF4444;'
                except ValueError:
                    return ''
                    
            styled_compstat = compstat_data.style.format({
                'total_crimes': '{:,}', 'solved': '{:,}', 'solve_rate': '{:.1f}%', 'moving_avg': '{:.1f}'
            }).map(map_compstat_formatting, subset=['solve_rate'])
            
            st.dataframe(styled_compstat, width="stretch", hide_index=True)
            
        else:
            st.warning("Materialized target views do not contain synchronized records yet.")
            if st.button("Synchronize Materialized Analytics View"):
                with db_cursor() as cur:
                    cur.execute("REFRESH MATERIALIZED VIEW district_weekly_stats;")
                st.success("Synchronization finalized. Refreshing interface.")
                st.rerun()
                
    except Exception as e:
        st.error(f"Internal Pipeline Communication Blocked: {e}")

# ── 7. PAGE 4: PREDPol HORIZON RISK ENGINE ────────────────────────────
elif page == "Risk Forecasts":
    st.markdown("<h1 class='glitch-title'>🔮 Forward Horizon Risk Engine</h1>", unsafe_allow_html=True)
    st.caption("PredPol-inspired statistical crime density projection maps over rolling 168-hour windows")
    st.markdown("---")
    
    forecasts = run_query("""
        SELECT d.name AS district, f.crime_type, f.forecast_date::text, LOWER(f.risk_level) as risk_level, f.predicted_count, f.confidence
        FROM risk_forecasts f JOIN districts d ON f.district_id = d.district_id
        WHERE f.forecast_date >= CURRENT_DATE
        ORDER BY 
            CASE LOWER(f.risk_level)
                WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4
            END, f.forecast_date;
    """)
    
    if not forecasts.empty:
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        f_col1.metric("Critical Vectors", len(forecasts[forecasts['risk_level']=='critical']))
        f_col2.metric("High Hazards", len(forecasts[forecasts['risk_level']=='high']))
        f_col3.metric("Elevated Arrays", len(forecasts[forecasts['risk_level']=='medium']))
        f_col4.metric("Baseline Normalcy", len(forecasts[forecasts['risk_level']=='low']))
        
        st.markdown("<br>### Volumetric Threat Matrix Mapping", unsafe_allow_html=True)
        
        def layout_color_threats(val):
            mapping = {
                'critical': 'background-color: rgba(239, 68, 68, 0.2); color: #EF4444; font-weight: bold;',
                'high': 'background-color: rgba(245, 158, 11, 0.2); color: #F59E0B;',
                'medium': 'background-color: rgba(59, 130, 246, 0.2); color: #3B82F6;',
                'low': 'background-color: rgba(16, 185, 129, 0.2); color: #10B981;'
            }
            return mapping.get(str(val).lower(), '')

        styled_forecast = forecasts.style.format({'predicted_count': '{:,}', 'confidence': '{:.1f}%'}).map(layout_color_threats, subset=['risk_level'])
        st.dataframe(styled_forecast, width="stretch", hide_index=True)
        
        # Matrix heat chart execution
        pivot = forecasts.pivot_table(index='district', columns='forecast_date', values='predicted_count', aggfunc='sum').fillna(0)
        fig_heat = px.imshow(pivot, color_continuous_scale='YlOrRd', title="Spatial Density Projections Matrix Ledger")
        fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("Algorithmic forecast streams are completely empty.")
        if st.button("Trigger Pipeline Calculations Now"):
            with db_cursor() as cur:
                cur.execute("CALL build_crime_patterns();")
                cur.execute("CALL generate_weekly_forecasts();")
            st.success("Algorithmic modeling finished.")
            st.rerun()

# ── 8. PAGE 5: ACTIVE HOTSPOT TRACKER ─────────────────────────────────
elif page == "Active Hotspots":
    st.markdown("<h1 class='glitch-title'>🔴 Active Hotspot Clusters</h1>", unsafe_allow_html=True)
    st.caption("Auto-generated by PostgreSQL engine triggers when 3+ crimes register within a 500m radius over rolling 7-day intervals")
    st.markdown("---")
    
    hotspots = run_query("""
        SELECT h.hotspot_id, d.name AS district, h.crime_type, h.risk_score, h.crime_count,
               h.generated_at::text, h.valid_until::text, h.latitude, h.longitude
        FROM hotspots h JOIN districts d ON h.district_id = d.district_id
        WHERE h.valid_until > NOW() ORDER BY h.risk_score DESC;
    """)
    
    if not hotspots.empty:
        st.metric("Gross Live Critical Hotspots Active", len(hotspots))
        
        h_map = folium.Map(location=[31.4904, 74.3436], zoom_start=12, tiles='CartoDB dark_matter')
        for _, h_row in hotspots.iterrows():
            folium.CircleMarker(
                location=[h_row['latitude'], h_row['longitude']],
                radius=max(int(h_row['risk_score'] / 8), 8),
                color='#EF4444',
                fill=True,
                fill_opacity=0.5,
                popup=f"<b>Hotspot Triggered</b><br>Count: {h_row['crime_count']} Events<br>Risk Index: {h_row['risk_score']}"
            ).add_to(h_map)
            
        st_folium(h_map, width="100%", height=450, returned_objects=[])
        
        st.markdown("<br>### Critical Hazard Ledger", unsafe_allow_html=True)
        st.dataframe(hotspots.drop(columns=['latitude', 'longitude']), width="stretch", hide_index=True)
    else:
        st.info("No active spatial anomalies currently monitored. System limits nominal.")
