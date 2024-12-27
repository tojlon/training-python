import streamlit as st
import requests

# Configurer l'application Streamlit
st.set_page_config(page_title="Olympique de Marseille", layout="wide")

# Fonction pour récupérer les données via API
def get_api_data(endpoint):
    api_url = f"https://api.ligue1.com/{endpoint}"  # Remplacer par l'API officielle
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erreur lors de la récupération des données.")
        return None

# Page d'accueil
def page_accueil():
    st.title("Olympique de Marseille")

    # Afficher le logo et une image du stade
    logo_url = "https://wall.alphacoders.com/big.php?i=990022"
    stade_url = "https://upload.wikimedia.org/wikipedia/commons/5/5e/Stade_V%C3%A9lodrome_%28Marseille%29.jpg"

    col1, col2 = st.columns(2)
    with col1:
        st.image(logo_url, caption="Logo de l'Olympique de Marseille", use_column_width=True)
    with col2:
        st.image(stade_url, caption="Stade Vélodrome", use_column_width=True)

# Derniers résultats
def page_derniers_resultats():
    st.title("Derniers résultats de l'Olympique de Marseille")

    # Exemple de récupération des derniers résultats via API
    results = get_api_data("matches/latest")
    if results:
        for match in results['matches']:
            st.subheader(f"{match['home_team']} {match['home_score']} - {match['away_score']} {match['away_team']}")
            st.write(f"Date : {match['date']}")

# Trophées remportés
def page_trophees():
    st.title("Trophées remportés par l'Olympique de Marseille")

    trophees = [
        {"nom": "Ligue des Champions", "annee": 1993},
        {"nom": "Championnat de France", "annee": [1937, 1948, 1971, 1972, 1989, 1990, 1991, 1992, 2010]},
        {"nom": "Coupe de France", "annee": [1924, 1926, 1927, 1935, 1938, 1943, 1969, 1972, 1976, 1989]},
    ]

    for trophee in trophees:
        st.subheader(trophee['nom'])
        st.write(f"Années gagnées : {', '.join(map(str, trophee['annee']))}")

# Statistiques des joueurs
def page_stats_joueurs():
    st.title("Statistiques des joueurs de l'Olympique de Marseille")

    # Exemple de récupération des joueurs via API
    players = get_api_data("players")
    if players:
        player_names = [player['name'] for player in players['players']]
        selected_player = st.selectbox("Choisissez un joueur", player_names)

        player_data = next(player for player in players['players'] if player['name'] == selected_player)
        st.image(player_data['photo'], caption=selected_player, use_column_width=True)
        st.write(f"Poste : {player_data['position']}")
        st.write(f"Buts marqués : {player_data['goals']}")
        st.write(f"Passes décisives : {player_data['assists']}")

# Structure des pages
pages = {
    "Accueil": page_accueil,
    "Derniers résultats": page_derniers_resultats,
    "Trophées remportés": page_trophees,
    "Statistiques des joueurs": page_stats_joueurs,
}

# Menu de navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Aller à", list(pages.keys()))

# Affichage de la page sélectionnée
pages[choice]()

