import argparse
import sqlite3

def connect(fileoutput):

    conn = sqlite3.connect(fileoutput)
    with open('db.schema', 'r') as schema:
        statements = schema.read()
        cursor = conn.cursor()
        cursor.executescript(statements)

    return conn

def parseArgs():
    
    parser = argparse.ArgumentParser("Extrair Informações dos Dados Abertos do TSE e inserir em um Novo Banco de Dados")
    parser.add_argument("-d", "--download", help="Mapa com a localização dos Arquivos para Download")
    parser.add_argument("-m", "--filemap", help="Mapa com a localização dos Arquivos de Dados")
    parser.add_argument("-f", "--filter", help="Nome do Arquivo com os critérios de filtro")
    parser.add_argument("-o", "--output", help="Nome do Arquivo/Diretório de Destino")
    parser.add_argument("--generateMap", help="Cria o esqueleto para o mapa de Localização dos Arquivos de Dados", action="store_true")
    parser.add_argument("--generateFilterMap", help="Cria o esqueleto para os Filtros dos Arquivos de Dados", action="store_true")
    parser.add_argument("-l", "--limit", help="Limitar número de linhas a serem processadas")

    return parser.parse_args()

if __name__ == '__main__':
    
    args = parseArgs()
    outputFile = args.output

    connect("teste.db")