import pandas as pd
import streamlit as st
import os

FILE_PATH = os.path.join('dados', 'Organização ESF - Respostas ao Formulário 1.csv')
COLUNA_ESF = 'De qual ESF você é?' 
VALOR_IGNORAR = 'Em Branco'

def fix_encoding_corruption(text: str) -> str:
    """
    Tenta corrigir a corrupção comum de encoding (ex: Ã© -> é)
    aplicando a re-codificação de latin1 para utf8.
    Isso é aplicado tanto nos nomes das colunas quanto no conteúdo das células.
    """
    try:
        if isinstance(text, str):
            return text.encode('latin1').decode('utf8')
        return text
    except:
        return text

@st.cache_data
def load_data():
    """Carrega o DataFrame, priorizando UTF-8, e realiza a limpeza inicial."""
    print(f"Tentando carregar o arquivo: {FILE_PATH}")
    
    df = None
    
    try:
        df = pd.read_csv(FILE_PATH, sep=',', encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(FILE_PATH, sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(FILE_PATH, sep=',', encoding='latin1')
            except Exception:
                try:
                    df = pd.read_csv(FILE_PATH, sep=';', encoding='latin1')
                except Exception as e:
                    st.error(f"Erro: Não foi possível carregar o arquivo. {e}")
                    return None
                    
    if df is None:
        return None

    df.columns = df.columns.str.strip()
    df.columns = [fix_encoding_corruption(col) for col in df.columns]
    
    df = df[df[COLUNA_ESF] != COLUNA_ESF] 
    
    df = df[df[COLUNA_ESF] != VALOR_IGNORAR]
    
    df = df.dropna(subset=[COLUNA_ESF])
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    print("Dados carregados e limpos com sucesso.")
    return df

def get_esf_list(df):
    """Retorna uma lista ordenada e única de todos os nomes de ESF."""
    if df is not None:
        esf_values = df[COLUNA_ESF].apply(fix_encoding_corruption)
        return sorted(esf_values.unique())
    return []

def get_chart_columns(df):
    """
    Retorna a lista de colunas que podem ser usadas para gerar gráficos categóricos.
    """
    colunas_para_ignorar = [
        'Carimbo de data/hora', 
        COLUNA_ESF, 
        'Nome do entrevistador',
        'Nome do Paciente',
        'Data de nascimento do paciente',
        'Sexo da pessoa atendida',
        'Idade da pessoa atendida',
        'Grau de Instrução da pessoa atendida'
    ]
    
    chart_cols = [col for col in df.columns if col not in colunas_para_ignorar]
    return chart_cols

SUGGESTED_CHART_COLUMNS = [
    'Quanto tempo você levou para conseguir essa consulta?',
    'Como você avalia a forma de marcação das consultas?',
    'Como você avalia a forma de marcação de exames laboratoriais?'
]