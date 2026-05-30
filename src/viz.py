import matplotlib.pyplot as plt

def plot_goals_histogram(df):
    """Histograma de goles por partido"""
    fig, ax = plt.subplots(figsize=(8, 4))
    df['total_goal_count'].hist(bins=range(0, int(df['total_goal_count'].max())+2), 
                                edgecolor='black', color='skyblue', ax=ax)
    ax.set_title('Distribución de goles por partido')
    ax.set_xlabel('Goles')
    ax.set_ylabel('Partidos')
    return fig

def plot_goals_over_time(df):
    """Evolución de goles por fecha (orden cronológico)"""
    if 'date_GMT' not in df.columns:
        return None
    df_sorted = df.sort_values('date_GMT')
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(range(len(df_sorted)), df_sorted['total_goal_count'], 'o-', markersize=4)
    ax.set_title('Goles por partido (orden cronológico)')
    ax.set_xlabel('Número de partido')
    ax.set_ylabel('Goles')
    ax.grid(True, alpha=0.3)
    return fig