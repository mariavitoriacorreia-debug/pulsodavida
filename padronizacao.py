import re
import unicodedata

def tratar_texto(texto):
    """
    Remove formatações indesejadas e padroniza o texto
    antes do envio ao Ollama.
    """

    # Remove acentos
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ASCII', 'ignore').decode('utf-8')

    # Converte para minúsculas
    texto = texto.lower()

    # Remove URLs
    texto = re.sub(r'http\S+|www\S+', '', texto)

    # Remove caracteres especiais, mantendo letras, números e espaços
    texto = re.sub(r'[^a-z0-9\s]', ' ', texto)

    # Remove espaços duplicados
    texto = re.sub(r'\s+', ' ', texto)

    return texto.strip()


# Exemplo de uso
texto_bruto = """
Relatório Hospitalar - 2025

O estoque de máscaras N95 está abaixo do mínimo.
Mais informações em: https://hospital.com/estoque
"""

texto_limpo = tratar_texto(texto_bruto)

print("Texto tratado:")
print(texto_limpo)