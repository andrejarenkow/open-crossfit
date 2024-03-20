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
    box = st.selectbox('Qual box você deseja ver as estatísticas?', options=df[df['city'].isin(cidade)]['name'])
    df_box_selecionado = df[df['name']==box]
    url_imagem = df_box_selecionado['images']['primary']['url']
    st.image(url_imagem)
                      

# Limpeza e tratamento dos dados
dados = pd.read_parquet('dados_crossfit.parquet')
dados['age'] = pd.to_numeric(dados['age'], errors='coerce')
dados['score_1'] = pd.to_numeric(dados['score_1'], errors='coerce')
dados['score_2'] = pd.to_numeric(dados['score_2'], errors='coerce')

try:
    dados_box = dados[dados['affiliateName']==box]
    
    #total alunos inscritos
    total_alunos_inscritos = len(dados_box)
    st.metric('Total atletas',total_alunos_inscritos)
    dados_box

except:
  st.subheader('Não há dados sobre este box na Open 2024')

