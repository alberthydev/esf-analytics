import streamlit as st
from modules.data_loader import load_data, get_esf_list, get_chart_columns, COLUNA_ESF
from modules.chart_generator import create_esf_bar_chart

st.set_page_config(
    page_title="ESF-Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("ESF-Analytics - Dashboard")
st.markdown("Analise de Satisfacao e Organização por Estrategia Saude da Família (ESF).")

df = load_data()

if df is not None:
    st.sidebar.header("Opcoes de Analise")

    esf_list = get_esf_list(df)
    esf_selecionado = st.sidebar.selectbox(
        "Selecione o ESF para Analise",
        options=esf_list
    )

    chart_cols = get_chart_columns(df)
    coluna_selecionada = st.sidebar.selectbox(
        "Selecione a Coluna para Visualizar",
        options=chart_cols
    )

    df_filtrado = df[df[COLUNA_ESF] == esf_selecionado]

    st.header(f"Analise Detalhada: **{esf_selecionado}**")
    st.info(f"Total de Respostas Coletadas para **{esf_selecionado}**: **{len(df_filtrado)}**")

    if not df_filtrado.empty:
        fig = create_esf_bar_chart(df_filtrado, coluna_selecionada, esf_selecionado)

        st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"Tabela de Frequencia para: {coluna_selecionada}")
        df_counts = df_filtrado[coluna_selecionada].value_counts().reset_index() 
        df_counts.columns = ['Resposta', 'Contagem']
        df_counts['% do Total'] = (df_counts['Contagem'] / df_counts['Contagem'].sum() * 100).round(1).astype(str) + '%'
        st.dataframe(df_counts, use_container_width=True)
    else:
        st.warning(f"Nenhum dado encontrado para o ESF {esf_selecionado} ou a coluna selecionada.")