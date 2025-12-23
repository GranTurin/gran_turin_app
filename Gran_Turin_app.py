import streamlit as st
from supabase import create_client, Client
import pandas as pd
import urllib.parse

# --- CONFIGURAÇÃO DO SUPABASE ---
SUPABASE_URL = "https://mvozbjdmfkezdlzipstw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12b3piamRtZmtlemRsemlwc3R3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY0NTEzMDksImV4cCI6MjA4MjAyNzMwOX0.pd76MIzgkfrbwvN0GlZxqIviKLEG49VCWRiXR4-13Bg"

# Conexão sem cache para teste
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Debug Gran Turin", layout="centered")

# --- BLOCO DE TESTE DE CONEXÃO ---
st.warning("🔍 Verificando Banco de Dados...")
try:
    teste_cat = supabase.table("categorias").select("*").execute()
    st.success(f"Conexão OK! Linhas encontradas na tabela categorias: {len(teste_cat.data)}")
    if len(teste_cat.data) == 0:
        st.error("A tabela 'categorias' existe, mas está VAZIA no Supabase.")
except Exception as e:
    st.error(f"Erro Real ao ler tabela: {e}")

st.divider()

tab1, tab2 = st.tabs(["💰 Preços", "⚙️ Cadastros"])

# --- ABA 2: CADASTROS (FOCO NO ERRO) ---
with tab2:
    st.subheader("Categorias")
    n_cat = st.text_input("Nova Categoria").upper()
    if st.button("Salvar"):
        res = supabase.table("categorias").insert({"nome": n_cat}).execute()
        st.write("Resposta do Banco ao salvar:", res.data)
        st.rerun()

    st.write("---")
    # Tentativa de listagem bruta
    dados_brutos = supabase.table("categorias").select("*").execute()
    st.write("Dados brutos vindos do Supabase:", dados_brutos.data)
