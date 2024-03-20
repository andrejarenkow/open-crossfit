import pandas as pd
import plotly.express as px
import requests
import numpy as np
import streamlit as st
from ridgeplot import ridgeplot

# Configurações da página
st.set_page_config(
    page_title="Open Crossfit",
    page_icon="	:weight_lifter:",
    layout="wide",
    initial_sidebar_state='expanded'
) 
col1, col2, col3 = st.columns([1,4,1])

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )


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

pais = st.selectbox('Selecione o país', options=sorted(df['country'].unique()), index=17)
cidade = st.multiselect('Selecione a cidade', options=df[df['country']==pais]['city'].unique(), default = ['PORTO ALEGRE', 'CAXIAS DO SUL'])
categoria = st.multiselect('Selecione quais categorias você quer comparar', ['Foundations', 'Scale', 'RX'], ['RX'])
                      

df_afiliados_cidade = df[df['city'].isin(cidade)]
lista_afiliados = sorted(df_afiliados_cidade['name'].values)


# Limpeza e tratamento dos dados
dados = pd.read_parquet('dados_crossfit.parquet')
dados['age'] = pd.to_numeric(dados['age'], errors='coerce')
dados['score_1'] = pd.to_numeric(dados['score_1'], errors='coerce')
dados['score_2'] = pd.to_numeric(dados['score_2'], errors='coerce')

# Score 24.1
dados_fizeram_1 = dados[dados['score_1']>0].reset_index(drop=True)
scores = dados_fizeram_1['scoreDisplay_1'].str.split(' reps', expand=True)[0].str.replace(' - s','').str.replace(' - f','')
dados_fizeram_1['scaled_descrito'] = dados_fizeram_1['scaled_1'].replace({'0':'RX', '1':'Scale', '2':'Foundations'})
segundos = []
for i in scores:
  #print(i)
  if len(i.split(':'))>1:
    score = int(i.split(':')[0])*60+int(i.split(':')[1])

  else:
    score = (180-int(i))*3+15*60

  segundos.append(score)

dados_fizeram_1['score_segundos'] = segundos

# Definindo a função para criar o array que vai no gráfico
def valores_array_box(nome_box, categoria):
  scores = pd.Series(dados_fizeram_1[(dados_fizeram_1['affiliateName']==nome_box)&(dados_fizeram_1['scaled_descrito'].isin(categoria))]['score_segundos'], name=nome_box).to_numpy()

  return scores

# Criar uma lista para botar o samples do Ridgeplot
lista_samples = []
lista_nomes_afiliados_selecionados = []

for afiliado in lista_afiliados:
  scores_afiliado = valores_array_box(afiliado, categoria)
  if len(scores_afiliado)>2:
    lista_samples.append(scores_afiliado)
    mediana = int(np.median(scores_afiliado))
    inscritos = len(scores_afiliado)
    lista_nomes_afiliados_selecionados.append(f'{afiliado}')# - Mediana {mediana} reps - {inscritos} atletas')


# Not only does 'ridgeplot(...)' come configured with sensible defaults
# but is also fully configurable to your own style and preference!
fig_1 = ridgeplot(
    samples=lista_samples,
    #bandwidth=4,
    kde_points=np.linspace(0, 1300, 500),
    colorscale="viridis",
    colormode="row-index",
    coloralpha=0.8,
    labels=lista_nomes_afiliados_selecionados,
    linewidth=2,
    spacing=0.5,
)

# Again, update the figure layout to your liking here
fig_1.update_layout(
    title="WOD 24.1",
    height=1000,
    width=400,
    plot_bgcolor="rgba(255, 255, 255, 0.0)",
    xaxis_gridcolor="rgba(0, 0, 0, 0.1)",
    yaxis_gridcolor="rgba(0, 0, 0, 0.1)",
    yaxis_title="Nome do box",
    xaxis_title="Tempo (segundos)",
    showlegend=False
)



# Score 24.2
dados_fizeram_2 = dados[dados['score_2']>0].reset_index(drop=True)
scores = dados_fizeram_2['scoreDisplay_2'].str.split(' reps', expand=True)[0].str.replace(' - s','').str.replace(' - f','')
dados_fizeram_2['score_reps'] = pd.to_numeric(scores)
dados_fizeram_2['scaled_descrito_2'] = dados_fizeram_2['scaled_2'].replace({'0':'RX', '1':'Scale', '2':'Foundations'})

# Plotando 24.2
# Definindo a função para criar o array que vai no gráfico
def valores_array_box(nome_box, categoria):
  scores = pd.Series(dados_fizeram_2[(dados_fizeram_2['affiliateName']==nome_box)&(dados_fizeram_2['scaled_descrito_2'].isin(categoria))]['score_reps'], name=nome_box).to_numpy()

  return scores

