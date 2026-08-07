import os
import glob
import re

# Pasta onde estão os documentos da base de conhecimento
PASTA_DOCUMENTOS = "base_conhecimento"

def padronizar_texto(texto):
    """
    Realiza a padronização do texto.
    """
    texto = texto.lower()                     # Converte para minúsculas
    texto = re.sub(r'\n+', ' ', texto)        # Remove quebras de linha
    texto = re.sub(r'\s+', ' ', texto)        # Remove espaços duplicados
    texto = re.sub(r'[^\w\s]', '', texto)     # Remove caracteres especiais
    return texto.strip()

def carregar_documentos():
    """
    Carrega todos os arquivos .txt da pasta e padroniza o conteúdo.
    """
    documentos = []

    arquivos = glob.glob(os.path.join(PASTA_DOCUMENTOS, "*.txt"))

    for arquivo in arquivos:
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        documento = {
            "arquivo": os.path.basename(arquivo),
            "texto_original": conteudo,
            "texto_padronizado": padronizar_texto(conteudo)
        }

        documentos.append(documento)

    return documentos

# Teste
if __name__ == "__main__":
    base = carregar_documentos()

    print(f"Documentos carregados: {len(base)}")

    for doc in base:
        print(f"\nArquivo: {doc['arquivo']}")
        print(doc["texto_padronizado"][:200], "...")