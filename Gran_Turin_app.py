import streamlit as st
import pandas as pd
import urllib.parse

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Gran Turin - Cardápio",
    page_icon="🍱",
    initial_sidebar_state="collapsed",
)

# Estilização CSS
st.markdown("""
    <style>
    .stButton button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.5em; 
        background-color: #25D366; 
        color: white; 
        font-weight: bold;
        border: none;
    }
    .stButton button:disabled { background-color: #d3d3d3; color: #888888; }
    .destaque-cardapio {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #25D366;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CARREGAMENTO DE DADOS
# Usando o ID da sua nova planilha fornecida
ID_PLANILHA = "1iXXBhK5lt0Eml_VE1BPXbxgSesjeVK9DJFCZAuklGd4"
URL_PLANILHA = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

@st.cache_data(ttl=60)
def carregar_dados():
    try:
        df = pd.read_csv(URL_PLANILHA)
        df.columns = df.columns.str.strip() 
        return df
    except Exception as e:
        st.error(f"Erro ao conectar com a planilha: {e}")
        return None

df = carregar_dados()

# 3. CABEÇALHO (Logo ao lado dos dados)
if df is not None:
    col_logo, col_info = st.columns([1, 2])
    
    with col_logo:
        st.image("https://raw.githubusercontent.com/GranTurin/gran_turin_app/main/logo.png", width=110)
    
    with col_info:
        st.markdown("**🍴 Sugestões de Hoje:**")
        # Pega as carnes e acompanhamentos para exibir no topo
        carnes_hoje = ", ".join(df['Carnes'].dropna().astype(str).tolist()[:3]) # Mostra as 3 primeiras
        acomps_hoje = ", ".join(df['Acompanhamentos'].dropna().astype(str).tolist()[:3])
        
        st.markdown(f"**🥩 Carnes:** {carnes_hoje}")
        st.markdown(f"**🥗 Acomps:** {acomps_hoje}")

st.divider()

# 4. INTERFACE DE PEDIDO
if df is not None:
    try:
        opcoes_carne = df['Carnes'].dropna().tolist()
        opcoes_acomp = df['Acompanhamentos'].dropna().tolist()
        opcoes_tamanho = df['Tamanho'].dropna().tolist()

        # Identificação
        with st.container(border=True):
            nome = st.text_input("👤 Seu Nome:", placeholder="Ex: João Silva")
            end = st.text_input("📍 Endereço/Loja:", placeholder="Ex: Rua Direita, 123")

        # Seleção
        st.subheader("📝 Monte seu prato")
        c1, c2 = st.columns(2)
        with c1:
            tamanho = st.selectbox("📏 Tamanho:", ["Selecione..."] + opcoes_tamanho)
        with c2:
            carne_escolhida = st.selectbox("🥩 Proteína:", ["Selecione..."] + opcoes_carne)
        
        acomps_escolhidos = st.multiselect("🥗 Escolha seus acompanhamentos:", opcoes_acomp)
        obs = st.text_area("🗒️ Observações:", placeholder="Ex: Sem cebola, enviar talher...")

        # Lógica do Botão (Impedir cliques acidentais)
        pode_enviar = nome and end and carne_escolhida != "Selecione..." and tamanho != "Selecione..."

        if not pode_enviar:
            st.info("💡 Preencha os campos obrigatórios para liberar o envio.")

        if st.button("🚀 GERAR PEDIDO NO WHATSAPP", disabled=not pode_enviar):
            txt_acomps = ", ".join(acomps_escolhidos) if acomps_escolhidos else "Padrão da casa"
            
            texto_pedido = (
                f"*🍱 NOVO PEDIDO - GRAN TURIN*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"*👤 CLIENTE:* {nome}\n"
                f"*📍 ENDEREÇO:* {end}\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"*📏 TAMANHO:* {tamanho}\n"
                f"*🥩 PROTEÍNA:* {carne_escolhida}\n"
                f"*🥗 ACOMPS:* {txt_acomps}\n"
                f"*🗒️ OBS:* {obs if obs else 'Nenhuma'}\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"✅ _Enviado via Cardápio Digital_"
            )
            
            numero_whatsapp = "5521986577315"
            link = f"https://wa.me/{numero_whatsapp}?text={urllib.parse.quote(texto_pedido)}"
            
            st.success("Pedido gerado!")
            st.link_button("🟢 CLIQUE AQUI PARA ENVIAR NO WHATSAPP", link)

    except Exception as e:
        st.error(f"Erro ao processar colunas: {e}")

st.markdown("---")
st.caption("Gran Turin - v2.7")
