import streamlit as st
import pandas as pd
import urllib.parse

###############Apagar se der ruim###########

# Configuração da página e Meta Tags para o WhatsApp
st.set_page_config(page_title="Gran Turin - Pedidos", page_icon="🍱")

st.markdown(
    f"""
    <head>
        <meta property="og:title" content="🍱 Gran Turin - Faça seu Pedido" />
        <meta property="og:description" content="Confira o cardápio de hoje e monte sua marmita!" />
        <meta property="og:image" content="https://raw.githubusercontent.com/GranTurin/gran_turin_app/main/logo.png" />
        <meta property="og:url" content="https://gran-turin-app.streamlit.app" />
        <meta property="og:type" content="website" />
    </head>
    """,
    unsafe_allow_html=True
)#######################ate aqui ####

#st.set_page_config(
#    page_title="Gran Turin",
#    page_icon="logo.png", # Isso coloca a logo na aba do navegador
#)


# LINK DA SUA PLANILHA (Cole o link do CSV aqui)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQBai98jFvBGaS_TM0Qaao5bGanhR85VbvSuFFJvbha1DW5gXJlyXXqEiq3dUgVvQTqplDcG3jQqqLG/pub?output=csv"
def carregar_dados():
    # Lê a planilha e remove linhas vazias
    df = pd.read_csv(URL_PLANILHA)
    return df

try:
    df = carregar_dados()
    opcoes_carne = df['Carnes'].dropna().tolist()
    opcoes_acomp = df['Acompanhamentos'].dropna().tolist()
except:
    st.error("Erro ao carregar o cardápio. Verifique o link da planilha!")
    opcoes_carne, opcoes_acomp = [], []

# --- Resto do código da interface ---
st.title("🍱 Cardápio Atualizado")
nome = st.text_input("Seu Nome:")
carne = st.selectbox("Escolha a Proteína:", opcoes_carne)
acomp = st.multiselect("Escolha os Acompanhamentos:", opcoes_acomp)

if st.button("Enviar Pedido"):
    msg = f"Olá! Pedido de {nome}: {carne} com {', '.join(acomp)}"
    link = f"https://wa.me/5521986577315?text={urllib.parse.quote(msg)}"
    st.link_button("Ir para o WhatsApp", link)














