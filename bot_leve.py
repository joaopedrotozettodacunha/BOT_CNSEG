from gnews import GNews
import pandas as pd
import time

# ==========================================
# CONFIGURAÇÃO
# ==========================================

google_news = GNews(
    language="pt",
    country="BR",
    max_results=100
)

PALAVRAS_CHAVE = [

    # Petrópolis
    "deslizamento Petrópolis",
    "movimento de massa Petrópolis",
    "desmoronamento Petrópolis",
    "soterramento Petrópolis",
    "encosta Petrópolis",
    "queda de barreira Petrópolis",

    # Rio de Janeiro
    "deslizamento Rio de Janeiro",
    "movimento de massa Rio de Janeiro",
    "desmoronamento Rio de Janeiro",
    "soterramento Rio de Janeiro",
    "encosta Rio de Janeiro",
    "queda de barreira Rio de Janeiro",

    # Teresópolis
    "deslizamento Teresópolis",
    "movimento de massa Teresópolis",
    "desmoronamento Teresópolis",
    "soterramento Teresópolis",
    "encosta Teresópolis",
    "queda de barreira Teresópolis",

    # Nova Friburgo
    "deslizamento Nova Friburgo",
    "movimento de massa Nova Friburgo",
    "desmoronamento Nova Friburgo",
    "soterramento Nova Friburgo",
    "encosta Nova Friburgo",
    "queda de barreira Nova Friburgo",

    # São Paulo
    "deslizamento São Paulo",
    "movimento de massa São Paulo",
    "desmoronamento São Paulo",
    "soterramento São Paulo",
    "encosta São Paulo",
    "queda de barreira São Paulo",

    # Salvador
    "deslizamento Salvador",
    "movimento de massa Salvador",
    "desmoronamento Salvador",
    "soterramento Salvador",
    "encosta Salvador",
    "queda de barreira Salvador",

    # Belo Horizonte
    "deslizamento Belo Horizonte",
    "movimento de massa Belo Horizonte",
    "desmoronamento Belo Horizonte",
    "soterramento Belo Horizonte",
    "encosta Belo Horizonte",
    "queda de barreira Belo Horizonte",

    # Recife
    "deslizamento Recife",
    "movimento de massa Recife",
    "desmoronamento Recife",
    "soterramento Recife",
    "encosta Recife",
    "queda de barreira Recife",

    # Santos
    "deslizamento Santos",
    "movimento de massa Santos",
    "desmoronamento Santos",
    "soterramento Santos",
    "encosta Santos",
    "queda de barreira Santos",

    # Cubatão
    "deslizamento Cubatão",
    "movimento de massa Cubatão",
    "desmoronamento Cubatão",
    "soterramento Cubatão",
    "encosta Cubatão",
    "queda de barreira Cubatão",

    # São Sebastião
    "deslizamento São Sebastião",
    "movimento de massa São Sebastião",
    "desmoronamento São Sebastião",
    "soterramento São Sebastião",
    "encosta São Sebastião",
    "queda de barreira São Sebastião",
]

# ==========================================
# TERMOS DE ALERTA/PREVISÃO
# ==========================================

PALAVRAS_ALERTA = [
    "alerta",
    "alerta de chuva",
    "alerta de vendaval",
    "alerta meteorológico",
    "defesa civil emite",
    "defesa civil alerta",
    "inmet alerta",
    "inmet emite",
    "aviso meteorológico",
    "aviso de chuva",
    "aviso de vendaval",
    "estado de atenção",
    "monitoramento"
]

PALAVRAS_PREVISAO = [
    "previsão",
    "preve",
    "prevê",
    "risco de",
    "possibilidade de",
    "pode ocorrer",
    "deve ocorrer",
    "espera-se",
    "chance de"
]

# ==========================================
# TERMOS DE EVENTO REAL
# ==========================================

PALAVRAS_EVENTO = [
    "atinge",
    "atingiram",
    "causa",
    "causou",
    "provoca",
    "provocou",
    "derruba",
    "derrubou",
    "deixa",
    "deixou",
    "destrói",
    "destruiu",
    "mata",
    "matou",
    "morre",
    "morreu",
    "alagamento",
    "alagamentos",
    "enchente",
    "enchentes",
    "inundação",
    "inundações",
    "deslizamento",
    "queda de barreira",
    "estragos",
    "danos",
    "prejuízos",
    "prejuizo",
    "afetou",
    "afetados",
    "atingidos"
]

# ==========================================
# CLASSIFICAÇÃO
# ==========================================

def classificar_noticia(titulo):

    titulo = titulo.lower()

    if any(p in titulo for p in PALAVRAS_ALERTA):
        return "ALERTA"

    if any(p in titulo for p in PALAVRAS_PREVISAO):
        return "PREVISAO"

    if any(p in titulo for p in PALAVRAS_EVENTO):
        return "EVENTO"

    return "OUTRO"


# ==========================================
# FILTRO
# ==========================================

def noticia_relevante(titulo):

    titulo = titulo.lower()

    # deve mencionar Ceará ou cidade importante
    locais = [
    "petrópolis",
    "petropolis",

    "rio de janeiro",

    "teresópolis",
    "teresopolis",

    "nova friburgo",

    "são paulo",
    "sao paulo",

    "salvador",

    "belo horizonte",

    "recife",

    "santos",

    "cubatão",
    "cubatao",

    "são sebastião",
    "sao sebastiao"
]
    if not any(local in titulo for local in locais):
        return False

    categoria = classificar_noticia(titulo)

    # mantém apenas eventos reais
    return categoria == "EVENTO"


# ==========================================
# COLETA
# ==========================================

dados = []

for termo in PALAVRAS_CHAVE:

    print(f"Buscando: {termo}")

    try:

        noticias = google_news.get_news(termo)

        print(f"Encontradas: {len(noticias)}")

        for noticia in noticias:

            titulo = noticia.get("title", "")

            link_real = str(
                noticia.get(
                    "link_real",
                    noticia.get("link", "")
                )
            ).strip()

            if not noticia_relevante(titulo):
                continue

            dados.append({
                "titulo": titulo,
                "link": noticia.get("url", ""),
                "link_original": link_real,
                "data": noticia.get("published date", ""),
                "fonte": noticia.get("publisher", {}).get("title", ""),
                "tipo": classificar_noticia(titulo)
            })

        time.sleep(1)

    except Exception as e:
        print(f"Erro: {e}")

# ==========================================
# DATAFRAME
# ==========================================

df = pd.DataFrame(dados)

if not df.empty:

    df.drop_duplicates(
        subset=["link"],
        inplace=True
    )

    df.drop_duplicates(
        subset=["titulo"],
        inplace=True
    )

    df.sort_values(
        by="data",
        inplace=True,
        ascending=False
    )

# ==========================================
# SALVAR
# ==========================================

arquivo = "cidades_MM.csv"

df.to_csv(
    arquivo,
    index=False,
    encoding="utf-8-sig"
)

# ==========================================
# ESTATÍSTICAS
# ==========================================

print("\nFinalizado")
print(f"Total de notícias: {len(df)}")
print(f"Arquivo salvo: {arquivo}")

if not df.empty:
    print("\nFontes encontradas:")
    print(df["fonte"].value_counts())
