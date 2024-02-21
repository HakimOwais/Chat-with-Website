import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_response(user_input):
    return "I don't know"

def get_vectorstore_from_url(url):
    # get the text in doc form
    loader = WebBaseLoader(url)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(documents)
    return document_chunks



#app config
st.set_page_config(page_title="Chat with your Website", 
                   layout="wide",
                   page_icon=":bar_chart:")


st.title("Chat with your Website")

if "chat_history" not in st.session_state:
    st.session_state.chat_history =[
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

#Sidebar
with st.sidebar:
    st.header("Menu")
    website_url = st.text_input("Enter Your URL")
    
if website_url is None or website_url =="":
    st.info("Please enter the website URL")

else:   
    document_chunks = get_vectorstore_from_url(website_url)
    with st.sidebar:
        st.write(document_chunks)
    
    #User input 
    user_query = st.chat_input("Type you message here...")
    if user_query is not None and user_query !="":
        response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))
        
            
    # chat conversation
    for message in st.session_state.chat_history:
        if isinstance(message,AIMessage):
            with st.chat_message("AI Chatbot"):
                st.write(message.content)
            
        elif isinstance(message,HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

