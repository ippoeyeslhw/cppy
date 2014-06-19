# coding: utf-8
__author__ = 'lhw'


#############################################################
import win32com
import win32com.client
import pythoncom
import new
import threading
import time


#############################################################
#
#  데코레이터를 사용하여 사용자 클래스에 덧붙인다.
#
#############################################################

def CpRqRpClass(com_str):
    def ret_decoclass(usr_cls):

        # request , response 메서드를 반드시 만들도록 한다.
        if hasattr(usr_cls, 'request') == False:
            raise Exception('"request" method is not exist in your class')

        if hasattr(usr_cls, 'response') == False:
            raise Exception('"response" method is not exist in your class')

        # 사이보스 플러스의 Req/Res 통신을 사용하기 위한 이벤트 핸들러
        class CpRqRpEventHandler:
            def OnReceived(self):
                #연결된 유저객체의 response 메서드를 재호출한다.
                self.usr_obj.response(self.com_obj)

        # 유저클래스를 상속하는 자식클래스를 생성
        class DecoratedCpRqRpClass(usr_cls):
            def __init__(self):
                # 사이보스 Rq/Rp 새로운 이벤트 핸들러를 생성한다.
                handler = new.classobj('CpRqRpEventHandler_%s'%id(self),
                    (CpRqRpEventHandler,),
                    {}
                )
                # 핸들러에 유저객체와 com객체 연결
                handler.usr_obj = self
                handler.com_obj = win32com.client.Dispatch(com_str)
                win32com.client.WithEvents(handler.com_obj, handler)
                # 핸들러를 유저객체에 연결
                self.handler = handler

                super(self.__class__, self).__init__()

            def request(self):
                # 유저클래스에서는 request를 정의하여야하며
                # com_obj 를 인자로 받도록 하여야 한다.
                super(self.__class__, self).request(self.handler.com_obj)

        return DecoratedCpRqRpClass

    return ret_decoclass

#############################################################
#
#  Useage:
#      1. request, response 메소드를 지닌 사용자 클래스를 정의
#      2. 해당 클래스를 CpRqRpClass 데코레이터로 Wrapping
#      3. 데코레이터의 인자는 COM객체 문자열을 넣어준다.
#
#############################################################
if __name__ == '__main__':

    @CpRqRpClass('dscbo1.StockMst')
    class DummyClass(object):
        def request(self, com_obj):
            com_obj.SetInputValue(0, 'A122630')
            com_obj.Request()

        def response(self, com_obj):
            print com_obj.GetHeaderValue(1)
            time.sleep(2)
            self.request()

    @CpRqRpClass('dscbo1.StockMst')
    class CloneClass(object):
        def request(self, com_obj):
            com_obj.SetInputValue(0, 'A114800')
            com_obj.Request()

        def response(self, com_obj):
            print com_obj.GetHeaderValue(1)
            time.sleep(2)
            self.request()

    a = DummyClass()
    print a.__class__
    b = CloneClass()
    print b.__class__

    a.request()
    time.sleep(0.5)
    b.request()

    while True:
        pythoncom.PumpWaitingMessages()
        time.sleep(0.01)




