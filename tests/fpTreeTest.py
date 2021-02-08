from fptree import fpGrowth


def runTest():
    i = 2
    simpDat = loadSimpDat()
    print(simpDat)
    initSet = fpGrowth.createInitSet(simpDat)
    print(initSet)
    myFPtree, myHeaderTab = fpGrowth.createTree(initSet, i)

    isValid = validateTree(myFPtree)
    print("is Tree valid : " + str(isValid))

    print("Min support " + str(i))

    print("----------------------------------------------- DataSet -----------------------------------------------")
    print("")
    print(simpDat)
    print("")
    print("----------------------------------------------- FP-tree -----------------------------------------------")
    print("")
    myFPtree.disp()
    print(
        "----------------------------------------------- Header-table -----------------------------------------------")
    print(myHeaderTab)

    #
    # condPats_a =  fpGrowth.findPrefixPath('a', myHeaderTab['a'][objects])
    # condPats_b = fpGrowth.findPrefixPath('b', myHeaderTab['b'][objects])
    # condPats_c = fpGrowth.findPrefixPath('c', myHeaderTab['c'][objects])
    # condPats_d = fpGrowth.findPrefixPath('d', myHeaderTab['d'][objects])
    # condPats_e = fpGrowth.findPrefixPath('e', myHeaderTab['e'][objects])
    # print("----------------------------------------------- condPats_a -----------------------------------------------")
    # print (condPats_a)
    # print("----------------------------------------------- condPats_b -----------------------------------------------")
    # print (condPats_b)
    # print("----------------------------------------------- condPats_c -----------------------------------------------")
    # print (condPats_c)
    # print("----------------------------------------------- condPats_d -----------------------------------------------")
    # print (condPats_d)
    # print("----------------------------------------------- condPats_e -----------------------------------------------")
    # print (condPats_e)

    freqItms = []
    fpGrowth.mineTree(myFPtree, myHeaderTab, 2, set([]), freqItms)


def loadSimpDat():
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
    # simpDat = [['r', 'z', 'h', 'j', 'p'],
    #            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
    #            ['z'],
    #            ['r', 'x', 'n', 'o', 's'],
    #            ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    #            ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat


def validateTree(myFPtree):
    isValid = False
    nodes = myFPtree.children.items()
    for treeNode in nodes:
        treeNode = treeNode[1]
        if treeNode.name == 'a' and treeNode.count == 8:
            isValid = validateSubRootA(treeNode)
        elif treeNode.name == 'b' and treeNode.count == 2:
            isValid = validateSubRootB(treeNode)
        else:
            isValid = False

    return isValid


def validateSubRootA(myFPtree):
    isValid = False

    # subRoot from e
    child = validateSun(myFPtree, 'b', 5)
    if child != None:
        grandChild = validateSun(child, 'c', 3)
        isValid = grandChild != None
        if (isValid):
            isValid = (validateSun(grandChild, 'd', 1) != None)

        if (isValid):
            isValid = (validateSun(child, 'd', 1) != None)

    # subRoot from d
    if (isValid):
        child = validateSun(myFPtree, 'd', 1)
        if child != None:
            isValid = (validateSun(child, 'e', 1) != None)

    #subRoot from c
    if (isValid):
        child = validateSun(myFPtree, 'c', 1)
        if child != None:
            grandChild = validateSun(child, 'd', 1)
            isValid = grandChild != None
            if (isValid):
                isValid = (validateSun(grandChild, 'e', 1) != None)

    return isValid


def validateSubRootB(myFPtree):
    isValid = False
    child = validateSun(myFPtree, 'c', 2)
    if child != None:
        isValid = (validateSun(child, 'e', 1) != None)
        if isValid == True:
            isValid = (validateSun(child, 'd', 1) != None)
    return isValid


def validateSun(myFPtree, name, count):
    nodes = myFPtree.children.items()
    for treeNode in nodes:
        treeNode = treeNode[1]
        if treeNode.name == name and treeNode.count == count:
            return treeNode

    return None


if __name__ == '__main__':
    runTest()
