# utils/itinerary.py

def get_itinerary():
    return [
        {
            "day": "1 Agosto",
            "route": "Milano → San Sebastián",
            "summary": "Viaggio lungo (1.100 km) con arrivo serale in Spagna.",
            "details": [
                "Partenza la mattina presto da Milano",
                "Soste brevi in Francia (carburante/cibo)",
                "Arrivo a San Sebastián verso sera",
                "Pernottamento in area camper vicino Zurriola"
            ]
        },
        {
            "day": "2 Agosto",
            "route": "San Sebastián → Zarautz → Getaria",
            "summary": "Giornata surf e relax in due località top dei Paesi Baschi.",
            "details": [
                "Surf alla spiaggia Zurriola (San Sebastián)",
                "Trasferimento a Zarautz, surf e pranzo",
                "Visita a Getaria nel pomeriggio",
                "Pernottamento a Zarautz (camper sul mare)"
            ]
        },
        {
            "day": "3 Agosto",
            "route": "Getaria → Laga Beach → Bilbao",
            "summary": "Surf in una delle spiagge più sceniche del viaggio e visita culturale a Bilbao.",
            "details": [
                "Surf mattutino a Laga Hondartza",
                "Arrivo a Bilbao nel pomeriggio",
                "Visita centro città e Guggenheim (facoltativo)",
                "Pernottamento a Bilbao o dintorni"
            ]
        },
        {
            "day": "4 Agosto",
            "route": "Bilbao → Santoña → Santander → Gijón",
            "summary": "Tappa ricca tra surf, natura e città costiere.",
            "details": [
                "Surf a Playa de Berria (Santoña)",
                "Pausa pranzo e visita a Santander",
                "Arrivo a Gijón nel tardo pomeriggio",
                "Surf al tramonto o relax a Playa San Lorenzo",
                "Pernottamento in camper a Gijón"
            ]
        },
        {
            "day": "5 Agosto",
            "route": "Gijón → Oviedo → Inizio Rientro",
            "summary": "Ultimo surf e visita a Oviedo prima del lungo viaggio di ritorno.",
            "details": [
                "Ultimo surf a Salinas o Playa San Lorenzo",
                "Breve visita a Oviedo (centro storico)",
                "Inizio viaggio di ritorno nel pomeriggio",
                "Notte in camper nel sud della Francia"
            ]
        },
        {
            "day": "6 Agosto",
            "route": "Rientro Francia → Milano",
            "summary": "Viaggio di rientro in Italia.",
            "details": [
                "Partenza la mattina presto",
                "Arrivo previsto a Milano nel tardo pomeriggio/sera"
            ]
        }
    ]


def get_city_info(city_name):
    info = {
        "San Sebastián": """
### Cosa vedere
- Parte vecchia (Parte Vieja)
- Monte Urgull e vista panoramica
- Spiaggia di La Concha

### Surf Spot
- Zurriola Beach: onda costante, perfetta anche per principianti/intermedi
        """,
        "Zarautz": """
### Cosa vedere
- Lungomare lunghissimo e vivace
- Piccoli bar di pintxos e ristorantini
- Centro città e zona surfisti

### Surf Spot
- Zarautz: uno dei migliori beach break della Spagna settentrionale
        """,
        "Getaria": """
### Cosa vedere
- Villaggio di pescatori pittoresco
- Statua di Juan Sebastián Elcano
- Stradine e bar sul porto

### Surf Spot
- Niente spot principali, ma ottimo per relax e cultura
        """,
        "Laga Beach": """
### Cosa vedere
- Spiaggia immersa nel verde del parco Urdaibai
- Punto panoramico vicino a Cabo Ogoño

### Surf Spot
- Laga: onde più potenti, perfetta per intermedi
        """,
        "Bilbao": """
### Cosa vedere
- Museo Guggenheim
- Casco Viejo (centro storico)
- Ponte Zubizuri e Ría de Bilbao

### Surf Spot
- Non ci sono spiagge in città, ma vicine a 30 min
        """,
        "Santoña": """
### Cosa vedere
- Riserva naturale del Monte Buciero
- Antichi forti militari

### Surf Spot
- Playa de Berria: grande e poco affollata, ottima per ogni livello
        """,
        "Santander": """
### Cosa vedere
- Paseo de Pereda e centro storico
- Palacio de la Magdalena
- Spiaggia El Sardinero

### Surf Spot
- Playa de Somo (vicino): ottimo beach break
        """,
        "Gijón": """
### Cosa vedere
- Spiaggia San Lorenzo
- Cimavilla (quartiere antico)
- Museo del Ferroviario

### Surf Spot
- San Lorenzo: facile accesso, onde regolari
        """,
        "Oviedo": """
### Cosa vedere
- Cattedrale gotica e centro storico
- Statua di Woody Allen
- Sidrerie tipiche (sidra asturiana)

### Surf Spot
- Nessuna spiaggia in città, ma vicino c'è Salinas
        """
    }
    return info.get(city_name, "Informazioni non disponibili.")
