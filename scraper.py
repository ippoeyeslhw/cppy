# coding: utf-8
from cppy.CpDib import StockCur
from cppy.CpDib import StockJpbid
import datetime

'''
5% 이상의 종목을 0.25간격동안 계속 감시하여 검출시 바로
실시간 체결 및 호가정보를 수신하여 db에 넣는 수집기
'''

def timStamp():
    stamp = datetime.datetime.now()
    return '%02d%02d%02d%03d'%(stamp.hour, stamp.minute, stamp.second, stamp.microsecond/1000)


class SampleStockCur(object):
    ''' 주식/업종/ELW 시세 데이터를 수신합니다'''

    def __init__(self, cod, dbcont):
        self.com = StockCur(self.publish)
        self.cod = cod
        self.dbcont = dbcont

    def subscribe(self):
        self.com.SetInputValue(0, self.cod)  # string  종목 코드
        self.com.Subscribe()

    def publish(self):
        h0 = self.com.GetHeaderValue(0)  # string  종목 코드
        h13 = self.com.GetHeaderValue(13)  # (long) 현재가
        h14 = self.com.GetHeaderValue(14)  # char  체결 상태
        h17 = self.com.GetHeaderValue(17)  # long  순간체결수량
        # INSERT INTO curtbl (sno, cod, tim, sb, qty)
        # cod : h0
        # tim : timStamp()
        # sb :  h14
        # qty : h17
        self.dbcont.add_cur((h0, timStamp(), chr(h14), h13, h17))

class SampleStockJpBid(object):
    ''' 주식/ETF/ELW 종목 매도,매수에 관한 1차 ~10차 호가/LP호가 및 호가잔량 수신'''

    def __init__(self, cod, dbcont):
        self.com = StockJpbid(self.publish)
        self.cod = cod
        self.dbcont = dbcont

    def subscribe(self):
        self.com.SetInputValue(0, self.cod)  # string  종목 코드
        self.com.Subscribe()

    def publish(self):
        h0 = self.com.GetHeaderValue(0)  # string  종목코드
        bids = []
        for i in range(3,23):
            bids.append(self.com.GetHeaderValue(i))
        h2 = self.com.GetHeaderValue(2)  # long  거래량
        itm = ((h0,timStamp()) + tuple(bids) + (h2,))
        self.dbcont.add_bid(itm)

from cppy.CpSysDib import CpSvrNew7043


class SampleCpSvrNew7043(object):
    ''' 거래소,코스닥 등락현황(상한,하한,상승,하락 등등) 데이터를 요청하고 수신합니다'''

    def __init__(self, q, comSets, dbcont):
        self.com = CpSvrNew7043(self.response)
        self.q = q
        self.comSets = comSets
        self.startRt = 5 # % percent
        self.endRt = 30 # % percent
        self.dbcont = dbcont
        self.poolSet = set()
        self.subs_li = []

    def request(self):
        self.com.SetInputValue(0,ord('0')) # 거래소 + 코스닥
        self.com.SetInputValue(1,ord('2')) # 상승
        self.com.SetInputValue(2,ord('1')) # 당일
        self.com.SetInputValue(3,21) # 전일대비율 상위순
        self.com.SetInputValue(4,ord('1')) # 관리제외
        self.com.SetInputValue(5,ord('3')) # 10만주이상
        self.com.SetInputValue(6,ord('0')) # 시가대비
        self.com.SetInputValue(7, self.startRt)
        self.com.SetInputValue(8, self.endRt)
        #self.com.Request()
        self.q.put(self.com)

    def response(self):
        h0 = self.com.GetHeaderValue(0)  # short  해당 종목 건수
        h1 = self.com.GetHeaderValue(1)  # short  총 종목 건수
        for i in range(h1):  # 조회할 건수를 세팅하세요
            d0 = self.com.GetDataValue(0, i)  # string  종목코드
            d1 = self.com.GetDataValue(1, i)  # string  종목명
            d2 = self.com.GetDataValue(2, i)  # long  현재가
            d3 = self.com.GetDataValue(3, i)  # char  대비플래그
            d4 = self.com.GetDataValue(4, i)  # long  대비
            d5 = self.com.GetDataValue(5, i)  # float  대비율(등락률)
            d6 = self.com.GetDataValue(6, i)  # long  거래량
            d7 = self.com.GetDataValue(7, i)  # long
            d8 = self.com.GetDataValue(8, i)  # long
            d10 = self.com.GetDataValue(10, i)  # long

            if d0 not in self.poolSet and len(d0) > 0:
                if len(self.poolSet) < 200:
                    # add pool
                    self.poolSet.add(d0)
                    # add cur, bid
                    cur = SampleStockCur(d0, self.dbcont)
                    bid = SampleStockJpBid(d0, self.dbcont)
                    cur.subscribe()
                    bid.subscribe()
                    self.subs_li.append(cur)
                    self.subs_li.append(bid)
                    # add lists
                    self.dbcont.add_cod((d0, d1, timStamp()))
                    print ('add: ', d1, d2, timStamp())

        if self.com.GetContinue() == 1:
            self.q.put(self.com)
        else:
            self.request()

from cppy.util import CpCybos
import cppy.util
import pythoncom
import time
import queue
import threading
import sqlite3


