from pydantic import BaseModel
from typing import Optional

class Comando(BaseModel):
    """
    Modelo de dados para representar um comando interpretado pela IA.

    Atributos:
        acao (str): Ação solicitada pelo usuário (ex: "adicionar_tarefa", "criar_reuniao").
        descricao (str, opcional): Texto descritivo da tarefa ou reunião.
        data (str, opcional): Data da ação no formato 'YYYY-MM-DD'.
        hora (str, opcional): Hora da ação no formato 'HH:MM'.
        duracao (int, opcional): Duração da ação em minutos (usado principalmente para reuniões).
    """
    acao: str
    descricao: Optional[str] = ""
    data: Optional[str] = None
    hora: Optional[str] = None
    duracao: Optional[int] = None 