import copy

class itemsetReportObj:
    def __init__(self, db, freqItemSet, index, infoTable):
        self.items = freqItemSet.itemSet
        self.infoTable = infoTable
        self.db = copy.deepcopy(db)
        self.index = index

    def toString(self):
        start = ""
        for item in self.items:
            set1 = set()
            set1.add(item)
            numClass0 = 0
            numClass1 = 0
            for tran in self.db.marine:
                if set1.issubset(self.db.marine[tran][0]):
                    numClass0 = numClass0 + 1
            for tran in self.db.fresh:
                if set1.issubset(self.db.fresh[tran][0]):
                    numClass1 = numClass1 + 1
            if start != "":
                start = start + '\n'

            start = start + str(self.index) + "|" + str(self.items) + "|" + item + "|" + str(
                self.infoTable[item]) + "|" + str(numClass0 + numClass1) + "|" + str(numClass0) + "|" + str(
                numClass0 / self.db.transactionClass0) + "|" + str(numClass1) + "|" + str(
                numClass1 / self.db.transactionClass1)

        return start
