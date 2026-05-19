import requests
import time
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

url = "https://eonet.gsfc.nasa.gov/api/v3/events"

CATEGORIAS = [
    "severeStorms",
    "floods",
    "landslides",
    "wildfires",
    "drought"
]

eventos = []

url_mapa = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"

mundo = gpd.read_file(url_mapa)


brasil = mundo[mundo["ADMIN"] == "Brazil"]

for categoria in CATEGORIAS:

    print(f"Coletando categoria: {categoria}")

    params = {
        "status": "closed",
        "days": 3650,
        "category": categoria

    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Erro:", response.status_code)
        continue

    dados = response.json()

    eventos_api = dados.get("events", [])

    print(f"Eventos encontrados: {len(eventos_api)}")

    for evento in eventos_api:

        geometria = evento.get("geometry", [])

        latitude = None
        longitude = None
        data_evento = ""

        if geometria:

            coords = geometria[0].get("coordinates", [])

            if len(coords) >= 2:
                longitude = coords[0]
                latitude = coords[1]

            data_evento = geometria[0].get("date", "")

        # Filtra apenas o Brasil
        if latitude is not None and longitude is not None:

            ponto = Point(longitude, latitude)

            if not brasil.contains(ponto).any():
                continue
        

        sources = evento.get("sources", [])

        link = ""

        if sources:
            link = sources[0].get("url", "")

        eventos.append({

            "titulo": evento.get("title", ""),
            "descricao": evento.get("description", ""),
            "categoria": categoria,
            "data": data_evento,
            "fonte": "NASA EONET",
            "link": link,
            "latitude": latitude,
            "longitude": longitude
        })

    time.sleep(1)


noticias = pd.DataFrame(eventos)


noticias = noticias.drop_duplicates(subset=["titulo"])


noticias.to_csv(
    "eventos_climaticos_nasa.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Total de eventos:", len(noticias))
