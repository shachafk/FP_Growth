import csv
from collections import defaultdict

marineDict = defaultdict(set)
freshDict = defaultdict(set)


def loadCsv(path1, path2):
    path_class0 = "preperations\inputFiles\\"  + path1 + '.csv'
    path_class1 = "preperations\inputFiles\\"  + path2 + '.csv'
    load(path_class0,marineDict)
    load(path_class1,freshDict)


def load(path,dict):
    with open(path, encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if row[2] != "Function unknown" and row[2] != "General function prediction only":
                dict[row[0]].add(row[1])

def getMarineDict():
    return marineDict


def getFreshDict():
    return freshDict


if __name__ == '__main__':
    loadCsv()
