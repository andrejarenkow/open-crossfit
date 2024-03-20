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

col2.header('Open Crossfit 24')


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
    cidade = st.multiselect('Selecione a cidade', options=df[df['country']==pais]['city'].unique(), default=['PORTO ALEGRE'])
    box = st.selectbox('Qual box você deseja ver as estatísticas?', options=sorted(df[df['city'].isin(cidade)]['name']))
    df_box_selecionado = df[df['name']==box]
    try:
        url_imagem = df_box_selecionado['images'].values[0]['logo']['url']
        st.image(url_imagem)
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
    
    #total alunos inscritos
    total_alunos_inscritos = len(dados_box)
    st.metric('Total atletas',total_alunos_inscritos)

    # Gráfico de pizza por gênero
    fig_gender = px.pie(dados_box, names='gender')
    st.plotly_chart(fig_gender)

    # Gráfico de barras para divisão de quantos foram em qual categoria em cada prova
    df_barras = pd.concat([df_grafico_barras(dados_box, 'scaled_descrito_1', '24.1'),
                           df_grafico_barras(dados_box, 'scaled_descrito_2', '24.2'),
                           df_grafico_barras(dados_box, 'scaled_descrito_3', '24.3')])
    # Criando a tabela dinâmica
    df_barras = df.value_counts(['Categoria','Prova']).reset_index()
    df_barras.columns = ['Categoria', 'Prova', 'Contagem']
    df_barras
    #fig_categorias = px.bar(df_barras, x="Prova", y="Contagem", color="Categoria")
    #st.plotly_chart(fig_categorias)
    
    dados_box

except:
  st.subheader('Não há dados sobre este box na Open 2024')

