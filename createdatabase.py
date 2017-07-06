from multiprocessing.dummy import Pool as ThreadPool
from sqlalchemy import create_engine
from datetime import datetime as dt
import pandas as pd
import traceback
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

        # get all table in history db
        self.fetchConn = sqlite3.connect(self.historyDBName)
        fetchQuery = "select name from sqlite_master where type='table' order by name"
        self.alreadylist = pd.read_sql(fetchQuery, self.fetchConn)

        # get all stock list
        database_file = os.path.dirname(os.path.abspath(__file__)) + '\\' + self.listDBName
        if not os.path.exists(database_file):
            # get all stock list from tushare
            data = ts.get_industry_classified()
            engine = create_engine('sqlite:///' + self.listDBName, echo=False)
            data.to_sql(self.listTableName, engine, if_exists='replace', index=False)
        connList = sqlite3.connect(self.listDBName)
        cursorList = connList.cursor()
        query = 'select * from ' + self.listTableName
        cursorList.execute(query)
        self.stocklist = cursorList.fetchall()
        cursorList.close()
        connList.close()

    def __del__(self):
        self.fetchConn.close()

    def saveHistoryList(self):
        # handle fetch data with thread pool
        pool = ThreadPool(4)
        try:
            pool.map(self.save, self.stocklist)
        except:
            pool.map(self.save, self.stocklist)
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
                print 'save ' + tabName
            except:
                traceback.print_exc()
                print 'save error ' + tabName

    def updateHistoryList(self):
        for stock in self.stocklist:
            code = stock[0][:6]
            tabName = self.historyTabPrefx + code
            if tabName in list(self.alreadylist.name):
                query = "select * from '%s' order by date" % tabName
                df = pd.read_sql(query, self.fetchConn)
                df = df.set_index('date')
                if dt.now().weekday() == 5:
                    today = str(pd.Timestamp(dt.now()) - pd.Timedelta(days=1))[:10]
                elif dt.now().weekday() == 6:
                    today = str(pd.Timestamp(dt.now()) - pd.Timedelta(days=2))[:10]
                else:
                    today = str(pd.Timestamp(dt.now()))[:10]
                if today != df.ix[-1].name[:10]:
                    # df.ix[-1] represent the newest day
                    try:
                        data = ts.get_k_data(code, start=df.ix[-1].name[:10])
                        engine = create_engine('sqlite:///' + self.historyDBName, echo=False)
                        data.to_sql(tabName, engine, if_exists='append', index=False)
                        print 'update success ' + tabName
                    except:
                        traceback.print_exc()
                        print 'update error ' + tabName

    def cleanifyData(self):
        for tabName in list(self.alreadylist.name):
            query = "select * from '%s' order by date" % tabName
            df = pd.read_sql(query, self.fetchConn)
            cur = self.fetchConn.cursor()
            # delete the repeat date only remain the max rowid repeat line
            delQuery = "delete from '%s' where rowid not in(select max(rowid) from '%s' group by date)" % (tabName, tabName)
            cur.execute(delQuery)
            self.fetchConn.commit()
            print 'scan ' + tabName

def saveHistoryData():
    make = MakeDataBase()
    make.saveHistoryList()

def updateHistoryData():
    make = MakeDataBase()
    make.updateHistoryList()

def cleanifyHistoryData():
    make = MakeDataBase()
    make.cleanifyData()