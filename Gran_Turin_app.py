import streamlit as st
from supabase import create_client, Client
import pandas as pd
import urllib.parse

# --- CONFIGURAÇÃO DO SUPABASE ---
SUPABASE_URL = "https://mvozbjdmfkezdlzipstw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12b3piamRtZmtlemRsemlwc3R3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY0NTEzMDksImV4cCI6MjA4MjAyNzMwOX0.pd76MIzgkfrbwvN0GlZxqIviKLEG49VCWRiXR4-13Bg"

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

st.set_page_config(page_title="Gestor Gran Turin", layout="centered")
st.title("📊 Gestor de Preços Gran Turin")

tab1, tab2 = st.tabs(["💰 Preços", "⚙️ Cadastros"])

# --- ABA 1: PREÇOS ---
with tab1:
    whatsapp_num = st.text_input("WhatsApp para envio (55+DDD+Número)", value="55")
    
    # Carregar dados para os selects
    res_p = supabase.table("lista_produtos").select("nome").order("nome").execute()
    res_m = supabase.table("lista_mercados").select("nome").order("nome").execute()
    prods = [p['nome'] for p in res_p.data] if res_p.data else []
    mercs = [m['nome'] for m in res_m.data] if res_m.data else []

    with st.expander("➕ Lançar Novo Preço"):
        col1, col2 = st.columns(2)
        p_sel = col1.selectbox("Produto", prods)
        m_sel = col2.selectbox("Mercado", mercs)
        v_sel = st.number_input("Preço R$", min_value=0.0, step=0.01)
        if st.button("Salvar Preço"):
            res_c = supabase.table("lista_produtos").select("categoria").eq("nome", p_sel).execute()
            cat = res_c.data[0]['categoria'] if res_c.data else "Geral"
            supabase.table("precos").insert({"produto": p_sel, "mercado": m_sel, "valor": v_sel, "categoria": cat}).execute()
            st.rerun()

    st.divider()
    
    # Listagem Comparativa
    res_all = supabase.table("precos").select("*").execute()
    if res_all.data:
        df = pd.DataFrame(res_all.data)
        # Botão WhatsApp
        texto_wa = "*🛒 RESUMO DE PREÇOS:*\n\n"
        for p in sorted(df['produto'].unique()):
            df_p = df[df['produto'] == p]
            win = df_p.loc[df_p['valor'].idxmin()]
            texto_resumo = f"✅ *{p}*\n📍 {win['mercado']}: R$ {win['valor']:.2f}\n\n"
            texto_wa += texto_resumo
        
        st.link_button("📲 Enviar Menores Preços", f"https://wa.me/{whatsapp_num}?text={urllib.parse.quote(texto_wa)}", type="primary")

# --- ABA 2: CADASTROS (AQUI ESTÁ O QUE VOCÊ PEDIU) ---
with tab2:
    st.header("⚙️ Ver e Gerenciar Cadastros")

    # --- 1. SEÇÃO DE CATEGORIAS ---
    with st.expander("📂 Ver / Cadastrar Categorias"):
        st.subheader("Categorias no Sistema")
        res_cat = supabase.table("categorias").select("*").order("nome").execute()
        if res_cat.data:
            for c in res_cat.data:
                col_a, col_b = st.columns([4, 1])
                col_a.write(f"• {c['nome']}")
                if col_b.button("🗑️", key=f"del_c_{c['id']}"):
                    supabase.table("categorias").delete().eq("id", c['id']).execute()
                    st.rerun()
        else:
            st.info("Nenhuma categoria cadastrada.")
        
        st.write("---")
        nova_c = st.text_input("Nova Categoria:").upper()
        if st.button("Adicionar Categoria"):
            supabase.table("categorias").insert({"nome": nova_c}).execute()
            st.rerun()

    # --- 2. SEÇÃO DE PRODUTOS ---
    with st.expander("📦 Ver / Cadastrar Produtos"):
        st.subheader("Produtos no Sistema")
        res_prod = supabase.table("lista_produtos").select("*").order("nome").execute()
        if res_prod.data:
            df_prod = pd.DataFrame(res_prod.data)[['nome', 'categoria', 'preco_alvo']]
            df_prod.columns = ['Produto', 'Categoria', 'Preço Alvo']
            st.table(df_prod) # Mostra a lista completa em tabela
            
            # Opção de deletar
            p_para_deletar = st.selectbox("Selecione um produto para excluir:", ["Selecione..."] + [p['nome'] for p in res_prod.data])
            if st.button("Confirmar Exclusão de Produto"):
                supabase.table("lista_produtos").delete().eq("nome", p_para_deletar).execute()
                st.rerun()
        else:
            st.info("Nenhum produto cadastrado.")

        st.write("---")
        n_p = st.text_input("Nome do Novo Produto:").upper()
        n_a = st.number_input("Preço Alvo do Produto:", min_value=0.0)
        # Pega as categorias existentes para o select
        lista_c = [c['nome'] for c in res_cat.data] if res_cat.data else []
        n_c = st.selectbox("Categoria do Produto:", lista_c)
        if st.button("Adicionar Produto"):
            supabase.table("lista_produtos").insert({"nome": n_p, "categoria": n_c, "preco_alvo": n_a}).execute()
            st.rerun()

    # --- 3. SEÇÃO DE MERCADOS ---
    with st.expander("🛒 Ver / Cadastrar Mercados"):
        st.subheader("Mercados no Sistema")
        res_merc = supabase.table("lista_mercados").select("*").order("nome").execute()
        if res_merc.data:
            for m in res_merc.data:
                col_m1, col_m2 = st.columns([4, 1])
                col_m1.write(f"• {m['nome']}")
                if col_m2.button("🗑️", key=f"del_m_{m['id']}"):
                    supabase.table("lista_mercados").delete().eq("id", m['id']).execute()
                    st.rerun()
        else:
            st.info("Nenhum mercado cadastrado.")

        st.write("---")
        n_m = st.text_input("Nome do Novo Mercado:").upper()
        if st.button("Adicionar Mercado"):
            supabase.table("lista_mercados").insert({"nome": n_m}).execute()
            st.rerun()
