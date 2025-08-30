import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st 

def format_time_column(df):
    #df['DATETIME'] = pd.to_datetime(df['DATETIME'], format="%H%M")
    df = df.sort_values('DATETIME')
    return df 

def plot_rose_graph(df):
    peak_wind_df = pd.DataFrame()

    peak_wind_df['PEAK_WIND'] = df['PEAK_WIND'].astype(int)

    peak_wind_df['PEAK_WIND_DIR'] = df['PEAK_WIND_DIR']

    peak_wind_df['PEAK_GUST'] = df['PEAK_GUST']


    #max_wind = max(peak_wind_df['PEAK_WIND'])

    wind_directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

    # Ensure Peak wind dir is categorical:

    peak_wind_df['PEAK_WIND_DIR'] = pd.Categorical(
        peak_wind_df['PEAK_WIND_DIR'],
        categories=wind_directions,
        ordered=True
    )

    wind_summary = peak_wind_df.groupby('PEAK_WIND_DIR')['PEAK_WIND'].mean().reindex(wind_directions)

    fig = px.bar_polar(
        r = wind_summary.values,
        theta= wind_summary.index,
        color= wind_summary.values,
        color_discrete_sequence= px.colors.sequential.Plasma_r,
        title="Peak Station Avg Wind (mph)"
    )

    fig.update_traces(marker_line_color="black", marker_line_width=1)
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig )


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
        name='Sinners Temp',
        line=dict(color='red'),
        marker=dict(size=4)
    ))

    fig.add_trace(go.Scatter(
        x=df['DATETIME'],
        y=df['GAD2_TEMP'],
        mode='lines+markers',
        name='Gad Temp',
        line=dict(color='green'),
        marker=dict(size=4)
    ))

    fig.add_trace(go.Scatter(
        x=df['DATETIME'],
        y=df['PEAK_TEMP'],
        mode='lines+markers',
        name='Peak Temp',
        line=dict(color='cyan'),
        marker=dict(size=4)
    ))

    fig.add_trace(go.Scatter(
        x=df['DATETIME'],
        y=df['REDSTACK_TEMP'],
        mode='lines+markers',
        name='Redstack Temp',
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

    # put the legend for temp history under that chart:
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )


    st.plotly_chart(fig, use_container_width=True)

