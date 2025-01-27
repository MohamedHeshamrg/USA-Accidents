import streamlit as st
import plotly.express as px 
import pandas as pd


st.set_page_config(
    layout="wide",
    page_title='US-Accidents Home Page',
    page_icon='🚗🚨'
)



url = "https://raw.githubusercontent.com/MohamedHeshamrg/USA-Accidents/c9d2ccc55db9f9a747b3208d1c74dd08edef0d16/multipage/sample.csv"
df = pd.read_csv(url, encoding='utf-8')


num_stats = df.describe()
cat_stats = df.describe(include='O')

# Sidebar
st.sidebar.success('Select page above')
st.markdown('<h1 style="text-align: center; color: cyan;">Home Page For US-Accidents Dash Board</h1>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🗓️ Data", '📈 Descriptive Stats'])

with tab1:
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown('<h3 style="text-align: center; color: MediumAquaMarine;">Dataset</h3>', unsafe_allow_html=True)
        st.dataframe(df.head(2000), height=800)

with tab2:
    col1, col2, col3 = st.columns([6, 0.5, 6])
    with col1:
        st.subheader('Numerical Descriptive Statistics')
        st.dataframe(num_stats.T, height=500)

    with col3:
        st.subheader('Categorical Descriptive Statistics')
        st.dataframe(cat_stats.T, height=800)
