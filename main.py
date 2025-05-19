from command_parser import interpretar_comando_struct
from tasks import adicionar_tarefa, listar_tarefas, excluir_todas_tarefas
from calendario import criar_reuniao_google_calendar

# Função auxiliar para exibir a resposta formatada no terminal
def exibir_resposta(mensagem):
    print("\n✅", mensagem if not mensagem.startswith("Erro") else f"❌ {mensagem}")

# Mostra todos os comandos anteriores e suas respectivas respostas
def exibir_historico(historico):
    print("\n📜 Histórico de comandos:")
    for i, item in enumerate(historico, 1):
        print(f"{i}. 🗣️ {item['comando']}")
        print(f"   🤖 {item['resposta']}\n")

# Função principal que roda o loop de entrada do terminal
def main():
    print("🤖 Agente Pessoal (Terminal)")
    print("Digite 'sair' para encerrar.")
    print("Comandos disponíveis: adicionar tarefa, listar tarefas, excluir tarefas, criar reunião\n")

    historico = [] # Lista para armazenar comandos e respostas

    while True:
        comando = input("🗣️ Comando: ")

        if comando.lower() in ["sair", "exit", "quit"]:
            print("👋 Até mais!")
            break

        # Interpreta o comando usando o modelo estruturado
        parsed = interpretar_comando_struct(comando)

        if isinstance(parsed, dict) and "erro" in parsed:
            resposta = parsed["erro"]
        else:
            acao = parsed.acao.lower()
            resposta = ""

            # Executa ação de acordo com o comando reconhecido
            if acao == "adicionar_tarefa":
                resposta = adicionar_tarefa(parsed.descricao)

            elif acao == "listar_tarefas":
                resposta = listar_tarefas()

            elif acao == "excluir_tarefas":
                confirm = input("⚠️ Isso vai excluir todas as tarefas. Confirmar (s/n)? ").lower()
                if confirm == "s":
                    resposta = excluir_todas_tarefas()
                else:
                    resposta = "Atenção: exclusão cancelada."

            elif acao == "criar_reuniao":
                resposta = criar_reuniao_google_calendar(
                    descricao=parsed.descricao,
                    data=parsed.data,
                    hora=parsed.hora
                )
            else:
                resposta = "Erro: ação não reconhecida."

        # Exibe e armazena a resposta
        exibir_resposta(resposta)
        historico.append({"comando": comando, "resposta": resposta})

        # Pergunta se o usuário quer visualizar o histórico
        ver_hist = input("📜 Ver histórico (s/n)? ").lower()
        if ver_hist == "s":
            exibir_historico(historico)

# Executa o agente se for o arquivo principal
if __name__ == "__main__":
    main()