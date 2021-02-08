import csv
from collections import defaultdict

#
marineDict = defaultdict(set)
freshDict = defaultdict(set)
cogInfo = defaultdict(set)


def loadCsv(path1, path2):
    path_class0 = "preperations\inputFiles\\" + path1 + '.csv'
    path_class1 = "preperations\inputFiles\\" + path2 + '.csv'
    load(path_class0, marineDict)
    load(path_class1, freshDict)


def load(path, dict):
    with open(path, encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if row[2] != "Function unknown" and row[2] != "General function prediction only":
                dict[row[0]].add(row[1])


def loadCsv(path1, path2, group,all):
    path_class0 = "preperations\inputFiles\\" + path1 + '.csv'
    path_class1 = "preperations\inputFiles\\" + path2 + '.csv'
    marineDict.clear()
    freshDict.clear()
    load(path_class0, marineDict, group,all)
    load(path_class1, freshDict, group,all)


def load(path, dict, group,all):
    with open(path, encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if all:
                dict[row[0]].add(row[1])

            elif row[3] == group:
                dict[row[0]].add(row[1])


def getMarineDict():
    return marineDict


def getFreshDict():
    return freshDict


if __name__ == '__main__':
    loadCsv()


def loadCogCsv(path):
    groups = []
    filePath = "preperations\inputFiles\\" + path + '.csv'
    with open(filePath, encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            groups.append(row[0])
    return groups


def loadInfoCsv(fileName):
    path = "preperations\inputFiles\\" + fileName + '.txt'
    with open(path) as txtfile:
        spamreader = csv.reader(txtfile, delimiter=';')
        for row in spamreader:
            cogInfo[row[0]].add( str(row[2] + "|" + row[3] + "|" + row[4]))
    return cogInfo