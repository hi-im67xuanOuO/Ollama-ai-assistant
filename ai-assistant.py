from langchain.globals import set_debug
from langchain.globals import set_verbose


from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


import streamlit as st
import os
import re
from langchain.schema import(SystemMessage, HumanMessage, AIMessage)


llm = Ollama(model='llama2')
embeddings = OllamaEmbeddings()

chat_history = ['My name is Emily.']
vector = FAISS.from_texts(chat_history, embeddings)
retriever = vector.as_retriever()


prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user","{input}"),
    ("user","Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)


prompt = ChatPromptTemplate.from_messages([
("system","Answer the user's questions based on the below context:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
("user","{input}"),
])
document_chain = create_stuff_documents_chain(llm, prompt)

retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)




def getans(input, chats):    
    response = retrieval_chain.invoke({
                    'input': input,
                    'chat_history': chats,
                })
    return response


chat_history = []


def insight(input_text, chat_his):
    res = ""
    if input_text and chat_his == []:
        response = retrieval_chain.invoke({
            'input': input_text,
            'chat_history': chat_his,
        })
        res = response['answer']
    else:
        if input_text:
            r = getans(input_text, chat_his)
            res = r['answer']
    return res





st.set_page_config(page_title="📹 RAG-GPT")



def gpt_app():

    st.header(" 📹 RAG-GPT : contextual conversational AI assistants")
    st.write(
    """
    This chatbot is equipped with the ability to understand and respond to user queries based on the context of the ongoing conversation. 
    Leveraging advanced natural language processing techniques, including historical chat analysis, the chatbot offers more relevant and coherent responses over time, creating a more engaging and personalized conversational experience and providing with highly relevant and personalized responses for users.    
    """
    )
    st.info(
    """
    Welcome! 👋 The RAG-GPT is an contextual conversational AI assistant designed for intelligent and context-aware interactions. ✨
    """,
    icon="👾",
    )


    ## Setting 1 ##
    # clear_button = st.sidebar.button("Clear Conversation", key="clear")
    # if clear_button or "messages" not in st.session_state:
    #     st.session_state.messages = [
    #     SystemMessage(
    #         content="you are a helpful AI assistant. Reply your answer briefly and abbreviately."
    #     )
    #     ]

    # if user_input := st.chat_input("Input your question!"):
    #     st.session_state.messages.append(HumanMessage(content=user_input))
    #     with st.spinner("Bot is typing ..."):
    #         messages = st.session_state.get("messages", [])
    #         answer = insight(user_input, messages)
    #         print(answer)
    #     st.session_state.messages.append(AIMessage(content=answer))            

    #     messages = st.session_state.get("messages", [])
    #     for message in messages:
    #         if isinstance(message, AIMessage):
    #             with st.chat_message("assistant"):
    #                 st.markdown(message.content)
    #         elif isinstance(message, HumanMessage):
    #             with st.chat_message("user"):
    #                 st.markdown(message.content)
    



    ## Setting 2 ##
    # Initialize chat history
    st.sidebar.header('ChatBot with RAG')
    st.sidebar.write(
    """
    Push the botton if you want to reset the conversation.
    """
    )
    clear_button = st.sidebar.button("Clear Conversation", key="clear")

    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = []
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if input_text := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(input_text)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": input_text})

        # response = f"Echo: {input_text}"
        # ans, chat_history = insight(input_text, chat_history)
        messages = st.session_state.get("messages", [])
        ans = insight(input_text, messages)
        response = f"{ans}"
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

                
gpt_app()
