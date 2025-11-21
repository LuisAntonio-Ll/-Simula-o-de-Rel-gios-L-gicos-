class Processo:
    """Representa um processo em um sistema distribuído com um Relógio Lógico de Lamport."""
    def __init__(self, id_processo):
        # O ID do processo (ex: 'P1', 'P2', 'P3') para identificação.
        self.id = id_processo
        # O Relógio Lógico de Lamport (TS - Timestamp), inicializado em 0.
        self.relogio = 0

    def evento_interno(self, descricao):
        """
        Simula um evento interno (local) no processo.
        Implementa a Regra 1 de Lamport: Incrementa o relógio antes de executar o evento.
        """
        # Regra 1: Incrementa o relógio.
        self.relogio += 1
        # Imprime o estado do processo e seu novo timestamp.
        print(f"[{self.id} | TS={self.relogio}]: Evento Interno - {descricao}")
        
        return self.relogio

    def enviar_mensagem(self, destinatario):
        """
        Simula o envio de uma mensagem para outro processo.
        Implementa a Regra 1 (incremento) e a Regra 2 (inclusão do TS).
        """
        # Regra 1: O processo incrementa seu relógio ANTES de enviar a mensagem.
        self.relogio += 1

        # Regra 2 (Envio): Inclui o timestamp atual na mensagem.
        timestamp_enviado = self.relogio
        
        print(f"[{self.id} | TS={self.relogio}]: Envia mensagem para {destinatario.id} com TS={timestamp_enviado}")
        
        # O timestamp é retornado para ser usado na função 'receber_mensagem'.
        return timestamp_enviado

    def receber_mensagem(self, remetente, timestamp_recebido):
        """
        Simula o recebimento de uma mensagem de outro processo.
        Implementa a Regra 2 (ajuste) e a Regra 1 (incremento).
        """
        # Guarda o relógio antes do ajuste para fins de log/visualização.
        relogio_antes = self.relogio
        
        # Regra 2 (Ajuste): L_j = max(L_j, t)
        # O relógio do receptor é ajustado para o máximo entre seu valor atual 
        # e o timestamp da mensagem recebida.
        self.relogio = max(self.relogio, timestamp_recebido)

        # Regra 1: O processo incrementa seu relógio APÓS o ajuste do max.
        # Isso garante que o evento de recebimento tenha um TS estritamente maior 
        # que o evento de envio (causalidade preservada: Envio -> Recebimento).
        self.relogio += 1

        # Logs detalhados do recebimento e ajuste.
        print(f"[{self.id} | TS={self.relogio}]: Recebe mensagem de {remetente.id} (TS_envio={timestamp_recebido}).")
        print(f"    * Ajuste: max({relogio_antes}, {timestamp_recebido}) -> Relógio atualizado para {self.relogio} (após incremento)")

        return self.relogio
    
# --- Inicialização e Simulação ---

# Criação das instâncias dos 3 processos.
P1 = Processo('P1')
P2 = Processo('P2')
P3 = Processo('P3')

print("## 🚀 Início da Simulação dos Relógios de Lamport ##")
print("-" * 50)
print(f"Estados Iniciais: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

# Variável para armazenar o timestamp da mensagem que está "em trânsito" entre os eventos.
mensagem_ts = None 

# 1. P1: Evento interno (Regra 1)
P1.evento_interno("Início da Tarefa")
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

# 2. P2: Envia mensagem para P3 (Regras 1 e 2)
mensagem_ts = P2.enviar_mensagem(P3)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

# 3. P3: Recebe mensagem de P2 (Regras 2 e 1)
P3.receber_mensagem(P2, mensagem_ts)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

# 4. P1: Envia mensagem para P2 (Regras 1 e 2)
mensagem_ts = P1.enviar_mensagem(P2)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

# 5. P3: Evento interno (Regra 1)
P3.evento_interno("Processamento de Dados")
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

# 6. P2: Recebe mensagem de P1 (Regras 2 e 1)
P2.receber_mensagem(P1, mensagem_ts)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

# 7. P2: Envia mensagem para P1 (Regras 1 e 2)
mensagem_ts = P2.enviar_mensagem(P1)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

# 8. P1: Recebe mensagem de P2 (Regras 2 e 1)
P1.receber_mensagem(P2, mensagem_ts)
print(f"Estados: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")
print("-" * 50)

print("## ✅ Fim da Simulação ##")
print(f"Estados Finais: P1={P1.relogio}, P2={P2.relogio}, P3={P3.relogio}")