from openai import OpenAI
import openai
import streamlit as st
client = OpenAI()

title = "Meu Chat AI"
st.set_page_config(layout="wide", page_title=title)
st.title(title)


if "messages" not in st.session_state:
    st.session_state.messages = []   

for message in st.session_state['messages']:
    st.chat_message(message['role']).markdown(message['content'])

prompt = st.chat_input("Sua Mensagem")
if prompt:
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=st.session_state.messages,
        stream=True
    )
      
    res = st.chat_message('ai').write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": res})
    
