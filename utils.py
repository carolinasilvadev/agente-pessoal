import os
from dotenv import load_dotenv
import openai

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
# Define a chave da API da OpenAI a partir da variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

def chamar_gpt(prompt, temperatura=0.5):
    """
    Envia um prompt para o modelo ChatGPT (gpt-3.5-turbo) e retorna a resposta formatada.

    Parâmetros:
    - prompt (str): Texto enviado como entrada para o modelo.
    - temperatura (float): Grau de criatividade da resposta (padrão = 0.5). 
      Valores maiores geram respostas mais criativas; menores, mais determinísticas.

    Retorna:
    - str: Resposta em texto gerada pelo modelo.
    """
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "user", "content": prompt}],
        temperature=temperatura
    )
    return resposta['choices'][0]['message']['content'].strip()
