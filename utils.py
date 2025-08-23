import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st 

def format_time_column(df):
    df['DATETIME'] = pd.to_datetime(df['TIME'], format="%H%M")
    df = df.sort_values('DATETIME')
    return df 

def plot_base_graph(df):
    fig = px.line(df, x="DATETIME", y="BASE_TEMP", markers=True)
    st.plotly_chart(fig, use_container_width=True)