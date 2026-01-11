# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import sqlite3
import io
import re

# 1. CONFIGURAÇÃO (Sempre a primeira coisa)
st.set_page_config(page_title="Circuit Flow Pro", layout="wide")

# 2. CONEXÃO COM O BANCO (Protegida)
def get_db_connection():
    # O segredo para não travar: timeout e check_same_thread
    conn = sqlite3.connect("geoloc_cache_v2.sqlite", check_same_thread=False, timeout=20)
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cache_geoloc (
            endereco TEXT PRIMARY KEY,
            lat REAL,
            lon REAL
        )
    """)
    conn.commit()
    return conn

# 3. FUNÇÕES LÓGICAS (Onde entra sua inteligência de negócio)
def limpar_texto(texto):
    if pd.isna(texto): return ""
    return str(texto).strip().upper()

# 4. INTERFACE
def main():
    st.title("🗺️ Novo Flow de Roteirização")
    conn = init_db()

    # Menu Lateral para organização
    menu = st.sidebar.selectbox("Escolha a Etapa:", ["Início", "Processar Planilha", "Ver Cache"])

    if menu == "Início":
        st.subheader("Bem-vindo ao novo sistema.")
        st.info("Este sistema foi recriado do zero para garantir velocidade e estabilidade.")
        
    elif menu == "Processar Planilha":
        st.subheader("Suba seu arquivo (CSV ou XLSX)")
        u_file = st.file_uploader("Arquivo original", type=['csv', 'xlsx'])
        
        if u_file:
            # Lógica de leitura automática
            try:
                if u_file.name.endswith('.csv'):
                    df = pd.read_csv(u_file)
                else:
                    df = pd.read_excel(u_file)
                
                st.success(f"Carregado: {len(df)} linhas.")
                st.dataframe(df.head(10)) # Mostra apenas as primeiras 10 para não travar a tela
                
                # Botão para processar
                if st.button("Executar Agrupamento"):
                    st.write("Processando... (aqui entra sua lógica de Fuzzy Matching)")
                    # Aqui chamaremos as funções de agrupamento que você já criou
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}")

    elif menu == "Ver Cache":
        st.subheader("Endereços Salvos")
        df_cache = pd.read_sql_query("SELECT * FROM cache_geoloc", conn)
        st.dataframe(df_cache, use_container_width=True)
        
        if st.button("Limpar Banco de Dados"):
            conn.execute("DELETE FROM cache_geoloc")
            conn.commit()
            st.rerun()

if __name__ == "__main__":
    main()
