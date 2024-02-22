import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()


def get_vectorstore_from_url(url):
    # get the text in doc form
    loader = WebBaseLoader(url)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(documents)
    
    vector_store = Chroma.from_documents(document_chunks,
                                         OpenAIEmbeddings())
    return vector_store

def get_context_retriever_from_url(vector_store):
    llm = ChatOpenAI()
    
    retriever = vector_store.as_retriever()
    
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user","Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    
    return retriever_chain


def get_conversational_rag_chain(retriever_chain):
    
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        ("user", "{input}"),
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

# def get_response(user_input):
#     #create conversation chain
#     retriever_chain = get_context_retriever_from_url(st.session_state.vector_store)
#     conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    
#     response = conversation_rag_chain.invoke({
#             "chat_history": st.session_state.chat_history,
#             "input": user_query
#         })
#     return response["answer"]


def get_response(user_query, vector_store, chat_history):
    # Create conversation chain
    retriever_chain = get_context_retriever_from_url(vector_store)

    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    response = conversation_rag_chain.invoke({
        "chat_history": chat_history,
        "input": user_query
    })

    return response["answer"]
     
#app config
st.set_page_config(page_title="Chat with your Website", 
                   layout="wide",
                   page_icon=":bar_chart:")


st.title("Chat with your Website")



#Sidebar
with st.sidebar:
    st.header("Menu")
    website_url = st.text_input("Enter Your URL")
    
if website_url is None or website_url =="":
    st.info("Please enter the website URL")


else:
    st.info(f"Chatting with {website_url}")
    if "website_data" not in st.session_state or st.session_state.website_data.get("url") != website_url:
        st.session_state.website_data = {
            "url": website_url,
            "vector_store": get_vectorstore_from_url(website_url),
            "chat_history": [AIMessage(content="Hello, I am a bot, How can I help?")]
        }
        
    # User Input
    user_query= st.chat_input("Type your message")

    if user_query is not None and user_query !="":
        response = get_response(user_query, st.session_state.website_data["vector_store"], st.session_state.website_data["chat_history"])
        
        st.session_state.website_data["chat_history"].append(HumanMessage(content=user_query))
        st.session_state.website_data["chat_history"].append(AIMessage(content=response))
        
    # conversation
    for message in st.session_state.website_data["chat_history"]:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)    