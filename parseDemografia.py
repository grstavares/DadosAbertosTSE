import sys
import os.path
import csv
import argparse

idxMunicipio = 4
idxZona = 6
idxSecao = 7
idxCodEstadoCivil = 8
idxDesEstadoCivil = 9
idxCodFaixaEtaria = 10
idxDesFaixaEtaria = 11
idxCodEscolaridade = 12
idxDesEscolaridade = 13
idxCodSexo = 14
idxDesSexo = 15
idxQtd = 16

controlVerbose = False

dictSecoes = dict()
notProcessedLines = list()

def extractZona(line):

    municipio = line[idxMunicipio]
    zona = line[idxZona]
    secao = line[idxSecao]
    codEstado = line[idxCodEstadoCivil]
    estadoCivil = line[idxDesEstadoCivil].replace("'", "`")
    codSexo = line[idxCodSexo]
    sexo = line[idxDesSexo].replace("'", "`")
    codFaixa = line[idxCodFaixaEtaria]
    faixa = line[idxDesFaixaEtaria].replace("'", "`")
    codEsc = line[idxCodEscolaridade]
    escolaridade = line[idxDesEscolaridade].replace("'", "`")
    qtd = int(line[idxQtd])

    key = (municipio, zona, secao, codSexo, codEstado, codFaixa, codEsc)
    if key in dictSecoes:
        dictSecoes[key] += qtd
    else:
        dictSecoes[key] = qtd

def processLine(line, linenumber):
    
    global controlVerbose

    if type(line) is list and len(line) > idxQtd:
        extractZona(line)
    else:
        notProcessedLines.append((linenumber, line))
        if controlVerbose:
            print("linha {} não pode ser processada!".format(linenumber))
        
def iterateTroughReader(reader, limit):
    
    global controlLimit

    count = 0
    for row in reader:
        processLine(row, count)
        count += 1
        if controlVerbose and count % 100 == 0:
            print("{} linhas processadas...".format(count))

        if limit > 0 and count == limit:
            break

def readInput(filename, limit):
    
    global controlVerbose

    reader = None
    if filename != None:
        if controlVerbose:
            print("Abrindo Arquivo...")

        with open(filename, 'r', encoding='ISO-8859-1') as file:
            reader = csv.reader(file, delimiter=';')
            iterateTroughReader(reader, limit)

    else:
        if controlVerbose:
            print("Lendo a partir da StdIn...")

        reader = csv.reader(sys.stdin, delimiter = ';')
        iterateTroughReader(reader, limit)

def writeOutput(filename):
    
    if filename != None:

        if os.path.exists(filename):
            writeMode = 'a' # append
        else:
            writeMode = 'w' # make a new file

        with open(filename, writeMode, newline = '', encoding = "utf-8") as file:
            if controlVerbose:
                print("Abrindo Arquivo de saída {}...".format(filename))

            writer = csv.writer(file, delimiter=";")
            for key, value in dictSecoes.items():
                row = list()
                row.append(key[0])
                row.append(key[1])
                row.append(key[2])
                row.append(key[3])
                row.append(key[4])
                row.append(key[5])
                row.append(key[6])
                row.append(value)
                writer.writerow(row)
    else:
        writer = csv.writer(sys.stdout, delimiter=";")
        for key, value in dictSecoes.items():
            row = list()
            row.append(key[0])
            row.append(key[1])
            row.append(key[2])
            row.append(key[3])
            row.append(key[4])
            row.append(value)
            writer.writerow(row)

    if controlVerbose:
        print("Escrevendo no arquivo de saída...")

def Main(fileinput, fileoutput, limit):

    if not os.path.exists(fileinput):
        print(os.path.basename(__file__) + " -> Arquivo de Entrada Inexistente!")
        return

    global controlVerbose

    readInput(fileinput, limit)
    writeOutput(fileoutput)

    if controlVerbose:
        print(os.path.basename(__file__) + "Procedimento encerrado, {} linhas escritas".format(len(dictSecoes)))
   
def parseArgs():
    
    parser = argparse.ArgumentParser("Extrair Dados Demográficos do Perfil de Eleitores - Dados Abertos do TSE")
    parser.add_argument("-f", "--file", help="Arquivo do Perfil de Eleitores segundo o Padrão TSE pós 2016")
    parser.add_argument("-o", "--output", help="Nome do Arquivo de Destino")
    parser.add_argument("-l", "--limit", help="Limitar número de linhas a serem processadas")
    parser.add_argument("-v", "--verbose", help="Show filenames to be changed before Confirmation", action="store_true")

    return parser.parse_args()

if __name__ == '__main__':
    
    args = parseArgs()
    controlVerbose = args.verbose
    controlLimit = 0 if args.limit == None else int(args.limit)

    inputFile = args.file
    limit = 0 if args.limit == None else int(args.limit)

    if os.path.exists(inputFile):
        Main(args.file, args.output, limit)

    else:
        print("Arquivo de Entrada Inexistente!")