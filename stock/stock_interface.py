# coding=utf-8

from flask import request

import stock.createdatabase as cdb
import stock.dataGenerator as dg
from global_var import app, generate_resp

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

stockFetcher = dg.TestGenerator()


@app.route('/api/stock/query', methods=['POST'])
def query_stock():
    # 例如 sql=select close,MA_5,date from code600552
    if not request.form:
        return generate_resp('invalid_params')  # 没有参数
    sql = request.form.get('sql')
    res = stockFetcher.get_sql_data(sql)
    return generate_resp('success', res)


@app.route('/api/stock/history', methods=['GET'])
def query_history():
    if not request.args:
        return generate_resp('invalid_params')  # 没有参数
    get_code = request.args.get('code')
    code = "code" + unicode(get_code)
    if not stockFetcher.contains_code(code):
        return generate_resp("not_found")
    res = stockFetcher.get_all_data(code)
    return generate_resp('success', res)


def init():
    pass
    # cdb.saveHistoryData()
    # cdb.cleanifyHistoryData()
