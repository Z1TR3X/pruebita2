import streamlit as st
import pandas as pd
from processing import load_data, get_basic_stats, filter_by_team
from viz import plot_goals_histogram, plot_goals_over_time

st.set_page_config(page_title="Eliminatorias Sudamericanas", layout="wide")
st.title("⚽ Dashboard de las Eliminatorias 2023-2026")
st.markdown("Fuente: Datos oficiales de partidos")

# Sidebar para cargar archivo
st.sidebar.header("1. Carga el archivo CSV")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo (formato CSV)", type=["csv"])

if uploaded_file is not None:
    # Cargar datos
    df = load_data(uploaded_file)
    st.sidebar.success("✅ Archivo cargado correctamente")
    
    # Mostrar estadísticas globales
    stats = get_basic_stats(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Partidos", stats['partidos'])
    col2.metric("Goles totales", stats['goles_totales'])
    col3.metric("Promedio goles", f"{stats['promedio_goles']:.2f}")
    col4.metric("Equipos distintos", stats['equipos'])
    
    # Filtro por equipo
    st.sidebar.header("2. Filtrar por equipo")
    equipos = sorted(pd.concat([df['home_team_name'], df['away_team_name']]).unique())
    equipo_sel = st.sidebar.selectbox("Selecciona un equipo", ["Todos"] + equipos)
    
    if equipo_sel != "Todos":
        df_filt = filter_by_team(df, equipo_sel)
        st.subheader(f"📋 Partidos de {equipo_sel}")
    else:
        df_filt = df
        st.subheader("📋 Últimos partidos")
    
    # Mostrar tabla
    st.dataframe(df_filt[['date_GMT', 'home_team_name', 'away_team_name', 
                          'home_team_goal_count', 'away_team_goal_count', 
                          'total_goal_count', 'stadium_name']].head(20))
    
    # Gráficos
    st.subheader("📊 Visualizaciones")
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        fig1 = plot_goals_histogram(df_filt)
        st.pyplot(fig1)
    with col_graf2:
        fig2 = plot_goals_over_time(df_filt)
        if fig2:
            st.pyplot(fig2)
        else:
            st.info("No se pudo generar el gráfico temporal")
else:
    st.info("👈 Usa el panel lateral para cargar el archivo CSV de las eliminatorias")
    st.markdown("""
    **Ejemplo de columnas esperadas:**  
    - `home_team_name`, `away_team_name`  
    - `home_team_goal_count`, `away_team_goal_count`, `total_goal_count`  
    - `date_GMT`, `stadium_name`  
    """)