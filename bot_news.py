import feedparser
import pandas as pd
from bs4 import BeautifulSoup

#RSS
URL = "https://news.google.com/rss/search?q=raios+tempestades+Brasil&hl=pt-BR&gl=BR&ceid=BR:pt-419"

URL_24H = "https://news.google.com/rss/search?q=raios+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"


URL_INMET = "https://news.google.com/rss/search?q=raios+site:inmet.gov.br&hl=pt-BR&gl=BR&ceid=BR:pt-419"


QUERIES = [
     "raios Brasil",
    "tempestades Brasil",
    "granizo Brasil",
    "enchentes Brasil",
    "alagamentos Brasil",
    "vendaval Brasil",
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


URLS = []

for query in QUERIES:
    url = (
        "https://news.google.com/rss/search?q="
        + query.replace(" ", "+")
        + "&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    )
    URLS.append(url)


noticias_coletadas = []

for url in URLS:
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
            "resumo": resumo
        })

noticias_coletadas_df = pd.DataFrame(noticias_coletadas)
noticias_coletadas_df.drop_duplicates(
    subset = ["link"]
)

#SALVAR EM CSV
noticias_coletadas_df.to_csv("noticias_riscos_climaticos.csv",
                             index = False,
                             encoding = "utf-8-sig")

#fazer paginação
