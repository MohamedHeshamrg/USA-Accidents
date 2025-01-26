import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
        layout = 'wide',
        page_title = 'DashBoard',
        page_icon= '📊'
)

tab1, tab2 = st.tabs(['📊  Univariate Analysis','📈 Bi/multi-variate Analysis '])



url = "https://raw.githubusercontent.com/MohamedHeshamrg/USA-Accidents/c9d2ccc55db9f9a747b3208d1c74dd08edef0d16/multipage/sample.csv"
df = pd.read_csv(url, encoding='utf-8')


with tab1:
    st.markdown('<h3 style="text-align: center; color : MediumAquaMarine;">Distribution of Numerical features</h3>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([5,1,5])
        col= col1.selectbox('select location feature to see its distribution',
                      ["state", "county","street",'timezone'], key=10)
        data_accident = df[col].value_counts()
        data_accident = pd.DataFrame(data_accident)
        data_accident.reset_index(inplace=True)
        fig = px.bar(data_accident[:15],y=col, x = 'count'
                ,color_discrete_sequence= px.colors.sequential.deep)
        
        col1.plotly_chart(fig, use_container_width= True)
        options = ['year','season','month','day','day_name','hour']
        col= col3.selectbox('select Time distribution', options, key=9)
        time_trends = df[col].value_counts().sort_index()
        time_trends = pd.DataFrame(time_trends).reset_index()
        time_trends.columns = [col, 'count'] 

        fig = px.bar(time_trends, x=col, y='count', color_discrete_sequence=px.colors.sequential.deep)

        col3.plotly_chart(fig, use_container_width= True)
        
        st.write('<h3 style="text-align: center; color : MediumAquaMarine;">Road features with filters</h3>', unsafe_allow_html=True)

    with st.container():
        col4, col5, col6 = st.columns([6,1,6])
        # sum the occurrences of each feature
        bump_sum = df['bump'].sum()
        crossing_sum = df['crossing'].sum()
        give_way_sum = df['give_way'].sum()
        junction_sum = df['junction'].sum()
        no_exit_sum = df['no_exit'].sum()
        railway_sum = df['railway'].sum()
        roundabout_sum = df['roundabout'].sum()
        station_sum = df['station'].sum()
        stop_sum = df['stop'].sum()
        traffic_calming_sum = df['traffic_calming'].sum()
        traffic_signal_sum = df['traffic_signal'].sum()
        turning_loop_sum = df['turning_loop'].sum()

    # Create a dictionary to store the sums
        d = {"columns":['bump','crossing','give_way','junction','no_exit','railway','roundabout','station','stop','traffic_calming'
                        ,'traffic_signal','turning_loop'],
         "sum" : [bump_sum,crossing_sum,give_way_sum,junction_sum,no_exit_sum,railway_sum,roundabout_sum,station_sum,stop_sum,traffic_calming_sum
                  ,traffic_signal_sum,turning_loop_sum]

            }

        road_df = pd.DataFrame(data=d).reset_index()
        fig = px.pie(road_df, names='columns', values='sum', color_discrete_sequence=px.colors.sequential.deep)
        col4.plotly_chart(fig, use_container_width=True)

        # col6
        
        fig= px.histogram(road_df, x='columns', y='sum', color_discrete_sequence=px.colors.sequential.deep)
        col6.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        col7, col8, col9 = st.columns([6,1,6])
        
        data_accident = df["weather_condition"].value_counts()
        data_accident = pd.DataFrame(data_accident)
        data_accident.reset_index(inplace=True)
        fig = px.bar(data_accident[:15],y='weather_condition', x = 'count'
                ,color_discrete_sequence= px.colors.sequential.deep,title = 'Distribution of weather_condition')

        col7.plotly_chart(fig, use_container_width=True)

        fig = px.histogram(df,x = 'severity',title='Distribution Severity levels',
             color_discrete_sequence= px.colors.sequential.deep)
        
        col9.plotly_chart(fig, use_container_width=True)
    with st.container():
        col10, col11, col21 = st.columns([3,6,3])
        col= col11.selectbox('select sunrise_sunset or twiligh feature to see its distribution',
                      ["sunrise_sunset", "twiligh"], key=8)
        if col == "sunrise_sunset" :
            sunrise_sunset_trends = df['sunrise_sunset'].value_counts().reset_index()
            fig = px.bar(sunrise_sunset_trends,x='sunrise_sunset',y = 'count',barmode="group", title= 'sunrise_sunset_count of accident in this time',
                           color_discrete_sequence=px.colors.sequential.deep)
            col11.plotly_chart(fig, use_container_width=True) 
        elif col == "twiligh":
            twilight_trends = df[['civil_twilight', 'nautical_twilight', 'astronomical_twilight']].melt()
            twilight_counts = twilight_trends['value'].value_counts().reset_index()
            fig = px.bar(twilight_counts,x='value',y = 'count',barmode="group", title= 'twilight_count of accident in this time',
                       color_discrete_sequence=px.colors.sequential.deep)
            col11.plotly_chart(fig, use_container_width=True) 

with tab2:
    st.markdown('<h3 style="text-align: center; color : MediumAquaMarine;">Correlation between Severity and Weather factors </h3>', unsafe_allow_html=True)
    
    # dist part
    with st.container():
        col1, col2, col3=st.columns([5,1,5])
        df_weather = df[['temperature(f)','humidity(%)', 'pressure(in)', 'wind_speed(mph)','severity']]
        fig= px.imshow(df_weather.corr()
                   ,color_continuous_scale=px.colors.sequential.deep)
        
        col1.plotly_chart(fig, use_container_width=True)
        
        col= col3.selectbox('select Weather factors feature to see its correlation with severity levels',
                      ['temperature(f)','humidity(%)', 'pressure(in)', 'wind_speed(mph)'], key=7)
        see = col3.radio('Select  Severity Level',[1,2,3,4,'ALL'], key=6, horizontal=True)
        data_accident = df.groupby([col,'severity']).agg({'severity':'count'})
        data_accident.reset_index(level = col , inplace = True )
        data_accident.index = data_accident.index.rename("new_data")
        data_accident.reset_index(inplace = True)
        data_accident.columns = ["severity",col,'count_of_severity']
        if see in [1,2,3,4]:
    
            fig = px.scatter(data_accident[data_accident['severity'] == see],y='count_of_severity', x= col ,marginal_x="box"
                        ,color='severity',title=f'Correlation of {col} and severity',color_continuous_scale=px.colors.sequential.deep)
            col3.plotly_chart(fig, use_container_width=True)

        elif see == 'ALL':
            fig = px.scatter(data_accident,y='count_of_severity', x= col ,marginal_x="box"
                        ,color='severity',title=f'Correlation of {col} and severity',color_continuous_scale=px.colors.sequential.deep)
            col3.plotly_chart(fig, use_container_width=True)
            
        st.write('<h3 style="text-align: center; color : Change in the number of accidents;"></h3>', unsafe_allow_html=True)

    with st.container():
        col1,col2,col3= st.columns([2,8,2])
        #col1
        col= col2.selectbox('select location feature to see Change in the number of accidents by years',
                      ["state", "county","street",'timezone'], key=5)
        
        if col == "state":
            
            see= col1.selectbox(f'select the {col} :',
                      df['state'].unique(), key=30) 
            data_accident = df.groupby([col, 'severity', 'year']).size().reset_index(name='count_of_severity')

            # Rename columns for clarity
            data_accident.columns = [col, 'severity', 'year', 'count_of_severity']
            data_accident = data_accident[data_accident[col] == see].sort_values(by = 'year')
            # line plot 
            fig = px.line(data_accident, y = 'count_of_severity',x = 'year',color = 'severity')

            col2.plotly_chart(fig, use_container_width=True)
            
        elif col == "county":
            see= col1.selectbox(f'select the {col} :',
                      df["county"].unique(), key=31)
            data_accident = df.groupby([col, 'severity', 'year']).size().reset_index(name='count_of_severity')

            # Rename columns for clarity
            data_accident.columns = [col, 'severity', 'year', 'count_of_severity']
            data_accident = data_accident[data_accident[col] == see].sort_values(by = 'year')
            # line plot 
            fig = px.line(data_accident, y = 'count_of_severity',x = 'year',color = 'severity')
            col2.plotly_chart(fig, use_container_width=True)

        elif col == "street":
            see= col1.selectbox(f'select the {col} :',
                      df["street"].unique(), key=32)
            data_accident = df.groupby([col, 'severity', 'year']).size().reset_index(name='count_of_severity')

            # Rename columns for clarity
            data_accident.columns = [col, 'severity', 'year', 'count_of_severity']
            data_accident = data_accident[data_accident[col] == see].sort_values(by = 'year')
            # line plot 
            fig = px.line(data_accident, y = 'count_of_severity',x = 'year',color = 'severity')
            col2.plotly_chart(fig, use_container_width=True)

        elif col == "timezone":
            see= col1.selectbox(f'select the {col} :',
                      df['timezone'].unique(), key=33)
            data_accident = df.groupby([col, 'severity', 'year']).size().reset_index(name='count_of_severity')

            # Rename columns for clarity
            data_accident.columns = [col, 'severity', 'year', 'count_of_severity']
            data_accident = data_accident[data_accident[col] == see].sort_values(by = 'year')
            # line plot 
            fig = px.line(data_accident, y = 'count_of_severity',x = 'year',color = 'severity')
            col2.plotly_chart(fig, use_container_width=True)
    with st.container():
        col1,col2,col3= st.columns([2,8,2])
        data_accident = df.groupby(['timezone','state', 'severity', 'year']).size().reset_index(name='count_of_severity')
        data_accident.columns = ["timezone","state", 'severity', 'year', 'count_of_accident_by_severity']
        sum_of_count = data_accident['count_of_accident_by_severity'].sum()
        data_accident['persentage'] = data_accident['count_of_accident_by_severity'].apply(lambda x : x/sum_of_count*100)
        
        fig = px.sunburst(data_accident,path = ['year','timezone','state','severity'],values='count_of_accident_by_severity'
                          ,color = 'persentage',color_continuous_scale=px.colors.sequential.deep)
        col2.plotly_chart(fig, use_container_width=True)
            
            
        
 



        
