from fptree import fpGrowth

## this class will hold all dataset information

class db:

    def __init__(self, marine, fresh):
        self.marine = marine
        self.fresh = fresh
        self.transactionClass0 = 0
        self.transactionClass1 = 0
        self.database = self.buildDatabase(marine, fresh)
        for tran in marine:
            marine[tran] = marine[tran], 0
        for tran in fresh:
            fresh[tran] = fresh[tran], 0

    def buildDatabase(self, dataSet0, dataset1):
        retDict = {}
        # class label 0
        values = dataSet0.values()
        sortedDataset = sorted(values, key=len)
        for trans in sortedDataset:
            self.transactionClass0 += 1
            tran = frozenset(trans)
            if tran in retDict:  # if already in retDict - increment the count
                retDict[tran] = ((retDict[tran][0] + 1), 0)
            else:  # else set count =objects
                retDict[tran] = (1, 0)

        # class label objects
        values = dataset1.values()
        sortedDataset = sorted(values, key=len)
        for trans in sortedDataset:
            self.transactionClass1 += 1
            tran = frozenset(trans)
            if tran in retDict:  # if already in retDict - increment the count
                retDict[tran] = ((retDict[tran][0] + 1), 0)
            else:  # else set count =objects
                retDict[tran] = (1, 0)

        return retDict

    def getDataSetforTree(self):
       # i = self.marine.values()
        marineDat = list()
        freshDat = list ()
        for i in self.marine.values():
            marineDat.append(i[0])
        for i in self.fresh.values():
            freshDat.append(i[0])
        initsetMarine = fpGrowth.createInitSet(marineDat)
        initsetFresg = fpGrowth.createInitSet(freshDat)
        dataSet = initsetMarine
        dataSet.update(initsetFresg)
        return dataSet
