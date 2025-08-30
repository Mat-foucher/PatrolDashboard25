# Dependencies:
import streamlit as st
from scraper import get_live_data
from utils import format_time_column, plot_base_graph, plot_rose_graph

def main():
    st.set_page_config(page_title="Snowbird Patrol Dashboard", layout="wide")

    # Page UI:
    

    df = get_live_data()
    df = format_time_column(df)

    

    # graph plots:
    c = st.container()
    col1, col2 = st.columns(2)

    with col1:
        st.title("Snowbird Patrol Dashboard")
        st.markdown(f"**Last Updated:** {df['DATETIME'].max()}")

    with col2:
        plot_rose_graph(df)

    with c:
        plot_base_graph(df)

if __name__ == '__main__':
    main()