# src/app.py - Dashboard completo con gráficos mejorados
import streamlit as st
import pandas as pd
from processing import load_data, get_basic_stats, filter_by_team
from viz import (
    plot_goals_histogram, 
    plot_goals_over_time, 
    plot_home_away_goals,
    plot_top_scorers_teams,
    plot_corners_per_match,
    plot_extra_analysis
)

# Configuración de la página
st.set_page_config(
    page_title="Eliminatorias Sudamericanas", 
    page_icon="⚽", 
    layout="wide"
)

# Título principal
st.title("⚽ Dashboard de las Eliminatorias Sudamericanas 2023-2026")
st.markdown("---")

# Sidebar para cargar archivo
st.sidebar.header("📂 Carga de datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Cargar datos
    df = load_data(uploaded_file)
    st.sidebar.success("✅ Archivo cargado correctamente")
    
    # Mostrar estadísticas globales
    stats = get_basic_stats(df)
    
    st.subheader("📈 Estadísticas generales del torneo")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📊 Partidos", stats['partidos'])
    col2.metric("⚽ Goles totales", stats['goles_totales'])
    col3.metric("📈 Promedio goles", f"{stats['promedio_goles']:.2f}")
    col4.metric("🏟️ Equipos", stats['equipos'])
    
    # Calcular BTTS (ambos anotan)
    btts = ((df['home_team_goal_count'] > 0) & (df['away_team_goal_count'] > 0)).mean() * 100
    col5.metric("🤝 BTTS", f"{btts:.1f}%")
    
    st.markdown("---")
    
    # Filtro por equipo
    st.sidebar.header("🔍 Filtros")
    equipos = sorted(pd.concat([df['home_team_name'], df['away_team_name']]).unique())
    equipo_sel = st.sidebar.selectbox("Selecciona un equipo", ["Todos"] + equipos)
    
    # Filtro por rango de goles
    min_goles = st.sidebar.slider("Mínimo de goles por partido", 0, 8, 0)
    
    # Aplicar filtros
    if equipo_sel != "Todos":
        df_filt = filter_by_team(df, equipo_sel)
        st.subheader(f"📋 Datos filtrados: {equipo_sel}")
    else:
        df_filt = df
        st.subheader("📋 Datos completos")
    
    df_filt = df_filt[df_filt['total_goal_count'] >= min_goles]
    
    # Mostrar tabla de partidos (colapsable)
    with st.expander("📋 Ver tabla de partidos"):
        columnas_mostrar = ['date_GMT', 'home_team_name', 'away_team_name', 
                            'home_team_goal_count', 'away_team_goal_count', 
                            'total_goal_count', 'stadium_name']
        st.dataframe(df_filt[columnas_mostrar].head(30))
    
    st.markdown("---")
    
    # ========== GRÁFICOS ==========
    st.subheader("📊 Visualizaciones interactivas")
    
    # Fila 1: Histograma y Evolución temporal
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.markdown("**📊 Distribución de goles**")
        fig1 = plot_goals_histogram(df_filt)
        st.pyplot(fig1)
    
    with col_graf2:
        st.markdown("**📈 Evolución de goles**")
        fig2 = plot_goals_over_time(df_filt)
        if fig2:
            st.pyplot(fig2)
    
    # Fila 2: Local vs Visitante y Top equipos
    col_graf3, col_graf4 = st.columns(2)
    
    with col_graf3:
        st.markdown("**🏠 Local vs Visitante ✈️**")
        fig3 = plot_home_away_goals(df_filt)
        st.pyplot(fig3)
    
    with col_graf4:
        st.markdown("**🏆 Top equipos goleadores**")
        fig4 = plot_top_scorers_teams(df_filt)
        st.pyplot(fig4)
    
    # Fila 3: Corners
    st.markdown("**📐 Análisis de corners**")
    fig5 = plot_corners_per_match(df_filt)
    st.pyplot(fig5)
    
    # ========== ANÁLISIS AVANZADO (dentro del if) ==========
    st.markdown("---")
    st.subheader("📈 Análisis avanzado")
    fig6 = plot_extra_analysis(df_filt)
    st.pyplot(fig6)
    # ========================================================
    
    # Mostrar información adicional en sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ Información")
    st.sidebar.info(f"""
    - **Partidos mostrados:** {df_filt.shape[0]}
    - **Rango de goles:** ≥ {min_goles}
    - **Equipo filtrado:** {equipo_sel if equipo_sel != 'Todos' else 'Ninguno'}
    """)
    
else:
    # Mensaje cuando no hay archivo cargado
    st.info("👈 **Usa el panel lateral para cargar el archivo CSV**")
    st.markdown("""
    ### 📋 Instrucciones:
    1. Haz clic en **"Browse files"** en el panel izquierdo
    2. Selecciona tu archivo CSV
    3. Explora las estadísticas y gráficos automáticamente
    """)