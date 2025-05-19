# 🤖 Agente Pessoal com IA

Um agente inteligente que entende comandos em linguagem natural para gerenciar tarefas e reuniões, com interface em terminal e Streamlit.

## ✨ Funcionalidades

- ✅ Adicionar, listar e excluir tarefas (salvas em JSON)
- 📅 Criar reuniões no Google Calendar com linguagem natural
- 🧠 Compreensão de comandos com LLM (LangChain + OpenAI)
- 💬 Interface em Streamlit com feedback visual (cards)
- 🔁 Histórico de comandos e respostas
- 💻 Execução via terminal (`main.py`) ou via app web (`app.py`)

## 🚀 Como usar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/agente-pessoal.git
cd agente-pessoal

### 2. Clone o repositório

Crie um .env com sua chave da OpenAI e credenciais do Google Calendar:

OPENAI_API_KEY=sk-xxxxxx
GOOGLE_CALENDAR_CLIENT_SECRET=client_secret.json

### 3. Instale as dependências

pip install -r requirements.txt


### 4. Rode o app

- Interface Web: 
streamlit run app.py

- Interface Terminal: 
python main.py

💡 Exemplos de comandos
- adicionar tarefa comprar pão
- criar reunião quinta às 10h com João
- listar tarefas
- excluir tarefas

🛠️ Tecnologias
Streamlit
LangChain
OpenAI API
Google Calendar API
Python


📁 Estrutura do Projeto

agente-pessoal/
│
├── app.py                  # Interface Streamlit
├── main.py                 # Execução via terminal
├── command_parser.py               # Parsing com LLM
├── tasks.py              # Gerenciamento de tarefas
├── calendario.py           # Integração Google Calendar
├── models.py           
├── parser.py           
├── utils.py        # Funções auxiliares
├── tarefas.json       # Armazena tarefas (gerado automaticamente)
├── .env                    # Variáveis de ambiente (não subir!)
├── requirements.txt
├── README.md
└── .gitignore
