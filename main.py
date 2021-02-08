from fptree import fpGrowth
from objects.itemsetReportObj import itemsetReportObj
from preperations import loadData, entropy_gain
from objects import db, reportObject
from objects.freqItemSet import freqItemSet
import time
import sys


def main(argv):
    groups = loadData.loadCogCsv("cog_info_groups_1")
    infoTable = loadData.loadInfoCsv("COG_INFO_TABLE")

    for group in groups:
        # minSup = 200
        # k = 9  # how many times transaction need to be covered before removed
        # if len(argv) != 3:
        #     i = len(argv)
        #     print("Argument was not supplied, using default values, minSup: ", str(minSup), "k: ", str(k))
        # else:
        #     minSup = int(argv[1])
        #     k = int(argv[2])

        start_time = time.time()
        # initialize data
        all = 0
        firstFile = "Marine_all"
        secondFile = "Fresh_all"
        loadData.loadCsv(firstFile, secondFile, group, all)
        database = db.db(loadData.getMarineDict(), loadData.getFreshDict())
        minSup = int((database.transactionClass0 + database.transactionClass1) * 0.4)
        k = 9
        report = list()
        itemsetreport = list()

        it = 0  # number of iteration
        deleted = -1
        itemSetsList = list()
        while 1:
            it = it + 1
            # prints
            print("_______________________iteration #", str(it), "_________________")
            print("Number of transactions: ", (database.transactionClass0 + database.transactionClass1))
            print("Number of transactions in class0: ", database.transactionClass0)
            print("Number of transactions in class1: ", database.transactionClass1)
            print("MinSup: ", minSup)
            maxSup = int((database.transactionClass0 + database.transactionClass1) * 0.8)
            print("MaxSup: ", maxSup)
            print("k: ", k)

            if deleted != 0:
                dataset = database.getDataSetforTree()

                if len(dataset) == 0:
                    break

                print("Number of items: ", calcNumOfItems(dataset))
                # build and mine fptree tree
                myFPtree, myHeaderTab = fpGrowth.createTree(dataset, minSup, maxSup)

                if myHeaderTab == None:
                    break

                freqItms = []
                fpGrowth.mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItms, maxSup)

                print("number of freqItems :", len(freqItms))
                print("Get freqItems list")
                itemSetsList = getfreqitemlist(database, freqItms, report)

            # find Max IG
            itemset_maxig = None
            maxIG = 0
            print("calc IG")
            for itemset in itemSetsList:
                itemset.informationgain = entropy_gain.infoGain(itemset, database)
                if (itemset.informationgain > maxIG):
                    maxIG = itemset.informationgain
                    itemset_maxig = itemset

            print("Max IG :", maxIG)
            if itemSetsList != None:
                # add item to report and remove from data

                if itemset_maxig != None:
                    if itemset_maxig in itemSetsList:
                        itemSetsList.remove(itemset_maxig)
                    addtoreport(report, itemsetreport, itemset_maxig, database, infoTable)
                    deleted = removefromdata(database, itemset_maxig, k)
                else:
                    break
            else:
                break
        printReport(report, group, itemsetreport, all)
        printMinSup(start_time, minSup, maxSup, group)


def getfreqitemlist(database, freqItms, report):
    itemsetslist = list()
    for item in report:
        j = item.itemSet
        if j in freqItms:
            freqItms.remove(j)
    for itemset in freqItms:
        itemsetslist.append(freqItemSet(itemset, database))

    return itemsetslist


def addtoreport(report, itemsetreport, itemset_maxig, database, infoTable):
    report.append(reportObject.reportObject(database, itemset_maxig, len(report)))
    itemsetreport.append(itemsetReportObj(database, itemset_maxig, len(report), infoTable))


def removefromdata(database, itemset_maxig, k):
    print("itemset appeared in ", len(itemset_maxig.geneFromClass0), " transactions from class 0")
    print("itemset appeared in ", len(itemset_maxig.geneFromClass1), " transactions from class 1")

    class0_before = database.transactionClass0
    class1_before = database.transactionClass1
    for tran in itemset_maxig.geneFromClass0:
        if database.marine[tran][1] >= k:
            del database.marine[tran]
            database.transactionClass0 -= 1
        else:
            tup = list(database.marine[tran])
            tup[1] = database.marine[tran][1] + 1
            database.marine[tran] = tuple(tup)

    for tran in itemset_maxig.geneFromClass1:
        if database.fresh[tran][1] >= k:
            del database.fresh[tran]
            database.transactionClass1 -= 1
        else:
            tup = list(database.fresh[tran])
            tup[1] = database.fresh[tran][1] + 1
            database.fresh[tran] = tuple(tup)

    print("deleted from class 0 :", class0_before - database.transactionClass0)
    print("deleted from class 1 :", class1_before - database.transactionClass1)
    return (class0_before - database.transactionClass0) + (
            class1_before - database.transactionClass1)  # return how many transactions deleted


def calcNumOfItems(dataset):
    numOfitems = 0
    for trans in dataset:  # first pass counts frequency of occurrence
        numOfitems += len(trans)
    return numOfitems


def printReport(report, group, itemsetreport, all):
    if all:
        filename = "outputFiles\\report\\" + "all" + ".txt"
    else:
        filename = "outputFiles\\report\\" + group + ".txt"
    f = open(filename, "w")
    header = "#|Itemset|informationGain|# of genomes in dataset| # of genomes in dataset from class0|# of genomes in dataset from class1 |# of genomes class0 where itemset occure|% of occurance in class 0|# of genomes class1 where itemset occure|% of occurance in class 1 " + '\n'
    f.write(header)
    for rep in report:
        toPrint = reportObject.__repr__(rep) + '\n'
        f.write(toPrint.replace('"', ''))
    print("\n" + filename + " was updated")

    if all:
        filename = "outputFiles\\report\\" + "all" + "_itemSets" + ".txt"
    else:
        filename = "outputFiles\\report\\" + group + "_itemSets" + ".txt"
    f = open(filename, "w")
    header = "index|Itemset|item|High level info|specific info|description|#of item total|# of genomes class0|% of class0 |# of genomes class1 |% of class1" + '\n'
    f.write(header)
    for rep in itemsetreport:
        toPrint = itemsetReportObj.toString(rep) + '\n'
        f.write(toPrint)
    print("\n" + filename + " was updated")


def printMinSup(strat_time, minSup, maxSup, group):
    filename = "outputFiles\\runtime\\" + group + ".txt"
    with open(filename, 'a') as file:
        file.write("Min Sup: " + str(minSup) + " ,Max Sup: " + str(maxSup) + " , Run time: " + str(
            (time.time() - strat_time)) + " Seconds" + '\n')
    print("\n" + filename + " was updated")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)
