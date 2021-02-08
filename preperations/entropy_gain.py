

from __future__ import division
from math import log



def entropy(class0, class1):
    return -(class0 * __Log2(class0) + class1 * __Log2(class1))


def infoGain(freqItemSet, db):
    # calculate the entropy for this dataset
    totaltrans = db.transactionClass0 + db.transactionClass1
    class0 = db.transactionClass0 / totaltrans
    class1 = db.transactionClass1 / totaltrans
    s_entropy = entropy(class0, class1)

    # split objects (split via value1)
    totaltransitemset = len(freqItemSet.geneFromClass0) + len(freqItemSet.geneFromClass1)
    s1_class0 = len(freqItemSet.geneFromClass0) / totaltransitemset
    s1_class1 = len(freqItemSet.geneFromClass1) / totaltransitemset
    s1_entropy = entropy(s1_class0, s1_class1)

    # split objects (split via value2)
    total_not = totaltrans - totaltransitemset  # total tran were itemset not there
    i = totaltransitemset / totaltrans
    if total_not != 0 :
        s2_class0 = (db.transactionClass0 - len(freqItemSet.geneFromClass0)) / total_not
        s2_class1 = (db.transactionClass1 - len(freqItemSet.geneFromClass1)) / total_not
        s2_entropy = entropy(s2_class0, s2_class1)
        j = 1 - i
        gain = s_entropy - ((i * s1_entropy) + (j * s2_entropy))

    else:
        gain = s_entropy - (i * s1_entropy)
    return gain


def __Log2(x):
    ans = 0
    try:
        if x != 0:
            ans = log(x, 2)
    except ValueError:
        pass
    return ans

