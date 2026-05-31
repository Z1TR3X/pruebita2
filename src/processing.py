import pandas as pd

def load_data(uploaded_file):
    """Carga el CSV desde el archivo subido"""
    df = pd.read_csv(uploaded_file)
    return df

def get_basic_stats(df):
    """Devuelve estadísticas básicas del torneo"""
    stats = {
        'partidos': len(df),
        'goles_totales': df['total_goal_count'].sum(),
        'promedio_goles': df['total_goal_count'].mean(),
        'equipos': len(pd.concat([df['home_team_name'], df['away_team_name']]).unique())
    }
    return stats


def filter_by_team(df, team_name):
    """Filtra partidos donde aparece un equipo (local o visitante)"""
    if not team_name:
        return df
    return df[(df['home_team_name'] == team_name) | (df['away_team_name'] == team_name)]