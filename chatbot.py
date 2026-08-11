# -*- coding: utf-8 -*-
"""
chatbot.py
----------
Chatbot "GestorHospitalar" — Sistema de Monitoramento de Insumos Básicos.
"""

from __future__ import annotations
import sys

from analise_dados import carregar_dados, AnalisadorInsumos
from cliente_ollama import perguntar_ao_modelo, servidor_disponivel, ErroOllama, MODELO_PADRAO

PROMPT_SISTEMA = """Você é o "GestorHospitalar", um assistente virtual especializado na \
gestão de estoque, insumos e materiais hospitalares.

Regras obrigatórias:
- Você SEMPRE recebe, junto da pergunta do usuário, um bloco "DADOS CALCULADOS" \
  extraído diretamente do banco de dados do hospital via Pandas.
- Use estritamente as informações e números fornecidos. NUNCA invente itens, quantidades ou prazos.
- Forneça respostas técnicas, diretas e adequadas ao ambiente hospitalar.
- Em caso de itens em nível crítico ou zerados, destaque o aviso de atenção.
- Se o bloco de dados vier vazio ou indicar intenção não reconhecida, responda educadamente \
  que não possui essa informação no momento e sugira exemplos de consulta (ex.: saldo de item, \
  materiais a vencer, alternativas de substituição ou custos por categoria).
"""


def roteador_de_intencao(pergunta: str, analisador: AnalisadorInsumos) -> str:
    """Mapeia palavras-chave para consultas do banco de dados de insumos."""
    p = pergunta.lower()

    # Consulta de saldo / localização / estoque específico
    if "onde encontro" in p or "saldo" in p or "quantidade" in p or "temos" in p:
        for item in ["soro", "seringa", "máscara", "mascara", "agulha", "gaze", "luva", "bomba", "cateter"]:
            if item in p:
                termo_busca = "máscara" if item == "mascara" else item
                dados = analisador.saldo_item(termo_busca)
                if not dados.empty:
                    return f"Saldo do item '{termo_busca}':\n{dados.to_string(index=False)}"
        dados = analisador.itens_zerados_ou_criticos()
        return f"Itens em nível crítico ou zerado:\n{dados.to_string(index=False)}"

    # Substituição / alternativas para falta de insumos
    if "substitu" in p or "alternativa" in p or "trocar" in p or "em falta" in p:
        for item in ["soro", "seringa", "máscara", "mascara", "agulha", "gaze", "luva", "cateter"]:
            if item in p:
                termo_busca = "máscara" if item == "mascara" else item
                dados = analisador.buscar_substituto(termo_busca)
                if not dados.empty:
                    return f"Alternativas/substitutos cadastrados para '{termo_busca}':\n{dados.to_string(index=False)}"
        return "Para consultar substitutos, informe o nome do insumo (ex.: soro, seringa, agulha, cateter)."

    # Vencimento / validade / lotes a vencer
    if "venc" in p or "validade" in p or "vencer" in p or "lote" in p:
        dados = analisador.itens_proximos_vencimento(dias=30)
        return f"Itens com vencimento nos próximos 30 dias:\n{dados.to_string(index=False)}"

    # Custo / valor gasto
    if "custo" in p or "gasto" in p or "financeiro" in p or "valor" in p:
        dados = analisador.custo_por_categoria()
        return f"Consolidado financeiro por categoria de insumo:\n{dados.to_string(index=False)}"

    # Locais / almoxarifados / setores
    if "setor" in p or "local" in p or "almoxarifado" in p or "onde" in p:
        locais = ", ".join(analisador.listar_locais())
        return f"Setores e almoxarifados registrados na base: {locais}"

    return ""  # Intenção não reconhecida


def montar_mensagens(pergunta: str, dados_calculados: str, historico: list[dict]) -> list[dict]:
    bloco_dados = dados_calculados if dados_calculados else "(nenhuma intenção reconhecida para esta pergunta)"

    mensagem_usuario = (
        f"PERGUNTA DO USUÁRIO: {pergunta}\n\n"
        f"DADOS CALCULADOS:\n{bloco_dados}"
    )

    mensagens = [{"role": "system", "content": PROMPT_SISTEMA}]
    mensagens.extend(historico)
    mensagens.append({"role": "user", "content": mensagem_usuario})
    return mensagens


def executar_chat() -> None:
    print("=" * 60)
    print(" GestorHospitalar — Sistema de Monitoramento de Insumos")
    print(" (Python + Pandas + Ollama)")
    print("=" * 60)

    if not servidor_disponivel():
        print(
            "\n[AVISO] Não foi possível conectar ao Ollama em http://localhost:11434.\n"
            "Certifique-se de executar 'ollama serve' em um terminal separado.\n"
            f"Modelo configurado: {MODELO_PADRAO}\n"
        )
        sys.exit(1)

    df = carregar_dados()
    analisador = AnalisadorInsumos(df)

    print(
        "\nExemplos de perguntas aceitas:\n"
        "  - Onde encontro soro fisiológico 0,9% no momento?\n"
        "  - Qual o saldo atual de seringas no Almoxarifado Central?\n"
        "  - Qual o substituto recomendado para agulha em falta?\n"
        "  - Qais materiais vencem nos próximos 30 dias?\n"
        "  - Qual é o custo total em estoque por categoria?\n"
        "Digite 'sair' para encerrar.\n"
    )

    historico: list[dict] = []

    while True:
        pergunta = input("Você: ").strip()
        if not pergunta:
            continue
        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("GestorHospitalar: Encerrando sessão de monitoramento.")
            break

        dados_calculados = roteador_de_intencao(pergunta, analisador)
        mensagens = montar_mensagens(pergunta, dados_calculados, historico)

        try:
            resposta = perguntar_ao_modelo(mensagens)
        except ErroOllama as erro:
            print(f"\n[ERRO] {erro}\n")
            continue

        print(f"\nGestorHospitalar: {resposta}\n")

        historico.append({"role": "user", "content": pergunta})
        historico.append({"role": "assistant", "content": resposta})
        historico[:] = historico[-6:]


if __name__ == "__main__":
    executar_chat()