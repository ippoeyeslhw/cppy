# coding: utf-8

from cppy.CpUtil import CpCybos
import cppy.util
import pythoncom
import time
import queue
from cppy.CpSysDib import CpSvrNew7043


class SampleCpSvrNew7043(object):
    ''' 거래소,코스닥 등락현황(상한,하한,상승,하락 등등) 데이터를 요청하고 수신합니다'''

    def __init__(self, q):
        self.com = CpSvrNew7043(self.response)
        self.q = q

    def request(self):
        self.com.SetInputValue(0, ord('0'))  # char  시장구분
        self.com.SetInputValue(1, ord('2'))  # char  선택기준구분
        self.com.SetInputValue(2, ord('1'))  # char  기준일자구분
        self.com.SetInputValue(3, 21)  # short  순서구분
        self.com.SetInputValue(4, ord('1'))  # char  관리구분
        self.com.SetInputValue(5, ord('3'))  # char  거래량구분
        self.com.SetInputValue(6, ord('0'))  # char  기간구분
        self.com.SetInputValue(7, 3)  # short  등락률 시작 (선택기준구분이 상승,하락인 경우만 유효)
        self.com.SetInputValue(8, 30)  # short  등락률 끝    (선택기준구분이 상승,하락인 경우만 유효)
        self.q.put(self.com)

    def response(self):
        h0 = self.com.GetHeaderValue(0)  # short  해당 종목 건수
        h1 = self.com.GetHeaderValue(1)  # short  총 종목 건수

        for i in range(h0):  # 조회할 건수를 세팅하세요
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

        # 연속처리
        iscont = self.com.GetContinue()
        if iscont == 1:
            self.q.put(self.com)
        else:
            self.request()




# ======================== #
cpcybos = CpCybos()
isconnect = cpcybos.GetIsConnect()

if isconnect == 1:
    # 접속되어 있는 경우

    # 일반적인 종목 리스트 얻어옴
    cod_lists = cppy.util.getCommonStockCods()

    print(len(cod_lists))

    # request 요청 객체 담아두는 queue 선언
    rqQueue = queue.Queue()

    # 메세지 펌핑 루프
    for rqBool in cppy.util.generatorIntervalRequest(rqQueue):
        pythoncom.PumpWaitingMessages()
        time.sleep(0.001)

else:
    print('cybosplus 접속끊겨있는 상태입니다.')
