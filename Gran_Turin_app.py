import streamlit as st
import pandas as pd
import urllib.parse

###############Apagar se der ruim###########

# O link da imagem deve ser DIRETO (terminar em .jpg ou .png)
# Dica: Use o link da sua logo que você subiu no GitHub
MINHA_LOGO = "https://raw.githubusercontent.com/GranTurin/gran_turin_app/refs/heads/main/logo.png"
#https://github.com/GranTurin/gran_turin_app/edit/main/logo.png
#https://raw.githubusercontent.com/seu-usuario/seu-repo/main/logo.png

st.markdown(f"""
    <head>
        <meta property="og:title" content="🍱 Marmitaria - Faça seu Pedido Aqui" />
        <meta property="og:description" content="Clique para ver o cardápio do dia e montar sua marmita!" />
        <meta property="og:image" content="{MINHA_LOGO}" />
        <meta property="og:type" content="website" />
    </head>
    """, unsafe_allow_html=True)

    # Se quiser exibir a logo também dentro do site:
st.image(LINK_DA_LOGO, width=150)

#######################ate aqui ####

st.set_page_config(
    page_title="Gran Turin",
    page_icon="logo.png", # Isso coloca a logo na aba do navegador
)
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













