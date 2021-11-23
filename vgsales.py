#importing modules
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Creating the app title
st.title('Video Game Sales Analysis')
st.write('This App shows the sale performance of video games both regionally and regionally')
st.text("Author: Temo Nyenye")


#Creating a sidebar

st.sidebar.header('Video Game Sales')

#Creating a file uploader

#defining the url varible



url = "DataSet/vgsales.csv"

data = st.sidebar.file_uploader('Upload Dataset',type=['csv'])

#if data file is uploaded
if data is not None:
    df = pd.read_csv(data)


    #Data preparation
    df['Year'] = df['Year'].values.astype(np.int64)
    df2 = df.fillna(value=0)
    vgsales = df2.drop_duplicates()
    Global = df.groupby(['Platform']).agg({'Global_Sales': 'sum'}).reset_index().sort_values('Global_Sales',
                                                                                             ascending=False).head(10)
    NA = df.groupby(['Platform']).agg({'NA_Sales': 'sum'}).reset_index().sort_values('NA_Sales', ascending=False).head(
        10)
    EU = df.groupby(['Platform']).agg({'EU_Sales': 'sum'}).reset_index().sort_values('EU_Sales', ascending=False).head(
        10)
    JP = df.groupby(['Platform']).agg({'JP_Sales': 'sum'}).reset_index().sort_values('JP_Sales', ascending=False).head(
        10)
    Other = df.groupby(['Platform']).agg({'Other_Sales': 'sum'}).reset_index().sort_values('Other_Sales',
                                                                                           ascending=False).head(10)
    Regions = pd.concat([Global, NA, EU, JP, Other], axis=1).reset_index()
    Popular_Consoles = Regions.sort_values('Global_Sales', ascending=False).iloc[:,
                       ~Regions.columns.duplicated()].replace(to_replace=np.nan, value=0).head(10)



#if data is not uploaded
else:
    df= pd.read_csv(url)

    #Data preparation
    df['Year'] = df['Year'].values.astype(np.int64)
    df2 = df.fillna(value=0)
    vgsales = df2.drop_duplicates()
    Global = df.groupby(['Platform']).agg({'Global_Sales': 'sum'}).reset_index().sort_values('Global_Sales',
                                                                                             ascending=False).head(10)
    NA = df.groupby(['Platform']).agg({'NA_Sales': 'sum'}).reset_index().sort_values('NA_Sales', ascending=False).head(
        10)
    EU = df.groupby(['Platform']).agg({'EU_Sales': 'sum'}).reset_index().sort_values('EU_Sales', ascending=False).head(
        10)
    JP = df.groupby(['Platform']).agg({'JP_Sales': 'sum'}).reset_index().sort_values('JP_Sales', ascending=False).head(
        10)
    Other = df.groupby(['Platform']).agg({'Other_Sales': 'sum'}).reset_index().sort_values('Other_Sales',
                                                                                           ascending=False).head(10)
    Regions = pd.concat([Global, NA, EU, JP, Other], axis=1).reset_index()
    Popular_Consoles = Regions.sort_values('Global_Sales', ascending=False).iloc[:,
                       ~Regions.columns.duplicated()].replace(to_replace=np.nan, value=0).head(10)




#Creating a drop down
menu= ['Overview','Leading Platforms','Leading Publishers(Sales)','Leading Publishers(Entries)','New Sequel Candidates','New Game Candidates']
selection = st.sidebar.selectbox('Insight', menu)

if selection == 'Overview':
    st.sidebar.write('This is the raw data. Data analysis was done onto this dataset to gain to gain insights.')
    st.write(df)
    st.write(data)


#Leading Platforms
if selection == 'Leading Platforms':
    st.header('Leading Platforms')
    st.write(Popular_Consoles)
    st.sidebar.write('This shows which platform is mostly used for gaming. The results inform game developers as to which platform should their games play on and which region is of significant market')
    plt.title('Top 10 Popular platforms with respect to game sales')
    plt.plot(Popular_Consoles['Platform'], Popular_Consoles['NA_Sales'], label='NA Sales')
    plt.plot(Popular_Consoles['Platform'], Popular_Consoles['EU_Sales'], label='EU Sales')
    plt.plot(Popular_Consoles['Platform'], Popular_Consoles['JP_Sales'], label='JP Sales')
    plt.plot(Popular_Consoles['Platform'], Popular_Consoles['Other_Sales'], label='Other Sales')
    plt.plot(Popular_Consoles['Platform'], Popular_Consoles['Global_Sales'], label='Global Sales')
    plt.legend()
    st.pyplot(plt)


#Leading Publishers(Sales)
if selection == 'Leading Publishers(Sales)':
    st.header('Leading Publishers(Sales)')
    st.sidebar.write('The results show the game developer with the most sales')
    Game_Publishers = df.groupby(['Publisher']).agg({'Global_Sales': 'sum'}).reset_index()
    Game_Publishers= Game_Publishers.sort_values('Global_Sales',ascending = False)
    Leading_Publishers = Game_Publishers.head(10)
    Leading_Publishers.plot.bar(x="Publisher", y="Global_Sales", rot=70, title="Top 10 Publishers in the worlds by Sales");
    plt.show(block=True)
    st.write(Leading_Publishers)
    st.pyplot(plt)


#Leading Publishers(Entries)
if selection == 'Leading Publishers(Entries)':
    st.header('Leading Publishers(Entries)')
    st.sidebar.write('The results show the game developer with the most number of game entries')
    Publishers = (df['Publisher'].value_counts().rename_axis('unique_values').to_frame('Counts').reset_index())
    Top_publishers = Publishers.nlargest(10, 'Counts')
    Popular_Publishers = Top_publishers.rename(columns={'unique_values': 'Publishers'})
    Popular_Publishers.plot.bar(x="Publishers", y="Counts", rot=70, title="Leading Publishers by game entries")
    plt.show(block=True)
    st.write(Popular_Publishers)
    st.pyplot(plt)


#New Game candidates
if selection== 'New Game Candidates':
    st.header('New Game Candidates')
    st.sidebar.write('This should inform publishers as to which game genre is popular.This will address the question of which genre should be getting new games')
    Genre = df.groupby(['Genre']).agg({'Global_Sales': 'sum'}).reset_index()
    Genre = Genre.sort_values('Global_Sales', ascending=False)
    Popular_Genre = Genre.head(10)
    Popular_Genre.plot.bar(x="Genre", y="Global_Sales", rot=70, title="Best selling games globally")
    plt.show(block=True)
    st.write(Popular_Genre)
    st.pyplot(plt)

#New Sequel Candidates
if selection == 'New Sequel Candidates':
    st.header('New Sequel Candidates')
    st.sidebar.write('This should inform publishers as to which games are popular. This will address the question of which games should be getting new game sequels')
    Games = df.drop(df.iloc[:, [0, 3, 5, 6, 7, 8, 9]], axis=1)
    Games = Games.sort_values('Global_Sales', ascending=False)
    Popular_Games = Games.head(10)
    Popular_Games.plot.bar(x="Name", y="Global_Sales", rot=70, title="Best selling games globally")
    plt.show(block=True)
    st.write(Popular_Games)
    st.pyplot(plt)

