# coding: utf-8

from cppy.CpUtil import CpCybos
import cppy.util
import pythoncom
import time
import queue







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
    for rqBool in cppy.util.genNontradeRequest(rqQueue):
        pythoncom.PumpWaitingMessages()
        time.sleep(0.001)

else:
    print('cybosplus 접속끊겨있는 상태입니다.')
