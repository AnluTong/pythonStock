import createdatabase as cdb
from numpy import *
import kMean as km

cdb.updateHistoryData()
cdb.cleanifyHistoryData()

# print "step 1: load data..."
# make = tg.TestGenerator()
# dataSet = make.getTestData()
#
# print "step 2: clustering..."
# dataSet = mat(dataSet)
# k = 10
# cenArray, assArray = km.kMeans(dataSet, k)
# patternSet = set()
# for pos in range(len(assArray)):
#     if pos < 10:
#         continue
#     pattern = int(assArray[pos, 0])
#     if pattern not in patternSet:
#         patternSet.add(pattern)
#         # make.showPosXHisTab(pos)
#         print pattern
#     if len(patternSet) == k:
#         break
#
# file_object = open('result.txt', 'w')
# try:
#     for pos in range(len(assArray)):
#         file_object.write(unicode(pos) + '  ')
#         file_object.write(unicode(assArray[pos]))
#         file_object.write('\r\n')
#     file_object.write('\r\n')
#     file_object.write(unicode(cenArray))
# finally:
#     file_object.close()
