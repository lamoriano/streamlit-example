#from collections import namedtuple
#import altair as alt
#import math
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Fun Fact",
    page_icon=":bar_chart:",
    layout="wide"
)


df = pd.read_excel(
    io = 'seasia_articles_funfact.xlsx',
    engine = 'openpyxl',
    sheet_name= 'DATA'
)



# ----- SIDEBAR -------
st.sidebar.header("Filter: ")
year = st.sidebar.selectbox(
    "Select the Year: ",
    options=df["Year"].unique(),
    #default=df["Year"].unique()
)
df_year = df.query("Year == @year")

country = st.sidebar.multiselect(
    "Select the Country: ",
    options=df_year["Country"].unique(),
    default=df_year["Country"].unique()
)
month = st.sidebar.multiselect(
    "Select the Month: ",
    options=df_year["Month"].unique(),
    default=df_year["Month"].unique()
)


df_selection = df_year.query(
    "Country == @country & Month == @month"
)

#st.dataframe(df_selection)

# ---- MAINPAGE -----
st.title(f":bar_chart: Summary of {year}")
st.markdown("##")

# --- KPI ---
total_share = int(df_selection["Share"].sum())
total_article = int(df_selection["Title"].count())
total_author = len(pd.unique(df_selection["Author"]))#int(df_selection["Author"].unique().count())

left_col, mid_col, right_col = st.columns(3)
with left_col:
    st.subheader(":star: Total Shared: ")
    st.subheader(f"{total_share} shared")
with mid_col:
    st.subheader(":newspaper: Total Article: ")
    st.subheader(f"{total_article} article(s)")
with right_col:
    st.subheader(":bust_in_silhouette: Total Author: ")
    st.subheader(f"{total_author} author(s)")

st.markdown("---")

# Share by Author
share_author = (
        df_selection.groupby(by=["Author"]).sum()[["Share"]].sort_values(by="Share")
    )

fig_author = px.bar(
    share_author,
    x="Share",
    y=share_author.index,
    orientation="h",
    title="<b>Shared by Author</b>",
    color_discrete_sequence=["#0083B8"] * len(share_author),
    template="plotly_white",
)

fig_author.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)




# Share by React
share_react = (
    df_selection.groupby(by=["React_1"]).sum()[["Share"]].sort_values(by="Share")
)
fig_react = px.bar(
    share_react,
    x=share_react.index,
    y="Share",
    orientation="v",
    title="<b>Shared by React</b>",
    color_discrete_sequence=["#0083B8"] * len(share_react),
    template="plotly_white",
)

fig_react.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_author, use_container_width=True)
right_col.plotly_chart(fig_react, use_container_width=True)

# Hide Style
hide_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_style, unsafe_allow_html=True)