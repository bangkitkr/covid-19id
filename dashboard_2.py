# Kita akan mulai dengan mengimpor beberapa library penting yang akan kita gunakan
import matplotlib matplotlib.use('Agg')
from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Membangun aplikasi dashboard
st.title("Dashboard COVID-19 di Indonesia")
st.write("Ini menunjukan ***kasus Virus Corona*** di Indonesia")
image = Image.open("Corona.jpeg")
st.image(image, width=500)
st.markdown("Dashboard akan memvisualisasikan Situasi Covid-19 di Indonesia")
st.markdown("Penyakit coronavirus (COVID-19) adalah penyakit menular yang disebabkan oleh coronavirus yang baru ditemukan. Sebagian besar orang yang terinfeksi virus COVID-19 akan mengalami penyakit pernapasan ringan hingga sedang dan sembuh tanpa memerlukan perawatan khusus.")
st.markdown('<style>body{background-color: lightblue}</style>', unsafe_allow_html=True)

# Import Dataset
@st.cache
def load_data():
    df = pd.read_csv("state_wise.csv")
    return df

df = load_data()

visualization = st.sidebar.selectbox('Select a Chart type',('Bar Chart', 'Pie Chart', 'Line Chart'))
state_select = st.sidebar.selectbox('Select a state', df['Location'].unique())
selected_state = df[df['Location'] == state_select]
st.title('Analisis tingkat lokasi')

def get_total_dataframe(df):
    total_dataframe = pd.DataFrame({
        'Status':['Total Kasus', 'Total Sembuh', 'Total Kematian', 'Total Kasus Aktif'],
        'Number of cases': (df.iloc[0]['Total Cases'],
                            df.iloc[0]['Total Recovered'],
                            df.iloc[0]['Total Deaths'],
                            df.iloc[0]['Total Active Cases'])
    })
    return total_dataframe

state_total = get_total_dataframe(selected_state)
if visualization == 'Bar Chart':
    state_total_graph = px.bar(state_total, x='Status', y='Number of cases',
                               labels={'Number of cases': 'Jumlah kasus di %s' % (state_select)}, color='Status')
    st.plotly_chart(state_total_graph)
elif visualization == 'Pie Chart':
    status_select = st.sidebar.radio('Covid-19 patient status', ('Total Kasus', 'Total Sembuh', 'Total Kematian', 'Total Kasus Aktif'))
    if status_select == 'Total Cases':
        st.markdown('## **Total Kasus**')
        fig = px.pie(df, values=df['Total Cases'][:5], names=df['Location'][:5])
        st.plotly_chart(fig)
    elif status_select == 'Total Active Cases':
        st.markdown('## **Total Kasus Aktif**')
        fig = px.pie(df, values=df['Total Active Cases'][:5], names=df['Location'][:5])
        st.plotly_chart(fig)
    elif status_select == 'Total Deaths':
        st.markdown('## **Total Kasus Kematian**')
        fig = px.pie(df, values=df['Total Deaths'][:5], names=df['Location'][:5])
        st.plotly_chart(fig)
    else:
        st.markdown('## **Total Kasus Sembuh**')
        fig = px.pie(df, values=df['Total Recovered'][:5], names=df['Location'][:5])
        st.plotly_chart(fig)
elif visualization == 'Line Chart':
    status_select = st.sidebar.radio('Covid-19 patient status', ('Total Cases', 'Total Recovered', 'Total Deaths', 'Total Active Cases'))
    if status_select == 'Total Cases':
        st.markdown('## **Total Kasus terkonfirmasi**')
        fig = px.line(df, x=df['Total Cases'], y=df['Location'])
        st.plotly_chart(fig)
    elif status_select == 'Total Active Cases':
        st.markdown('## **Total Kasus aktif**')
        fig = px.line(df, x=df['Total Active Cases'], y=df['Location'])
        st.plotly_chart(fig)
    elif status_select == 'Total Deaths':
        st.markdown('## **Total Kasus Kematian**')
        fig = px.line(df, x=df['Total Deaths'], y=df['Location'])
        st.plotly_chart(fig)
    else:
        st.markdown('## **Total Kasus Sembuh**')
        fig = px.line(df, x=df['Total Recovered'], y=df['Location'])
        st.plotly_chart(fig)

def get_table():
    datatable = df[['Location', 'Total Cases', 'Total Recovered', 'Total Deaths', 'Total Active Cases']].sort_values(by=['Total Cases'],
                ascending=False)
    return datatable

datatable = get_table()
st.dataframe(datatable)
