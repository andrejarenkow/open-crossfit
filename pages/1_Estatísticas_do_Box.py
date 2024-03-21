import pandas as pd
import plotly.express as px
import requests
import numpy as np
import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="Open Crossfit",
    page_icon="	:weight_lifter:",
    layout="wide",
    initial_sidebar_state='expanded'
) 
col1, col2, col3 = st.columns([1,4,1])

# Função para acessar os valores da lista
def acessar_latitude(lista):
    return lista[1]

# Função para acessar os valores da lista
def acessar_longitude(lista):
    return lista[0]

# Lista afiliados
request = 'https://www.crossfit.com/wp-content/uploads/affiliates.json'
r = requests.get(request)
data = r.json()
df = pd.DataFrame([d.get('properties', {}) for d in data['features']])
map = pd.DataFrame([d.get('geometry', {}) for d in data['features']])
df = pd.concat([df,map], axis=1)
df['lat'] = df['coordinates'].apply(acessar_latitude)
df['lon'] = df['coordinates'].apply(acessar_longitude)
df['city'] = df['city'].str.strip().str.upper()

# Using "with" notation
with st.sidebar:
    st.subheader('OPEN 2024')
    pais = 'BR'
    cidade = st.multiselect('Selecione a cidade', options=sorted(df[df['country']==pais]['city'].unique()), default=['PORTO ALEGRE'])
    box = st.selectbox('Qual box você deseja ver as estatísticas?', options=sorted(df[df['city'].isin(cidade)]['name']))
    df_box_selecionado = df[df['name']==box]
    try:
        url_imagem = df_box_selecionado['images'].values[0]['logo']['url']
        st.image(url_imagem, width=300)
    except:
        url_imagem = df_box_selecionado['images'].values[0]['primary']['url']
        st.image(url_imagem)
    
                      

# Limpeza e tratamento dos dados
dados = pd.read_parquet('dados_crossfit.parquet')
dados['scaled_descrito_1'] = dados['scaled_1'].replace({'0':'RX', '1':'Scale', '2':'Foundations'})
dados['scaled_descrito_2'] = dados['scaled_2'].replace({'0':'RX', '1':'Scale', '2':'Foundations'})
dados['scaled_descrito_3'] = dados['scaled_3'].replace({'0':'RX', '1':'Scale', '2':'Foundations'})

dados['age'] = pd.to_numeric(dados['age'], errors='coerce')
dados['score_1'] = pd.to_numeric(dados['score_1'], errors='coerce')
dados['score_2'] = pd.to_numeric(dados['score_2'], errors='coerce')
dados['score_3'] = pd.to_numeric(dados['score_3'], errors='coerce')

# Função para criar o gráfico de barras
def df_grafico_barras(df, coluna, nome_prova):
    df_novo = pd.DataFrame(df[coluna])
    df_novo.columns = ['Categoria']
    df_novo['Prova'] = nome_prova

    return df_novo

try:
    dados_box = dados[dados['affiliateName']==box]
    total_atletas_box = len(dados_box)
    dados_box['imagem_perfil'] = dados_box['profilePicS3key'].apply(lambda x: 'https://profilepicsbucket.crossfit.com/' + x)
    col2.header(f'Open Crossfit 24 - Estatísticas {box}, {total_atletas_box} atletas')
    
    # Layout
    c1, c2, c3 = st.columns(3)


    # Gráfico de pizza por gênero
    fig_gender = px.pie(dados_box, names='gender', title='Divisão de atletas por gênero', width=400, color='gender',
                        color_discrete_map={'F':'indianred', 'M':'royalblue'})
    c1.plotly_chart(fig_gender, )

    # Gráfico de barras para divisão de quantos foram em qual categoria em cada prova
    df_barras = pd.concat([df_grafico_barras(dados_box, 'scaled_descrito_1', '24.1'),
                           df_grafico_barras(dados_box, 'scaled_descrito_2', '24.2'),
                           df_grafico_barras(dados_box, 'scaled_descrito_3', '24.3')])
    # Criando a tabela dinâmica
    df_barras = df_barras.value_counts(['Categoria','Prova']).reset_index().sort_values('Prova')
    df_barras.columns = ['Categoria', 'Prova', 'Contagem']
    fig_categorias = px.bar(df_barras, x="Prova", y="Contagem", color="Categoria", title='Número de atletas por categoria por prova',
                           color_discrete_map={'RX':'#03DAC5', 'Scale':'#BB86FC', 'Foundations':'#FF4181'}, width=400)
    # Definindo o tipo de eixo x como 'category'
    fig_categorias.update_xaxes(type='category')
    c2.plotly_chart(fig_categorias)

    # Plotando distribuição de faixa etária
    # Definir faixas etárias de 10 em 10 anos
    faixas_etarias = range(10, 81, 5)
    
    # Criar coluna com faixas etárias
    dados_box['faixa_etaria'] = pd.cut(dados_box['age'], bins=faixas_etarias)
    
    # Contar o número de registros em cada faixa etária
    contagem_faixas = dados_box['faixa_etaria'].value_counts().sort_index().reset_index()
    contagem_faixas.columns = ['Faixa Etária', 'Número de Pessoas']
    
    # Converter faixas etárias para strings
    contagem_faixas['Faixa Etária'] = contagem_faixas['Faixa Etária'].astype(str)
    
    # Plotar o histograma com o Plotly Express
    fig = px.bar(contagem_faixas, x='Faixa Etária', y='Número de Pessoas',
                 labels={'Faixa Etária': 'Faixa Etária', 'Número de Pessoas': 'Número de Pessoas'},
                 title='Atletas por Faixas Etárias', width=400)
    fig.update_xaxes(type='category')
    c3.plotly_chart(fig)

    # Tabela
    dados_tabela_box = dados_box[['competitorName','imagem_perfil', 'affiliateName', 'age','scaled_descrito_1','scoreDisplay_1','scaled_descrito_2', 'scoreDisplay_2','scaled_descrito_3', 'scoreDisplay_3']]
    st.dataframe(dados_tabela_box.sort_values('competitorName'),
                 column_config={
                    "imagem_perfil": st.column_config.ImageColumn(
                                        "Imagem",
        ),
                     'competitorName':st.column_config.Column('Atleta'),
                     'affiliateName':st.column_config.Column('Afiliado'),
                     'age':st.column_config.NumberColumn('Idade'),
                     'scaled_descrito_1':st.column_config.Column('Categoria 24.1'),
                     'scoreDisplay_1':st.column_config.Column('Score 24.1'),
                     'scaled_descrito_2':st.column_config.Column('Categoria 24.2'),
                     'scoreDisplay_2':st.column_config.Column('Score 24.2'),
                     'scaled_descrito_3':st.column_config.Column('Categoria 24.3'),
                     'scoreDisplay_3':st.column_config.Column('Score 24.3'),
    },
    hide_index=True,
                )
    #dados_box
except:
  st.subheader('Não há dados sobre este box na Open 2024')


with st.sidebar:
    st.markdown('Página criada por [André Jarenkow](https://www.linkedin.com/in/andre-jarenkow/)')



