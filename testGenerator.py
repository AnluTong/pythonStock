from multiprocessing.dummy import Pool as ThreadPool
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import tushare as ts
import sqlite3
import os

class TestGenerator(object):
    def __init__(self):
        self.notSaveFileName = 'Notsaved.txt'
        self.historyDBName = 'History.db'
        self.listDBName = 'Stocklist.db'
        self.listTableName = 'Allist'
        self.historyTabPrefx = 'code'
        self.errorList = []

        # get all table in history db
        self.fetchConn = sqlite3.connect(self.historyDBName)
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