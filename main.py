# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fptree import fpGrowth
from preperations import loadData
from objects import db, reportObject
import entropy_gain
from objects.freqItemSet import freqItemSet
import time


def main():
    start_time = time.time()
    # initialize data
    print("---load CSV %s seconds ---" % (time.time() - start_time))
    loadData.loadCsv()
    database = db.db(loadData.getMarineDict(), loadData.getFreshDict())
    report = list()
    minSup = 2
    finish = 0

    while finish < 1:
        # prints
        print("---load dataset %s seconds ---" % (time.time() - start_time))
        dataset = database.getDataSetforTree()
        # minSup =  int(0.97 * len(dataset))
        if (len(dataset) == 0):
            break
        # build and mine fp tree
        print("---create FP tree %s seconds ---" % (time.time() - start_time))
        myFPtree, myHeaderTab = fpGrowth.createTree(dataset, minSup)
        print("---finish create FP tree %s seconds ---" % (time.time() - start_time))

        if myHeaderTab == None:
            break

        print("Number of transactions: ", (database.transactionClass0 + database.transactionClass1))
        print("Number of transactions in class0: ", database.transactionClass0)
        print("Number of transactions in class1: ", database.transactionClass1)
        print("Number of items: ", calcNumOfItems(dataset))
        print("MinSup: ", minSup)

        freqItms = []
        print("---mine tree tree %s seconds ---" % (time.time() - start_time))
        fpGrowth.mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItms)
        print("---finish mine tree tree %s seconds ---" % (time.time() - start_time))
        print("number of freqItems :", len(freqItms))

        # find Max IG
        itemset_maxig = None
        maxIG = 0
        itemSetsList = getfreqitemlist(database, freqItms)
        print("---calc maxig %s seconds ---" % (time.time() - start_time))
        for itemset in itemSetsList:
            itemset.informationgain = entropy_gain.infoGain(itemset, database)
            if (itemset.informationgain > maxIG):
                maxIG = itemset.informationgain
                itemset_maxig = itemset

        print("---finish calc ig %s seconds ---" % (time.time() - start_time))
        print("Max IG :", maxIG)
        print("ItemSet With MaxIG :", itemset_maxig.itemSet, "appeared # :",
              len(itemset_maxig.geneFromClass0) + len(itemset_maxig.geneFromClass1), " times")

        # add item to report and remove from data
        addtoreport(report, itemset_maxig, database)
        print("---delete transactions %s seconds ---" % (time.time() - start_time))
        removefromdata(database, itemset_maxig)


def getfreqitemlist(database, freqItms):
    itemsetslist = list()
    for itemset in freqItms:
        itemsetslist.append(freqItemSet(itemset, database))
    return itemsetslist


def addtoreport(report, itemset_maxig, database):
    report.append(reportObject.reportObject(database, itemset_maxig, len(report)))


def removefromdata(database, itemset_maxig):
    print("about to delete ", len(itemset_maxig.geneFromClass0), " from class 0")
    print("about to delete ", len(itemset_maxig.geneFromClass1), " from class 1")

    class0_before = database.transactionClass0
    class1_before = database.transactionClass1
    for tran in itemset_maxig.geneFromClass0:
        del database.marine[tran]
        database.transactionClass0 -= 1

    for tran in itemset_maxig.geneFromClass1:
        del database.fresh[tran]
        database.transactionClass1 -= 1

    print("deleted from class 0 :", class0_before - database.transactionClass0)
    print("deleted from class 1 :", class1_before - database.transactionClass1)


def calcNumOfItems(dataset):
    numOfitems = 0
    for trans in dataset:  # first pass counts frequency of occurrence
        numOfitems += len(trans)
    return numOfitems


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
