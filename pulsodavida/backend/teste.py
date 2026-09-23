#inportaçães
import csv
import pathlib from pathlib

CAMINHO ="../pulsodavida/database/dados.csv"
import pandas as pd

def carregar_dados():
    dados = pd.read_csv(CAMINHO, sep=";")
    print("Dados carregados com sucesso!")
    return dados

#def carregar dados

def analisar_estrutura(dados):

    print("\n===== ESTRUTURA DOS DADOS =====")

    print("\nPrimeiras linhas:")
    print(dados.head())

    print("\nDimensões:")
    print(dados.snape)

    print("\nTipos")
    print(dados.dtypes)

    print("\nValores ausentes:")
    print(dados.isnull().sum())






def main(): 
    df = carregar_dados(CAMINHO)
    print(df.head())

    analisar_estrutura(dados)
 
    if __name__ == __main__:
        main()
