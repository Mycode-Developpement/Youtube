"""
vidéo disponible sur la chaîne Youtube : @Mycode-Developpement 
-> https://youtu.be/yDhK2Uwa03M
"""

from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import streamlit as st
import openrouteservice


st.set_page_config(page_title="GOOGLE MAPS", layout="wide")
st.title("🕊️ Google Maps avec Geopy et OpenRouteService")

## saisie 

st.sidebar.header("Saisie de l'adresse")
adresse_depart = st.sidebar.text_input("Entrez une adresse de départ", "Champs-Elysées, Paris")
adresse_arrivee = st.sidebar.text_input("Entrez une adresse d'arrivée", "Lyon, France")
mode = st.sidebar.selectbox("Mode de transport", ["driving-car", "cycling-regular", "foot-walking"])

if st.sidebar.button("Calculer l'itinéraire"):
    geolocator = Nominatim(user_agent="geo_app_mycode")
    
    location_depart = geolocator.geocode(adresse_depart, timeout=10)
    location_arrive = geolocator.geocode(adresse_arrivee, timeout=10)
    
    if not location_depart or not location_arrive:
        st.sidebar.error("Adresse non trouvée. Veuillez vérifier l'adresse saisie.")
    
    else:
        
        coords_depart = [location_depart.longitude, location_depart.latitude]
        coords_arrive = [location_arrive.longitude, location_arrive.latitude]
        
        client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjVjZjQxMTllNmVlYzQ2YjU5YzBmNTBiYWNjYzgxYmEyIiwiaCI6Im11cm11cjY0In0=")
        
        route = client.directions(
        profile=mode,
        coordinates=[coords_depart, coords_arrive],
        format='geojson'
        )
        
        segment = route['features'][0]['properties']['segments'][0]
        distance = segment['distance'] / 1000
        duration = segment['duration'] / 60

        #session state pour stocker les coordonnées
        st.session_state["coords_depart"] = coords_depart
        st.session_state["coords_arrive"] = coords_arrive
        st.session_state["route"] = route
        st.session_state["distance"] = distance
        st.session_state["duree"] = duration

if 'route' in st.session_state:
    
    st.sidebar.success("Itinéraire calculé avec succès !")
    st.sidebar.info(f"Distance : {st.session_state['distance']:.2f} km")
    st.sidebar.info(f"Durée : {st.session_state['duree']:.2f} minutes")
    
    map = folium.Map(location=st.session_state["coords_depart"][::-1], zoom_start=10)
    
    folium.GeoJson(st.session_state["route"], name="Itinéraire",).add_to(map)
    
    folium.Marker(
        location=st.session_state["coords_depart"][::-1],
        popup=f"Départ: {adresse_depart}",
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(map)
    
    folium.Marker(
        location=st.session_state["coords_arrive"][::-1],
        popup=f"Arrivée: {adresse_arrivee}",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(map)
    
    st_folium(map, width=1000, height=600)
