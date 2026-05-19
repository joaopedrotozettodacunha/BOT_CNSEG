import feedparser
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time


#RSS

ANOS = range(2005, 2027)

QUERIES = [
    "raios Brasil",
    "tempestades Brasil",
    "granizo Brasil",
    "enchentes Brasil",
    "inundação Brasil",
    "deslizamento de terra Brasil",
    "movimentos de massa Brasil"
    "alagamentos Brasil",
    "vendaval Brasil",
    "ventos fortes Brasil"
    "descarga atmosférica Brasil",
    "apagão tempestade Brasil",
    "chuvas fortes Brasil",
    "desastre climático Brasil"
]

RISCOS_CLIMATICOS = [
    "raio",
    "vendaval",
    "granizo",
    "geada",
    "enchentes"
]



noticias_coletadas = []


#Google News RSS

for query in QUERIES:

    

    for ano in ANOS:
        q = (
            f"{query} "
            f"after:{ano}-01-01 "
            f"before:{ano+1}-01-01"
        )

        url = (
            "https://news.google.com/rss/search?q="
            + q.replace(" ", "+")
            + "&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        )

        noticias = feedparser.parse(url)


        for noticia in noticias.entries:

            print("Título:", noticia.title,"Link:", noticia.link)

            titulo = noticia.title
            link = noticia.link
            data = noticia.published
            fonte = noticia.source.title
            resumo = noticia.summary
            resumo = BeautifulSoup(
                resumo, "html.parser"
            ).get_text() #retira o texto do html

            noticias_coletadas.append({
                "titulo": titulo,
                "link": link,
                "data": data,
                "fonte": fonte,
                "resumo": resumo,
                "ano_noticia": ano
        })
            
        time.sleep(1) #evita bloqueio do google

#Relief API com Paginação

url_relief = "https://api.reliefweb.int/v2/disasters"

limit = 100
offset = 0

while True:

    params = {
        "appname": "nome_do_projeto",
        "limit": limit,
        "offset": offset,
        "query": "(flood OR storm)",
        "filter[field]": "country",
        "filter[value]": "brazil"
    }

    response = requests.get(url_relief, params=params)

    if response.status_code != 200:
        print("Erro API:", response.status_code)
        break

    noticias = response.json()
    items = noticias.get("data", [])

    print(f"ReliefWeb página offset={offset} -> {len(items)} resultados")

    if not items:
        break

    for item in items:

        fields = item.get("fields", {})

        noticias_coletadas.append({
            "titulo": fields.get("name", ""),
            "link": fields.get("url", ""),
            "data": fields.get("date", {}).get("created", ""),
            "fonte": "ReliefWeb",
            "resumo": fields.get("description", ""),
            "ano_noticia": str(fields.get("date", {}).get("created", ""))[:4],
            "origem": "ReliefWeb"
        })
    if len(items) < limit:
        break

    offset += limit

    time.sleep(2)


noticias_coletadas_df = pd.DataFrame(noticias_coletadas)
noticias_coletadas_df = noticias_coletadas_df.drop_duplicates(
    subset = ["link"]
)

noticias_coletadas_df = noticias_coletadas_df.sort_values(by = "ano_noticia", ascending = True)
# salvar em csv
noticias_coletadas_df.to_csv("noticias_riscos_climaticos.csv",
                             index = False,
                             encoding = "utf-8-sig")

print("Total de Notícias:", len(noticias_coletadas_df))

