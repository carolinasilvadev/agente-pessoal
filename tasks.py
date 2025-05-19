import json
import os

# Caminho do arquivo onde as tarefas serão salvas
ARQUIVO = "agenda.json"

# =========================
# Funções de manipulação de tarefas
# =========================


def carregar_agenda():
    """
    Carrega a lista de tarefas do arquivo JSON.
    Retorna uma lista vazia se o arquivo não existir.
    
    Retorna:
        list: Lista de tarefas carregadas do arquivo.
    """
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_agenda(agenda):
    """
    Salva a lista de tarefas no arquivo JSON.
    
    Parâmetros:
        agenda (list): Lista de tarefas a ser salva.
    """
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(agenda, f, indent=4, ensure_ascii=False)

# Inicializa a variável global com as tarefas carregadas do arquivo
agenda = carregar_agenda()

def adicionar_tarefa(descricao):
    """
    Adiciona uma nova tarefa à agenda e salva no arquivo.
    
    Parâmetros:
        descricao (str): Descrição da tarefa a ser adicionada.
    
    Retorna:
        str: Mensagem de sucesso ou erro.
    """
    try:
        agenda.append(descricao)
        salvar_agenda(agenda)
        return f"Tarefa adicionada: {descricao}"
    except Exception as e:
        return f"Erro ao adicionar tarefa: {e}"

def listar_tarefas():
    """
    Lista todas as tarefas salvas na agenda.
    
    Retorna:
        str: Lista formatada das tarefas ou mensagem de atenção/erro.
    """
    try:
        if not agenda:
            return "Atenção: você não tem tarefas salvas."
        return "\n".join(f"- {tarefa}" for tarefa in agenda)
    except Exception as e:
        return f"Erro ao listar tarefas: {e}"


def excluir_todas_tarefas():
    """
    Exclui todas as tarefas da agenda (limpa o arquivo).
    
    Retorna:
        str: Mensagem de confirmação.
    """
    global agenda
    agenda = []
    salvar_agenda(agenda)
    return "Todas as tarefas foram excluídas."