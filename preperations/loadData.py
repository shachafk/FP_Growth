import csv
from collections import defaultdict
marineDict = defaultdict(set)
freshDict = defaultdict(set)

def loadCsv():
    with open('preperations/Marine_RNA.csv', encoding='utf-8-sig') as csvfile:
    #with open('preperations/Marine_uid_value.csv', encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            marineDict[row[0]].add(row[1])
                ##append(row[1])

    with open('preperations/Fresh_RNA.csv', encoding='utf-8-sig') as csvfile:
    #with open('preperations/Fresh_uid_value.csv', encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            freshDict[row[0]].add(row[1])

def getMarineDict():
    return marineDict

def getFreshDict():
    return freshDict

if __name__ == '__main__':
    loadCsv()
