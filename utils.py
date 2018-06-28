import os.path
import ast
import shutil

def createPath(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def getMapFromFile(inputFile):
    
    with open(inputFile, 'r') as file:
        content = file.read()
        return ast.literal_eval(content)

def clearDir(dirname):

    shutil.rmtree(dirname, ignore_errors=True)