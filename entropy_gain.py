# -*- coding: utf-8 -*-

# calculating the Entropy and Information Gain for: Learning with Trees
# by: Aziz Alto

# see Information Gain:
# http://www.autonlab.org/tutorials/infogain.html


from __future__ import division
from math import log2
from math import log


def entropy(pi):
    '''so
    return the Entropy of a probability distribution:
    entropy(p) = − SUM (Pi * log(Pi) )
    defintion:
            entropy is a metric to measure the uncertainty of a probability distribution.
    entropy ranges between 0 to 1
    Low entropy means the distribution varies (peaks and valleys).
    High entropy means the distribution is uniform.
    See:
            http://www.cs.csi.cuny.edu/~imberman/ai/Entropy%20and%20Information%20Gain.htm
    '''

    total = 0
    for p in pi:
        p = p / sum(pi)
        if p != 0:
            total += p * log(p, 2)
        else:
            total += 0
    total *= -1
    return total


def gain(d, a):
    '''
    return the information gain:
    gain(D, A) = entropy(D)−􏰋 SUM ( |Di| / |D| * entropy(Di) )
    '''
    total = 0
    for v in a:
        total += sum(v) / sum(d) * entropy(v)

    gain = entropy(d) - total
    return gain


def calcInfoGain(item, dataSet):
    labelCounts = {0, 1}  ## dict of all possible classes
    currentLabel = item[0][1]

    numEntries = 0;
    for entry in dataSet:
        if entry[1] == currentLabel:
            numEntries +=1

    IG = 0.0
    prob = float(item[1] / numEntries)
    IG -= prob * log(prob, 2)
    return IG

def entropy(class0, class1):
	return -(class0 * log2(class0) + class1 * log2(class1))

def infoGain(freqItemSet, db):

    #calculate the entropy for this dataset
    totaltrans = db.transactionClass0 + db.transactionClass1
    class0 = db.transactionClass0 / totaltrans
    class1 = db.transactionClass1 / totaltrans
    s_entropy = entropy(class0, class1)
   # print('Dataset Entropy: %.3f bits' % s_entropy)

    # split 1 (split via value1)
    totaltransitemset = len(freqItemSet.geneFromClass0) + len(freqItemSet.geneFromClass1)
    s1_class0 = len(freqItemSet.geneFromClass0) / totaltransitemset
    s1_class1 = len(freqItemSet.geneFromClass1) / totaltransitemset
    # calculate the entropy of the first group
    s1_entropy = entropy(s1_class0, s1_class1)
 #   print('Group1 Entropy: %.3f bits' % s1_entropy)

    # calculate the information gain
    i = totaltransitemset / totaltrans
    gain = s_entropy - (i * s1_entropy)
  #  print('Information Gain: %.3f bits' % gain)
    return gain

# TEST
def test():
    ###__ example 1 (AIMA book, fig18.3)

    # set of example of the dataset
    willWait = [6, 6]  # Yes, No

    # attribute, number of members (feature)
    patron = [[4, 0], [2, 4], [0, 2]]  # Some, Full, None

    print(gain(willWait, patron))

    ###__ example 2 (playTennis homework)

    # set of example of the dataset
    playTennis = [9, 5]  # Yes, No

    # attribute, number of members (feature)
    outlook = [
        [4, 0],  # overcase
        [2, 3],  # sunny
        [3, 2]  # rain
    ]
    temperature = [
        [2, 2],  # hot
        [3, 1],  # cool
        [4, 2]  # mild
    ]
    humidity = [
        [3, 4],  # high
        [6, 1]  # normal
    ]
    wind = [
        [6, 2],  # weak
        [3, 3]  # strong
    ]

    print(gain(playTennis, outlook))
    print(gain(playTennis, temperature))
    print(gain(playTennis, humidity))
    print(gain(playTennis, wind))
    print(calcInfoGain(outlook))


if __name__ == '__main__':
    test()
