import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st 

def format_time_column(df):
    #df['DATETIME'] = pd.to_datetime(df['DATETIME'], format="%H%M")
    df = df.sort_values('DATETIME')
    return df 

def plot_base_graph(df):
    #fig = px.line(df, x="DATETIME", y="BASE_TEMP", markers=True)

    # Base Temp Fig:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['DATETIME'],
        y=df['BASE_TEMP'],
        mode='lines+markers',
        name='Base Temp',
        line=dict(color='royalblue'),
        marker=dict(size=4)
    ))

    fig.add_trace(go.Scatter(
        x=df['DATETIME'],
        y=df['SINN_TEMP'],
        mode='lines+markers',
        name='Base Temp',
        line=dict(color='red'),
        marker=dict(size=4)
    ))

    fig.add_trace(go.Scatter(
        x=df['DATETIME'],
        y=df['GAD2_TEMP'],
        mode='lines+markers',
        name='Base Temp',
        line=dict(color='green'),
        marker=dict(size=4)
    ))

    fig.add_trace(go.Scatter(
        x=df['DATETIME'],
        y=df['PEAK_TEMP'],
        mode='lines+markers',
        name='Base Temp',
        line=dict(color='cyan'),
        marker=dict(size=4)
    ))

    fig.add_trace(go.Scatter(
        x=df['DATETIME'],
        y=df['REDSTACK_TEMP'],
        mode='lines+markers',
        name='Base Temp',
        line=dict(color='purple'),
        marker=dict(size=4)
    ))

    fig.update_layout(
        title="Station Temp (F) Two Day Report",
        xaxis_title="Datetime",
        yaxis_title="Temperature (F)",
        template='plotly_dark',
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)