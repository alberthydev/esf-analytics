import pandas as pd
import streamlit as st
import gspread 
import os

GOOGLE_SHEET_TITLE = st.secrets["app_config"]["google_sheet_title"] 
COLUNA_ESF = 'De qual ESF você é?'
VALOR_IGNORAR = 'Em Branco'

def fix_encoding_corruption(text: str) -> str:
    """Tenta corrigir a corrupção de encoding em valores de texto."""
    try:
        if isinstance(text, str):
            return text.encode('latin1').decode('utf8')
        return text
    except:
        return text

@st.cache_data
def load_data():
    """
    Autentica com o Google Sheets API usando st.secrets e carrega os dados.
    """
    print(f"Tentando carregar dados do Google Sheet: {GOOGLE_SHEET_TITLE}")

    try:
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])

        spreadsheet = gc.open(GOOGLE_SHEET_TITLE)
        
        worksheet = spreadsheet.sheet1 
        
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)

    except Exception as e:
        st.error(f"""
        Erro ao carregar dados do Google Sheets.
        Verifique as permissões da Service Account e o nome/ID da planilha.
        Detalhes: {e}
        """)
        return None

    df.columns = df.columns.str.strip()
    df.columns = [fix_encoding_corruption(col) for col in df.columns]
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

    df = df[df[COLUNA_ESF] != COLUNA_ESF] 
    
    df = df[df[COLUNA_ESF] != VALOR_IGNORAR]

    df[COLUNA_ESF].replace('', pd.NA, inplace=True)
    
    df = df.dropna(subset=[COLUNA_ESF])

    print("Dados carregados e limpos com sucesso a partir do Google Sheets.")
    return df 

def get_esf_list(df):
    """Retorna uma lista ordenada e única de todos os nomes de ESF, com encoding corrigido."""
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