import pandas as pd
import streamlit as st
import os

FILE_PATH = os.path.join('dados', 'Organização ESF - Respostas ao Formulário 1.csv')
COLUNA_ESF = 'De qual ESF você é?'
VALOR_IGNORAR = 'Em Branco'

@st.cache.data
def load_data():
    """
    Carrega o DataFrame, realiza a limpeza inicial e retorna os dados prontos.
    Tenta diferentes configurações de leitura (separador e encoding).
    """
    print("Tentando carregar o arquivo: {FILE_PATH}")

    try:
        df = pd.read_csv(FILE_PATH, sep=',', encoding='latin1')
    except Exception as e:
        try:
            df = pd.read_csv(FILE_PATH, sep=';', encoding='latin1')
        except Exception:
            st.error(f"Erro: Nao foi possivel carregar o arquivo. Verifique o caminho e a codificacao. {e}")
            return None
    
    df.columns = df.columns.str.strip()
    df = df[df[COLUNA_ESF] != VALOR_IGNORAR]

    df = df.dropna(subset=[COLUNA_ESF])

    for col in df.select_dtype(include=['objetc']).columns:
        df[col] = df[col].astype(str).str.strip()
    
    print("Dados carregados com sucesso")
    return df