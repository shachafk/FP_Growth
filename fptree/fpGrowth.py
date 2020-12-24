from operator import itemgetter

import fptree.treeNode
import time
from fptree import treeNode
from objects.freqItemSet import freqItemSet
from math import log2


def loadSimpDat():
    # simpDat = [['r', 'z', 'h', 'j', 'p'],
    #            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
    #            ['z'],
    #            ['r', 'x', 'n', 'o', 's'],
    #            ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    #            ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    # simpDat = [['a', 'b'],
    #            ['a', 'b', 'c'],
    #            ['a'],
    #            ['a', 'd'],
    #            ['a', 'b', 'c', 'e'],
    #            ['a', 'b', 'd', 'f'],
    #            ['b','c']]
    simpDat = [['a', 'b'],
               ['b', 'c', 'd'],
               ['a', 'c', 'd', 'e'],
               ['a', 'd', 'e'],
               ['a', 'b', 'c'],
               ['a', 'b', 'c', 'd'],
               ['a'],
               ['a', 'b', 'c'],
               ['a', 'b', 'd'],
               ['b', 'c', 'e']]
    return simpDat


def createInitSet(dataSet):
    retDict = {}
   # dataSet.sort()
 #   sortedDataset = sorted(dataSet, key=len)
    for trans in dataSet:
        tran = frozenset(trans)
        if tran in retDict: # if already in retDict - increment the count
            retDict[tran] = (retDict[tran] + 1)
        else : # else set count =1
            retDict[tran] = 1

    return retDict

def createInitSet2Clasess(dataSet0, dataset1):
    retDict = {}
    # class label 0
    dataSet0.sort()
    sortedDataset = sorted(dataSet0, key=len)
    for trans in sortedDataset:
        tran = frozenset(trans)
        if tran in retDict: # if already in retDict - increment the count
            retDict[tran] = (retDict[tran] + 1)
        else : # else set count =1
            retDict[tran] = 1

    #class label 1
    dataset1.sort()
    sortedDataset = sorted(dataset1, key=len)
    for trans in sortedDataset:
        tran = frozenset(trans)
        if tran in retDict:  # if already in retDict - increment the count
            retDict[tran] = (retDict[tran] + 1)
        else:  # else set count =1
            retDict[tran] = 1

    return retDict



def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):  # Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def createTree(dataSet, minSup=1):  # create FP-tree from dataset but don't mine
    headerTable = {}
    # go over dataSet twice
    for trans in dataSet:  # first pass counts frequency of occurrence
        for item in trans:
            headerTable[item] = (headerTable.get(item, 0) + dataSet[trans])
    for k in list(headerTable):  # remove items not meeting minSup
        if headerTable[k] < minSup:
            del (headerTable[k])

    newHeader = orderTable(headerTable)
    headerTable = newHeader
    freqItemSet = set(headerTable.keys())

    # print 'freqItemSet: ',freqItemSet
    if len(freqItemSet) == 0: return None, None  # if no items meet min support -->get out
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]  # reformat headerTable to use Node link
    # print 'headerTable: ',headerTable


    retTree = treeNode.treeNode('Null Set', 1, None)  # create tree
    for tranSet, count in dataSet.items():  # go through dataset 2nd time
        localD = {}
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
    #     localD= dict(sorted(localD.items(), key=lambda p: p[0], reverse=True)) # sort by alphabet
    #         localD = sorted(localD.items(), key=lambda p: p[1], reverse=True) #sort by frequency
            localD= sorted(localD.items(), key=lambda p: p[1], reverse=True)
            orderedItems = [v[0] for v in localD]
            updateTree(orderedItems, retTree, headerTable, count)  # populate tree with ordered freq itemset
            # retTree.disp()
            # print("___________________________________")
    return retTree, headerTable  # return tree and header table


def orderTable(headerTable):
    # order header table by count and alpabet
    items = headerTable.items()
    keys = headerTable.keys()
    values = headerTable.values()
    orderedHeader = dict(sorted(headerTable.items(), key=lambda k: (k[0])))
    i = len(orderedHeader)
    for k in orderedHeader:
        orderedHeader[k] = orderedHeader[k], i
        i = i - 1
    orderedHeader = dict(sorted(orderedHeader.items(), key=lambda k: (k[1]), reverse=True))
    newHeader = {}
    for k in orderedHeader:
        newHeader[k] = orderedHeader[k][0]

    return newHeader


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:  # check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count)  # incrament count
    else:  # add items[0] to inTree.children
        inTree.children[items[0]] = treeNode.treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:  # update header table
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:  # call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def ascendTree(leafNode, prefixPath):  # ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):  # treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
  #  print ("header table size", len(headerTable))
    start_time = time.time()
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]  # (sort header table)
    for basePat in bigL:  # start from bottom of header table
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #itemAndSupport = (newFreqSet,headerTable.items[newFreqSet][0])
        # print('finalFrequent Item: ', newFreqSet)  # append to set
        freqItemList.append(newFreqSet)
       # k = calcIGub(freqItemList,database)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        # print('condPattBases :', basePat, condPattBases)
        # 2. construct cond FP-tree from cond. pattern base
        myCondTree, myHead = createTree(condPattBases, minSup)
        #  print('head from conditional tree: ', myHead)
        if myHead != None:  # 3. mine cond. FP-tree
            # print('--------------------------------------------------')
            # print('conditional tree for: ', newFreqSet)
            #myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def calcIGub(freqItemList,database):
    itemset = freqItemSet(freqItemList[0],database)
    totalTran = len(database.marine) + len(database.fresh)
    ## c =0
    ## p ( x = 1) = support
    support = len(itemset.geneFromClass0) + len(itemset.geneFromClass1)
    ## p (c=1) = p
    p = len(database.marine) / (len(database.marine) + len(database.fresh))
    #P(c =1 I x = 1) = q
    q = len(itemset.geneFromClass1) / support
    IGub =0
    if q == 1:
        IGub = -p * log2(p)  - (1-p)* log2(1-p) + (p-support)* log2((p-support)/ 1- support) + (1-p) * log2((1-p)/(1-support))
    return IGub
