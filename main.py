import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# load the dataset
data = pd.read_csv('data/Summer_olympic_Medals.csv')

# create the header on web app
st.subheader('Summer Olympic Medal Tally Dashboard')

# create filters for user based on year and countries
year = st.selectbox('Select Year', sorted(data['Year'].unique()))

# country filter
country = st.multiselect('Select Country', sorted(data['Country_Name'].unique()))

# apply the filters to the data 
filtered_data = data[(data['Year'] == year)]

if country:
    filtered_data = filtered_data[filtered_data['Country_Name'].isin(country)]


# Summarize and sort the data - medal counts by country, calculate total medals and sort data by number of gold medals in descending order
medal_counts = filtered_data.groupby('Country_Name')[['Gold', 'Silver', 'Bronze']].sum().reset_index()

# calculate total medals
medal_counts['Total'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']

# sort by gold medals in descending order and select top 10.
top_10_medal_counts = medal_counts.sort_values(by='Gold', ascending=False).head(10)

# create grouped bar chart
fig = go.Figure(data=[
    go.Bar(name='Gold', x=top_10_medal_counts['Country_Name'],
           y=top_10_medal_counts['Gold'], marker_color='#FFD700'),
    go.Bar(name='Silver', x=top_10_medal_counts['Country_Name'],
           y=top_10_medal_counts['Silver'], marker_color='#C0C0C0'),
    go.Bar(name='Bronze', x=top_10_medal_counts['Country_Name'],
           y=top_10_medal_counts['Bronze'], marker_color='#CD7F32')
    ])

# set barmode to goup and add titles for chart and axes.
fig.update_layout(barmode='group', title='Top 10 Countries Medal Count',
                  xaxis_title='Country', yaxis_title='Medal Count')

st.plotly_chart(fig, use_container_width=True)

# display the data table
#Display the full sorted medal counts table without the first column and with a total column
medal_counts = medal_counts.sort_values(by='Gold', ascending=False)
medal_counts_display = medal_counts[['Country_Name', 'Gold', 'Silver', 'Bronze', 'Total']]

# Set country name as an index and remove index name
medal_counts_display.set_index('Country_Name', inplace=True)

st.write('Medal Counts')
st.dataframe(medal_counts_display)