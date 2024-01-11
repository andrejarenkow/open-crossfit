import pandas as pd
import seaborn as sns
import plotly.express as px
import requests
import numpy as np

# Configurações da página
st.set_page_config(
    page_title="Ovitrampas",
    page_icon="	:bug:",
    layout="wide",
    initial_sidebar_state='collapsed'
) 
col1, col2, col3 = st.columns([1,4,1])

#col1.image('logo_cevs (1).png', width=200)
col2.header('Open Crossfit')
#col3.image('logo_estado (3).png', width=300)
