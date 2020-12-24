class freqItemSet:
    def __init__(self, itemSet, database):
        self.itemSet = itemSet
        self.geneFromClass0 = list()
        self.geneFromClass1 = list()
        self.informationgain = 0
        self.calatotaltran(database)


    def calatotaltran(self,db):
        itemSet = self.itemSet

        items = db.marine.items()
        for tran in items :
            exists= itemSet.issubset(tran[1])
            if (exists):
                self.geneFromClass0.append(tran[0])

        items = db.fresh.items()
        for tran in items:
            exists = itemSet.issubset(tran[1])
            if (exists):
                self.geneFromClass1.append(tran[0])

        return 0
