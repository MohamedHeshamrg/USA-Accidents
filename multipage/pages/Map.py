import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
        layout = 'wide',
        page_title = 'Map DashBoard',
        page_icon= '🗺️'
)



@st.cache_data
def load_data():
    return pd.read_csv(r"..\sample.csv")  # or "../sample.csv"

df = load_data()

    
    
with st.container():
        col1, col2, col3 = st.columns([2,8,2])
        fig = px.scatter_map(df, lat="start_lat", lon="start_lng", color="severity",
                  color_continuous_scale=px.colors.sequential.deep,
                  map_style="carto-positron")


        col2.plotly_chart(fig, use_container_width= True)
        
        

with st.container():
        col4, col5, col6 = st.columns([1,9,1])
        fig = px.scatter_geo(df,lat = 'start_lat',lon='start_lng' , color="severity",
               animation_frame="year", projection="natural earth",color_continuous_scale=px.colors.sequential.deep)
        col5.plotly_chart(fig, use_container_width= True)

