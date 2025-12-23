import streamlit as st
from supabase import create_client, Client
import pandas as pd
import urllib.parse

# --- CONFIGURAÇÃO DO SUPABASE ---
SUPABASE_URL = "https://mvozbjdmfkezdlzipstw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12b3piamRtZmtlemRsemlwc3R3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY0NTEzMDksImV4cCI6MjA4MjAyNzMwOX0.pd76MIzgkfrbwvN0GlZxqIviKLEG49VCWRiXR4-13Bg"

# Conexão direta sem cache para garantir que os dados apareçam
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Gestor Gran Turin", layout="centered")
st.title("📊 Gestor de Preços Gran Turin")

tab1, tab2 = st.tabs(["💰 Preços", "⚙️ Cadastros"])

# --- ABA 1: PREÇOS ---
with tab1:
    whatsapp_num = st.text_input("WhatsApp para envio (55+DDD+Número)", value="55")
    
    # Carregar dados para os selects
    try:
        res_p = supabase.table("lista_produtos").select("nome").order("nome").execute()
        res_m = supabase.table("lista_mercados").select("nome").order("nome").execute()
        prods = [p['nome'] for p in res_p.data] if res_p.data else []
        mercs = [m['nome'] for m in res_m.data] if res_m.data else []
    except:
        prods, mercs = [], []

    with st.expander("➕ Lançar Novo Preço"):
        col1, col2 = st.columns(2)
        p_sel = col1.selectbox("Produto", prods)
        m_sel = col2.selectbox("Mercado", mercs)
        v_sel = st.number_input("Preço R$", min_value=0.0, step=0.01)
        if st.button("Salvar Preço"):
            res_c = supabase.table("lista_produtos").select("categoria").eq("nome", p_sel).execute()
            cat = res_c.data[0]['categoria'] if res_c.data else "Geral"
            supabase.table("precos").insert({"produto": p_sel, "mercado": m_sel, "valor": v_sel, "categoria": cat}).execute()
            st.success("Preço salvo!")
            st.rerun()

    st.divider()
    
    res_all = supabase.table("precos").select("*").execute()
    if res_all.data:
        df = pd.DataFrame(res_all.data)
        # Lógica de Cores e WhatsApp...
        for cat in sorted(df['categoria'].unique()):
            st.markdown(f"#### 📂 {cat}")
            df_cat = df[df['categoria'] == cat]
            for p in sorted(df_cat['produto'].unique()):
                precos_p = df_cat[df_cat['produto'] == p].sort_values(by="valor")
                min_v = precos_p['valor'].min()
                st.write(f"**📦 {p}**")
                for _, row in precos_p.iterrows():
                    bg = "#d4edda" if row['valor'] == min_v else "#ffffff"
                    st.markdown(f'<div style="background-color:{bg}; padding:10px; border-radius:5px; border:1px solid #eee; color:black; margin-bottom:5px;"><b>{row["mercado"]}</b>: R$ {row["valor"]:.2f}</div>', unsafe_allow_html=True)

# --- ABA 2: CADASTROS (CORRIGIDA) ---
with tab2:
    st.header("⚙️ Gerenciar Cadastros")

    # 1. CATEGORIAS
    st.subheader("1. Categorias")
    with st.container():
        # BUSCA DADOS PRIMEIRO
        res_c = supabase.table("categorias").select("nome").order("nome").execute()
        if res_c.data:
            # Criamos uma string com todas as categorias separadas por vírgula ou lista
            lista_nomes = ", ".join([c['nome'] for c in res_c.data])
            st.info(f"**Já Cadastradas:** {lista_nomes}")
        else:
            st.warning("Nenhuma categoria encontrada.")
        
        c_in, c_bt = st.columns([3, 1])
        nova_cat = c_in.text_input("Nova Categoria:", key="new_cat").upper()
        if c_bt.button("Adicionar", key="add_cat"):
            if nova_cat:
                supabase.table("categorias").insert({"nome": nova_cat}).execute()
                st.rerun()

    st.divider()

    # 2. PRODUTOS
    st.subheader("2. Produtos")
    with st.container():
        res_p_list = supabase.table("lista_produtos").select("nome, categoria").order("nome").execute()
        if res_p_list.data:
            df_p = pd.DataFrame(res_p_list.data)
            st.dataframe(df_p, use_container_width=True)
        else:
            st.warning("Nenhum produto encontrado.")

        p_nome = st.text_input("Nome do Produto:", key="new_p").upper()
        p_alvo = st.number_input("Preço Alvo:", min_value=0.0, key="new_a")
        # Busca categorias para o select
        cats_for_sel = [c['nome'] for c in res_c.data] if res_c.data else []
        p_cat = st.selectbox("Categoria:", cats_for_sel, key="sel_cat_p")
        
        if st.button("Salvar Produto", key="save_p"):
            if p_nome and p_cat:
                supabase.table("lista_produtos").insert({"nome": p_nome, "categoria": p_cat, "preco_alvo": p_alvo}).execute()
                st.rerun()

    st.divider()

    # 3. MERCADOS
    st.subheader("3. Mercados")
    with st.container():
        res_m_list = supabase.table("lista_mercados").select("nome").order("nome").execute()
        if res_m_list.data:
            merc_nomes = ", ".join([m['nome'] for m in res_m_list.data])
            st.info(f"**Mercados:** {merc_nomes}")
        else:
            st.warning("Nenhum mercado encontrado.")

        m_nome = st.text_input("Novo Mercado:", key="new_m").upper()
        if st.button("Adicionar Mercado", key="add_m"):
            if m_nome:
                supabase.table("lista_mercados").insert({"nome": m_nome}).execute()
                st.rerun()
