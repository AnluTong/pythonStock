from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from numpy import *

import model.createdatabase as cdb
import model.dataGenerator as dg
import model.kMean as km


# # db op
def createData():
    cdb.saveHistoryData()
    cdb.cleanifyHistoryData()
#
#
# def kmean():
#     print "step 1: load data..."
#     make = dg.TestGenerator()
#     dataSet, codeSet = make.getTestData()
#
#     print "step 2: clustering..."
#     dataSet = mat(dataSet)
#     k = 15
#     cenArray, assArray = km.kMeans(dataSet, k)
#     dict = {}
#     for pos in range(len(assArray)):
#         pattern = int(assArray[pos, 0])
#         if pattern not in dict:
#             dict[pattern] = [codeSet[pos]]
#         else:
#             e = dict[pattern]
#             e.append(codeSet[pos])
#
#     # print cluster result
#     file_object = open('result.txt', 'w')
#     try:
#         for key in dict:
#             file_object.write('cluster begin pattern %s \n' % key)
#             for code in dict[key]:
#                 file_object.write('%s, ' % code)
#             file_object.write('\n\n\n')
#     finally:
#         file_object.close()
#
#
# def averageLineStrategy():
#     make = dg.TestGenerator()
#     make.getCloseAndAverageData(u'code600552')


# flask op
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('sql')
stockFetcher = dg.TestGenerator()


def abort_if_code_doesnt_exist(code):
    if not stockFetcher.contains_code(code):
        abort(404, message="stock {} doesn't exist".format(code))


class StockHistory(Resource):
    # for example
    # curl http://localhost:5000/history/600552
    def get(self, code_id):
        code_id = "code" + unicode(code_id)
        abort_if_code_doesnt_exist(code_id)
        return stockFetcher.get_all_data(code_id)


class StockQuery(Resource):
    # for example
    # curl http://localhost:5000/query -d "sql=select close,MA_5,date from code600552" -X POST -v
    def post(self):
        args = parser.parse_args()
        return stockFetcher.get_sql_data(args['sql'])


##
## Actually setup the Api resource routing here
##
api.add_resource(StockHistory, '/history/<code_id>')
api.add_resource(StockQuery, '/query')

if __name__ == '__main__':
    createData()
    app.run(debug=True)
