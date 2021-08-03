import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
df = df.sort_values(['Confirmed'], ascending=False)


st.title('COVID-19 Dashboard For India')
st.markdown('The dashboard will visualize the Covid-19 situation in India')
st.markdown('Coronavirus disease (COVID-19) is an infectious disease caused\
by a newly discovered coronavirus.')

st.image('https://www.emeraldgrouppublishing.com/sites/default/files/image/covid-cells.jpg')

st.markdown('Most people infected with the COVID-19 virus will experience mild\
to moderate respiratory illness and recover without requiring special treatment. \
Older people, and those with underlying medical problems like cardiovascular disease,\
diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness.')

l=['Confirmed','Recovered','Deaths','Active']
colors=['Chocolate','Crimson','ForestGreen','SpringGreen']
#'Cyan','DarkOrchid','Indigo','SeaGreen'
row1=st.beta_columns(4)
for i in range(4):
    row1[i].markdown(f'<h1 style="color:{colors[i]};font-size:24px;"><u>{l[i]}</u></h1>', unsafe_allow_html=True)
row2 = st.beta_columns(4)
row2[0].markdown(f'<h1 style="color:{colors[0]};font-size:24px;"><u>{df.Confirmed[0]}</u></h1>', unsafe_allow_html=True)
row2[1].markdown(f'<h1 style="color:{colors[1]};font-size:24px;"><u>{df.Recovered[0]}</u></h1>', unsafe_allow_html=True)
row2[2].markdown(f'<h1 style="color:{colors[2]};font-size:24px;"><u>{df.Deaths[0]}</u></h1>', unsafe_allow_html=True)
row2[3].markdown(f'<h1 style="color:{colors[3]};font-size:24px;"><u>{df.Active[0]}</u></h1>', unsafe_allow_html=True)




# All india line chart
second_df = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
#second_df
second_df_active = second_df[['Date','Daily Confirmed']]
#second_df_active
fig = px.line(x=second_df_active.Date, y=second_df_active["Daily Confirmed"])
st.plotly_chart(fig)



st.sidebar.title('Visualization Selector')
st.sidebar.markdown('Select the Plots/Charts accordingly:')

plots = ['Bar Plot', 'Pie Chart']
select = st.sidebar.selectbox('Visualization Type', plots, key='1')
if not st.sidebar.checkbox('Hide', True, key='2'):
    if select == 'Pie Chart':
        st.title('Selected top 5 cities')
        fig = px.pie(df, values=df['Confirmed'][1:6], names=df['State'][1:6], title='Total confirmed cases')
        st.plotly_chart(fig)
    if select == 'Bar Plot':
        st.title('Selected top 5 cities')
        fig = go.Figure(data=[
            go.Bar(name='Confirmed', x=df['State'][1:6], y=df['Confirmed'][1:6]),
            go.Bar(name='Recovered', x=df['State'][1:6], y=df['Recovered'][1:6]),
            go.Bar(name='Active', x=df['State'][1:6], y=df['Active'][1:6])
            ])
        st.plotly_chart(fig)


state_select = st.sidebar.selectbox('Select a state:', df['State'][1:-1])
status_select = st.sidebar.radio('Covid-19 patient status', ('Confirmed Cases', 'Active Cases', 'Recovered Cases', 'Death Cases'))
st.write('## **State Level Analysis**')
selected_state = df[df['State']==state_select]

def get_total_df(df):
    total_df = pd.DataFrame({
        'Status':['Confirmed','Recovered','Deaths','Active'],
        'Number of Cases':(df.iloc[0]['Confirmed'],df.iloc[0]['Recovered'],df.iloc[0]['Deaths'],df.iloc[0]['Active'])
        })
    return total_df

state_total = get_total_df(selected_state)
fig = px.bar(state_total, x = 'Status', y = 'Number of Cases', color='Status')
st.plotly_chart(fig)
#if select == 'Pie Chart':
if status_select == 'Confirmed Cases':
    st.title('Total Confirmed Cases')
    fig = px.pie(df, values=df['Confirmed'][1:-1], names=df['State'][1:-1])
    st.plotly_chart(fig)
elif status_select == 'Recovered Cases':
    st.title('Total Recovered Cases')
    fig = px.pie(df, values=df['Recovered'][1:-1], names=df['State'][1:-1])
    st.plotly_chart(fig)
elif status_select == 'Active Cases':
    st.title('Total Active Cases')
    fig = px.pie(df, values=df['Active'][1:-1], names=df['State'][1:-1])
    #fig = go.Figure(data=[go.Pie(labels=df['State'], values=df['Active'])])
    st.plotly_chart(fig)
elif status_select == 'Death Cases':
    st.title('Total Death Cases')
    fig = px.pie(df, values=df['Deaths'][1:-1], names=df['State'][1:-1])
    st.plotly_chart(fig)


# 
