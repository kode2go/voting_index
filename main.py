import streamlit as st
from base import base
from about import about

import streamlit as st
import pandas as pd
from urllib.request import urlopen
from streamlit_option_menu import option_menu
import json
import requests
from streamlit_lottie import st_lottie
import pickle
from pathlib import Path 
import streamlit_authenticator as stauth 

#Layout
st.set_page_config(
    page_title="Islamicity Index",
    layout="wide",
    initial_sidebar_state="expanded")



#Data Pull and Functions
st.markdown("""
<style>
.big-font {
    font-size:80px !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)

# def main():

#Options Menu
with st.sidebar:
    # st.sidebar.title(f"Welcome {name}")
    selected = option_menu('Islamicity Index', ["Intro",
    'About'], 
    icons=['play-btn','search','info-circle'],menu_icon='intersect', default_index=0)
    # authenticator.logout("Logout","sidebar")
    lottie = load_lottiefile("similo3.json")
    st_lottie(lottie,key='loc')    

  

if selected == "Intro":    
    base()
elif selected == "About":
    about()
