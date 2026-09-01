import csv
import sqlite3

# Conteúdo dos dados do CSV
dados_csv = """Id;categoria;pergunta;resposta;intencao
1;"Estoque";"Quais materiais estão em falta?";"Os materiais em situação crítica precisam de atenção e reposição prioritária.";"consultar_falta"
2;"Estoque";"Quais materiais estão em situação crítica?";"Os materiais classificados como Crítico precisam de reposição prioritária.";"consultar_criticos"
3;"Estoque";"Quais materiais estão em alerta?";"Os materiais classificados como Alerta estão abaixo do estoque mínimo.";"consultar_alerta"
4;"Estoque";"Como consultar a quantidade de um material?";"Informe o nome do material para consultar sua quantidade registrada no estoque.";"consultar_quantidade"
5;"Cadastro";"Como cadastrar um material?";"Informe nome, categoria, quantidade em estoque, quantidade mínima e localização.";"cadastrar_material"
"""

# Criação da conexão com o banco SQLite (cria o arquivo 'banco_projeto.db')
conn = sqlite3.connect("banco_projeto.db")
cursor = conn.cursor()

# Criação da tabela
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS base_conhecimento (
    id INTEGER PRIMARY KEY,
    categoria TEXT NOT NULL,
    pergunta TEXT NOT NULL,
    resposta TEXT NOT NULL,
    intencao TEXT NOT NULL
)
"""
)

# Leitura e inserção dos dados
linhas = dados_csv.strip().split("\n")[1:]  # Ignora o cabeçalho
for linha in csv.reader(linhas, delimiter=";"):
    if linha:
        cursor.execute(
            """
            INSERT INTO base_conhecimento (id, categoria, pergunta, resposta, intencao)
            VALUES (?, ?, ?, ?, ?)
        """,
            (int(linha[0]), linha[1], linha[2], linha[3], linha[4]),
        )

# Salva as alterações e fecha a conexão
conn.commit()
conn.close()

print("Arquivo de banco de dados 'banco_projeto.db' criado com sucesso!")