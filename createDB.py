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
from parseCandidaturas import Main as parseCandidaturas
from parseSecoesEleitorais import Main as parseSecoesEleitorais

def insertMasterData(db, outputDir):

    filename = os.path.join(outputDir, 'masterData.txt')
    masterDataDict = getFileMap(filename)
    counter = 0

    estadoCivil = masterDataDict['EstadoCivil']
    for key, value in estadoCivil.items():
            statement = "INSERT INTO enumEstadoCivil (id, desc) VALUES ({}, '{}');".format(key, value)
            db.execute(statement)
            counter += 1

    escolaridade = masterDataDict['Escolaridade']
    for key, value in escolaridade.items():
            statement = "INSERT INTO enumEscolaridade (id, desc) VALUES ({}, '{}');".format(key, value)
            db.execute(statement)
            counter += 1

    faixaEtaria = masterDataDict['FaixaEtaria']
    for key, value in faixaEtaria.items():
            statement = "INSERT INTO enumIdade (id, desc) VALUES ({}, '{}');".format(key, value)
            db.execute(statement)
            counter += 1

    sexo = masterDataDict['Sexo']
    for key, value in sexo.items():
            statement = "INSERT INTO enumSexo (id, desc) VALUES ({}, '{}');".format(key, value)
            db.execute(statement)
            counter += 1

    statement = 'COMMIT;'
    db.execute(statement)
    print("{} dados mestres inseridos!".format(counter))

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
            sec = row[2]
            qtd = row[3]

            statement = "INSERT INTO zonasEleitorais (cod_municipio, num_zona, num_secao, qtd_eleitores) VALUES ({}, {}, {}, {});".format(mun, zon, sec, qtd)
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
            sec = row[2]
            sex = row[3]
            est = row[4]
            ida = row[5]
            esc = row[6]
            qtd = row[7]

            statement = "INSERT INTO dadosDemograficos (cod_municipio, num_zona, num_secao, id_sexo, id_estadoCivil, id_idade, id_escolaridade ,qtd_eleitores) VALUES ({}, {}, {}, {}, {}, {}, {}, {});".format(mun, zon, sec, sex, est, ida, esc, qtd)
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

def insertCandidatos(db, outputDir):
    
    filename = os.path.join(outputDir, 'candidatos.txt')
    with open(filename, 'r', encoding='utf-8') as file:
        
        reader = csv.reader(file, delimiter=';')
        counter = 0
        for row in reader:
            cod = row[0]
            cpf = row[1]
            nom = row[2]
            par = row[3]
            dat = row[4]
            sex = row[5]
            ins = row[6]
            est = row[7]
            rac = row[8]
            nac = row[9]
            ema = row[10]

            statement = "INSERT INTO candidatos (num_tse, num_cpf, nome_completo, sigla_partido, data_nascimento, sexo, grau_instrucao, estado_civil, raca_informada, nacionalidade, email)"
            statement += " VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(cod, cpf, nom, par, dat, sex, ins, est, rac, nac, ema)
            db.execute(statement)
            counter += 1
            if counter % 100 == 0:
                statement = 'COMMIT;'
                db.execute(statement)

    statement = 'COMMIT;'
    db.execute(statement)
    print("{} candidatos inseridos!".format(counter))

def insertCandidaturas(db, outputDir):
    
    filename = os.path.join(outputDir, 'eleicoes.txt')
    with open(filename, 'r', encoding='utf-8') as file:
        
        reader = csv.reader(file, delimiter=';')
        counter = 0
        for row in reader:
            cod = row[0]
            ano = row[1]
            tur = row[2]
            des = row[3]
            uf = row[4]
            car = row[5]
            num = row[6]
            res = row[7]

            statement = "INSERT INTO eleicoes (num_tse, ano, turno, num_urna, uf, desc, cargo, resultado)"
            statement += " VALUES ({}, {}, {}, {}, '{}', '{}', '{}', '{}');".format(cod, ano, tur, num, uf, des, car, res)
            db.execute(statement)
            counter += 1
            if counter % 100 == 0:
                statement = 'COMMIT;'
                db.execute(statement)

    statement = 'COMMIT;'
    db.execute(statement)
    print("{} candidaturas inseridas!".format(counter))

def insertEleicoes(db, outputDir):
    
    filename = os.path.join(outputDir, 'votacoes.txt')
    with open(filename, 'r', encoding='utf-8') as file:
        
        reader = csv.reader(file, delimiter=';')
        counter = 0
        for row in reader:
            ano = row[0]
            tur = row[1]
            mun = row[2]
            zon = row[3]
            sec = row[4]
            car = row[5]
            num = row[6]
            qtd = row[7]
            des = row[8]
            uf = row[9]

            statement = "INSERT INTO votacoes (ano, turno, cod_municipio, num_zona, num_secao, num_urna, qtd_votos, desc, cargo)"
            statement += " VALUES ({}, {}, {}, {}, {}, {}, {}, '{}', '{}');".format(ano, tur, mun, zon, sec, num, qtd, des, car)
            db.execute(statement)
            counter += 1
            if counter % 100 == 0:
                statement = 'COMMIT;'
                db.execute(statement)

    statement = 'COMMIT;'
    db.execute(statement)
    print("{} votações de seções eleitorais inseridas!".format(counter))

def Main(fileMap, fileoutput, limit):
    
    outputDir = 'parsed_' + str(datetime.datetime.now())

    print("Extraindo dados do Perfil de Eleitores...")
    parsePerfilEleitorado(fileMap, outputDir, limit)

    print("Extraindo dados do Perfil de Candidatos...")
    parseCandidaturas(fileMap, outputDir, limit)

    print("Extraindo dados do resultado das Seções Eleitorais...")
    parseSecoesEleitorais(fileMap, outputDir, limit)

    print("Criando Banco de Dados...")
    
    db = database.connect(fileoutput)
    insertMasterData(db, outputDir)
    insertMunicipios(db, outputDir)
    insertZonas(db, outputDir)
    insertDemografia(db, outputDir)
    insertCandidatos(db, outputDir)
    insertCandidaturas(db, outputDir)
    insertEleicoes(db, outputDir)

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
    parser.add_argument("-u", "--uf", help="Filtrar processamento por UF")
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
    uf = args.uf

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
                extractedFiles = extractData(value, dirname, uf)
                allExtracted[key] = extractedFiles

            Main(allExtracted, outputFile, limit)