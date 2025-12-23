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

# --- ABA 2: CADASTROS (REESCRITA PARA FORÇAR EXIBIÇÃO) ---
with tab2:
    st.header("⚙️ Ver e Gerenciar Cadastros")

    # --- CATEGORIAS ---
    with st.expander("📂 Lista de Categorias", expanded=True):
        res_cat = supabase.table("categorias").select("*").execute()
        if res_cat.data:
            # Mostra em uma lista simples
            for c in res_cat.data:
                st.markdown(f"✅ **{c.get('nome', 'Sem Nome')}**")
        else:
            st.warning("Nenhuma categoria encontrada no banco.")
        
        st.write("---")
        nova_c = st.text_input("Cadastrar Nova Categoria:").upper()
        if st.button("Salvar Categoria"):
            supabase.table("categorias").insert({"nome": nova_c}).execute()
            st.rerun()

    # --- PRODUTOS ---
    with st.expander("📦 Lista de Produtos", expanded=True):
        res_prod = supabase.table("lista_produtos").select("*").execute()
        if res_prod.data:
            df_prod = pd.DataFrame(res_prod.data)
            st.dataframe(df_prod, use_container_width=True)
        else:
            st.warning("Nenhum produto encontrado no banco.")

        st.write("---")
        n_p = st.text_input("Cadastrar Novo Produto:").upper()
        n_a = st.number_input("Preço Alvo:", min_value=0.0)
        # Puxa categorias para o select
        cat_options = [c['nome'] for c in res_cat.data] if res_cat.data else []
        n_c = st.selectbox("Categoria:", cat_options)
        if st.button("Salvar Produto"):
            supabase.table("lista_produtos").insert({"nome": n_p, "categoria": n_c, "preco_alvo": n_a}).execute()
            st.rerun()

    # --- MERCADOS ---
    with st.expander("🛒 Lista de Mercados", expanded=True):
        res_merc = supabase.table("lista_mercados").select("*").execute()
        if res_merc.data:
            for m in res_merc.data:
                st.markdown(f"🏠 **{m.get('nome', 'Sem Nome')}**")
        else:
            st.warning("Nenhum mercado encontrado no banco.")

        st.write("---")
        n_m = st.text_input("Cadastrar Novo Mercado:").upper()
        if st.button("Salvar Mercado"):
            supabase.table("lista_mercados").insert({"nome": n_m}).execute()
            st.rerun()
