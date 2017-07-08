import dataGenerator as dg
import createdatabase as cdb
from numpy import *
import kMean as km

def createData():
    cdb.saveHistoryData()
    cdb.cleanifyHistoryData()

def kmean():
    print "step 1: load data..."
    make = dg.TestGenerator()
    dataSet, codeSet = make.getTestData()

    print "step 2: clustering..."
    dataSet = mat(dataSet)
    k = 15
    cenArray, assArray = km.kMeans(dataSet, k)
    dict = {}
    for pos in range(len(assArray)):
        pattern = int(assArray[pos, 0])
        if pattern not in dict:
            dict[pattern] = [codeSet[pos]]
        else:
            e = dict[pattern]
            e.append(codeSet[pos])

    # print cluster result
    file_object = open('result.txt', 'w')
    try:
        for key in dict:
            file_object.write('cluster begin pattern %s \n' % key)
            for code in dict[key]:
                file_object.write('%s, ' % code)
            file_object.write('\n\n\n')
    finally:
        file_object.close()

def averageLineStrategy():
    make = dg.TestGenerator()
    make.getCloseAndAverageData(u'code600552')

if __name__ == "__main__":
    averageLineStrategy()