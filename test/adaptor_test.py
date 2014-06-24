# coding: utf-8
__author__ = 'lhw'



from cppy.adaptor import CpRqRpClass

@CpRqRpClass('dscbo1.StockMst')
class StkMst(object):
    def request(self, com_obj):
        com_obj.SetInputValue(0, 'A122630')
        com_obj.Request()

    def response(self, com_obj):
        print com_obj.GetHeaderValue(1)



if __name__ == '__main__':

    stkmst = StkMst()
    stkmst.request()

    import pythoncom, time
    while True:
        pythoncom.PumpWaitingMessages()
        time.sleep(0.01)