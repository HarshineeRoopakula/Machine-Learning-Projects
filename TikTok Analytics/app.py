import streamlit as st
import pandas as pd
# import subprocess to run tiktok script from command line
from subprocess import call
import plotly.express as px

#Set page width to wide
st.set_page_config(layout="wide")

st.sidebar.markdown("<div><img src='http://assets.stickpng.com/images/5cb78678a7c7755bf004c14c.png' width=100 /><h1 style='display:inline-block'>Tiktok Analytics</h1></div>",unsafe_allow_html=True)
st.sidebar.markdown("This dashboard allows you to analyze trending 📈 tiktoks using Python and Streamlit.")
st.sidebar.markdown("To get started <ol><li> Enter the <i>hashtag</i> you wish to analyze</li> <li> Hit <i>Get Data</i>.</li> <li>Get Analyzing</li></ol>",unsafe_allow_html=True)

hashtag = st.text_input("Search for a hashtag here",value ="")

if st.button("Get Data"):
    call(['python','tiktok.py',hashtag])
    df = pd.read_csv("tiktokdata.csv")
    fig = px.histogram(df,x="desc",y="stats_diggCount",hover_data=['desc'],height=300)
    st.plotly_chart(fig,use_container_width=True)
    left_column,right_column = st.columns(2)
    scatter1=px.scatter(df,x="stats_shareCount",y="stats_commentCount",hover_data=['desc'],size="stats_playCount",color="stats_playCount")
    left_column.plotly_chart(scatter1,use_container_width=True)
    scatter2=px.scatter(df,x="authorStats_videoCount",y="authorStats_heartCount",hover_data=['author_nickname'],size="authorStats_followerCount",color="authorStats_followerCount")
    right_column.plotly_chart(scatter2,use_container_width=True)

    df
