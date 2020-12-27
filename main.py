from fptree import fpGrowth
from preperations import loadData, entropy_gain
from objects import db, reportObject
from objects.freqItemSet import freqItemSet
import time
import sys



def main(argv):
    minSup = 200
    k = 9  # how many times transaction need to be covered before removed
    if len(argv) != 3:
        i = len(argv)
        print("Argument was not supplied, using default values, minSup: ", str (minSup), "k: ", str(k))
    else:
        minSup= int (argv[1])
        k = int (argv[2])
    start_time = time.time()
    # initialize data
    loadData.loadCsv("Marine_all", "Fresh_all")
    database = db.db(loadData.getMarineDict(), loadData.getFreshDict())
    report = list()

    it = 0  # number of iteration
    deleted = 1
    itemSetsList = list()
    while 1:
        it = it + 1
        # prints
        print("_______________________iteration #", str(it), "_________________")
        print("Number of transactions: ", (database.transactionClass0 + database.transactionClass1))
        print("Number of transactions in class0: ", database.transactionClass0)
        print("Number of transactions in class1: ", database.transactionClass1)
        print("MinSup: ", minSup)
        print("k: ", k)

        if deleted > 0:
            dataset = database.getDataSetforTree()

            if len(dataset) == 0:
                break

            print("Number of items: ", calcNumOfItems(dataset))
            # build and mine fptree tree
            myFPtree, myHeaderTab = fpGrowth.createTree(dataset, minSup)

            if myHeaderTab == None:
                break

            freqItms = []
            fpGrowth.mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItms)

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
            itemSetsList.remove(itemset_maxig)
            addtoreport(report, itemset_maxig, database)
            deleted = removefromdata(database, itemset_maxig, k)
        else:
            break
    printReport(report)
    printMinSup(start_time, minSup)


def getfreqitemlist(database, freqItms, report):
    itemsetslist = list()
    for item in report:
        j = item.itemSet
        if j in freqItms:
            freqItms.remove(j)
    for itemset in freqItms:
        itemsetslist.append(freqItemSet(itemset, database))

    return itemsetslist


def addtoreport(report, itemset_maxig, database):
    report.append(reportObject.reportObject(database, itemset_maxig, len(report)))


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


def printReport(report):
    f = open("outputFiles\\report_output.txt", "w")
    for rep in report:
        toPrint = reportObject.__repr__(rep) + '\n'
        f.write(toPrint)
    print("\nfile outputFiles\\report_output.txt was updated" )

def printMinSup(strat_time, minSup):
    with open('outputFiles\\runTime.txt', 'a') as file:
        file.write("Min Sup: " + str(minSup) + " , Run time: " + str((time.time() - strat_time)) + " Seconds" + '\n')
    print("file outputFiles\\runTime.txt was updated")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)
