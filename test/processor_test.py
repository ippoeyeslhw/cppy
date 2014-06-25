__author__ = 'lhw'


import multiprocessing
import pythoncom, time



class CpScheduler(multiprocessing.Process):
    def __init__(self):
        self.req_adaptors = multiprocessing.Queue()
        self.sub_adaptors = multiprocessing.Queue()
        super(CpScheduler, self).__init__()

    def run(self):
        # 초기화


        while True:
            # 매 인터벌 간격에 수행해야 할 일들


            # looping
            pythoncom.PumpWaitingMessages()
            time.sleep(0.001)




class EventProcessor(multiprocessing.Process):
    def __init__(self):
        super(EventProcessor, self).__init__()

    def run(self):
        pass



