import dateparser
from datetime import datetime

def extrair_data_e_hora(texto):
    """
    Extrai data e hora de um texto usando a biblioteca `dateparser`.
    
    A função tenta identificar uma data/hora futura com base no conteúdo textual.
    
    Parâmetros:
        texto (str): Texto com a data e/ou hora, ex: "amanhã às 15h", "22 de maio às 10:00".
    
    Retorna:
        tuple:
            - data (str): Data no formato 'YYYY-MM-DD' (ex: '2025-05-22')
            - hora (str): Hora no formato 'HH:MM' (ex: '14:00')
            - Se não for possível extrair uma data futura, retorna (None, None).
    """
    data_hora = dateparser.parse(
        texto,
        settings={
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": datetime.now(),
            "PARSERS": ["relative-time", "absolute-time", "custom-formats"],
        }
    )
    # Verifica se a data foi reconhecida e se está no futuro
    if data_hora and data_hora > datetime.now():
        data = data_hora.strftime("%Y-%m-%d")
        hora = data_hora.strftime("%H:%M")
        return data, hora
    else:
        return None, None
