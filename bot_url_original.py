from gnews import GNews
from googlenewsdecoder import gnewsdecoder
import pandas as pd
import time

google_news = GNews(
    language="pt",
    country="BR",
    max_results=100
)
PALAVRAS_CHAVE = [
    "seca Rio de Janeiro",
    "estiagem Rio de Janeiro",

    "seca Angra dos Reis",
    "estiagem Angra dos Reis",

    "seca Aperibé",
    "estiagem Aperibé",

    "seca Araruama",
    "estiagem Araruama",

    "seca Areal RJ",
    "estiagem Areal RJ",

    "seca Armação dos Búzios",
    "estiagem Armação dos Búzios",

    "seca Arraial do Cabo",
    "estiagem Arraial do Cabo",

    "seca Barra do Piraí",
    "estiagem Barra do Piraí",

    "seca Barra Mansa",
    "estiagem Barra Mansa",

    "seca Belford Roxo",
    "estiagem Belford Roxo",

    "seca Bom Jardim RJ",
    "estiagem Bom Jardim RJ",

    "seca Bom Jesus do Itabapoana",
    "estiagem Bom Jesus do Itabapoana",

    "seca Cabo Frio",
    "estiagem Cabo Frio",

    "seca Cachoeiras de Macacu",
    "estiagem Cachoeiras de Macacu",

    "seca Cambuci RJ",
    "estiagem Cambuci RJ",

    "seca Campos dos Goytacazes",
    "estiagem Campos dos Goytacazes",

    "seca Cantagalo RJ",
    "estiagem Cantagalo RJ",

    "seca Carapebus",
    "estiagem Carapebus",

    "seca Cardoso Moreira",
    "estiagem Cardoso Moreira",

    "seca Carmo RJ",
    "estiagem Carmo RJ",

    "seca Casimiro de Abreu",
    "estiagem Casimiro de Abreu",

    "seca Comendador Levy Gasparian",
    "estiagem Comendador Levy Gasparian",

    "seca Conceição de Macabu",
    "estiagem Conceição de Macabu",

    "seca Cordeiro RJ",
    "estiagem Cordeiro RJ",

    "seca Duas Barras RJ",
    "estiagem Duas Barras RJ",

    "seca Duque de Caxias",
    "estiagem Duque de Caxias",

    "seca Engenheiro Paulo de Frontin",
    "estiagem Engenheiro Paulo de Frontin",

    "seca Guapimirim",
    "estiagem Guapimirim",

    "seca Iguaba Grande",
    "estiagem Iguaba Grande",

    "seca Itaboraí",
    "estiagem Itaboraí",

    "seca Itaguaí",
    "estiagem Itaguaí",

    "seca Italva",
    "estiagem Italva",

    "seca Itaocara",
    "estiagem Itaocara",

    "seca Itaperuna",
    "estiagem Itaperuna",

    "seca Itatiaia",
    "estiagem Itatiaia",

    "seca Japeri",
    "estiagem Japeri",

    "seca Laje do Muriaé",
    "estiagem Laje do Muriaé",

    "seca Macaé",
    "estiagem Macaé",

    "seca Macuco RJ",
    "estiagem Macuco RJ",

    "seca Magé",
    "estiagem Magé",

    "seca Mangaratiba",
    "estiagem Mangaratiba",

    "seca Maricá",
    "estiagem Maricá",

    "seca Mendes RJ",
    "estiagem Mendes RJ",

    "seca Mesquita RJ",
    "estiagem Mesquita RJ",

    "seca Miguel Pereira",
    "estiagem Miguel Pereira",

    "seca Miracema RJ",
    "estiagem Miracema RJ",

    "seca Natividade RJ",
    "estiagem Natividade RJ",

    "seca Nilópolis",
    "estiagem Nilópolis",

    "seca Niterói",
    "estiagem Niterói",

    "seca Nova Friburgo",
    "estiagem Nova Friburgo",

    "seca Nova Iguaçu",
    "estiagem Nova Iguaçu",

    "seca Paracambi",
    "estiagem Paracambi",

    "seca Paraíba do Sul",
    "estiagem Paraíba do Sul",

    "seca Paraty",
    "estiagem Paraty",

    "seca Paty do Alferes",
    "estiagem Paty do Alferes",

    "seca Petrópolis",
    "estiagem Petrópolis",

    "seca Pinheiral",
    "estiagem Pinheiral",

    "seca Piraí",
    "estiagem Piraí",

    "seca Porciúncula",
    "estiagem Porciúncula",

    "seca Porto Real RJ",
    "estiagem Porto Real RJ",

    "seca Quatis",
    "estiagem Quatis",

    "seca Queimados",
    "estiagem Queimados",

    "seca Quissamã",
    "estiagem Quissamã",

    "seca Resende",
    "estiagem Resende",

    "seca Rio Bonito",
    "estiagem Rio Bonito",

    "seca Rio Claro RJ",
    "estiagem Rio Claro RJ",

    "seca Rio das Flores",
    "estiagem Rio das Flores",

    "seca Rio das Ostras",
    "estiagem Rio das Ostras",

    "seca Santa Maria Madalena",
    "estiagem Santa Maria Madalena",

    "seca Santo Antônio de Pádua",
    "estiagem Santo Antônio de Pádua",

    "seca São Fidélis",
    "estiagem São Fidélis",

    "seca São Francisco de Itabapoana",
    "estiagem São Francisco de Itabapoana",

    "seca São Gonçalo",
    "estiagem São Gonçalo",

    "seca São João da Barra",
    "estiagem São João da Barra",

    "seca São João de Meriti",
    "estiagem São João de Meriti",

    "seca São José de Ubá",
    "estiagem São José de Ubá",

    "seca São José do Vale do Rio Preto",
    "estiagem São José do Vale do Rio Preto",

    "seca São Pedro da Aldeia",
    "estiagem São Pedro da Aldeia",

    "seca São Sebastião do Alto",
    "estiagem São Sebastião do Alto",

    "seca Sapucaia RJ",
    "estiagem Sapucaia RJ",

    "seca Saquarema",
    "estiagem Saquarema",

    "seca Seropédica",
    "estiagem Seropédica",

    "seca Silva Jardim",
    "estiagem Silva Jardim",

    "seca Sumidouro",
    "estiagem Sumidouro",

    "seca Tanguá",
    "estiagem Tanguá",

    "seca Teresópolis",
    "estiagem Teresópolis",

    "seca Trajano de Moraes",
    "estiagem Trajano de Moraes",

    "seca Três Rios",
    "estiagem Três Rios",

    "seca Valença RJ",
    "estiagem Valença RJ",

    "seca Varre-Sai",
    "estiagem Varre-Sai",

    "seca Vassouras",
    "estiagem Vassouras",

    "seca Volta Redonda",
    "estiagem Volta Redonda"
]
# ==========================================
# TERMOS DE ALERTA/PREVISÃO
# ==========================================
PALAVRAS_ALERTA = [
    "alerta de seca",
    "alerta de estiagem",
    "alerta para seca",
    "alerta para estiagem",
    "alerta meteorológico de seca",
    "alerta meteorológico de estiagem",
    "defesa civil emite alerta de seca",
    "defesa civil emite alerta de estiagem",
    "defesa civil alerta para seca",
    "defesa civil alerta para estiagem",
    "inmet alerta para seca",
    "inmet alerta para estiagem",
    "inmet emite alerta de seca",
    "inmet emite alerta de estiagem",
    "aviso de seca",
    "aviso de estiagem",
    "aviso meteorológico de seca",
    "aviso meteorológico de estiagem",
    "estado de atenção para seca",
    "estado de atenção para estiagem",
    "situação de seca",
    "situação de estiagem",
    "monitoramento da seca",
    "monitoramento de estiagem",
    "monitoramento da estiagem",
    "condições de seca",
    "condições de estiagem"
]
PALAVRAS_PREVISAO = [
    "previsão de seca",
    "previsão de estiagem",
    "previsão de período seco",
    "previsão de estiagem prolongada",
    "prevê seca",
    "prevê estiagem",
    "preve seca",
    "preve estiagem",
    "risco de seca",
    "risco de estiagem",
    "risco de estiagem prolongada",
    "possibilidade de seca",
    "possibilidade de estiagem",
    "pode ocorrer seca",
    "pode ocorrer estiagem",
    "deve ocorrer seca",
    "deve ocorrer estiagem",
    "espera-se seca",
    "espera-se estiagem",
    "chance de seca",
    "chance de estiagem",
    "tendência de seca",
    "tendência de estiagem",
    "período seco prolongado",
    "período de estiagem prolongado",
    "agravamento da seca",
    "agravamento da estiagem",
    "intensificação da seca",
    "intensificação da estiagem"
]
# ==========================================
# TERMOS DE EVENTO REAL
# ==========================================
PALAVRAS_EVENTO = [
    # Evento diretamente identificado
    "seca",
    "secas",
    "estiagem",
    "estiagens",
    "seca prolongada",
    "estiagem prolongada",
    "seca severa",
    "estiagem severa",
    "seca extrema",
    "estiagem extrema",
    # Impactos sobre água
    "falta de água",
    "falta d'água",
    "falta de abastecimento",
    "escassez de água",
    "escassez hídrica",
    "crise hídrica",
    "racionamento de água",
    "racionamento",
    # Recursos hídricos afetados
    "rio secou",
    "rios secaram",
    "rio com baixa vazão",
    "rios com baixa vazão",
    "baixa vazão",
    "vazão reduzida",
    "nível dos rios baixou",
    "nível dos rios caiu",
    "nível baixo dos rios",
    "reservatório secou",
    "reservatórios secos",
    "reservatório com nível baixo",
    "reservatórios com níveis baixos",
    # Consequências
    "atinge",
    "atingiram",
    "afeta",
    "afetou",
    "afetam",
    "afetados",
    "atingidos",
    "causa",
    "causou",
    "causando",
    "provoca",
    "provocou",
    "provocando",
    "deixa",
    "deixou",
    "deixando",
    # Abastecimento
    "abastecimento afetado",
    "abastecimento comprometido",
    "abastecimento prejudicado",
    "abastecimento interrompido",
    "abastecimento de água afetado",
    # Agricultura e produção
    "perda de safra",
    "perdas agrícolas",
    "prejuízos agrícolas",
    "lavouras afetadas",
    "lavouras prejudicadas",
    "plantação afetada",
    "produção afetada",
    "produção agrícola prejudicada",
    "perda na produção",
    "perdas na agricultura",
    "prejuízos na agricultura",
    # Pecuária
    "gado afetado",
    "rebanho afetado",
    "pecuária afetada",
    "perdas na pecuária",
    "falta de água para o gado",
    "falta de água para animais",
    # Decretação / situação oficial
    "decreta emergência",
    "decretou emergência",
    "decreto de emergência",
    "situação de emergência",
    "estado de emergência",
    "emergência por seca",
    "emergência por estiagem",
    "calamidade por seca",
    "calamidade por estiagem",
    # Danos e prejuízos
    "danos",
    "prejuízos",
    "prejuizo",
    "estragos",
    "perdas",
    "perdas econômicas",
    "prejuízos econômicos"
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
    "rio de janeiro",
    "rio de janeiro estado",

    "angra dos reis",
    "aperibé", "aperibe",
    "araruama",
    "areal",
    "armação dos búzios", "armacao dos buzios",
    "arraial do cabo",
    "barra do piraí", "barra do pirai",
    "barra mansa",
    "belford roxo",
    "bom jardim",
    "bom jesus do itabapoana",
    "cabo frio",
    "cachoeiras de macacu",
    "cambuci",
    "campos dos goytacazes",
    "cantagalo",
    "carapebus",
    "cardoso moreira",
    "carmo",
    "casimiro de abreu",
    "comendador levy gasparian",
    "conceição de macabu", "conceicao de macabu",
    "cordeiro",
    "duas barras",
    "duque de caxias",
    "engenheiro paulo de frontin",
    "guapimirim",
    "iguaba grande",
    "itaboraí", "itaborai",
    "itaguaí", "itaguai",
    "italva",
    "itaocara",
    "itaperuna",
    "itatiaia",
    "japeri",
    "laje do muriaé", "laje do muriae",
    "macaé", "macae",
    "macuco",
    "magé", "mage",
    "mangaratiba",
    "maricá", "marica",
    "mendes",
    "mesquita",
    "miguel pereira",
    "miracema",
    "natividade",
    "nilópolis", "nilopolis",
    "niterói", "niteroi",
    "nova friburgo",
    "nova iguaçu", "nova iguacu",
    "paracambi",
    "paraíba do sul", "paraiba do sul",
    "paraty",
    "paty do alferes",
    "petrópolis", "petropolis",
    "pinheiral",
    "piraí", "pirai",
    "porciúncula", "porciuncula",
    "porto real",
    "quatis",
    "queimados",
    "quissamã", "quissama",
    "resende",
    "rio bonito",
    "rio claro",
    "rio das flores",
    "rio das ostras",
    "santa maria madalena",
    "santo antônio de pádua", "santo antonio de padua",
    "são fidélis", "sao fidelis",
    "são francisco de itabapoana", "sao francisco de itabapoana",
    "são gonçalo", "sao goncalo",
    "são joão da barra", "sao joao da barra",
    "são joão de meriti", "sao joao de meriti",
    "são josé de ubá", "sao jose de uba",
    "são josé do vale do rio preto", "sao jose do vale do rio preto",
    "são pedro da aldeia", "sao pedro da aldeia",
    "são sebastião do alto", "sao sebastiao do alto",
    "sapucaia",
    "saquarema",
    "seropédica", "seropedica",
    "silva jardim",
    "sumidouro",
    "tanguá", "tangua",
    "teresópolis", "teresopolis",
    "trajano de moraes",
    "três rios", "tres rios",
    "valença", "valenca",
    "varre-sai",
    "vassouras",
    "volta redonda"
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
arquivo = "seca_estiagem_RJ.csv"
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
