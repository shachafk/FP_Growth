from fptree import treeNode


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        tran = frozenset(trans)
        if tran in retDict:  # if already in retDict - increment the count
            retDict[tran] = (retDict[tran] + 1)
        else:  # else set count =objects
            retDict[tran] = 1

    return retDict



def createInitSet2Clasess(dataSet0, dataset1):
    retDict = {}
    # class label 0
    dataSet0.sort()
    sortedDataset = sorted(dataSet0, key=len)
    for trans in sortedDataset:
        tran = frozenset(trans)
        if tran in retDict:  # if already in retDict - increment the count
            retDict[tran] = (retDict[tran] + 1)
        else:  # else set count =objects
            retDict[tran] = 1

    # class label objects
    dataset1.sort()
    sortedDataset = sorted(dataset1, key=len)
    for trans in sortedDataset:
        tran = frozenset(trans)
        if tran in retDict:  # if already in retDict - increment the count
            retDict[tran] = (retDict[tran] + 1)
        else:  # else set count =objects
            retDict[tran] = 1

    return retDict


def updateHeader(nodeToTest, targetNode):  # this version does not use recursion
    while (nodeToTest.nodeLink != None):  # Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def order(localD):
    localD = dict(sorted(localD.items(), key=lambda p: p[0]))
    orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]

    return orderedItems


def createTree(dataSet, minSup=1):  # create FP-tree from dataset but don't mine
    headerTable = {}
    # go over dataSet twice
    for trans in dataSet:  # first pass counts frequency of occurrence
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable):  # remove items not meeting minSup
        if headerTable[k] < minSup:
            del (headerTable[k])

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
            orderedItems = order(localD)
          # orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)  # populate tree with ordered freq itemset
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
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]  # (sort header table)
    for basePat in bigL:  # start from bottom of header table
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        if len(newFreqSet) < 4:
            freqItemList.append(newFreqSet)
            condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
            myCondTree, myHead = createTree(condPattBases, minSup)
            if myHead != None:
                mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

#
# def calcIGub(freqItemList, database):
#     itemset = freqItemSet(freqItemList[0], database)
#     totalTran = len(database.marine) + len(database.fresh)
#     ## c =0
#     ## p ( x = objects) = support
#     support = len(itemset.geneFromClass0) + len(itemset.geneFromClass1)
#     ## p (c=objects) = p
#     p = len(database.marine) / (len(database.marine) + len(database.fresh))
#     # P(c =objects I x = objects) = q
#     q = len(itemset.geneFromClass1) / support
#     IGub = 0
#     if q == 1:
#         IGub = -p * log2(p) - (1 - p) * log2(1 - p) + (p - support) * log2((p - support) / 1 - support) + (
#                 1 - p) * log2((1 - p) / (1 - support))
#     return IGub
