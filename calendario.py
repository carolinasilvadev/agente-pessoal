from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz
import os

# Escopo necessário para criar eventos no Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CALENDAR_TIMEZONE = 'America/Sao_Paulo'

def autenticar_google_calendar():
    """
    Realiza a autenticação com a API do Google Calendar.
    Salva o token localmente em 'token.json' após o primeiro login.
    """
    creds = None
    if os.path.exists('token.json'):
        # Usa token salvo anteriormente
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        # Inicia o fluxo de autenticação via navegador
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)


def parse_data_hora(data_str, hora_str):
    """
    Tenta converter strings de data e hora para objeto datetime.
    Suporta múltiplos formatos de data.

    Retorna:
        datetime: objeto combinado de data e hora
    """
    formatos_data = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"]
    for formato in formatos_data:
        try:
            return datetime.strptime(f"{data_str} {hora_str}", f"{formato} %H:%M")
        except ValueError:
            continue
    raise ValueError(f"Formato de data inválido: {data_str}")


def criar_reuniao_google_calendar(descricao, data, hora, duracao=60):
    """
    Cria um evento no Google Calendar com base nas informações fornecidas.

    Parâmetros:
        descricao (str): Título da reunião
        data (str): Data no formato 'YYYY-MM-DD', 'DD-MM-YYYY' ou 'DD/MM/YYYY'
        hora (str): Hora no formato 'HH:MM'
        duracao (int): Duração do evento em minutos (padrão: 60)

    Retorna:
        str: Mensagem de confirmação ou erro
    """
    try:
        service = autenticar_google_calendar()

        # Converte data e hora em datetime e ajusta para o timezone correto
        dt_inicio = parse_data_hora(data, hora)
        dt_fim = dt_inicio + timedelta(minutes=duracao)

        dt_inicio = dt_inicio.astimezone(pytz.timezone("America/Sao_Paulo"))
        dt_fim = dt_fim.astimezone(pytz.timezone("America/Sao_Paulo"))

        # Define o evento a ser criado
        evento = {
            'summary': descricao or "Reunião",
            'start': {'dateTime': dt_inicio.isoformat(), 'timeZone': "America/Sao_Paulo"},
            'end': {'dateTime': dt_fim.isoformat(), 'timeZone': "America/Sao_Paulo"},
        }

        # Cria o evento na agenda principal do usuário
        service.events().insert(calendarId='primary', body=evento).execute()

        # Monta mensagem mais natural para o usuário
        dia_semana = dt_inicio.strftime("%A")  # Ex: "Thursday"
        data_formatada = dt_inicio.strftime("%d/%m/%Y às %H:%M")

        return f"📅 Reunião marcada para **{dia_semana} ({data_formatada})** com o título: _{descricao}_"

    except Exception as e:
        return f"Erro ao criar reunião: {str(e)}"