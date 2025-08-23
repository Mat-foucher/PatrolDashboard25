# Dependencies:
import streamlit as st
from scraper import get_live_data
from utils import format_time_column, plot_graph

st.set_page_config(page_title="Snowbird Patrol Dashboard", layout="wide")

st.title("Snowbird Patrol Dashboard")

df = get_live_data()
df = format_time_column(df)

st.markdown(f"**Last Updated:** {df['DATETIME'].max()}")

plot_graph(df)