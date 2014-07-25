# coding=utf-8
from cppy.adaptor import CpRqRpClass, CpSubPubClass
from cppy.processor import EventProcessor

# 이벤트 처리기, 이 모듈이 실행될시 할당됨
evntproc = None


###################################################
# Adaptors : 발생한 이벤트를 처리기에 전달하는 역할
#
###################################################

# 주식 현재가
@CpSubPubClass('dscbo1.StockCur')
class StkCur(object):
    def __init__(self, itm_cod='A122630'):
        self.itm_cod = itm_cod

    def subscribe(self, com_obj):
        com_obj.Unsubscribe()
        com_obj.SetInputValue(0, self.itm_cod)
        com_obj.Subscribe()

    def publish(self, com_obj):
        nowpr    = com_obj.GetHeaderValue(13) # 현재가
        sellbuy  = com_obj.GetHeaderValue(14) # 매수매도구분(체결시)
        clsqty   = com_obj.GetHeaderValue(17) # 순간체결수량

        # 이벤트처리기에 전달
        evntproc.push('cls_%s'%(self.itm_cod),(nowpr, chr(sellbuy), clsqty))


# 주식 호가잔량
@CpSubPubClass('dscbo1.StockJpBid')
class StkBid(object):
    def __init__(self):
        self.itm_cod = 'A122630'

    def subscribe(self, com_obj):
        com_obj.Unsubscribe()
        com_obj.SetInputValue(0, self.itm_cod)
        com_obj.Subscribe()

    def publish(self, com_obj):
        tlist = []
        for i in xrange(3,23,4):
            itm = (
                com_obj.GetHeaderValue(i+0),
                com_obj.GetHeaderValue(i+1),
                com_obj.GetHeaderValue(i+2),
                com_obj.GetHeaderValue(i+3)
            )
            tlist.append(itm)
        # 이벤트 처리기에 전달
        evntproc.push('ord_%s'%self.itm_cod, tlist)




###################################################
# Observers : 자신의 키 패턴에 매칭되는 이벤트를 처리함
#
###################################################

# 체결시 출력
def cls_echo(serieses, key, dat):
    print 'key:%s, dat:%s'%(key,dat)

# 호가변경시 출력
def ord_echo(serieses, key, dat):
    print 'key:%s, dat:%s'%(key, dat)

if __name__ == "__main__":

    # 이벤트 처리기 세팅
    evntproc = EventProcessor()
    evntproc.add_observer(['cls_*'], cls_echo)
    evntproc.add_observer(['ord_*'], ord_echo)
    evntproc.start()

    # 현재가, 매수매도구분, 순간체결량을 생산
    stkcur1 = StkCur()
    stkcur1.itm_cod = 'A122630'
    stkcur1.subscribe()

    stkcur2 = StkCur()
    stkcur2.itm_cod = 'A114800'
    stkcur2.subscribe()

    # 호가잔량 생산
    stkbid1 = StkBid()
    stkbid1.itm_cod = 'A122630'
    stkbid1.subscribe()

    stkbid2 = StkBid()
    stkbid2.itm_cod = 'A114800'
    stkbid2.subscribe()

    import pythoncom, time
    while True:
        pythoncom.PumpWaitingMessages()
        time.sleep(0.01)

