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

def get_esf_list(df):
    """
    Retorna uma lista ordenada e única de todos os nomes de ESF.
    """
    if df is not None:
        return sorted(df[COLUNA_ESF].unique())
    return []

def get_chart_columns(df):
    """
    Retorna a lista de colunas que podem ser usadas para gerar gráficos categóricos.
    Vamos incluir todas as colunas que não são as colunas de identificação e tempo.
    """
    colunas_para_ignorar = [
        'Carimbo de data/hora',
        COLUNA_ESF,
        'Nome do entrevistador',
        'Nome do Paciente',
        'Data de nascimento do paciente',
        'Sexo da pessoa atendida',
        'Idade da pessoa atendida   ',
        '  Grau de Instrução da pessoa atendida  '
    ]

    charts_cols = [col for col in df.columns if col not in colunas_para_ignorar]
    return charts_cols

SUGGESTED_CHART_COLUMNS = [
    'Quanto tempo você levou para conseguir essa consulta?   ',
    'Como você avalia a forma de marcação das consultas?   ',
    'Como você avalia a forma de marcação de exames laboratoriais?   '
]