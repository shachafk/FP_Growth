from fptree import fpGrowth


class db:

    def __init__(self, marine, fresh):
        self.marine = marine
        self.fresh = fresh
        self.transactionClass0 = 0
        self.transactionClass1 = 0
        self.database = self.buildDatabase(marine, fresh)

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
            else:  # else set count =1
                retDict[tran] = (1, 0)

        # class label 1
        values = dataset1.values()
        sortedDataset = sorted(values, key=len)
        for trans in sortedDataset:
            self.transactionClass1 += 1
            tran = frozenset(trans)
            if tran in retDict:  # if already in retDict - increment the count
                retDict[tran] = ((retDict[tran][0] + 1), 1)
            else:  # else set count =1
                retDict[tran] = (1, 1)

        return retDict

    def getDataSetforTree(self):
        marineDat = list(self.marine.values())
        freshDat = list(self.fresh.values())
        initsetMarine = fpGrowth.createInitSet(marineDat)
        initsetFresg = fpGrowth.createInitSet(freshDat)
        dataSet = initsetMarine
        dataSet.update(initsetFresg)
        return dataSet
