import plotly.express as px
import pandas as pd

def create_esf_bar_chart(df: pd.DataFrame, column_name: str, esf_name: str):
    """
    Gera um gráfico de barras interativo (Plotly) para a coluna selecionada,
    mostrando a frequência das respostas para o ESF.
    """

    if df.empty:
        return None;
    
    df_counts = df[column_name].value_counts().reset_index()
    df_counts.columns = ['Resposta', 'Contagem']

    fig = px.bar(
        df_counts,
        x='Contagem',
        y='Resposta',
        orientation='h',
        title=f'Distribuicão de Respostas: "{column_name}" em {esf_name}',
        labels={'Resposta': 'Opção de Resposta', 'Contagem': 'Frequência (Nº de Respostas)'},
        color='Contagem',
        color_continuous_scale=px.colors.sequential.Teal,
    )
    
    fig.update_layout(
        title_x=0.5, 
        yaxis={'categoryorder':'total ascending'},
        hovermode="y unified" 
    )

    return fig
