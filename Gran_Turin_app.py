import streamlit as st
import urllib.parse

# Configuração da página
st.set_page_config(page_title="Pedido de Marmitas", page_icon="🍱")

st.title("🍱 Monte sua Marmita")

# 1. Definição do Cardápio
opcoes_carne = ["Frango Grelhado", "Carne de Panela", "Iscas de Peixe", "Omelete"]
opcoes_acompanhamento = ["Arroz Branco", "Feijão Carioca", "Purê de Batata", "Salada", "Farofa"]

# 2. Interface de Escolha
nome_cliente = st.text_input("Seu Nome:")
carne_escolhida = st.selectbox("Escolha a Proteína:", opcoes_carne)
acompanhamentos = st.multiselect("Escolha os Acompanhamentos:", opcoes_acompanhamento)

# 3. Processamento do Pedido
if st.button("Enviar Pedido pelo WhatsApp"):
    if nome_cliente and carne_escolhida:
        # Monta o texto da mensagem
        lista_acomp = ", ".join(acompanhamentos)
        texto = (
            f"Olá! Gostaria de fazer um pedido:\n\n"
            f"*Nome:* {nome_cliente}\n"
            f"*Proteína:* {carne_escolhida}\n"
            f"*Acompanhamentos:* {lista_acomp}"
        )
        
        # Gera o link (substitua pelo SEU número com DDD)
        numero_whatsapp = "5521986577315" 
        link = f"https://wa.me/{numero_whatsapp}?text={urllib.parse.quote(texto)}"
        
        st.success("Pedido gerado com sucesso!")
        st.link_button("Abrir WhatsApp para enviar", link)
    else:
        st.error("Por favor, preencha seu nome e escolha a carne.")