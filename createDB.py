import os
import sys
import ast
import csv
import random
import argparse
import sqlite3
import datetime

import dadosAbertos
import database
import utils
from downloadData import Main as downloadData
from extractData import Main as extractData
from parsePerfilEleitorado import Main as parsePerfilEleitorado

def insertMunicipios(db, outputDir):

    filename = os.path.join(outputDir, 'municipios.txt')
    with open(filename, 'r', encoding='utf-8') as file:
        
        reader = csv.reader(file, delimiter=';')
        counter = 0
        for row in reader:
            cod = row[0]
            uf = row[1]
            nome = row[2]

            statement = "INSERT INTO municipios (cod_tse, uf, nome) VALUES ({}, '{}', '{}');".format(cod, uf, nome)
            db.execute(statement)
            counter += 1
            if counter % 100 == 0:
                statement = 'COMMIT;'
                db.execute(statement)

    statement = 'COMMIT;'
    db.execute(statement)
    print("{} municípios inseridos!".format(counter))

def insertZonas(db, outputDir):

    filename = os.path.join(outputDir, 'zonasEleitorais.txt')
    with open(filename, 'r', encoding='utf-8') as file:
        
        reader = csv.reader(file, delimiter=';')
        counter = 0
        for row in reader:
            mun = row[0]
            zon = row[1]
            qtd = row[2]

            statement = "INSERT INTO zonasEleitorais (cod_municipio, num_zona, qtd_eleitores) VALUES ({}, {}, {});".format(mun, zon, qtd)
            db.execute(statement)
            counter += 1
            if counter % 100 == 0:
                statement = 'COMMIT;'
                db.execute(statement)

    statement = 'COMMIT;'
    db.execute(statement)
    print("{} Zonas Eleitorais inseridas!".format(counter))

def insertDemografia(db, outputDir):

    dictSex = dict()
    dictIda = dict()
    dictEsc = dict()

    filename = os.path.join(outputDir, 'DadosDemograficos.txt')
    with open(filename, 'r', encoding='utf-8') as file:
        
        reader = csv.reader(file, delimiter=';')
        counter = 0
        idCounter = 50
        needcommit = False

        for row in reader:
            mun = row[0]
            zon = row[1]
            sex = row[2]
            ida = row[3]
            esc = row[4]
            qtd = row[5]

            if sex not in dictSex.keys():
                idCounter += 5
                idSex = idCounter
                dictSex[sex] = idSex
                statement = "INSERT INTO enumSexo (id, desc) VALUES ({}, '{}');".format(idSex, sex)
                db.execute(statement)
                needcommit = True
            else:
                idSex = dictSex[sex]

            if ida not in dictIda.keys():
                idCounter += 5
                idIda = idCounter
                dictIda[ida] = idIda
                statement = "INSERT INTO enumIdade (id, desc) VALUES ({}, '{}');".format(idIda, ida)
                db.execute(statement)
                needcommit = True
            else:
                idIda = dictIda[ida]

            if esc not in dictEsc.keys():
                idCounter += 5
                idEsc = idCounter
                dictEsc[esc] = idEsc
                statement = "INSERT INTO enumEscolaridade (id, desc) VALUES ({}, '{}');".format(idEsc, esc)
                db.execute(statement)
                needcommit = True
            else:
                idEsc = dictEsc[esc]

            statement = "INSERT INTO dadosDemograficos (cod_municipio, num_zona, id_sexo, id_idade, id_escolaridade ,qtd_eleitores) VALUES ({}, {}, {}, {}, {}, {});".format(mun, zon, idSex, idIda, idEsc, qtd)
            db.execute(statement)

            counter += 1
            if counter % 100 == 0:
                statement = 'COMMIT;'
                db.execute(statement)
                needcommit = False

    if needcommit:
        statement = 'COMMIT;'
        db.execute(statement)
    
    print("{} Dados Demográficos inseridos!".format(counter))

def Main(fileMap, fileoutput, limit):
    
    print("Extraindo dados do Perfil de Eleitores")
    outputDir = 'parsed_' + str(datetime.datetime.now())
    parsePerfilEleitorado(fileMap, outputDir, limit)

    db = database.connect(fileoutput)
    insertMunicipios(db, outputDir)
    insertZonas(db, outputDir)
    insertDemografia(db, outputDir)

    utils.clearDir(outputDir)

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
    parser.add_argument("-o", "--output", help="Nome do Arquivo/Diretório de Destino")
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

        if inputFile == None and downloadFile == None:
            print("Você deve informar um Arquivo com as urls para download ou um Mapa com a localização dos arquivos já baixados!")

        if inputFile != None:
            map = getFileMap(inputFile)
            Main(map, outputFile, limit)

        if downloadFile != None:
            downloadDict = getFileMap(downloadFile)
            map = downloadData(downloadDict, 'downloaded')

            allExtracted = dict()
            datePart = str(datetime.date.today())
            for key, value in map.items():
                dirname = os.path.join('extracted', key, datePart)
                extractedFiles = extractData(value, dirname)
                allExtracted[key] = extractedFiles

            Main(allExtracted, outputFile, limit)