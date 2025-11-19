import streamlit as st
from modules.data_loader import load_data, get_esf_list, get_chart_columns, COLUNA_ESF
from modules.chart_generator import create_esf_bar_chart

st.set_page_config(
    page_title="ESF-Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_password():
    """Retorna True se o usuário digitou a senha correta."""
    
    SECRET_PASSWORD = st.secrets["app_config"]["access_password"]
    
    if 'password_correct' not in st.session_state:
        st.session_state['password_correct'] = False

    def password_entered():
        """Verifica se a senha digitada está correta."""
        if st.session_state["password"] == SECRET_PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  
        else:
            st.session_state["password_correct"] = False
            st.error("Acesso Negado: Senha incorreta.")

    if st.session_state["password_correct"]:
        return True

    st.title("🔒 Acesso Restrito: ESF-Analytics")
    st.text_input(
        "Digite a Chave de Acesso:", type="password", on_change=password_entered, key="password"
    )
    return False

if check_password():
    
    st.title("ESF-Analytics: Dashboard Interativo")
    st.markdown("Análise de Satisfação e Organização por Estratégia Saúde da Família (ESF).")

    df = load_data()

    if df is not None:
        
        st.sidebar.header("Opções de Análise")
        
        esf_list = get_esf_list(df)
        esf_selecionado = st.sidebar.selectbox(
            "Selecione o ESF para Análise",
            options=esf_list
        )
        
        chart_cols = get_chart_columns(df)
        coluna_selecionada = st.sidebar.selectbox(
            "Selecione a Coluna para Visualizar",
            options=chart_cols
        )
        
        df_filtrado = df[df[COLUNA_ESF] == esf_selecionado]
        
        st.header(f"Análise Detalhada: **{esf_selecionado}**")
        
        st.info(f"Total de Respostas Coletadas para **{esf_selecionado}**: **{len(df_filtrado)}**")
        
        if not df_filtrado.empty:
            fig = create_esf_bar_chart(df_filtrado, coluna_selecionada, esf_selecionado)
            
            st.plotly_chart(fig, width='stretch')
            
            st.subheader(f"Tabela de Frequência para: {coluna_selecionada}")
            df_counts = df_filtrado[coluna_selecionada].value_counts().reset_index()
            df_counts.columns = ['Resposta', 'Contagem']
            df_counts['% do Total'] = (df_counts['Contagem'] / df_counts['Contagem'].sum() * 100).round(1).astype(str) + '%'
            st.dataframe(df_counts, width='stretch')
            
        else:
            st.warning(f"Nenhum dado encontrado para o ESF {esf_selecionado} ou a coluna selecionada.")