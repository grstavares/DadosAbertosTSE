import sys
import os.path
import csv
import argparse

idTse = 11
idxAno = 2
idxTurno = 3
idxDesc = 4
idxUF = 5
idxCargo = 9
idxNum = 12
idxResult = 44

controlVerbose = False

dictCandidatura = list()
notProcessedLines = list()

def extractCandidatura(line):

    idT = line[idTse]
    ano = line[idxAno]
    tur = line[idxTurno]
    des = line[idxDesc].replace("'", "`")
    uf = line[idxUF]
    car = line[idxCargo].replace("'", "`")
    num = line[idxNum]
    res = line[idxResult]

    item = (idT, ano, tur, des, uf, car, num, res)
    dictCandidatura.append(item)

def processLine(line, linenumber):
    
    global controlVerbose

    if type(line) is list and len(line) > idxNum:
        extractCandidatura(line)
    else:
        notProcessedLines.append((linenumber, line))
        if controlVerbose:
            print("linha {} não pode ser processada!".format(linenumber))
        
def iterateTroughReader(reader, limit):

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
            for item in dictCandidatura:
                writer.writerow(item)
    else:
        writer = csv.writer(sys.stdout, delimiter=";")
        for item in dictCandidatura:
            writer.writerow(item)

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
        print(os.path.basename(__file__) + "Procedimento encerrado, {} linhas escritas".format(len(dictCandidatos)))

def parseArgs():
    
    parser = argparse.ArgumentParser("Extrair Candidatos do Perfil de Candidatos - Dados Abertos do TSE")
    parser.add_argument("-f", "--file", help="Arquivo do Perfil de Candidatos segundo o Padrão TSE pós 2014")
    parser.add_argument("-o", "--output", help="Nome do Arquivo de Destino")
    parser.add_argument("-l", "--limit", help="Limitar número de linhas a serem processadas")
    parser.add_argument("-v", "--verbose", help="Show filenames to be changed before Confirmation", action="store_true")

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

    