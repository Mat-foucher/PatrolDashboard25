# Dependencies:
import streamlit as st
from scraper import get_live_data
from utils import format_time_column, plot_base_graph, plot_rose_graph, plot_indi1
from gyro_component import gyro_heading
import os


def main(option='PEAK'):
    # Call the gyro detection:
    gyro_heading()

    # Page UI:
    df = get_live_data()
    df = format_time_column(df)

    # Password Protection:
    # if "authenticated" not in st.session_state:
    #     st.session_state.authenticated = False 

    # stored_password = os.environ.get('PASSWORD')

    

    # if not st.session_state.authenticated:
        
    #     with st.form("Login Form"):
    #         pass_input = st.text_input("Enter Password:", type="password")
    #         submitted = st.form_submit_button('Submit')

    #         if submitted:
    #             if pass_input == stored_password:
    #                 st.success("Access Granted")
    #                 st.session_state.authenticated = True
    #             else:
    #                 st.error("Incorrect Password")
    #     st.stop()

    # if st.session_state.authenticated:

    st.set_page_config(page_title="Snowbird Patrol Dashboard")

    

    # For the elements to be less sparse:
    g = st.container()
    
    # layout - make sure each element is declared in the order you want them to be on the dashboard!!!:
    col1, col2 = st.columns(2)
    c = st.container()
    
    with g:
        with col1:
            st.title("Snowbird Patrol Dashboard (UNOFFICIAL)")
            st.markdown(f"**Last Updated:** {df['DATETIME'].max()}")
            col11, col12 = st.columns(2)
            with col11:
                plot_indi1(df,'PEAK')
            
            with col12:
                plot_indi1(df,'REDSTACK')

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