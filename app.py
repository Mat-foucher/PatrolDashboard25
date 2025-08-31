# Dependencies:
import streamlit as st
from scraper import get_live_data
from utils import format_time_column, plot_base_graph, plot_rose_graph
from gyro_component import gyro_heading

def main(option='PEAK'):
    st.set_page_config(page_title="Snowbird Patrol Dashboard", layout="wide")

    # Call the gyro detection:
    gyro_heading()

    # Page UI:
    df = get_live_data()
    df = format_time_column(df)

    

    # layout - make sure each element is declared in the order you want them to be on the dashboard!!!:
    col1, col2 = st.columns(2)
    c = st.container()
    

    with col1:
        st.title("Snowbird Patrol Dashboard")
        st.markdown(f"**Last Updated:** {df['DATETIME'].max()}")

    with col2:
        # Selection Button:
        option = st.selectbox(
            "Choose Weather Station:",
            ("PEAK", "REDSTACK")
        )
        plot_rose_graph(df,option)

        


    with c:
        plot_base_graph(df)

if __name__ == '__main__':
    main()