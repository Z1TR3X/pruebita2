# src/viz.py - Versión Profesional con Mejoras Extremas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

# Configuración global de estilo profesional
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 10

# Paleta de colores profesional
COLORS = {
    'primary': '#2E86AB',      # Azul principal
    'secondary': '#A23B72',    # Morado
    'success': '#18A999',      # Verde
    'warning': '#F18F01',      # Naranja
    'danger': '#C73E1D',       # Rojo
    'info': '#6A4E9B',         # Púrpura
    'dark': '#2D3142',         # Gris oscuro
    'light': '#E5E5E5',        # Gris claro
    'gradient': ['#2E86AB', '#18A999', '#F18F01', '#C73E1D']
}

def plot_goals_histogram(df):
    """Histograma profesional con gradiente de colores"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    goles = df['total_goal_count'].dropna()
    
    if len(goles) == 0:
        ax.text(0.5, 0.5, 'No hay datos de goles', ha='center', va='center', transform=ax.transAxes)
        return fig
    
    # Calcular distribución
    bins = range(0, int(goles.max()) + 3)
    n, bins, patches = ax.hist(goles, bins=bins, edgecolor='white', linewidth=1.5, alpha=0.85)
    
    # Gradiente de colores por barra
    colors_gradient = plt.cm.RdYlGn(np.linspace(0, 1, len(patches)))
    for i, patch in enumerate(patches):
        patch.set_facecolor(colors_gradient[i])
    
    # Estadísticas
    media = goles.mean()
    mediana = goles.median()
    moda = goles.mode().iloc[0] if not goles.mode().empty else 0
    varianza = goles.var()
    
    # Líneas estadísticas
    ax.axvline(media, color=COLORS['primary'], linestyle='--', linewidth=2.5, 
               label=f'📊 Media: {media:.2f}', alpha=0.9)
    ax.axvline(mediana, color=COLORS['secondary'], linestyle='-.', linewidth=2.5, 
               label=f'📈 Mediana: {mediana:.2f}', alpha=0.9)
    ax.axvline(moda, color=COLORS['warning'], linestyle=':', linewidth=2.5, 
               label=f'⭐ Moda: {moda:.0f}', alpha=0.9)
    
    # Sombreado del área
    ax.fill_betweenx([0, max(n)], media - np.std(goles), media + np.std(goles), 
                      alpha=0.1, color=COLORS['primary'], label=f'±1 Desviación típica')
    
    # Personalización avanzada
    ax.set_title('⚽ DISTRIBUCIÓN DE GOLES POR PARTIDO\nEliminatorias Sudamericanas 2023-2026', 
                 fontsize=16, fontweight='bold', pad=20, fontfamily='sans-serif')
    ax.set_xlabel('Goles totales en el partido', fontsize=13, fontweight='semibold')
    ax.set_ylabel('Frecuencia (número de partidos)', fontsize=13, fontweight='semibold')
    
    # Leyenda posicionada fuera
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), framealpha=0.9, edgecolor='black')
    
    # Cuadrícula mejorada
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Etiquetas en las barras
    for i, (barra, valor) in enumerate(zip(patches, n)):
        if valor > 0:
            ax.text(barra.get_x() + barra.get_width()/2, valor + max(n)*0.02, 
                   f'{int(valor)}', ha='center', va='bottom', fontsize=9, 
                   fontweight='bold', color=COLORS['dark'])
    
    # Marco decorativo
    for spine in ax.spines.values():
        spine.set_edgecolor(COLORS['dark'])
        spine.set_linewidth(1.5)
    
    plt.tight_layout()
    return fig


def plot_goals_over_time(df):
    """Evolución de goles con análisis de tendencias"""
    if 'date_GMT' not in df.columns or len(df) == 0:
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.text(0.5, 0.5, 'No hay datos suficientes', ha='center', va='center', transform=ax.transAxes)
        return fig
    
    df_sorted = df.sort_values('date_GMT').reset_index(drop=True)
    goles = df_sorted['total_goal_count'].values
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Calcular tendencias
    x = range(len(goles))
    z = np.polyfit(x, goles, 1)
    tendencia = np.poly1d(z)
    
    # Área bajo la curva (gradiente)
    ax.fill_between(x, 0, goles, alpha=0.2, color=COLORS['primary'], label='Área bajo la curva')
    
    # Línea principal con marcadores
    ax.plot(x, goles, 'o-', markersize=5, linewidth=2, 
            color=COLORS['primary'], alpha=0.8, label='Goles por partido', markeredgecolor='white', markeredgewidth=1)
    
    # Línea de tendencia polinómica
    ax.plot(x, tendencia(x), '--', linewidth=2.5, color=COLORS['danger'], 
            label=f'Tendencia general: {z[0]:+.3f}x + {z[1]:+.2f}', alpha=0.9)
    
    # Media móvil (ventana dinámica)
    window = max(3, len(goles) // 10)
    if len(goles) >= window:
        media_movil = np.convolve(goles, np.ones(window)/window, mode='valid')
        ax.plot(range(window//2, len(goles)-window//2), media_movil, 's-', 
                linewidth=2.5, color=COLORS['success'], 
                label=f'Media móvil ({window} partidos)', alpha=0.8, markersize=3)
    
    # Promedio general
    media_general = goles.mean()
    ax.axhline(media_general, color=COLORS['secondary'], linestyle='-.', linewidth=2, 
               label=f'📊 Promedio general: {media_general:.2f}')
    
    # Bandas de percentiles
    percentil_25 = np.percentile(goles, 25)
    percentil_75 = np.percentile(goles, 75)
    ax.axhspan(percentil_25, percentil_75, alpha=0.1, color=COLORS['info'], 
               label=f'Rango intercuartil (25°-75° percentil)')
    
    # Destacar máximos y mínimos
    max_idx = np.argmax(goles)
    min_idx = np.argmin(goles)
    ax.plot(max_idx, goles[max_idx], 'D', markersize=10, color=COLORS['warning'], 
            markeredgecolor='white', markeredgewidth=2, label=f'Máximo: {goles[max_idx]} goles')
    ax.plot(min_idx, goles[min_idx], 'v', markersize=10, color=COLORS['danger'], 
            markeredgecolor='white', markeredgewidth=2, label=f'Mínimo: {goles[min_idx]} goles')
    
    # Personalización
    ax.set_title('📈 EVOLUCIÓN DE GOLES A LO LARGO DEL TORNEO\nAnálisis de tendencias y patrones', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Número de partido (orden cronológico)', fontsize=13, fontweight='semibold')
    ax.set_ylabel('Goles totales por partido', fontsize=13, fontweight='semibold')
    
    # Leyenda optimizada
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), framealpha=0.9, fontsize=9)
    
    # Cuadrícula y ejes
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.set_ylim(bottom=0)
    
    plt.tight_layout()
    return fig


def plot_home_away_goals(df):
    """Comparación profesional Local vs Visitante con violines"""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    home_goals = df['home_team_goal_count'].dropna()
    away_goals = df['away_team_goal_count'].dropna()
    
    if len(home_goals) == 0 or len(away_goals) == 0:
        ax.text(0.5, 0.5, 'No hay datos suficientes', ha='center', va='center', transform=ax.transAxes)
        return fig
    
    # Preparar datos para violín
    data_to_plot = [home_goals, away_goals]
    
    # Crear gráfico de violín (más informativo que boxplot)
    parts = ax.violinplot(data_to_plot, positions=[1, 2], showmeans=True, showmedians=True, showextrema=True)
    
    # Personalizar violines
    colors_violin = [COLORS['primary'], COLORS['secondary']]
    for i, pc in enumerate(parts['bodies']):
        pc.set_facecolor(colors_violin[i])
        pc.set_alpha(0.7)
        pc.set_edgecolor('black')
        pc.set_linewidth(1.5)
    
    # Personalizar líneas estadísticas
    parts['cmeans'].set_color('red')
    parts['cmeans'].set_linewidth(2.5)
    parts['cmedians'].set_color('yellow')
    parts['cmedians'].set_linewidth(2.5)
    parts['cmaxes'].set_color(COLORS['dark'])
    parts['cmins'].set_color(COLORS['dark'])
    
    # Agregar puntos individuales (jitter)
    for i, data in enumerate(data_to_plot, 1):
        x_jitter = np.random.normal(i, 0.04, size=len(data))
        ax.scatter(x_jitter, data, alpha=0.3, s=20, color=colors_violin[i-1], zorder=0)
    
    # Estadísticas detalladas
    home_mean = home_goals.mean()
    away_mean = away_goals.mean()
    home_median = home_goals.median()
    away_median = away_goals.median()
    home_std = home_goals.std()
    away_std = away_goals.std()
    
    # Prueba estadística básica (diferencia de medias)
    diff_means = home_mean - away_mean
    advantage = "Local" if diff_means > 0 else "Visitante"
    
    # Caja de texto con estadísticas
    stats_box = f"""ESTADÍSTICAS COMPARATIVAS:
    ┌{"─"*35}┐
    │        LOCAL    │  VISITANTE  │
    ├{"─"*35}┤
    │ Media   {home_mean:6.2f}    │   {away_mean:6.2f}     │
    │ Mediana {home_median:6.0f}    │   {away_median:6.0f}     │
    │ Std Dev {home_std:6.2f}    │   {away_std:6.2f}     │
    └{"─"*35}┘
    
    ➤ Ventaja local: {abs(diff_means):.2f} goles/partido
    ➤ {advantage} anota más en promedio"""
    
    ax.text(0.02, 0.98, stats_box, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', 
                                              alpha=0.9, edgecolor=COLORS['dark'], linewidth=1.5))
    
    # Personalización
    ax.set_title('🏟️ COMPARACIÓN DE RENDIMIENTO: LOCAL vs VISITANTE\nAnálisis de distribución de goles', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Goles por partido', fontsize=13, fontweight='semibold')
    ax.set_xticks([1, 2])
    ax.set_xticklabels(['🏠 LOCAL', '✈️ VISITANTE'], fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.2, axis='y', linestyle='-')
    
    # Ajustar límites
    y_max = max(home_goals.max(), away_goals.max()) + 1
    ax.set_ylim(bottom=0, top=y_max)
    
    plt.tight_layout()
    return fig


def plot_top_scorers_teams(df):
    """Top equipos con visualización avanzada"""
    # Contar goles
    home_goals = df.groupby('home_team_name')['home_team_goal_count'].sum()
    away_goals = df.groupby('away_team_name')['away_team_goal_count'].sum()
    all_teams = home_goals.add(away_goals, fill_value=0).sort_values(ascending=False).head(12)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Crear colores gradiente
    colors_gradient = plt.cm.plasma(np.linspace(0.2, 0.9, len(all_teams)))
    
    # Barras horizontales
    bars = ax.barh(range(len(all_teams)), all_teams.values, color=colors_gradient, 
                   edgecolor='black', linewidth=1.5, alpha=0.85)
    
    # Destacar top 3
    for i, bar in enumerate(bars[:3]):
        bar.set_edgecolor('gold')
        bar.set_linewidth(3)
        bar.set_alpha(1)
    
    # Agregar efectos de sombra
    for i, bar in enumerate(bars):
        ax.text(all_teams.values[i] + max(all_teams.values)*0.01, i, 
               f'{int(all_teams.values[i])}', va='center', fontsize=10, 
               fontweight='bold', color=COLORS['dark'])
    
    # Personalización
    ax.set_yticks(range(len(all_teams)))
    ax.set_yticklabels(all_teams.index, fontsize=10)
    ax.set_xlabel('Goles totales', fontsize=13, fontweight='semibold')
    ax.set_title('🏆 TOP EQUIPOS GOLEADORES DEL TORNEO\nRanking de poder ofensivo', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Invertir para que el mejor quede arriba
    ax.invert_yaxis()
    
    # Cuadrícula
    ax.grid(True, alpha=0.2, axis='x', linestyle='-')
    ax.set_axisbelow(True)
    
    # Marco
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
    
    # Agregar medallitas para top 3
    medals = ['🥇', '🥈', '🥉']
    for i in range(min(3, len(bars))):
        ax.text(-max(all_teams.values)*0.05, i, medals[i], 
                fontsize=15, va='center', ha='right')
    
    plt.tight_layout()
    return fig


def plot_corners_per_match(df):
    """Distribución de corners con análisis avanzado"""
    corners = (df['home_team_corner_count'].fillna(0) + df['away_team_corner_count'].fillna(0))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Histograma con curva de densidad
    bins = range(0, int(corners.max()) + 3)
    n, bins, patches = ax.hist(corners, bins=bins, edgecolor='white', linewidth=1.5, 
                                alpha=0.7, color=COLORS['info'], density=False)
    
    # Curva de densidad (KDE aproximado)
    from scipy import stats
    kde = stats.gaussian_kde(corners)
    x_range = np.linspace(0, corners.max(), 100)
    ax2 = ax.twinx()
    ax2.plot(x_range, kde(x_range) * len(corners) * 1.5, 'r-', linewidth=2.5, 
             label='Densidad', alpha=0.8)
    ax2.set_ylabel('Densidad', fontsize=11, color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Estadísticas
    media = corners.mean()
    mediana = corners.median()
    std_dev = corners.std()
    
    # Líneas estadísticas
    ax.axvline(media, color=COLORS['success'], linestyle='--', linewidth=2.5, 
               label=f'📊 Media: {media:.1f}', alpha=0.9)
    ax.axvline(mediana, color=COLORS['warning'], linestyle='-.', linewidth=2.5, 
               label=f'📈 Mediana: {mediana:.1f}', alpha=0.9)
    
    # Rango típico (media ± std)
    ax.axvspan(media - std_dev, media + std_dev, alpha=0.1, color=COLORS['primary'], 
               label=f'Rango típico (media ± σ)')
    
    # Personalización
    ax.set_title('📐 DISTRIBUCIÓN DE CORNERS POR PARTIDO\nAnálisis de juego por bandas', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Corners totales en el partido', fontsize=13, fontweight='semibold')
    ax.set_ylabel('Frecuencia (número de partidos)', fontsize=13, fontweight='semibold')
    
    # Leyenda combinada
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', bbox_to_anchor=(1, 1))
    
    # Cuadrícula
    ax.grid(True, alpha=0.2, axis='y', linestyle='-')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    return fig


def plot_extra_analysis(df):
    """Análisis extra: correlación y rendimiento"""
    fig = plt.figure(figsize=(14, 6))
    
    # Crear subplots
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    
    # GRÁFICO 1: Relación posesión vs goles
    possession_diff = df['home_team_possession'].fillna(50) - df['away_team_possession'].fillna(50)
    goals_diff = df['home_team_goal_count'].fillna(0) - df['away_team_goal_count'].fillna(0)
    
    ax1.scatter(possession_diff, goals_diff, alpha=0.5, c=COLORS['primary'], s=50, edgecolors='white')
    ax1.axhline(0, color='black', linestyle='-', linewidth=0.5)
    ax1.axvline(0, color='black', linestyle='-', linewidth=0.5)
    
    # Línea de tendencia
    if len(possession_diff) > 1:
        z = np.polyfit(possession_diff, goals_diff, 1)
        p = np.poly1d(z)
        x_range = np.linspace(possession_diff.min(), possession_diff.max(), 100)
        ax1.plot(x_range, p(x_range), '--', color=COLORS['danger'], linewidth=2, 
                label=f'Tendencia: {z[0]:+.2f}x {z[1]:+.2f}')
    
    ax1.set_xlabel('Diferencia de posesión (Local - Visitante) %', fontsize=11)
    ax1.set_ylabel('Diferencia de goles (Local - Visitante)', fontsize=11)
    ax1.set_title('📊 Posesión vs Rendimiento\n¿Más posesión = más goles?', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.2)
    ax1.legend()
    
    # GRÁFICO 2: Análisis de tarjetas
    total_cards = df['home_team_yellow_cards'].fillna(0) + df['away_team_yellow_cards'].fillna(0) + \
                  (df['home_team_red_cards'].fillna(0) + df['away_team_red_cards'].fillna(0)) * 2
    
    if len(total_cards) > 0:
        card_bins = range(0, int(total_cards.max()) + 3)
        ax2.hist(total_cards, bins=card_bins, edgecolor='white', color=COLORS['warning'], alpha=0.7)
        ax2.axvline(total_cards.mean(), color=COLORS['danger'], linestyle='--', linewidth=2, 
                   label=f'Media: {total_cards.mean():.1f}')
    
    ax2.set_xlabel('Tarjetas por partido (amarilla=1, roja=2)', fontsize=11)
    ax2.set_ylabel('Partidos', fontsize=11)
    ax2.set_title('🟨 Análisis de disciplina\nDistribución de tarjetas', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.2)
    ax2.legend()
    
    fig.suptitle('📈 ANÁLISIS AVANZADO DEL JUEGO\nPatrones y correlaciones', 
                 fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig