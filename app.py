import streamlit as st


st.set_page_config(page_title="Chat with your Website", 
                   layout="wide",
                   page_icon=":bar_chart:")


st.title("Chat with your Website")

with st.sidebar:
    st.header("Menu")
    website_url = st.text_input("Enter Your URL")