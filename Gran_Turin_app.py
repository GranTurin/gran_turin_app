import streamlit as st
import pandas as pd
import urllib.parse

# LINK DA SUA PLANILHA (Cole o link do CSV aqui)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQBai98jFvBGaS_TM0Qaao5bGanhR85VbvSuFFJvbha1DW5gXJlyXXqEiq3dUgVvQTqplDcG3jQqqLG/pubhtml"

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
    link = f"https://wa.me/5511999999999?text={urllib.parse.quote(msg)}"
    st.link_button("Ir para o WhatsApp", link)


