import streamlit as st
import pandas as pd
import pydeck as pdk
import sqlite3
from datetime import datetime
from utils.itinerary import get_itinerary, get_city_info
import plotly.express as px
import requests

# DB init
conn = sqlite3.connect("roadtrip.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS notes (day TEXT, content TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS expenses (item TEXT, amount REAL, person TEXT, settled INTEGER DEFAULT 0)''')
c.execute('''CREATE TABLE IF NOT EXISTS links (title TEXT, url TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS checklist (day TEXT, task TEXT)''')
conn.commit()

# Countdown
countdown_date = datetime(2025, 8, 1)
days_left = (countdown_date - datetime.now()).days

st.set_page_config(page_title="Surf Road Trip - Nord Spagna", layout="wide")
st.title("🌊 Surf Road Trip - Nord Spagna 2025")
st.metric("⏳ Giorni al viaggio", f"{days_left} giorni")

# --- Sidebar ---
st.sidebar.title("🚗 Menu Navigazione")
page = st.sidebar.radio("Vai a:", [
    "🗺️ Mappa + Itinerario",
    "🌍 Cosa vedere",
    "💰 Budget Tracker",
    "📝 Diario di bordo",
    "✅ Check giornaliero",
    "🔗 Link utili"
])

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

@st.cache_data(ttl=3600)
def get_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=it"
    return requests.get(url).json()

# --- Contenuti dinamici ---
data = pd.read_json("data/tappe.json")
itinerary = get_itinerary()

if page == "🌍 Cosa vedere":
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

            try:
                api_key = st.secrets["OPENWEATHERMAP_API_KEY"]
                if pd.isna(row['lat']) or pd.isna(row['lon']):
                    st.markdown("⚠️ Coordinate mancanti per questa città.")
                else:
                    response = get_weather(row['lat'], row['lon'], api_key)
                    if 'main' in response and 'weather' in response:
                        temp = response['main']['temp']
                        weather = response['weather'][0]['description']
                        st.markdown(f"### ☀️ Meteo attuale: {temp}°C - {weather}")
                    else:
                        st.markdown(f"⚠️ Errore OpenWeather: {response.get('message', 'risposta imprevista')}")
            except Exception as e:
                st.markdown(f"❌ Errore nella richiesta meteo: {e}")

            img_path = f"images/{row['name'].replace(' ', '_').lower()}.jpg"
            st.image(img_path, use_container_width=True, caption=f"Vista da {row['name']}")

elif page == "🗺️ Mappa + Itinerario":
    st.header("📍 Mappa Itinerario")
    route_coords = [[9.19, 45.46], [-1.98, 43.32], [-2.17, 43.28], [-2.20, 43.30],
                    [-2.66, 43.42], [-2.94, 43.26], [-3.45, 43.44], [-3.80, 43.46],
                    [-5.66, 43.54], [-5.85, 43.36]]
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/streets-v12',
        initial_view_state=pdk.ViewState(latitude=43.0, longitude=-2.5, zoom=6, pitch=0),
        layers=[
            pdk.Layer('ScatterplotLayer', data=data, get_position='[lon, lat]', get_color='[200, 30, 0, 160]', get_radius=5000),
            pdk.Layer('TextLayer', data=data, get_position='[lon, lat]', get_text='name', get_size=16, get_color='[0, 0, 0]', get_angle=0),
            pdk.Layer("PathLayer", data=[{"path": route_coords}], get_path="path", get_width=4, get_color='[0, 100, 255]', width_min_pixels=2),
        ]))

    st.header("⏺️ Itinerario Giornaliero")
    for day in itinerary:
        with st.expander(f"{day['day']} - {day['route']}"):
            st.markdown(f"**{day['summary']}**")
            st.markdown("".join(f"- {item}" for item in day['details']))

