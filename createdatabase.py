from multiprocessing.dummy import Pool as ThreadPool
from sqlalchemy import create_engine
import pandas as pd
import tushare as ts
import sqlite3
import os

class MakeDataBase(object):
    """used for create stock list db and stock history db"""

    def __init__(self):
        # constructor
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

    def getStockList(self):
        data = ts.get_industry_classified()
        engine = create_engine('sqlite:///' + self.listDBName, echo=False)
        data.to_sql(self.listTableName, engine, if_exists='replace', index=False)

    def saveHistoryData(self):
        database_file = os.path.dirname(os.path.abspath(__file__)) + '\\' + self.listDBName
        if not os.path.exists(database_file):
            self.getStockList()
        connList = sqlite3.connect(self.listDBName)
        cursorList = connList.cursor()
        query = 'select * from ' + self.listTableName
        cursorList.execute(query)
        stocklist = cursorList.fetchall()
        cursorList.close()
        connList.close()

        # handle fetch data with thread pool
        pool = ThreadPool(4)
        try:
            pool.map(self.save, stocklist)
        except:
            pool.map(self.save, stocklist)
        pool.close()
        pool.join()

    def save(self, stock):
        code = stock[0][:6]
        tabName = self.historyTabPrefx + code
        if tabName not in list(self.alreadylist.name):
            try:
                data = ts.get_k_data(code, start='2014-01-01')
                engine = create_engine('sqlite:///' + self.historyDBName, echo=False)
                data.to_sql(tabName, engine, if_exists='replace', index=False)
            except:
                self.errorList.append(stock[0])
                print self.errorList
