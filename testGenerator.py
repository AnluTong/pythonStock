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
        testCount = '60'
        dataSet = []
        for name in list(self.alreadylist.name):
            selectQuery = "select * from " + name + " order by 'date' desc limit " + testCount + " offset 0"
            result = pd.read_sql(selectQuery, self.fetchConn)
            if len(result) < int(testCount):
                continue

            # get average array
            ave = []
            for line in range(int(testCount)):
                ave.append((result['open'][line] + result['close'][line]) / 2)

            # get array every 3 day
            adj = []
            i = 0
            value = 0
            for meanPrice in ave:
                if i > 2:
                    adj.append(value / 3)
                    value = 0
                    i = 0
                value += meanPrice
                i += 1

            # get stander array value from 0 - 1
            standArray = []
            maxV = max(adj)
            minV = min(adj)
            div = maxV - minV
            for v in adj:
                standArray.append((v - minV) / div)

            dataSet.append(standArray)
        return dataSet

    def showPosXHisTab(self, pos):
        name = list(self.alreadylist.name)[pos]
        selectQuery = "select * from " + name + " order by 'date' desc limit 90 offset 0"
        result = pd.read_sql(selectQuery, self.fetchConn)
        prices = list(result['close'])
        code = result['code'][pos]
        maxP = max(prices)
        minP = min(prices)
        ave = (maxP + minP) / 2
        maxY = ave * 1.5
        minY = ave * 0.5

        plt.plot(range(len(prices)), prices, 'r')
        plt.xlabel('date')
        plt.ylabel('price')

        plt.ylim(minY, maxY)
        plt.title(code)
        plt.legend()
        plt.show()