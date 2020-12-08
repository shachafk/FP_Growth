import csv
from collections import defaultdict
marineDict = defaultdict(set)
freshDict = defaultdict(set)

def loadCsv():
    with open('Marine_uid_value.csv', encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            marineDict[row[0]].add(row[1])

    with open('fresh_uid_value.csv', encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            marineDict[row[0]].add(row[1])

def getMarineDict():
    return marineDict

def getFreshDict():
    return freshDict

if __name__ == '__main__':
    loadCsv()
