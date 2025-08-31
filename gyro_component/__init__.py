import streamlit.components.v1 as components
import os

def gyro_heading():
    component_dir = os.path.dirname(__file__)
    html_path = os.path.join(component_dir, "frontend.html")

    with open(html_path, "r") as f:
        html_string = f.read()

    components.html(html_string, height=60, width=300)