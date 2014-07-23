# coding=utf-8
from cppy.adaptor import CpRqRpClass, CpSubPubClass
from cppy.processor import EventProcessor

evntproc = None

@CpRqRpClass('CpSysDib.StockChart')
class StkChart(object):
    def request(self, com_obj):
        com_obj.SetInputValue(0, 'A003540')
        com_obj.SetInputValue(1, ord('2'))
        com_obj.SetInputValue(4, 1000)
        com_obj.SetInputValue(5, [5])
        com_obj.SetInputValue(6, ord('D'))

        com_obj.Request()

    def response(self, com_obj):
        cnt = com_obj.GetHeaderValue(3) #  수신개수
        for i in xrange(cnt):
            # 키와 값을 인자로 하여 이벤트처리기에 전달
            evntproc.push('A003540_%s_dt'%i, com_obj.GetDataValue(0,i))



def echo(serieses, key, dat):
    print 'key:%s, dat:%s'%(key,dat)



# 윈도우의 경우 multiprocessing 사용시 (EventProcessor)
# if __name__ == "__main__" 에서 사용해야함
# https://docs.python.org/2/library/multiprocessing.html
if __name__ == "__main__":

    # 이벤트처리기 구동
    evntproc = EventProcessor()
    # 옵저버를 등록함, A003540으로 시작하는 키가 도착하면 echo 를 수행함
    evntproc.add_observer(['A003540*'], echo)
    evntproc.start()

    # 차트 데이터 요청 (비동기)
    stkchart = StkChart()
    stkchart.request()


    import pythoncom, time
    while True:
        pythoncom.PumpWaitingMessages()
        time.sleep(0.01)
