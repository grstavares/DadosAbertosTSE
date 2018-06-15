import os
import sys
import ast
import random
import argparse
import sqlite3
import datetime

import dadosAbertos
from downloadData import Main as downloadData
from extractData import Main as extractData
from parseMunicipios import Main as parseMunicipios
from parseZonasEleitorais import Main as parseZonas

def connect():
    print("Conectado!")

def insertMunicipios():
    print("Inserindo Municípios...")

def insertZonas():
    print("Inserindo Zonas...")

def Main(fileMap, fileoutput, limit):
    
    eleitores = fileMap[dadosAbertos.kPerfilEleitores()]
    #votacao = fileMap[kVotacaoCandidatos]

    uniqueName = random.randint(1, 999999)
    fileMunicipios = str(uniqueName).zfill(6) + kMunicipios + ".tmp"
    fileZonas = str(uniqueName).zfill(6) + kZonasEleitorais + ".tmp"

    parseMunicipios(eleitores, fileMunicipios, limit)
    parseZonas(eleitores, fileZonas, limit)

    connect()
    insertMunicipios()
    insertZonas()

    os.remove(fileMunicipios)
    os.remove(fileZonas)

    print("Done!")

def generateMap(output):
    
    fileMap = dict()
    placeholder = 'INSERT URL HERE!'

    for item in dadosAbertos.allKeys():
        fileMap[item] = placeholder
    
    if output != None:
        with open(output, 'w', newline = '', encoding = "utf-8") as file:
            file.write(str(fileMap))
    
    else:
        sys.stdout.write(str(fileMap))

def generateFilterMap(output):
    
    fileMap = dict()
    filters = {'UF':'INSERT HERE', 'ANO':'INSERT HERE'}

    for item in dadosAbertos.allKeys():
        fileMap[item] = filters
    
    if output != None:
        with open(output, 'w', newline = '', encoding = "utf-8") as file:
            file.write(str(fileMap))
    
    else:
        sys.stdout.write(str(fileMap))

def parseArgs():
    
    parser = argparse.ArgumentParser("Extrair Informações dos Dados Abertos do TSE e inserir em um Novo Banco de Dados")
    parser.add_argument("-d", "--download", help="Mapa com a localização dos Arquivos para Download")
    parser.add_argument("-m", "--filemap", help="Mapa com a localização dos Arquivos de Dados")
    parser.add_argument("-f", "--filter", help="Nome do Arquivo com os critérios de filtro")
    parser.add_argument("-o", "--output", help="Nome do Arquivo de Destino")
    parser.add_argument("--generateMap", help="Cria o esqueleto para o mapa de Localização dos Arquivos de Dados", action="store_true")
    parser.add_argument("--generateFilterMap", help="Cria o esqueleto para os Filtros dos Arquivos de Dados", action="store_true")
    parser.add_argument("-l", "--limit", help="Limitar número de linhas a serem processadas")

    return parser.parse_args()

def getFileMap(inputFile):
    
    with open(inputFile, 'r') as file:
        content = file.read()
        return ast.literal_eval(content)

def inputMap(args):
    
    if args.filemap != None:
        map = getFileMap(args.filemap)
        return map
    
    if args.download != None:
        map = downloadData(args.download, 'donwloaded')
        return map
    
    return None

if __name__ == '__main__':
    
    args = parseArgs()
    outputFile = args.output

    if args.generateMap:
        generateMap(outputFile)
    elif args.generateFilterMap:
        generateFilterMap(outputFile)
    else:
        
        inputFile = args.filemap
        downloadFile = args.download
        limit = 0 if args.limit == None else int(args.limit)

        if inputFile != None:
            map = getFileMap(inputFile)
            Main(map, outputFile, limit)
        
        if downloadFile != None:
            #downloadDict = getFileMap(downloadFile)
            #map = downloadData(downloadDict, 'downloaded')
            map = getFileMap('downloadManifest.map')

            allExtracted = dict()
            for key, value in map.items():
                dirname = key + str(datetime.date.today())
                extractedFiles = extractData(value, dirname)
                allExtracted[key] = extractedFiles

            with open(outputFile, 'w', newline = '', encoding = "utf-8") as file:
                file.write(str(allExtracted))

            #Main(map, outputFile, limit)