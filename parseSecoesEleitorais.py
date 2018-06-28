import argparse
import os.path

import utils
import dadosAbertos as dados
from parseVotacao import Main as parseVotacao

def Main(filesMap, outputdir, limit):

    listaSessoes = filesMap[dados.kVotacaoCandidatos()]
    fileVotacao = os.path.join(outputdir, "votacoes.txt")
    utils.createPath(fileVotacao)

    for filename in listaSessoes:
        parseVotacao(filename, fileVotacao, limit)

def parseArgs():
    
    parser = argparse.ArgumentParser("Extrar Informações existentes no Arquivo de Votos da Seção Eleitoral - Dados Abertos do TSE")
    parser.add_argument("-f", "--file", help="Arquivo do Perfil de Candidatos segundo o Padrão TSE pós 2010")
    parser.add_argument("-o", "--output", help="Nome do Diretório de Destino")
    parser.add_argument("-l", "--limit", help="Limitar número de linhas a serem processadas")
    parser.add_argument("-v", "--verbose", help="Informar atividades em nível de depuração", action="store_true")

    return parser.parse_args()

if __name__ == '__main__':
    
    args = parseArgs()
    controlVerbose = args.verbose

    inputFile = args.file
    limit = 0 if args.limit == None else int(args.limit)

    if os.path.exists(inputFile):
        inputMap = utils.getMapFromFile(inputFile)
        if inputMap == None:
            print("Arquivo de Entrada Inválido!")    
        else:
            Main(inputMap, args.output, limit)

    else:
        print("Arquivo de Entrada Inexistente!")