class DbControl(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path
        self.create_tbl_query_cur = '''
        CREATE TABLE IF NOT EXISTS curtbl
        ( sno INTEGER, cod TEXT, tim TEXT, sb TEXT, pr INTEGER, qty INTEGER,
          PRIMARY KEY (sno, cod) )
        '''
        self.insert_tbl_query_cur = '''
        INSERT INTO curtbl (sno, cod, tim, sb, pr, qty)
        VALUES(?, ?, ?, ?, ?, ?)
        '''
        self.create_idx_query_cur = '''
        CREATE INDEX curtbl_idx ON curtbl ( cod ASC, tim ASC )
        '''
        self.create_tbl_query_bid = '''
        CREATE TABLE IF NOT EXISTS bidtbl
        ( sno INTEGER, cod TEXT, tim TEXT,
        sll1_pr INTEGER, buy1_pr INTEGER, sll1_qty INTEGER, buy1_qty INTEGER,
        sll2_pr INTEGER, buy2_pr INTEGER, sll2_qty INTEGER, buy2_qty INTEGER,
        sll3_pr INTEGER, buy3_pr INTEGER, sll3_qty INTEGER, buy3_qty INTEGER,
        sll4_pr INTEGER, buy4_pr INTEGER, sll4_qty INTEGER, buy4_qty INTEGER,
        sll5_pr INTEGER, buy5_pr INTEGER, sll5_qty INTEGER, buy5_qty INTEGER,
        vol INTEGER,
        PRIMARY KEY (sno, cod) )
        '''
        self.insert_tbl_query_bid = '''
        INSERT INTO bidtbl
        ( sno , cod , tim ,
        sll1_pr , buy1_pr , sll1_qty , buy1_qty ,
        sll2_pr , buy2_pr , sll2_qty , buy2_qty ,
        sll3_pr , buy3_pr , sll3_qty , buy3_qty ,
        sll4_pr , buy4_pr , sll4_qty , buy4_qty ,
        sll5_pr , buy5_pr , sll5_qty , buy5_qty ,
        vol )
        VALUES
        (? , ? , ? ,
        ? , ? , ? , ? ,
        ? , ? , ? , ? ,
        ? , ? , ? , ? ,
        ? , ? , ? , ? ,
        ? , ? , ? , ? ,
        ? )
        '''
        self.create_idx_query_bid = '''
        CREATE INDEX bidtbl_idx ON bidtbl ( cod ASC, tim ASC )
        '''
        self.create_tbl_query_list = '''
        CREATE TABLE IF NOT EXISTS codlist
        ( cod TEXT,nm TEXT,tim TEXT,
        PRIMARY KEY(cod))
        '''
        self.insert_tbl_query_list = '''
        INSERT INTO codlist ( cod, nm, tim )
        VALUES (? ,? ,?)
        '''
        # queue
        self.cur_q = queue.Queue()
        self.bid_q = queue.Queue()
        self.lis_q = queue.Queue()
        # sno
        self.cur_sno =0
        self.bid_sno =0


    def add_cur(self, itm):
        self.cur_q.put(itm)

    def add_bid(self, itm):
        self.bid_q.put(itm)

    def add_cod(self, itm):
        self.lis_q.put(itm)


    def run(self):
        # create tables
        self.conn = sqlite3.connect(self.path)
        print ('[IO THREAD] db connect')
        # table + index
        self.conn.execute(self.create_tbl_query_cur)
        self.conn.execute(self.create_idx_query_cur)
        self.conn.execute(self.create_tbl_query_bid)
        self.conn.execute(self.create_idx_query_bid)
        self.conn.execute(self.create_tbl_query_list)
        self.conn.commit()
        print ('[IO THREAD] create tables')

        while True:
            # lists updt
            if self.lis_q.qsize() >= 1:
                itm = self.lis_q.get_nowait()
                self.conn.execute(self.insert_tbl_query_list, itm)
                self.conn.commit()
            # cur updt
            if self.cur_q.qsize() >= 512:
                itm_li = []
                for i in range(512):
                    itm = self.cur_q.get_nowait()
                    itm_li.append(tuple([self.cur_sno])+itm)
                    self.cur_sno += 1
                self.conn.executemany(self.insert_tbl_query_cur, itm_li)
                self.conn.commit()
                print ('[IO THREAD] insert bulk cur 512')
            # bid updt
            if self.bid_q.qsize() >= 512:
                itm_li = []
                for i in range(512):
                    itm = self.bid_q.get_nowait()
                    itm_li.append(tuple([self.bid_sno])+itm)
                    self.bid_sno += 1
                self.conn.executemany(self.insert_tbl_query_bid, itm_li)
                self.conn.commit()
                print ('[IO THREAD] insert bulk bid 512')
            time.sleep(0.01)



if __name__ == '__main__':
    cpcybos = CpCybos()

    if cpcybos.GetIsConnect() == 1:
        #lists = cppy.util.get_common_codlist()
        commonSets = set(cppy.util.getCommonStockCods())

        # request queue
        nrq = queue.Queue()

        # db
        dt = datetime.datetime.now()
        dt_nm = 'test_%s%s%s.db'%(dt.year, dt.month, dt.day)
        dbcontrol = DbControl(dt_nm)
        dbcontrol.start() # thread start (DB IO only)

        # cp  objects
        cp7043 = SampleCpSvrNew7043(nrq, commonSets, dbcontrol) # 7043
        cp7043.request()

        # event loop
        for bRq in cppy.util.generatorIntervalRequest(nrq):
            pythoncom.PumpWaitingMessages()
            time.sleep(0.001)
    else:
        print('not connected X')

