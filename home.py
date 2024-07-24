import streamlit as st
from dotenv import load_dotenv
from utils_files import ler_mensagens, ler_mensagem_por_nome_arquivo, desconverte_nome_mensagem, le_chave, listar_conversas, salva_chave, salvar_mensagens
from utils_openai import retorna_resposta_modelo
load_dotenv()

def inicializacao():
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    if not "conversa_atual" in st.session_state:
        st.session_state.conversa_atual = []

    if not "modelo" in st.session_state:
        st.session_state.modelo = "gpt-3.5-turbo"

    if not "api_key" in st.session_state:
        st.session_state.api_key = le_chave()

def pagina_principal():

    mensagens = ler_mensagens(st.session_state["mensagens"])

    st.header("Meu Chat IA", divider=True)

    for mensagem in mensagens:
        chat = st.chat_message(mensagem["role"])
        chat.markdown(mensagem["content"])

    prompt = st.chat_input("Fale com o chat")
    if prompt:
        nova_mensagem = {"role": "user", "content": prompt}
        chat = st.chat_message(nova_mensagem["role"])
        chat.markdown(nova_mensagem["content"])
        mensagens.append(nova_mensagem)

        chat = st.chat_message("assistant")
        placeholder = chat.empty()
        placeholder.markdown("|")
        resposta_completa = ""
        respostas = retorna_resposta_modelo(
            mensagens,
            st.session_state["api_key"],
            modelo=st.session_state["modelo"],
            stream=True,
        )

        for resposta in respostas:
            if resposta.choices[0].delta.content:
                resposta_completa += resposta.choices[0].delta.content
            placeholder.markdown(resposta_completa + "|")

        placeholder.markdown(resposta_completa)
        nova_mensagem = {"role": "assistant", "content": resposta_completa}
        mensagens.append(nova_mensagem)

        st.session_state["mensagens"] = mensagens
        salvar_mensagens(mensagens)

def tab_conversas(tab):
    tab.button(
        "Nova Conversa",
        on_click=seleciona_conversa,
        args=("",),
        use_container_width=True,
    )
    tab.markdown("")
    conversas = listar_conversas()

    for nome_arquivo in conversas:
        tab.button(
            desconverte_nome_mensagem(nome_arquivo).capitalize(),
            on_click=seleciona_conversa,
            args=(nome_arquivo,),
            disabled=nome_arquivo == st.session_state["conversa_atual"],
            use_container_width=True,
        )

def seleciona_conversa(nome_arquivo):
    if nome_arquivo == "":
        st.session_state.mensagens = []
    else:
        mensagem = ler_mensagem_por_nome_arquivo(nome_arquivo)
        st.session_state.mensagens = mensagem
    st.session_state["conversa_atual"] = nome_arquivo

def tab_configuracoes(tab):
    modelo_escolhido = tab.selectbox("Selecione o modelo", ["gpt-3.5-turbo", "gpt-4"])
    st.session_state["modelo"] = modelo_escolhido

    chave = tab.text_input("Adicione sua api key", value=st.session_state["api_key"])

    if chave != st.session_state["api_key"]:
        st.session_state["api_key"] = chave
        salva_chave(chave)
        st.success("Chave salva com sucesso")

inicializacao()
pagina_principal()
tab1, tab2 = st.sidebar.tabs(["Conversas", "Configurações"])
tab_conversas(tab1)
tab_configuracoes(tab2)
