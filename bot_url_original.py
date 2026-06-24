from gnews import GNews
from googlenewsdecoder import gnewsdecoder
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
    "queda de barreira Petrópolis"
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
# RESOLUÇÃO DO LINK REAL (decodifica o redirect do Google News)
# ==========================================

def resolver_link_real(url_google, tentativas=2, espera=1):
    """
    O gnews retorna a URL no formato news.google.com/rss/articles/...
    Esse link é um redirect resolvido via JavaScript, então requests
    comuns (e até o fallback HEAD do próprio gnews) não conseguem
    seguir o redirecionamento -> retornam a própria URL do Google.

    Aqui decodificamos o token base64 embutido na URL para extrair
    o link real da matéria, sem precisar de navegador.
    """
    if "news.google.com" not in url_google:
        return url_google

    for tentativa in range(tentativas):
        try:
            resultado = gnewsdecoder(url_google, interval=espera)
            if resultado.get("status") and resultado.get("decoded_url"):
                return resultado["decoded_url"]
        except Exception:
            pass
        time.sleep(espera)

    # Se não conseguiu decodificar (ex: matéria muito antiga, rate limit),
    # devolve a URL do Google mesmo, para não perder a linha.
    return url_google


# ==========================================
# FILTRO
# ==========================================

def noticia_relevante(titulo):

    titulo = titulo.lower()

    # deve mencionar Ceará ou cidade importante
    locais = [
    "petrópolis",
    "petropolis"
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

            # CORREÇÃO: a lib gnews retorna a chave 'url' (não existem
            # 'link' nem 'link_real' no dicionário de cada notícia).
            # Esse 'url' geralmente ainda é um link de redirect do
            # Google News (news.google.com/rss/articles/...), então
            # decodificamos para obter o link real do veículo.
            url_bruta = noticia.get("url", "")
            link_original = resolver_link_real(url_bruta).strip()

            if not noticia_relevante(titulo):
                continue

            dados.append({
                "titulo": titulo,
                "link_original": link_original,
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
        subset=["link_original"],
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

arquivo = "noticias_url_original.csv"

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
