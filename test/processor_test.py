<<<<<<< HEAD
# coding: utf-8
=======
>>>>>>> origin/processor_impl
__author__ = 'lhw'


import multiprocessing
import pythoncom, time
<<<<<<< HEAD
import collections



class QueueControler(multiprocessing.Process):
    def __init__(self):
        super(QueueControler, self ).__init__()
        self.buf   = multiprocessing.Queue()
        self.q_set = dict()
        self.DEQUE_SIZE = 4096

    # 다른 프로세스에 의해 불려지는 인터페이스
    # 일단 데이터가 buffer에 push 된다.
    def push(self, key, data):
        ts = time.time() # time stamp
        self.buf.put((ts,key,data))

    # buffer 에 쌓인 데이터를 일괄 처리한다.
    def __buf_sweep(self):
        #############################################
        # 버퍼에 쌓인 데이터를 각 key 에 맞게
        # 덱에 분배를 한다 이때 sliding window 의 성격을
        # 만들기 위해 덱의 크기를 일정하게 유지한다.
        ##############################################

        # 정해진 크기만큼 분할해서 처리
        for i in xrange(self.DEQUE_SIZE):
            if self.buf.empty():
                break

            itm = self.buf.get()
            ts  = itm[0]
            key = itm[1]
            dat = itm[2]

            # 키가 큐집합에 없는 경우 덱 추가
            if (key in self.q_set) == False:
                self.q_set[key] = collections.deque()

            # 덱에 원소 추가 (왼쪽으로 넣는다)
            self.q_set[key].appendleft((ts, dat))

        # 모든 덱의 사이즈를 조정
        for key in self.q_set.keys():
            while self.DEQUE_SIZE <= len(self.q_set[key]):
                # 덱에 원소 제거 (오른쪽으로 뺀다)
                self.q_set[key].pop()


    def run(self):
        while True:
            # 반복 실행될 작업
            self.__buf_sweep()

=======



class CpScheduler(multiprocessing.Process):
    def __init__(self):
        self.req_adaptors = multiprocessing.Queue()
        self.sub_adaptors = multiprocessing.Queue()
        super(CpScheduler, self).__init__()

    def run(self):
        while True:
            # looping

            pythoncom.PumpWaitingMessages()
>>>>>>> origin/processor_impl
            time.sleep(0.001)




<<<<<<< HEAD




if __name__ == '__main__':
    print 'processor_test.py'

    qc = QueueControler()
    qc.start()  # 다른 프로세스에 의해 실행

    cnt = 0
    while True:
        print 'start'
        time.sleep(5)
        qc.push('test', 'test.data%s'%cnt)
        cnt += 1
=======
class EventProcessor(multiprocessing.Process):
    def __init__(self):
        super(EventProcessor, self).__init__()

    def run(self):
        pass
>>>>>>> origin/processor_impl



