

class reportObject:
    def __init__(self, db,freqItemSet,index):
        self.itemSet = freqItemSet.itemSet
        self.numOfTransTotal = db.transactionClass1 + db.transactionClass0
        self.numOfTransTotalClass0 = db.transactionClass0
        self.numOfTransTotalClass1 = db.transactionClass1
        self.numOfTransItemClass0 = len(freqItemSet.geneFromClass0)
        self.numOfTransItemClass1 = len(freqItemSet.geneFromClass1)
        self.index = index


