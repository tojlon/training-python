import streamlit as st
from nba_api.stats.endpoints import leaguegamefinder, leaguestandings, playercareerstats
from nba_api.stats.static import teams, players
from datetime import datetime

# Titre de l'application
st.title("NBA Stats en Temps Réel")

# Définir les saisons disponibles
current_year = datetime.now().year
seasons = [f"{year}-{str(year + 1)[-2:]}" for year in range(current_year - 5, current_year + 1)]
selected_season = st.sidebar.selectbox("Choisir une saison", seasons[::-1])

# Catégories disponibles
categories = ["Statistiques par Match", "Statistiques par Équipe", "Statistiques par Joueur"]
selected_category = st.sidebar.radio("Choisir une catégorie", categories)

# Format saison pour nba_api (ex: "2022-23" -> "2022-23")
api_season = selected_season

# Fonction pour récupérer les données des matchs
def get_match_stats(season):
    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season)
    games = gamefinder.get_data_frames()[0]
    return games

# Fonction pour récupérer les données des équipes
def get_team_stats(season):
    standings = leaguestandings.LeagueStandings(season=season)
    teams_data = standings.get_data_frames()[0]
    return teams_data

# Fonction pour récupérer les données des joueurs
def get_player_stats(player_name):
    player_list = players.find_players_by_full_name(player_name)
    if player_list:
        player_id = player_list[0]["id"]
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        stats = career_stats.get_data_frames()[0]
        return stats
    else:
        return None

# Affichage en fonction de la catégorie
if selected_category == "Statistiques par Match":
    st.header("Statistiques par Match")
    games = get_match_stats(api_season)
    if not games.empty:
        for index, game in games.iterrows():
            st.subheader(f"{game['TEAM_NAME']} vs {game['MATCHUP']}")
            st.write(f"Date : {game['GAME_DATE']}")
            st.write(f"Score : {game['PTS']} - {game['PLUS_MINUS']}")
    else:
        st.write("Aucune donnée trouvée pour cette saison.")

elif selected_category == "Statistiques par Équipe":
    st.header("Statistiques par Équipe")
    teams_data = get_team_stats(api_season)
    if not teams_data.empty:
        for index, team in teams_data.iterrows():
            st.subheader(team["TeamName"])
            st.write(f"Victoires : {team['W']}")
            st.write(f"Défaites : {team['L']}")
    else:
        st.write("Aucune donnée trouvée pour cette saison.")

elif selected_category == "Statistiques par Joueur":
    st.header("Statistiques par Joueur")
    player_name = st.text_input("Entrez le nom du joueur", "")
    if player_name:
        player_stats = get_player_stats(player_name)
        if player_stats is not None and not player_stats.empty:
            st.write(player_stats)
        else:
            st.write("Aucune statistique trouvée pour ce joueur.")

# Notes complémentaires
st.sidebar.info("Cette application utilise nba_api pour récupérer les données NBA.")
