import streamlit as st
import requests

# Configuration de l'application Streamlit
st.set_page_config(page_title="Olympique de Marseille", layout="wide")

# Clé API Football-Data.org (remplacez par votre propre clé)
API_KEY = st.secrets['API_KEY']
BASE_URL = "https://api.football-data.org/v4"

# Headers pour les requêtes
HEADERS = {"X-Auth-Token": API_KEY}

# Fonction pour récupérer les données via l'API
def get_api_data(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur {response.status_code} lors de la récupération des données.")
        return None

# Page d'accueil
def page_accueil():
    st.title("Olympique de Marseille")

    # Afficher le logo et une image du stade à partir des fichiers locaux
    logo_path = "om_logo.jpg"  # Assurez-vous que l'image est dans le bon répertoire
    stade_path = "velodrome_stadium.webp"  # Assurez-vous que l'image est dans le bon répertoire

    col1, col2 = st.columns(2)
    with col1:
        st.image(logo_path, caption="Logo de l'Olympique de Marseille", use_container_width=True)
    with col2:
        st.image(stade_path, caption="Stade Vélodrome", use_container_width=True)

# Derniers résultats
def page_derniers_resultats():
    st.title("Derniers résultats de l'Olympique de Marseille")

    # Récupérer les résultats de l'OM (ID de l'équipe de l'OM)
    results = get_api_data("matches?team=Olympique_Marseille")
    
    if results:
        for match in results['matches']:
            # Assurez-vous que 'homeTeam' et 'awayTeam' existent dans les données
            if 'homeTeam' in match and 'awayTeam' in match and 'score' in match:
                home_team = match['homeTeam']['name']
                away_team = match['awayTeam']['name']
                score_home = match['score']['fullTime']['homeTeam']
                score_away = match['score']['fullTime']['awayTeam']
                st.subheader(f"{home_team} {score_home} - {score_away} {away_team}")
                st.write(f"Date : {match['utcDate']}")
            else:
                st.write("Les données du match sont incomplètes.")

# Trophées remportés
def page_trophees():
    st.title("Trophées remportés par l'Olympique de Marseille")

    trophees = [
        {"nom": "Ligue des Champions", "annee": [1993]},
        {"nom": "Championnat de France", "annee": [1937, 1948, 1971, 1972, 1989, 1990, 1991, 1992, 2010]},
        {"nom": "Coupe de France", "annee": [1924, 1926, 1927, 1935, 1938, 1943, 1969, 1972, 1976, 1989]},
    ]

    for trophee in trophees:
        st.subheader(trophee['nom'])
        st.write(f"Années gagnées : {', '.join(map(str, trophee['annee']))}")

# Structure des pages
pages = {
    "Accueil": page_accueil,
    "Derniers résultats": page_derniers_resultats,
    "Trophées remportés": page_trophees,
}

# Menu de navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Aller à", list(pages.keys()))

# Affichage de la page sélectionnée
pages[choice]()