# Criar uma lista para botar o samples do Ridgeplot
lista_samples = []
lista_nomes_afiliados_selecionados = []

#categoria = 'RX'

for afiliado in lista_afiliados:
  scores_afiliado = valores_array_box(afiliado, categoria)
  if len(scores_afiliado)>2:
    lista_samples.append(scores_afiliado)
    mediana = int(np.median(scores_afiliado))
    inscritos = len(scores_afiliado)
    lista_nomes_afiliados_selecionados.append(f'{afiliado}')# - Mediana {mediana} reps - {inscritos} atletas')


# Not only does 'ridgeplot(...)' come configured with sensible defaults
# but is also fully configurable to your own style and preference!
fig_2 = ridgeplot(
    samples=lista_samples,
    #bandwidth=4,
    kde_points=np.linspace(0, 1300, 500),
    colorscale="viridis",
    colormode="row-index",
    coloralpha=0.8,
    labels=lista_nomes_afiliados_selecionados,
    linewidth=2,
    spacing=0.5,
)

# Again, update the figure layout to your liking here
fig_2.update_layout(
    title="WOD 24.2",
    height=1000,
    width=400,
    plot_bgcolor="rgba(0, 255, 255, 0.0)",
    xaxis_gridcolor="rgba(0, 0, 0, 0.1)",
    yaxis_gridcolor="rgba(0, 0, 0, 0.1)",
    #yaxis_title="Nome do box",
    xaxis_title="Repetições",
    showlegend=False
)

# 24.3
dados['score_3'] = pd.to_numeric(dados['score_3'])
dados_fizeram_3 = dados[dados['score_3']>0].reset_index(drop=True)

scores = dados_fizeram_3['scoreDisplay_3'].str.split(' reps', expand=True)[0].str.replace(' - s','').str.replace(' - f','')
segundos = []
for i in scores:
  #print(i)
  if len(i.split(':'))>1:
    score = int(i.split(':')[0])*60+int(i.split(':')[1])

  else:
    score = (180-int(i))*3+15*60

  segundos.append(score)

dados_fizeram_3['score_segundos'] = segundos

dados_fizeram_3['Taura'] = ['Taura' if affiliate == 'Taura CrossFit' else 'Outros' for affiliate in dados_fizeram_3['affiliateName']]
dados_fizeram_3['scaled_descrito_3'] = dados_fizeram_3['scaled_3'].replace({'0':'RX', '1':'Scale', '2':'Foundations'})

# Definindo a função para criar o array que vai no gráfico
def valores_array_box(nome_box, categoria):
  scores = pd.Series(dados_fizeram_3[(dados_fizeram_3['affiliateName']==nome_box)&(dados_fizeram_3['scaled_descrito_3'].isin(categoria))]['score_segundos'], name=nome_box).to_numpy()

  return scores

# Criar uma lista para botar o samples do Ridgeplot
lista_samples = []
lista_nomes_afiliados_selecionados = []


for afiliado in lista_afiliados:
  scores_afiliado = valores_array_box(afiliado, categoria)
  if len(scores_afiliado)>2:
    lista_samples.append(scores_afiliado)
    mediana = int(np.median(scores_afiliado))
    inscritos = len(scores_afiliado)
    lista_nomes_afiliados_selecionados.append(f'{afiliado}')# - Mediana {mediana} segundos - {inscritos} atletas')


# Not only does 'ridgeplot(...)' come configured with sensible defaults
# but is also fully configurable to your own style and preference!
fig_3 = ridgeplot(
    samples=lista_samples,
    #bandwidth=4,
    kde_points=np.linspace(750, 1500, 500),
    colorscale="viridis",
    colormode="row-index",
    coloralpha=0.8,
    labels=lista_nomes_afiliados_selecionados,
    linewidth=2,
    spacing=0.5,
)

# Again, update the figure layout to your liking here
fig_3.update_layout(
    title=f"WOD Open 24.3",
    height=1000,
    width=400,
    plot_bgcolor="rgba(255, 255, 255, 0.0)",
    xaxis_gridcolor="rgba(0, 0, 0, 0.1)",
    yaxis_gridcolor="rgba(0, 0, 0, 0.1)",
    #yaxis_title="Nome do box",
    xaxis_title="Tempo (segundos)",
    showlegend=False
)

# Show us the work!
st.subheader(f'Comparativo Open 2024, Categorias {categoria}, {cidade}')
col1, col2, col3 = st.columns(3)
col1.plotly_chart(fig_1)
col2.plotly_chart(fig_2)
col3.plotly_chart(fig_3)
