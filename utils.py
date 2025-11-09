import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st 
import os
# from openai import OpenAI
from gyro_component import gyro_heading

# Use ChatGPT to summarize the conditions from the past 24 hours:

#client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# def AISummary(df):
#     df_string = df.to_string()
#     context = f"""
#     You are a weather reporting assistant that will read the last 24 hours of recent weather data from various weather stations and givew a brief summary, in the 
#     style of AIARE condition reports. Be brief and to the point, with the midnset that you are giving insights to an on mountain ski patrol team that needs to make
#     quick decisions.The weather data for the last 24 hours is as follows: \n
#     Data: {df_string}"""

#     response = client.chat.completions.create(
#       model="gpt-4o",
#       messages=[{"role": "user", "content": context}],
#       temperature=0.7
#     )

#     return response.choices[0].message.content


def format_time_column(df):
    #df['DATETIME'] = pd.to_datetime(df['DATETIME'], format="%H%M")
    
    df = df.sort_values('DATETIME')
    return df 

def plot_indi1(df,option):
    fig = go.Figure()

    try:
        windmask = df[df['DATETIME'] == df['DATETIME'].max()]
        df[option+'_WIND'] = df[option+'_WIND'].astype(int)

        

        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            delta = {'reference': df[option + '_WIND'].mean()},
            value = int(windmask[option + '_WIND'].iloc[0]),
            title = {'text': 'Last ' + option + " Avg Wind Speed (mph)", 'font':{'size':10}},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {'axis': { 'range':[None, df[option + '_WIND'].max()]}}
            
        ))

        fig.update_layout(template='plotly_dark', height=250)

        return fig
    except:
        st.error('Could not find weather station data - check BIGROUNDUP')

def plotbar(bsdf):
    bigsnowfig = go.Figure(
        data= [
        go.Bar(
            x=bsdf['DATE'], 
            y=bsdf['BASE_HS'],
            text=bsdf['BASE_HS'],
            name = 'BASE_HS'
            ),
        go.Bar(
            x=bsdf['DATE'], 
            y=bsdf['SIN_HS'],
            text=bsdf['SIN_HS'],
            name='SIN_HS'
            ),
        go.Bar(
            x=bsdf['DATE'],
            y=bsdf['PH1_HS'],
            text=bsdf['PH1_HS'],
            name='PH1_HS'
        ),
        go.Bar(
            x=bsdf['DATE'],
            y=bsdf['G2_HS'],
            text=bsdf['G2_HS'],
            name='G2_HS'
        )
        ]
    )
    #bigsnowfig.update_layout(barmode='stack')
    bigsnowfig.update_layout(title_text='Snow Height by Station (in)')
    bigsnowfig.show()



def plot_rose_graph(df, option):
        
    try:
        peak_wind_df = pd.DataFrame()

        peak_wind_df[option + '_WIND'] = df[option + '_WIND'].astype(int)

        peak_wind_df[option + '_WIND_DIR'] = df[option + '_WIND_DIR']

        peak_wind_df[option + '_GUST'] = df[option + '_GUST']


        #max_wind = max(peak_wind_df['PEAK_WIND'])

        wind_directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

        # Ensure Peak wind dir is categorical:

        peak_wind_df[option + '_WIND_DIR'] = pd.Categorical(
            peak_wind_df[option + '_WIND_DIR'],
            categories=wind_directions,
            ordered=True
        )

        wind_summary = peak_wind_df.groupby(option + '_WIND_DIR')[option + '_WIND'].mean().reindex(wind_directions)

        windmask = df[df['DATETIME'] == df['DATETIME'].max()]

        fig = px.bar_polar(
            r = np.round(wind_summary.values,2),
            theta= wind_summary.index,
            color= np.round(wind_summary.values,2),
            color_discrete_sequence= px.colors.sequential.Plasma_r,
            title= option + " 24 hr Wind (mph)",
            subtitle= f"Most Recent: {windmask[option + '_WIND_DIR'].iloc[0]}" + " at " + f"{windmask[option + '_WIND'].iloc[0]}" + " mph"
        )

        #fig.update_traces(marker_line_color="black", marker_line_width=1)
        fig.update_layout(
            template='plotly_dark',
            coloraxis_colorbar=dict(title=None),
            coloraxis_showscale=False
        )

        


        st.plotly_chart(fig)
    except:
        st.error('Could not find weather station data - check BIGROUNDUP')
        







def plot_base_graph(df):
    #fig = px.line(df, x="DATETIME", y="BASE_TEMP", markers=True)
    try:
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

        fig.add_trace(go.Scatter(
            x=df['DATETIME'],
            y=df['PH1_TEMP'],
            mode='lines+markers',
            name='Phone 1 Temp',
            line=dict(color='orange'),
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
                y=-1.0,
                xanchor="center",
                x=0.5
            )
        )


        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error('Could not find weather station data - check BIGROUNDUP')
