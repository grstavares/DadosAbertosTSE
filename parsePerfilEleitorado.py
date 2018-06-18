import argparse
import os.path

import utils
import dadosAbertos as dados
from parseMunicipios import Main as parseMunicipios
from parseZonasEleitorais import Main as parseZonasEleitorais
from parseDemografia import Main as parseDemografia

def Main(filesMap, outputdir, limit):

    listaPerfilEleitores = filesMap[dados.kPerfilEleitores()]
    fileMunicipios = os.path.join(outputdir, "municipios.txt")
    fileZonasEleitorais = os.path.join(outputdir, "zonasEleitorais.txt")
    fileDemografia  = os.path.join(outputdir, "DadosDemograficos.txt")
    utils.createPath(fileMunicipios)

    for filename in listaPerfilEleitores:
        parseMunicipios(filename, fileMunicipios, limit)
        parseZonasEleitorais(filename, fileZonasEleitorais, limit)
        parseDemografia(filename, fileDemografia, limit)

def parseArgs():
    
    parser = argparse.ArgumentParser("Extrar Informações existentes no Arquivo de Perfil de Eleitores - Dados Abertos do TSE")
    parser.add_argument("-f", "--file", help="Arquivo do Perfil de Eleitores segundo o Padrão TSE pós 2016")
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
        Main(args.file, args.output, limit)

    else:
        print("Arquivo de Entrada Inexistente!")