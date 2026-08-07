# Memória da conversa
memoria_conversa = []

def adicionar_interacao(pergunta, resposta):
    """
    Armazena uma interação entre o usuário e o Ollama.
    """
    memoria_conversa.append({
        "usuario": pergunta,
        "ollama": resposta
    })

def obter_historico():
    """
    Retorna o histórico completo da conversa.
    """
    return memoria_conversa

# Exemplo de uso

pergunta = "Há máscaras N95 disponíveis no estoque?"
resposta = "Atualmente o estoque de máscaras N95 está abaixo do nível mínimo recomendado."

adicionar_interacao(pergunta, resposta)

pergunta = "Qual material possui maior quantidade disponível?"
resposta = "As luvas descartáveis apresentam a maior quantidade disponível em estoque."

adicionar_interacao(pergunta, resposta)

# Exibe o histórico
for i, conversa in enumerate(obter_historico(), start=1):
    print(f"Interação {i}")
    print(f"Usuário: {conversa['usuario']}")
    print(f"Ollama: {conversa['ollama']}\n")