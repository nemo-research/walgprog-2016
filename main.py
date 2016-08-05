import sys
import os
import csv

import similarity
from config import Config
from ast import ast
from ui import get_opts, read_docs_from_list

def getObjeto(auxLista, stringArq):
    auxIndex = auxLista.index(stringArq)
    return auxLista.__getitem__(auxIndex)

def splitNomeQuesta(stringArq):
    auxString = stringArq.split("2014-T01-E")
    return auxString[1].split(".py")[0]


def _main():
    """ Main function. Prints the AST of a file. """
    config = Config()
    filesname = get_opts(sys.argv[1:], config)
    files = []
    if len(filesname) == 1 and os.path.isfile(filesname[0]):
        for line in ast(config, '\n'.join(open(filesname[0]).readlines())):
            print line
        return
    for filename in filesname:
        if os.path.isdir(filename):
            for root, dirs, d_files in os.walk(filename):
                for d_file in d_files:
                    files.append(root + os.sep + d_file)
        else:
            files.append(filename)
    files = filter(lambda item: item.endswith('.py'), files)
    docs = read_docs_from_list(config, files)
    y = docs.values()[0]
    conn = similarity.main(config['sim'], [x for x in docs.values() if x])
    print "Com erro de sintax: %s. Sem erro de sintax: %s." % (len([x for x in docs.values() if not x]), (len([x for x in docs.values() if x])))

    linhaString = []
    linhaString.append("")
    
    for i in range(len(docs.values())):
        linhaString.append("e" + str(i))       
    #print linhaString
    
    with open('test.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d1, d2, value in conn:
            #print d1.name, d2.name, value        
            spamwriter.writerow([d1.name, d2.name, value])

    linhaAnterior = ""
    listaColunas = []
    auxLista = []

    with open('test2.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(linhaString)
        for d1, d2, value in conn:
            
            #print d1.name, d2.name, value
            auxNomeQuestao =  splitNomeQuesta(d1.name)
            #spamwriter.writerow([test])
            if (not auxLista.__contains__(auxNomeQuestao)):
                auxLista.append(auxNomeQuestao)
                listaColunas.append({auxNomeQuestao: [value]})
            elif (auxLista.__contains__(auxNomeQuestao)):
                auxKey = getObjeto(auxLista, auxNomeQuestao)
                for item in listaColunas:
                    if (item.has_key(auxKey)):
                        item.get(auxKey).append(value)
        for i in listaColunas:    
            spamwriter.writerow([i, len(i.values()[0])]) 
            spamwriter.writerow([])
#    print listaColunas
if __name__ == '__main__':
    _main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    