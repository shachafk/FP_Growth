# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import fpGrowth
import loadData

def main():

    loadData.loadCsv()
    marineDict = loadData.getMarineDict()
    freshDict = loadData.getFreshDict()
    simpDat = fpGrowth.loadSimpDat()
    print (simpDat)
    initSet = fpGrowth.createInitSet(simpDat)
    print (initSet)
    myFPtree, myHeaderTab = fpGrowth.createTree(initSet, 2)

    print("----------------------------------------------- DataSet -----------------------------------------------")
    print("")
    print(simpDat)
    print("")
    print("----------------------------------------------- FP-tree -----------------------------------------------")
    print("")
    myFPtree.disp()
    print("----------------------------------------------- Header-table -----------------------------------------------")
    print(myHeaderTab)

    freqItms = []
    fpGrowth.mineTree(myFPtree,myHeaderTab,2,set ([]), freqItms)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


