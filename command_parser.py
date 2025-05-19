from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from types import SimpleNamespace
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv
import openai

# Carrega variáveis de ambiente (como OPENAI_API_KEY) do arquivo .env
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# 1. Definir os campos que queremos extrair do comando do usuário
response_schemas = [
    ResponseSchema(
        name="acao",
        description=(
            "Ação a ser executada: 'agendar_evento', 'adicionar_tarefa', 'excluir_tarefas', 'listar_tarefas'"
        )
    ),
    ResponseSchema(name="descricao", description="Descrição da tarefa ou evento"),
    ResponseSchema(name="data", description="Data no formato YYYY-MM-DD, se aplicável"),
    ResponseSchema(name="hora", description="Hora no formato HH:MM, se aplicável"),
]

# Cria o parser estruturado com base nos campos definidos
parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 2. Template de prompt que orienta a LLM a gerar uma resposta estruturada
prompt = PromptTemplate(
    template="""
Você é um assistente que interpreta comandos em linguagem natural e responde com informações estruturadas.

Comandos possíveis:
- Para adicionar uma tarefa: "anotar comprar pão"
- Para agendar um evento: "marcar consulta médica amanhã às 9h"
- Para excluir todas as tarefas: "limpar lista de tarefas", "apagar tudo", "deletar tarefas"
- Para listar tarefas: "quais são minhas tarefas", "mostrar o que tenho anotado"
Responda apenas no formato solicitado abaixo.

{format_instructions}

Comando: {comando}
""",
    input_variables=["comando"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

def interpretar_comando_struct(comando):
    """
    Interpreta um comando de linguagem natural usando um modelo da OpenAI via LangChain.

    Parâmetros:
        comando (str): Texto do comando fornecido pelo usuário.

    Retorna:
        objeto com os campos: acao, descricao, data, hora (ou erro, se falhar).
    """
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        prompt_formatado = prompt.format(comando=comando)
        resposta = llm.predict(prompt_formatado)
        return parser.parse(resposta)
    except Exception as e:
        return SimpleNamespace(erro=f"Erro ao interpretar o comando: {str(e)}")

