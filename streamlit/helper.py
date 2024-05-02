import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px


def fetch_medal_tally(df, years, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if years == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if years == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if years != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(years)]
    if years != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(years))]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x
# def medal_tally(df):
#     medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
#     medal_tally=medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
#
#     medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
#
#     medal_tally['Gold']=medal_tally['Gold'].astype('int')
#     medal_tally['Silver'] = medal_tally['Silver'].astype('int')
#     medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
#     medal_tally['total'] = medal_tally['total'].astype('int')
#     return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years = [int(year) for year in years]
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df):
    value_counts_res=df.drop_duplicates(['Year','region'])['Year'].value_counts()
    value_counts_df = value_counts_res.reset_index()
    nati = value_counts_df.rename(columns={'index': 'Edition', 'Year': 'No of countries'})
    new_df = nati.sort_values('count')
    # nations_overtime=df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index()
    # nationsnew= nations_overtime.rename(columns={'index': 'Edition', 'Year': 'No of countries'})
    return new_df

def data_over_time1(df):
    value_counts_res=df.drop_duplicates(['Year','Event'])['Year'].value_counts()
    value_counts_df = value_counts_res.reset_index()
    nati = value_counts_df.rename(columns={'index': 'Edition', 'Year': 'No of events'})
    new_df = nati.sort_values('count')
    return new_df

def data_over_time2(df):
    value_counts_res=df.drop_duplicates(['Year','Name'])['Year'].value_counts()
    value_counts_df = value_counts_res.reset_index()
    nati = value_counts_df.rename(columns={'index': 'Edition', 'Year': 'No of events'})
    new_df = nati.sort_values('count')
    return new_df

# def most_successful(df,sport):
#     temp_df=df.dropna(subset=["Medal"])
#     if sport != "Overall":
#         temp_df=temp_df[temp_df["Sport"]==sport]
#     x= temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
#     x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
#     return x

def year_wise_medal_count(df,country):
    # removing null from medal
    tem_df = df.dropna(subset=['Medal'])

    # if its a team sport only 1 medal should be counted
    tem_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = tem_df[tem_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import seaborn as sns
import matplotlib.pyplot as plt

def country_event_heatmap(df,country):
    tem_df = df.dropna(subset=['Medal'])
    # if its a team sport only 1 medal should be counted
    tem_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = tem_df[tem_df['region'] == country]
    pt=new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df,country):
    temp_df = df[df['region'] == country]
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df[temp_df["region"] == country]
    temp_df_unique = temp_df.drop_duplicates(subset=['Name'])
    x=temp_df_unique['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'Sport']].drop_duplicates('Name')
    # streamlit.write(x.head())
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x
#
# athlete_events_df = pd.read_csv('athlete_events.csv')
# world_data_df = pd.read_excel('world_values.xlsx')
# athlete_events_df = pd.merge(athlete_events_df, world_data_df[['latitude', 'longitude', 'country']], left_on='Team', right_on='country', how='left')
# athlete_events_df.drop(columns='country', inplace=True)
# st.write(athlete_events_df.columns)
#
# def calculate_medal_count(data):
#     medal_counts = data.groupby('Team')['Medal'].count().reset_index(name='Medal_Count')
#     return medal_counts
#
# # Calculate medal counts
# medal_counts_df = calculate_medal_count(athlete_events_df)
# st.write(medal_counts_df)
# medal_counts_df_merged=pd.merge(athlete_events_df, medal_counts_df[['Team', 'Medal_Count']], left_on='Team', right_on='Team', how='left')
# st.write(medal_counts_df_merged)
# def create_choropleth_map(data, title):
#     fig = px.scatter_geo(data, lat='latitude', lon='longitude', color='Medal_Count',
#                          hover_name='Team', size='Medal_Count',
#                          projection='natural earth', title=title)
#     return fig
#
#
# # Create the choropleth map
# map_title = 'Geographical Distribution of Olympic Medal Counts'
# fig = create_choropleth_map(medal_counts_df_merged, map_title)
#
# # Show the map
# fig.show()