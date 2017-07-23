import sqlite3

import pandas as pd

import averageLineStrategy as als


class TestGenerator(object):
    def __init__(self):
        self.notSaveFileName = 'Notsaved.txt'
        self.historyDBName = 'History.db'
        self.listDBName = 'Stocklist.db'
        self.listTableName = 'Allist'
        self.historyTabPrefx = 'code'
        self.errorList = []

        # get all table in history db
        self.fetchConn = sqlite3.connect(self.historyDBName, check_same_thread=False)
        fetchQuery = "select name from sqlite_master where type='table' order by name"
        self.alreadylist = pd.read_sql(fetchQuery, self.fetchConn)

    def __del__(self):
        self.fetchConn.close()

    def getTestData(self):
        testCount = 60
        dataSet = []
        codeSet = []
        for name in list(self.alreadylist.name):
            selectQuery = "select * from %s order by date desc limit %d offset 0" % (name, testCount)
            result = pd.read_sql(selectQuery, self.fetchConn)
            if len(result) < testCount:
                continue

            codeSet.append(result['code'][0])
            # get average array open close high low
            ave = []
            for line in range(testCount):
                ave.append((result['open'][line] + result['close'][line]) / 2)

            filter = []
            minAve = min(ave)
            rangeAve = max(ave) - minAve
            for line in ave:
                filter.append((line - minAve) / rangeAve * 100)

            element = []
            value = []
            for minK in filter:
                value.append(minK)
                if len(value) == 3:
                    k = (value[2] - value[0]) / 2
                    value = []
                    element.append(k)
            dataSet.append(element)
        return dataSet, codeSet

    def getCloseAndAverageData(self, code):
        selectQuery = "select close,MA_5,MA_21,date from %s" % code
        result = pd.read_sql(selectQuery, self.fetchConn)
        # need at least 40 days
        if len(result) < 40:
            return
        closeData = list(result.close)
        aveData = list(result.MA_5)
        dateData = list(result.date)
        ave21Data = list(result.MA_21)
        if len(closeData) != len(aveData) and len(closeData) != len(dateData) and len(closeData) != len(ave21Data):
            return
        singleCodeData = []
        for i in range(len(closeData)):
            singleCodeData.append([closeData[i], aveData[i], ave21Data[i], dateData[i]])
        result = als.averageLineStratey(singleCodeData)
        for p in result:
            print p
            print "\n"

    def contains_code(self, code):
        return code in list(self.alreadylist.name)

    def get_all_data(self, code):
        selectQuery = "select * from %s" % code
        result = pd.read_sql(selectQuery, self.fetchConn)
        response = []
        for i in xrange(len(result)):
            line = {}
            for name in result:
                line[name] = result[name][i]
            response.append(line)
        return response

    # for example
    # 'select close,MA_5 from code600552'
    def get_sql_data(self, sql):
        result = pd.read_sql(sql, self.fetchConn)
        response = []
        for i in xrange(len(result)):
            line = {}
            for name in result:
                line[name] = result[name][i]
            response.append(line)
        return response
