import openai

def retorna_resposta_modelo(
    mensagens, openai_key, modelo="gpt-3.5-turbo", temperatura=0, stream=False
):
    openai.api_key = openai_key
    res = openai.chat.completions.create(
        model=modelo, messages=mensagens, temperature=temperatura, stream=stream
    )

    return res