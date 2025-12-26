import streamlit as st
import pandas as pd
import urllib.parse

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Gran Turin - Cardápio",
    page_icon="🍱",
    initial_sidebar_state="collapsed",
)

# Meta tags para o preview no WhatsApp (og:image)
st.markdown(
    """
    <head>
        <meta property="og:title" content="🍱 Gran Turin - Cardápio Digital" />
        <meta property="og:description" content="Monte seu pedido e envie pelo WhatsApp!" />
        <meta property="og:image" content="https://raw.githubusercontent.com/GranTurin/gran_turin_app/main/logo.png" />
    </head>
    """, unsafe_allow_html=True
)

# Estilização CSS para Mobile e Botões
st.markdown("""
    <style>
    .main { overflow-y: auto; }
    .stButton button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.5em; 
        background-color: #25D366; 
        color: white; 
        font-weight: bold;
        border: none;
    }
    .stButton button:hover { border: 1px solid #128C7E; color: white; }
    .stButton button:disabled { background-color: #d3d3d3; color: #888888; cursor: not-allowed; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    </style>
    """, unsafe_allow_html=True)

# 2. CARREGAMENTO DE DADOS (Google Sheets CSV)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQBai98jFvBGaS_TM0Qaao5bGanhR85VbvSuFFJvbha1DW5gXJlyXXqEiq3dUgVvQTqplDcG3jQqqLG/pub?output=csv"

@st.cache_data(ttl=60) # Atualiza a cada 1 minuto
def carregar_dados():
    try:
        df = pd.read_csv(URL_PLANILHA)
        df.columns = df.columns.str.strip() 
        return df
    except Exception as e:
        st.error(f"Erro ao conectar com a planilha: {e}")
        return None

df = carregar_dados()

# 3. INTERFACE
st.image("https://raw.githubusercontent.com/GranTurin/gran_turin_app/main/logo.png", width=100)
st.title("🍱 Cardápio do Dia")
st.write("Preencha os dados e monte seu prato abaixo:")

if df is not None:
    try:
        # Extração das listas (ignorando valores vazios)
        opcoes_carne = df['Carnes'].dropna().tolist()
        opcoes_acomp = df['Acompanhamentos'].dropna().tolist()
        opcoes_tamanho = df['Tamanho'].dropna().tolist()

        # FORMULÁRIO DE IDENTIFICAÇÃO
        with st.container(border=True):
            nome = st.text_input("👤 Seu Nome:", placeholder="Como quer ser chamado?")
            end = st.text_input("📍 Endereço/Loja:", placeholder="Ex: Rua Direita, 123 ou Loja B")

        # SELEÇÃO DO PEDIDO (Proteínas e Tamanho agora no topo)
        st.subheader("📝 Escolhas Principais")
        col1, col2 = st.columns(2)
        with col1:
            tamanho = st.selectbox("📏 Tamanho:", ["Selecione..."] + opcoes_tamanho)
        with col2:
            carne = st.selectbox("🥩 Proteína:", ["Selecione..."] + opcoes_carne)
        
        st.subheader("🥗 Acompanhamentos")
        acomps = st.multiselect("Escolha seus acompanhamentos:", opcoes_acomp)
        
        obs = st.text_area("🗒️ Observações (Opcional):", placeholder="Ex: Sem feijão, mandar talher, etc.")

        st.divider()

        # Verificação de campos obrigatórios
        pode_enviar = nome and end and carne != "Selecione..." and tamanho != "Selecione..."

        # 4. LÓGICA DE ENVIO
        if not pode_enviar:
            st.warning("⚠️ Preencha Nome, Endereço, Tamanho e Proteína para liberar o pedido.")
        
        # O botão fica desabilitado (disabled) se os campos não estiverem preenchidos
        if st.button("🚀 GERAR PEDIDO NO WHATSAPP", disabled=not pode_enviar):
            
            txt_acomps = ", ".join(acomps) if acomps else "Padrão da casa"
            
            # Formatação da mensagem para o WhatsApp
            texto_pedido = (
                f"*🍱 NOVO PEDIDO - GRAN TURIN*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"*👤 CLIENTE:* {nome}\n"
                f"*📍 ENDEREÇO:* {end}\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"*📏 TAMANHO:* {tamanho}\n"
                f"*🥩 PROTEÍNA:* {carne}\n"
                f"*🥗 ACOMPS:* {txt_acomps}\n"
                f"*🗒️ OBS:* {obs if obs else 'Nenhuma'}\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"✅ _Enviado via Cardápio Digital_"
            )
            
            # Link do WhatsApp
            numero_whatsapp = "5521986577315"
            link = f"https://wa.me/{numero_whatsapp}?text={urllib.parse.quote(texto_pedido)}"
            
            st.success("Tudo pronto! Clique no botão verde para abrir o WhatsApp.")
            st.link_button("🟢 ABRIR WHATSAPP E CONCLUIR", link)

    except KeyError as e:
        st.error(f"Erro: A coluna {e} não foi encontrada na planilha. Verifique se os nomes estão corretos!")
else:
    st.info("Aguardando carregamento dos dados da planilha...")

st.markdown("---")
st.caption("Gran Turin - Sistema de Pedidos v2.6")
