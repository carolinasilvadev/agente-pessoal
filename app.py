import streamlit as st
# from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from models import Comando   # Modelo Pydantic para estruturação do comando
from tasks import adicionar_tarefa, listar_tarefas, excluir_todas_tarefas
import os
from dotenv import load_dotenv
import openai
from calendario import criar_reuniao_google_calendar

# Carregar variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuração da página Streamlit
st.set_page_config(page_title="Agente Pessoal", layout="centered")

# Inicializa parser com modelo Pydantic para validar a estrutura do comando
parser = PydanticOutputParser(pydantic_object=Comando)

# Armazena o histórico de comandos/respostas na sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Prompt que o LLM usará para estruturar a resposta
prompt = PromptTemplate(
    template="""
Você é um assistente que interpreta comandos do usuário sobre tarefas.
Responda SOMENTE com um JSON no seguinte formato:
{format_instructions}

As ações possíveis são: "adicionar_tarefa", "listar_tarefas", "excluir_tarefas", "criar_reuniao".

Comando: {comando}
""",
    input_variables=["comando"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Função para interpretar comando e estruturar resposta como objeto `Comando`
def interpretar_comando_struct(comando: str):
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        prompt_formatado = prompt.format(comando=comando)
        resposta = llm.predict(prompt_formatado)
        # print("Resposta LLM:", resposta)
        return parser.parse(resposta)
    except Exception as e:
        return {"erro": f"Erro ao interpretar o comando: {str(e)}"}
    
# Mapeia variações comuns de ações para um padrão
def mapear_acao(acao: str) -> str:
    a = acao.lower().replace(" ", "_")
    acoes_validas = {
        "adicionar_tarefa": "adicionar_tarefa",
        "adicionar_tarefas": "adicionar_tarefa",
        "incluir_tarefas": "adicionar_tarefa",
        "listar_tarefas": "listar_tarefas",
        "listar_tarefa": "listar_tarefas",
        "excluir_tarefas": "excluir_tarefas",
        "excluir_tarefa": "excluir_tarefas",
        "deletar_tarefas": "excluir_tarefas",
        "remover_tarefas": "excluir_tarefas",
        "criar_reuniao": "criar_reuniao",
        "agendar_reuniao": "criar_reuniao",
    }
    return acoes_validas.get(a, "")

# Exibe um "card" estilizado com a resposta
def mostrar_card(texto, titulo="✅ Confirmação"):
    st.markdown(f"""
    <div style="border:1px solid #ccc; border-radius: 10px; padding: 15px; background-color: #f9f9f9;">
        <h4>{titulo}</h4>
        <p>{texto}</p>
    </div>
    """, unsafe_allow_html=True)

# === INTERFACE PRINCIPAL ===
st.title("🧠 Agente Pessoal de Tarefas")

comando = st.text_input("Digite um comando (ex: 'Adicionar tarefa comprar pão'):")

if comando:
    parsed = interpretar_comando_struct(comando)

    if "erro" in parsed:
        st.error(parsed["erro"])
    else:
        # Mapear a ação retornada para o padrão esperado
        acao_mapeada = mapear_acao(parsed.acao)

        if not acao_mapeada:
            st.error("Erro: ação não reconhecida.")
        else:
            if acao_mapeada == "adicionar_tarefa":
                resultado = adicionar_tarefa(parsed.descricao)

            elif acao_mapeada == "listar_tarefas":
                resultado = listar_tarefas()

            elif acao_mapeada == "excluir_tarefas":
                st.warning("⚠️ Isso vai excluir todas as tarefas salvas.")
                if st.button("Confirmar exclusão"):
                    resultado = excluir_todas_tarefas()
                else:
                    resultado = "Atenção: clique no botão acima para confirmar a exclusão."
            
            elif acao_mapeada == "criar_reuniao":
                resultado = criar_reuniao_google_calendar(
                    parsed.descricao,
                    parsed.data,
                    parsed.hora,
                    parsed.duracao or 60
                )
            else:
                resultado = "Erro: ação não reconhecida."

            # Exibir feedback com base no tipo de mensagem
            if resultado.startswith("Erro"):
                st.error(resultado)
            elif resultado.startswith("Atenção"):
                st.warning(resultado)
            else:
                if acao_mapeada == "listar_tarefas":
                    st.markdown(resultado, unsafe_allow_html=False)
                else:
                    mostrar_card(resultado)

            # Salvar no histórico
            st.session_state.historico.append({
                "comando": comando,
                "resposta": resultado
            })

# Mostrar histórico de interações
with st.expander("📜 Ver histórico"):
    for item in st.session_state.historico[::-1]:
        st.markdown(f"**🗣️ Comando:** {item['comando']}")
        st.markdown(f"**🤖 Resposta:** {item['resposta']}")
        st.markdown("---")
