
import sys
import os.path
import csv
import argparse

idTse = 11
idxNome = 10
idxCpf = 13
idxPartido = 18
idxNascimento = 26
idxSexo = 30
idxInstrucao = 32
idxEstadoCivil = 34
idxRaca = 36
idxNacionalidade = 38
idxEmail = 45

controlVerbose = False

dictCandidatos = dict()
notProcessedLines = list()

def extractCandidato(line):

    idT = line[idTse]
    cpf = line[idxCpf]
    nom = line[idxNome].replace("'", "`")
    par = line[idxPartido].replace("'", "`")
    dat = line[idxNascimento]
    sex = line[idxSexo].replace("'", "`")
    ins = line[idxInstrucao].replace("'", "`")
    est = line[idxEstadoCivil].replace("'", "`")
    rac = line[idxRaca].replace("'", "`")
    nac = line[idxNacionalidade].replace("'", "`")
    ema = line[idxEmail].replace("'", "`")

    if idT not in dictCandidatos:
        dictCandidatos[idT] = (cpf, nom, par, dat, sex, ins, est, rac, nac, ema)

def processLine(line, linenumber):
    
    global controlVerbose

    if type(line) is list and len(line) > idxNome:
        extractCandidato(line)
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
            for key, value in dictCandidatos.items():
                row = list()
                row.append(key)
                row.append(value[0])
                row.append(value[1])
                row.append(value[2])
                row.append(value[3])
                row.append(value[4])
                row.append(value[5])
                row.append(value[6])
                row.append(value[7])
                row.append(value[8])
                row.append(value[9])
                writer.writerow(row)
    else:
        writer = csv.writer(sys.stdout, delimiter=";")
        for key, value in dictCandidatos.items():
            row = list()
            row.append(key)
            row.append(value[0])
            row.append(value[1])
            row.append(value[2])
            row.append(value[3])
            row.append(value[4])
            row.append(value[5])
            row.append(value[6])
            row.append(value[7])
            row.append(value[8])
            row.append(value[9])
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

    