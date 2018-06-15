import argparse
import os
import sys

def walkDir(dirname):
    
    files = []

    for root, dirs, filenames in os.walk(dirname, topdown=False):
        for name in filenames:
            files.append(os.path.join(root, name))
    
    return files

def filter(lista, value):

    filtered = []

    for element in lista:
        if value.lower() in element.lower():
            filtered.append(element)
    
    return filtered

def Main(inputDir, year, uf):
    
    filtered = walkDir(inputDir)

    if uf != None:
        filtered = filter(filtered, uf)
    
    if year != None:
        filtered = filter(filtered, year)
        
    return filtered

def parseArgs():
    
    parser = argparse.ArgumentParser("Filtrar Dados - Dados Abertos do TSE")
    parser.add_argument("-i", "--input", help="Diretório de Entrada")
    parser.add_argument("-o", "--output", help="Arquivo de Destino")
    parser.add_argument("-y", "--year", help="Filtrar por ano")
    parser.add_argument("-u", "--uf", help="Filtrar por UF")
    parser.add_argument("-v", "--verbose", help="Show filenames to be changed before Confirmation", action="store_true")

    return parser.parse_args()

def writeOutput(result, outfile):
    
    if outfile != None:
        with open(outfile, 'w', newline = '', encoding = "utf-8") as file:
            file.write(str(result))
    else:
        sys.stdout.write(str(result))

if __name__ == '__main__':
    
    args = parseArgs()

    inputFile = args.input
    outputFile = args.output
    
    if inputFile != None:
        result = Main(inputFile, args.year, args.uf)
        writeOutput(result, outputFile)
            

    else:       
        print("Diretório de Entrada Inválido!")