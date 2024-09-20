import pickle
from pathlib import Path

import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from yaml.loader import SafeLoader
import yaml

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")

hide_bar= """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        visibility:hidden;
        width: 0px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        visibility:hidden;
    }
    </style>
"""

# --- USER AUTHENTICATION ---
with open(Path(__file__).parent/'assets/secrets/credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config.get('preauthorized', None)
)

name, authentication_status, username = authenticator.login( "main")

if authentication_status == False:
    st.error("Username/password is incorrect")
    st.markdown(hide_bar, unsafe_allow_html=True)

if authentication_status == None:
    st.warning("Please enter your username and password")
    st.markdown(hide_bar, unsafe_allow_html=True)


if authentication_status:
    # # ---- SIDEBAR ----
    st.sidebar.title(f":wave: Welcome {name}")

    img_path = str(Path(__file__).parent) + '/assets/imgs/logo_correct.png'
    st.image(img_path)

    st.write(":blue[𝙏𝙔𝙋𝙄𝘾𝘼𝙇] 𝙥𝙧𝙤𝙫𝙞𝙙𝙚𝙨 𝙞𝙣𝙩𝙚𝙜𝙧𝙖𝙩𝙚𝙙 𝙚𝙣𝙜𝙞𝙣𝙚𝙚𝙧𝙞𝙣𝙜 𝙨𝙤𝙡𝙪𝙩𝙞𝙤𝙣𝙨. 𝙊𝙪𝙧 𝙨𝙘𝙤𝙥𝙚 𝙤𝙛 𝙨𝙚𝙧𝙫𝙞𝙘𝙚𝙨 𝙘𝙤𝙫𝙚𝙧𝙨 𝙡𝙖𝙣𝙙𝙨𝙘𝙖𝙥𝙚 𝙙𝙚𝙨𝙞𝙜𝙣𝙨, 𝙡𝙖𝙣𝙙𝙨𝙘𝙖𝙥𝙚 𝙡𝙞𝙜𝙝𝙩𝙞𝙣𝙜 𝙙𝙚𝙨𝙞𝙜𝙣𝙨, 𝙞𝙧𝙧𝙞𝙜𝙖𝙩𝙞𝙤𝙣 𝙣𝙚𝙩𝙬𝙤𝙧𝙠 𝙙𝙚𝙨𝙞𝙜𝙣𝙨 𝙖𝙣𝙙 𝙞𝙣𝙩𝙚𝙧𝙞𝙤𝙧 𝙙𝙚𝙨𝙞𝙜𝙣𝙨. 𝙒𝙚 𝙖𝙩 𝙏𝙔𝙋𝙄𝘾𝘼𝙇 𝙗𝙚𝙡𝙞𝙚𝙫𝙚 𝙩𝙝𝙖𝙩 𝙝𝙞𝙜𝙝 𝙦𝙪𝙖𝙡𝙞𝙩𝙮 𝙞𝙨 𝙖𝙘𝙝𝙞𝙚𝙫𝙚𝙙 𝙩𝙝𝙧𝙤𝙪𝙜𝙝 𝙘𝙧𝙚𝙙𝙞𝙗𝙞𝙡𝙞𝙩𝙮 𝙖𝙣𝙙 𝙩𝙧𝙖𝙣𝙨𝙥𝙖𝙧𝙚𝙣𝙘𝙮 𝙞𝙣 𝙙𝙚𝙨𝙞𝙜𝙣, 𝙨𝙤 𝙝𝙚𝙧𝙚 𝙬𝙚 𝙖𝙘𝙝𝙞𝙚𝙫𝙚 𝙩𝙝𝙚 𝙙𝙞𝙛𝙛𝙞𝙘𝙪𝙡𝙩 𝙚𝙦𝙪𝙖𝙩𝙞𝙤𝙣, 𝙤𝙛𝙛𝙚𝙧𝙞𝙣𝙜 𝙩𝙝𝙚 𝙝𝙞𝙜𝙝𝙚𝙨𝙩 𝙦𝙪𝙖𝙡𝙞𝙩𝙮 𝙨𝙩𝙖𝙣𝙙𝙖𝙧𝙙𝙨 𝙬𝙞𝙩𝙝 𝙩𝙝𝙚 𝙛𝙖𝙨𝙩𝙚𝙨𝙩 𝙞𝙢𝙥𝙡𝙚𝙢𝙚𝙣𝙩𝙖𝙩𝙞𝙤𝙣 𝙖𝙣𝙙 𝙛𝙤𝙡𝙡𝙤𝙬-𝙪𝙥 𝙧𝙖𝙩𝙚 𝙛𝙤𝙧 𝙤𝙪𝙧 𝙘𝙪𝙨𝙩𝙤𝙢𝙚𝙧𝙨.")
    

    ###---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)


    authenticator.logout("Logout", "sidebar")
