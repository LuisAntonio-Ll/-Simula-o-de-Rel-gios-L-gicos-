class Processo:
    def __init__(self, id_processo):

        self.id = id_processo

        self.relogio = 0

    def evento_interno(self, descricao):
  
        self.relogio += 1
        print(f"[{self.id} | TS={self.relogio}]: Evento Interno - {descricao}")

        return self.relogio

    def enviar_mensagem(self, destinatario):

        self.relogio += 1

        timestamp_enviado = self.relogio
        print(f"[{self.id} | TS={self.relogio}]: Envia mensagem para {destinatario.id} com TS={timestamp_enviado}")

        return timestamp_enviado

    def receber_mensagem(self, remetente, timestamp_recebido):

        relogio_antes = self.relogio
        self.relogio = max(self.relogio, timestamp_recebido)

        self.relogio += 1

        print(f"[{self.id} | TS={self.relogio}]: Recebe mensagem de {remetente.id} (TS_envio={timestamp_recebido}).")
        print(f"    * Ajuste: max({relogio_antes}, {timestamp_recebido}) -> Relógio atualizado para {self.relogio} (após incremento)")

        return self.relogio
    

P1 = Processo('P1')
P2 = Processo('P2')
P3 = Processo('P3')

print("## 🚀 Início da Simulação dos Relógios de Lamport ##")
print("-" * 50)
print(f"Estados Iniciais: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

mensagem_ts = None 

P1.evento_interno("Início da Tarefa")
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

mensagem_ts = P2.enviar_mensagem(P3)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

P3.receber_mensagem(P2, mensagem_ts)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

mensagem_ts = P1.enviar_mensagem(P2)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

P3.evento_interno("Processamento de Dados")
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

P2.receber_mensagem(P1, mensagem_ts)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

mensagem_ts = P2.enviar_mensagem(P1)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

P1.receber_mensagem(P2, mensagem_ts)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

print("## ✅ Fim da Simulação ##")
print(f"Estados Finais: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")