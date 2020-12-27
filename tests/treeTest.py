from fptree import fpGrowth


def runTest():
    minSup = 3
    simpDat = loadSimpDat()
    print(simpDat)
    initSet = fpGrowth.createInitSet(simpDat)
    print(initSet)
    myFPtree, myHeaderTab = fpGrowth.createTree(initSet, minSup)


    print("Min support " + str(minSup))

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
    fpGrowth.mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItms)


def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat



if __name__ == '__main__':
    runTest()
