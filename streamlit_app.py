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
    initial_sidebar_state='collapsed'
) 
col1, col2, col3 = st.columns([1,4,1])

#col1.image('logo_cevs (1).png', width=200)
col2.header('Open Crossfit 24')
#col3.image('logo_estado (3).png', width=300)
