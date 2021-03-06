import sys
import os.path
import csv
import argparse

idxUf = 3
idxCod = 4
idxNome = 5

controlVerbose = False

dictMunicipios = dict()
notProcessedLines = list()

def setLimit(limit):
    global controlLimit
    controlLimit = limit

def extractMunicipio(line):

    uf = line[idxUf]
    cod = line[idxCod]
    nom = line[idxNome].replace("'", "`")

    if cod not in dictMunicipios:
        dictMunicipios[cod] = (uf, nom)

def processLine(line, linenumber):
    
    global controlVerbose

    if type(line) is list and len(line) > idxNome:
        extractMunicipio(line)
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
            for key, value in dictMunicipios.items():
                row = list()
                row.append(key)
                row.append(value[0])
                row.append(value[1])
                writer.writerow(row)
    else:
        writer = csv.writer(sys.stdout, delimiter=";")
        for key, value in dictMunicipios.items():
            row = list()
            row.append(key)
            row.append(value[0])
            row.append(value[1])
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
        print(os.path.basename(__file__) + "Procedimento encerrado, {} linhas escritas".format(len(dictMunicipios)))

def parseArgs():
    
    parser = argparse.ArgumentParser("Extrair Municípios do Perfil de Eleitores - Dados Abertos do TSE")
    parser.add_argument("-f", "--file", help="Arquivo do Perfil de Eleitores segundo o Padrão TSE pós 2016")
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

    