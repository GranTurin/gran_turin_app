import streamlit as st
import pandas as pd
import urllib.parse

# 1. CONFIGURAÇÃO DA PÁGINA E PREVIEW
st.set_page_config(
    page_title="Gran Turin",
    page_icon="logo.png",
)

# Meta tags para o WhatsApp
st.markdown(
    f"""
    <head>
        <meta property="og:title" content="🍱 Gran Turin - Cardápio Digital" />
        <meta property="og:description" content="Monte seu pedido e envie pelo WhatsApp!" />
        <meta property="og:image" content="https://raw.githubusercontent.com/GranTurin/gran_turin_app/main/logo.png" />
        <meta property="og:type" content="website" />
    </head>
    """,
    unsafe_allow_html=True
)

# 2. CARREGAMENTO DE DADOS
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQBai98jFvBGaS_TM0Qaao5bGanhR85VbvSuFFJvbha1DW5gXJlyXXqEiq3dUgVvQTqplDcG3jQqqLG/pub?output=csv"

def carregar_dados():
    try:
        df = pd.read_csv(URL_PLANILHA)
        df.columns = df.columns.str.strip() # Remove espaços nos nomes das colunas
        return df
    except:
        return None

df = carregar_dados()

if df is not None:
    try:
        opcoes_carne = df['Carnes'].dropna().tolist()
        opcoes_acomp = df['Acompanhamentos'].dropna().tolist()
        opcoes_tamanho = df['Tamanho'].dropna().tolist()
    except Exception as e:
        st.error(f"Erro ao ler colunas da planilha: {e}")
        opcoes_carne, opcoes_acomp, opcoes_tamanho = [], [], []
else:
    st.error("Erro ao carregar o cardápio. Verifique o link da planilha!")
    opcoes_carne, opcoes_acomp, opcoes_tamanho = [], [], []

# 3. INTERFACE DO USUÁRIO
st.image("https://raw.githubusercontent.com/GranTurin/gran_turin_app/main/logo.png", width=120)
st.title("🍱 Cardápio do Dia")

nome = st.text_input("Seu Nome:", placeholder="Digite seu nome aqui")
end = st.text_input("Endereço ou Loja:", placeholder="Ex: Rua X, nº 10 ou Loja Tal")

# CORREÇÃO DO ERRO: Cada campo agora tem um nome (Label) único
tamanho_escolhido = st.selectbox("Escolha o Tamanho da Marmita:", ["Selecione..."] + opcoes_tamanho)
carne_escolhida = st.selectbox("Escolha a Carne/Proteína:", ["Selecione..."] + opcoes_carne)

acomp_escolhidos = st.multiselect("Escolha os Acompanhamentos:", opcoes_acomp)
obs = st.text_area("Alguma observação? (Opcional)")

# 4. BOTÃO E ENVIO
if st.button("🚀 ENVIAR PEDIDO AGORA"):
    # Verifica se os campos obrigatórios estão preenchidos
    if nome and end and carne_escolhida != "Selecione..." and tamanho_escolhido != "Selecione...":
        
        itens_txt = ", ".join(acomp_escolhidos) if acomp_escolhidos else "Nenhum selecionado"
        
        # Montagem da mensagem
        msg = (
            f"*NOVO PEDIDO - REALIZADO*\n\n"
            f"*Cliente:* {nome}\n"
            f"*Endereço:* {end}\n"
            f"*Tamanho:* {tamanho_escolhido}\n"
            f"*Proteina:* {carne_escolhida}\n"
            f"*Acompanhamentos:* {itens_txt}\n"
            f"*Observações:* {obs if obs else 'Nenhuma'}"
        )
        
        # Codificação para o link do WhatsApp
        msg_link = urllib.parse.quote(msg)
        link_final = f"https://wa.me/5521986577315?text={msg_link}"
        
        st.success("Tudo pronto! Clique no botão abaixo para confirmar no WhatsApp.")
        st.link_button("👉 CONFIRMAR NO WHATSAPP", link_final)
    else:
        st.error("⚠️ Por favor, preencha o Nome, Endereço, Tamanho e Carne!")

st.markdown("---")
st.caption("Gran Turin - Sistema de Pedidos Inteligente")
