import streamlit as st
import plotly.express as px
import requests
import pandas as pd


# Configurações da página
st.set_page_config(
    page_title="Open Crossfit",
    page_icon="	:weight_lifter:",
    layout="wide",
    initial_sidebar_state='expanded'
) 
col1, col2, col3 = st.columns([1,4,1])

col2.header('Open Crossfit 24')

texto = """
A competição Open de CrossFit é um evento anual organizado pela CrossFit, Inc. que atrai atletas de todo o mundo. 
O Open é a primeira etapa das competições CrossFit Games, que são o ápice da temporada competitiva do CrossFit.

Durante o Open, os participantes enfrentam uma série de workouts (treinos) desafiadores ao longo de cinco semanas consecutivas.
Cada semana, um novo workout é anunciado e os atletas têm alguns dias para completá-lo e registrar sua pontuação oficial online. 
Os workouts geralmente combinam uma variedade de movimentos funcionais, como levantamento de peso, ginástica e exercícios cardiovasculares, testando a força, resistência, velocidade e habilidade dos atletas.

O Open é conhecido por sua natureza inclusiva, pois atletas de todos os níveis de habilidade e idades podem participar.
Além disso, o Open é uma oportunidade para os competidores se desafiarem, estabelecerem metas pessoais e fazerem parte da comunidade global do CrossFit.

Ao final das cinco semanas, os resultados são tabulados e os melhores atletas de cada categoria (individual, times, idade etc.)
avançam para as próximas etapas das competições CrossFit Games, onde competirão contra os melhores do mundo em busca do título de "Fittest on Earth" (Mais em Forma da Terra).
"""

c1, c2 = st.columns(2)

c1.markdown(texto)

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

