import argparse
import zipfile
import os.path
import sys

def createPath(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def Main(inputFile, outputDir):
    
    filename = 'extractManifest.list'
    manifestPath = os.path.join(outputDir, filename)
    createPath(manifestPath)

    print("Extraindo", inputFile)
    extractedFiles = list()
    with open(inputFile, 'rb') as f:

        count = 0
        file = zipfile.ZipFile(f)
        for name in file.namelist():
            if '.txt' in name:
                count += 1
                extractedPath = os.path.join(outputDir, name)
                extractedFiles.append(extractedPath)
                file.extract(name,outputDir)

        print('{} arquivos extraídos'.format(count))
        return extractedFiles

def parseArgs():
    
    parser = argparse.ArgumentParser("Extração dos Dados - Dados Abertos do TSE")
    parser.add_argument("-i", "--input", help="Arquivo de Entrada")
    parser.add_argument("-o", "--output", help="Diretório de Destino")
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
    
    if inputFile != None:
        
        result = Main(inputFile, outputDir)

        filename = 'extractManifest.list'
        manifestPath = os.path.join(outputDir, filename)
        writeOutput(result, manifestPath)

    else:       
        print("Arquivo de Entrada Inválido!")