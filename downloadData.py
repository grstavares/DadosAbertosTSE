from multiprocessing.dummy import Pool
import urllib.request
import argparse
import os.path
import errno
import sys
import ast

import dadosAbertos as dados

bufferSize = 8192

def createPath(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def _reporthook(numblocks, blocksize, filesize, url=None):

    base = os.path.basename(url)
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
    except:
        percent = 100
    if numblocks != 0:
        sys.stdout.write("\b"*70)
    
    sys.stdout.write("%-66s%3d%%" % (base, percent))

def download(filename, url):
    
    createPath(filename)

    if sys.stdout.isatty():
        urllib.request.urlretrieve(url, filename,
                           lambda nb, bs, fs, url=url: _reporthook(nb,bs,fs,url))
        sys.stdout.write('\n')
    else:
        urllib.request.urlretrieve(url, filename=filename)


def getFileMap(inputFile):
    
    with open(inputFile, 'r') as file:
        content = file.read()
        return ast.literal_eval(content)

def Main(dictFiles, outputDir):
    
    outputDict = dict()

    print('Iniciando o download...')
    for key, value in dictFiles.items():
        filename = key if outputDir == None else os.path.join(outputDir, key)
        filename += '.zip'
        download(filename, value)
        outputDict[key] = filename

    return outputDict

def generateMap(output):
    
    fileMap = dict()
    placeholder = 'INSERT URL HERE!'

    for item in dados.allKeys():
        fileMap[item] = placeholder
    
    if output != None:
        with open(output, 'w', newline = '', encoding = "utf-8") as file:
            file.write(str(fileMap))
    
    else:
        sys.stdout.write(str(fileMap))

def parseArgs():
    
    parser = argparse.ArgumentParser("Fazer o Download dos Dados - Dados Abertos do TSE")
    parser.add_argument("-g", "--generateMap", help="Cria o esqueleto para o mapa de Localização dos Arquivos de Dados")
    parser.add_argument("-i", "--input", help="Mapa com Localização dos Arquivos de Destino")
    parser.add_argument("-o", "--output", help="Nome do Diretório de Destino")
    parser.add_argument("-v", "--verbose", help="Show filenames to be changed before Confirmation", action="store_true")

    return parser.parse_args()

def writeOutput(result, outfile):
    
    if outfile != None:
        with open(outfile, 'w', newline = '', encoding = "utf-8") as file:
            file.write(str(result))
    else:
        sys.stdout.write(str(outfile))

if __name__ == '__main__':
    
    args = parseArgs()

    inputFile = args.input
    outputDir = args.output
    
    if args.generateMap != None:
        generateMap(args.generateMap)
    else:
        
        if inputFile != None:
            inputMap = getFileMap(inputFile)
            result = Main(inputMap, outputDir)

            filename = 'downloadManifest.map'
            manifestPath = os.path.join(outputDir, filename)
            writeOutput(result, manifestPath)

        else:       
            print("Arquivo de Entrada Inválido!")