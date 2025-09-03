# Dependencies:
import streamlit as st
from scraper import get_live_data
from utils import format_time_column, plot_base_graph, plot_rose_graph
from gyro_component import gyro_heading
import os

def main(option='PEAK'):
    # Call the gyro detection:
    gyro_heading()

    # Page UI:
    df = get_live_data()
    df = format_time_column(df)

    # Password Protection:

    stored_password = os.environ.get('PASSWORD')

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False 
    
   

    if not st.session_state.authenticated:
        pass_input = st.text_input("Enter Password:", type="password")
        if st.button("Submit"):
            st.success("Access Granted")
            st.session_state.authenticated = True
        else:
            st.error("Incorrect Password")

    if st.session_state.authenticated:

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

                # c1,c2,c3,c4,c5 = st.columns(5)

                # with c1:
                #     st.metric("Base Temp",df['BASE_TEMP'].iloc[len(df['BASE_TEMP']-1)])
                # with c2:
                #     st.metric("Sinners Temp",df['SINN_TEMP'].iloc[len(df['SINN_TEMP']-1)])
                # with c3:
                #     st.metric("Peak Temp",df['PEAK_TEMP'].iloc[len(df['PEAK_TEMP']-1)])
                # with c4:
                #     st.metric("Gad Temp",df['GAD2_TEMP'].iloc[len(df['GAD2_TEMP']-1)])
                # with c5:
                #     st.metric("Redstack Temp:", df['REDSTACK_TEMP'].iloc[len(df['REDSTACK_TEMP']-1)])

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