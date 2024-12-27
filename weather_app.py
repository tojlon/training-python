import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Dictionnaire des emojis pour les conditions météo
weather_emojis = {
    'clear sky': '☀️',      # Soleil
    'few clouds': '🌤️',     # Quelques nuages
    'scattered clouds': '⛅', # Nuages épars
    'broken clouds': '☁️',   # Nuages
    'shower rain': '🌧️',    # Pluie
    'rain': '🌧️',           # Pluie
    'thunderstorm': '🌩️',   # Orage
    'snow': '❄️',            # Neige
    'mist': '🌫️'            # Brume
}

# Fonction pour récupérer les données météo
def get_weather_data():
    url = "http://samples.openweathermap.org/data/2.5/forecast?q=München,DE&appid=b1b15e88fa797225412429c1c50c122a1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur lors de la récupération des données météo. Code HTTP: {response.status_code}")
        return None

# Fonction pour transformer les données en DataFrame et ajouter l'emoji de la condition
def create_forecast_dataframe(data):
    forecasts = []
    for forecast in data['list']:
        datetime = forecast['dt_txt']
        temp_kelvin = forecast['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        weather_description = forecast['weather'][0]['description']
        
        # Récupérer l'emoji en fonction de la description
        weather_emoji = weather_emojis.get(weather_description, '🌥️')  # Emoji par défaut si condition inconnue
        
        forecasts.append([datetime, temp_celsius, weather_description, weather_emoji])

    df = pd.DataFrame(forecasts, columns=['Date/Heure', 'Température (°C)', 'Conditions', 'Emoji'])
    return df

# Affichage de l'interface Streamlit
st.title("Analyse Météo à Munich")
st.markdown("Cette application affiche les prévisions météorologiques pour Munich.")

# Récupérer les données
data = get_weather_data()

if data:
    # Créer le DataFrame à partir des données
    df_forecasts = create_forecast_dataframe(data)

    # Afficher les données dans la sidebar sous forme de tableau avec emojis pour les conditions
    st.sidebar.subheader("Prévisions météo")
    
    # Concatenation de l'emoji dans la colonne "Conditions"
    df_forecasts['Conditions'] = df_forecasts['Conditions'] + " " + df_forecasts['Emoji']
    
    # Affichage du tableau dans la sidebar
    st.sidebar.write(df_forecasts[['Date/Heure', 'Température (°C)', 'Conditions']])

    # Sauvegarder les prévisions en CSV
    csv = df_forecasts.to_csv(index=False)
    st.sidebar.download_button(label="Télécharger les prévisions", data=csv, file_name="forecasts.csv", mime="text/csv")

    # Affichage du graphique
    st.subheader("Graphique des températures")
    plt.figure(figsize=(10, 6))
    plt.plot(df_forecasts['Date/Heure'], df_forecasts['Température (°C)'], marker='o', color='b')
    plt.xticks(rotation=45)
    plt.xlabel("Date/Heure")
    plt.ylabel("Température (°C)")
    plt.title("Température à Munich sur les prochaines 5 jours")
    st.pyplot(plt)
