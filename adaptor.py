import win32com
import win32com.client


def class_factory(com_str):
    class ProductClass(object):
        def __init__(self, handler):
            '''
            :param handler: 이벤트 수신시 동작할 callable 객체, 함수
            '''
            if callable(handler) == False:
                raise "not callable object"

            class Handler:
                def OnReceived(self):
                    self.handler()
            self.disp = win32com.client.Dispatch(com_str)
            win32com.client.WithEvents(self.disp, Handler)
            Handler.handler = handler
            self.handler_cls = Handler

        def SetInputValue(self, typ, val):
            self.disp.SetInputValue(typ, val)

        def GetHeaderValue(self, typ):
            return self.disp.GetHeaderValue(typ)

        def GetDataValue(self, typ, idx):
            return self.disp.GetDataValue(typ, idx)

        def Request(self):
            self.disp.Request()

        def BlockRequest(self):
            self.disp.BlockRequest()

        def Subscribe(self):
            self.disp.Subscribe()

        def Unsubscribe(self):
            self.disp.Unsubscribe()

    return ProductClass