elif page == "💰 Budget Tracker":
    st.header("💰 Budget Tracker")
    with st.form("Aggiungi spesa"):
        item = st.text_input("Voce di spesa")
        amount = st.number_input("Importo", min_value=0.0, format="%.2f")
        person = st.text_input("Chi ha pagato?")
        submitted = st.form_submit_button("Salva")
        if submitted:
            c.execute("INSERT INTO expenses (item, amount, person) VALUES (?, ?, ?)", (item, amount, person))
            conn.commit()
            st.success("Spesa salvata!")

    filter_option = st.radio("Visualizza:", ["Tutte", "Non saldate", "Saldate"])
    if filter_option == "Tutte":
        df = pd.read_sql_query("SELECT rowid, * FROM expenses", conn)
    elif filter_option == "Non saldate":
        df = pd.read_sql_query("SELECT rowid, * FROM expenses WHERE settled = 0", conn)
    else:
        df = pd.read_sql_query("SELECT rowid, * FROM expenses WHERE settled = 1", conn)

    if "settled" not in df.columns:
        df["settled"] = 0

    df["pagato"] = df["settled"].astype(bool)
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    for idx, row in edited_df.iterrows():
        if row["pagato"]:
            c.execute("UPDATE expenses SET settled = 1 WHERE rowid = ?", (int(row["rowid"]),))
        else:
            c.execute("UPDATE expenses SET settled = 0 WHERE rowid = ?", (int(row["rowid"]),))
    conn.commit()

    if filter_option == "Tutte":
        df = pd.read_sql_query("SELECT * FROM expenses", conn)
    elif filter_option == "Non saldate":
        df = pd.read_sql_query("SELECT * FROM expenses WHERE settled = 0", conn)
    else:
        df = pd.read_sql_query("SELECT * FROM expenses WHERE settled = 1", conn)

    total = df.groupby("person")["amount"].sum()
    avg = df["amount"].sum() / 4
    st.markdown("### 💸 Bilancio tra persone")
    for p in total.index:
        diff = total[p] - avg
        if diff > 0:
            st.success(f"{p} ha pagato {diff:.2f}€ in più")
        elif diff < 0:
            st.warning(f"{p} deve versare {-diff:.2f}€")
        else:
            st.info(f"{p} è in pari")

    fig = px.pie(values=total.values, names=total.index, title="Distribuzione Spese per Persona")
    st.plotly_chart(fig, use_container_width=True)

elif page == "📝 Diario di bordo":
    st.header("📝 Diario di Bordo")
    selected_day = st.selectbox("Seleziona il giorno", [d['day'] for d in itinerary])
    existing_note = c.execute("SELECT content FROM notes WHERE day = ?", (selected_day,)).fetchone()
    default_note = existing_note[0] if existing_note else ""
    note = st.text_area("Scrivi le tue note:", value=default_note)
    if st.button("Salva nota"):
        c.execute("DELETE FROM notes WHERE day = ?", (selected_day,))
        c.execute("INSERT INTO notes VALUES (?, ?)", (selected_day, note))
        conn.commit()
        st.success("Nota salvata")

elif page == "✅ Check giornaliero":
    st.header("✅ Check Giornaliero")
    selected_day = st.selectbox("Giorno", [d['day'] for d in itinerary])
    tasks = [row[0] for row in c.execute("SELECT task FROM checklist WHERE day = ?", (selected_day,)).fetchall()]
    new_task = st.text_input("Aggiungi nuova attività")
    if st.button("Aggiungi"):
        c.execute("INSERT INTO checklist VALUES (?, ?)", (selected_day, new_task))
        conn.commit()
        st.success("Attività aggiunta")
    for t in tasks:
        checked = st.checkbox(t, key=f"{selected_day}_{t}")
        if st.button(f"Rimuovi '{t}'", key=f"del_{selected_day}_{t}"):
            c.execute("DELETE FROM checklist WHERE day = ? AND task = ?", (selected_day, t))
            conn.commit()
            st.rerun()

elif page == "🔗 Link utili":
    st.header("🔗 Link Utili")
    with st.form("Aggiungi link"):
        title = st.text_input("Titolo")
        url = st.text_input("URL")
        if st.form_submit_button("Aggiungi"):
            c.execute("INSERT INTO links VALUES (?, ?)", (title, url))
            conn.commit()
            st.success("Link aggiunto!")
    links = c.execute("SELECT * FROM links").fetchall()
    for t, u in links:
        st.markdown(f"- [{t}]({u})")
