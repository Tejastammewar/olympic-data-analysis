import streamlit as st
import pandas as pd

import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympic Analysis")

user_menu=st.sidebar.radio(
    'Select an Option ',
    ('medal tally','Overall Analysis','Country-wise Analysis','Map-Analysis')
)
# st.dataframe(df)

if user_menu=="medal tally":
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select year",years)
    selected_country=st.sidebar.selectbox("Select country",country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    if selected_year!='Overall' and selected_country=='Overall':
        st.title("Medal Tally in "+str(selected_year)+" Olympics ")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country+ "'s overall performance " )
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country+" performance in "+str(selected_year)+" Olympics")
    st.table(medal_tally)

if user_menu=="Overall Analysis":

    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    somenew = helper.data_over_time(df)
    fig=px.line(somenew,x='No of countries',y='count')
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='No of countries')
    st.title("Participating nations")
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time1(df)
    fig=px.line(events_over_time,x="No of events",y='count')
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='No of events')
    st.title('Events over the years')
    st.plotly_chart(fig)

    athlete_over_time=helper.data_over_time2(df)
    fig=px.line(athlete_over_time,x="No of events",y='count')
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='No of athletes')
    st.title('Athletes over the years')
    st.plotly_chart(fig)

    st.title("Number of events over time(Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

# st.title("Most Successful Athletes")
# sport_list=df['Sport'].unique().tolist()
# sport_list.sort()
# sport_list.insert(0,'Overall')

# selected_sport=st.selectbox('Select a sport',sport_list)
# x=helper.most_successful(df,selected_sport)
# st.table(x)

if user_menu=="Country-wise Analysis":

    st.sidebar.title('Country wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('Select a country',country_list)

    country_df=helper.year_wise_medal_count(df,selected_country)
    fig=px.line(country_df,x="Year",y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    country_map=helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax=sns.heatmap(country_map,annot=True)
    st.pyplot(fig)

    st.title("Top atheletes of "+selected_country)
    top10df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10df)

if user_menu=="Map-Analysis":
    # def medal_tally(df):
    #     medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    #     medal_tally=medal_tally.groupby('Team').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    #     medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    #     medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    #     medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    #
    #
    #     medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    #     medal_tally['total'] = medal_tally['total'].astype('int')
    #
    #
    #     return medal_tally

    def medal_tally(df):
        # Drop duplicates based on specified columns
        medal_tally = df.drop_duplicates(
            subset=['ID', 'Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

        # Group by 'Team' and count the medals
        medal_counts = medal_tally.groupby('Team')['Medal'].value_counts().unstack(fill_value=0)

        # Reset index to make 'Team' a regular column
        medal_counts.reset_index(inplace=True)

        # Rename columns for clarity
        medal_counts.columns.name = None

        # Calculate total medals
        medal_counts['Total'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']

        return medal_counts


    def calculate_medal_count(data):
        medal_counts = data.groupby('Team').sum()[['Gold', 'Silver', 'Bronze']].reset_index()
        medal_counts['Total'] = medal_counts[['Gold', 'Silver', 'Bronze']].sum(axis=1)
        return medal_counts


    def create_choropleth_map(data, title):
        fig = px.choropleth(data, locations='Team', locationmode='country names',
                            color='Total', hover_name='Team',
                            projection='natural earth', title=title)
        return fig


    athlete_events_df = pd.read_csv('athlete_events.csv')
    world_data_df = pd.read_excel('world_values.xlsx')
    athlete_events_df = pd.merge(athlete_events_df, world_data_df[['latitude', 'longitude', 'country']], left_on='Team',
                                 right_on='country', how='left')
    athlete_events_df.drop(columns='country', inplace=True)
    st.write(athlete_events_df.columns)

    # Calculate medal counts
    x=medal_tally(athlete_events_df)
    st.write(x.columns)
    st.write(x)
    medal_counts_df = calculate_medal_count(x)

    # Create the choropleth map
    map_title = 'Geographical Distribution of Olympic Medal Counts'
    fig = create_choropleth_map(medal_counts_df, map_title)

    # Show the map
    st.plotly_chart(fig)







