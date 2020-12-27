# this class will hold report information

class reportObject:
    def __init__(self, db, freqItemSet, index):
        self.itemSet = freqItemSet.itemSet
        self.numOfTransTotal = db.transactionClass1 + db.transactionClass0
        self.numOfTransTotalClass0 = db.transactionClass0
        self.numOfTransTotalClass1 = db.transactionClass1
        self.numOfTransItemClass0 = len(freqItemSet.geneFromClass0)
        self.numOfTransItemClass1 = len(freqItemSet.geneFromClass1)
        self.index = index
        self.ig = freqItemSet.informationgain


def __repr__(self):
    return repr(
        'index: ' + str(self.index) + ',itemset: ' + str(self.itemSet) + ',informationGain: ' + str (self.ig) + ",numOfTransTotal: " + str(self.numOfTransTotal)
        + ",numOfTransTotalClass0: " + str(self.numOfTransTotalClass0) + ",numOfTransTotalClass1: " + str(
            self.numOfTransTotalClass1)
        + ",numOfTransItemClass0: " + str(self.numOfTransItemClass0) + ",numOfTransItemClass1: " + str(
            self.numOfTransItemClass1)
    )
