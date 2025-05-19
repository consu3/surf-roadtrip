import streamlit as st
import pandas as pd
import pydeck as pdk
from utils.itinerary import get_itinerary, get_city_info

st.set_page_config(page_title="Surf Road Trip - Nord Spagna", layout="wide")
st.title("🌊 Surf Road Trip - Nord Spagna 2025")

# --- Sidebar ---
st.sidebar.title("🚗 Info Viaggio")
st.sidebar.markdown("""
**Date:** 1 - 6 Agosto  
**Persone:** 4  
**Chilometri totali:** ~3170 km  
**Budget a testa:** 218€

**Dettagli Costi:**
- Camper: 225€
- Cauzione: 500€ (rimborsabile)
- Assicurazione: 42€ a testa (168€ totali)
- Benzina stimata: 70€ a testa
- Spesa cibo: 50€ a testa
""")

# --- MAPPA INTERATTIVA ---
st.header("📍 Mappa Itinerario")
data = pd.read_json("data/tappe.json")

# Linea percorso Milano → Oviedo (semplificata)
route_coords = [
    [9.19, 45.46],  # Milano
    [-1.98, 43.32],  # San Sebastián
    [-2.17, 43.28],  # Zarautz
    [-2.20, 43.30],  # Getaria
    [-2.66, 43.42],  # Laga
    [-2.94, 43.26],  # Bilbao
    [-3.45, 43.44],  # Santoña
    [-3.80, 43.46],  # Santander
    [-5.66, 43.54],  # Gijón
    [-5.85, 43.36],  # Oviedo
]

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/streets-v12',
    initial_view_state=pdk.ViewState(
        latitude=43.0,
        longitude=-2.5,
        zoom=6,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=5000,
        ),
        pdk.Layer(
            'TextLayer',
            data=data,
            get_position='[lon, lat]',
            get_text='name',
            get_size=16,
            get_color='[0, 0, 0]',
            get_angle=0,
        ),
        pdk.Layer(
            "PathLayer",
            data=[{"path": route_coords}],
            get_path="path",
            get_width=4,
            get_color='[0, 100, 255]',
            width_min_pixels=2,
        )
    ]
))

# --- ITINERARIO ---
st.header("⏺️ Itinerario Giornaliero")
itinerary = get_itinerary()
for day in itinerary:
    with st.expander(f"{day['day']} - {day['route']}"):
        st.markdown(f"**{day['summary']}**")
        st.markdown("\n".join(f"- {item}" for item in day['details']))

# --- INFO TAPPE ---
st.header("🌍 Cosa Vedere nelle Tappe")
for i, row in data.iterrows():
    with st.expander(f"{row['name']}"):
        info = get_city_info(row['name'])
        best_beaches = {
            "San Sebastián": ["Playa de la Concha", "Playa de Ondarreta", "Zurriola Beach (surf)"],
            "Zarautz": ["Zarautz Beach (surf)", "Playa de Malkorbe"],
            "Getaria": ["Gaztetape Beach", "Malkorbe"],
            "Laga Beach": ["Playa de Laga (surf)", "Playa de Laida"],
            "Bilbao": ["Playa de Sopelana", "Playa de Plentzia"],
            "Santoña": ["Playa de Berria (surf)", "Playa de San Martín"],
            "Santander": ["Playa del Sardinero", "Playa de Mataleñas", "Playa de Somo (surf)"],
            "Gijón": ["Playa de San Lorenzo (surf)", "Playa de Poniente"],
            "Oviedo": ["Playa de Salinas (vicino ad Avilés)", "Playa de Xagó"]
        }
        beaches = best_beaches.get(row['name'], [])
        if beaches:
            st.markdown("### Spiagge da non perdere:")
            for b in beaches:
                st.markdown(f"- {b}")
        st.markdown(info)

        # Aggiunta immagini (placeholder con percorso immagini locale o URL online)
        img_path = f"images/{row['name'].replace(' ', '_').lower()}.jpg"
        st.image(img_path, use_container_width=True, caption=f"Vista da {row['name']}")
