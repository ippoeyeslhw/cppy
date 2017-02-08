# coding: utf-8
from cppy.CpUtil import CpCodeMgr
from cppy.CpUtil import CpCybos

import queue

def getCommonStockCods():
    '''
    일반적인 종목코드를 리스트로 반환합니다.
    (거래소+코스닥, 우선주제외, 스팩제외, 경고위험제외, 관리종목제외, 거래정지중단제외, 리츠워런트ETFETN제외)
    :return: code list
    '''
    ret = []
    codmgr = CpCodeMgr()

    kospi_cods = codmgr.GetStockListByMarket(CpCodeMgr.CPC_MARKET_KOSPI)
    kosdq_cods = codmgr.GetStockListByMarket(CpCodeMgr.CPC_MARKET_KOSDAQ)

    # 리스트를 합침
    cods_list = kospi_cods + kosdq_cods

    for cod in cods_list:
        # 감리구분: 정상 + 주의 종목 까지
        cont_kind = codmgr.GetStockControlKind(cod)
        if cont_kind != CpCodeMgr.CPC_CONTROL_NONE:
            if cont_kind != CpCodeMgr.CPC_CONTROL_ATTENTION:
                continue

        # 관리구분: 관리종목 제외
        super_kind = codmgr.GetStockSupervisionKind(cod)
        if super_kind != CpCodeMgr.CPC_SUPERVISION_NONE:
            continue

        # 상태구분: 정상 (정지,중단 제외)
        stat_kind = codmgr.GetStockStatusKind(cod)
        if stat_kind != CpCodeMgr.CPC_STOCK_STATUS_NORMAL:
            continue

        # 부구분 : 주권만 선택 (ETF, 리츠, 워런트 등등 제외)
        sec_kind = codmgr.GetStockSectionKind(cod)
        if sec_kind != CpCodeMgr.CPC_KSE_SECTION_KIND_ST:
            continue

        # 우선주제외
        if codmgr.isCommonStock(cod) == False:
            continue

        # 스팩제외
        if codmgr.isSpacStock(cod) == True:
            continue

        # 통과종목 append
        ret.append(cod)

    ret.sort()
    return ret


def genNontradeRequest(q, waitTick=250):
    '''
    Non-trade Rq/Rp 균등시간 요청하기 위한 제네레이터
    :param q: Request 메서드가 있는 객체
    :param waitTick:  next 호출 횟수 간격
    :return: Request호출시 True, 그외 False
    '''
    if q.__class__.__name__ != 'Queue':
        raise 'param queu error'

    cpcybos = CpCybos()
    desc_cnt = 0

    q = queue.Queue()
    while True:
        ret = False
        # tick count 수가 없으면 (request 가능)
        if desc_cnt <= 0:
            # 가능 개수를 센다.
            rcnt = cpcybos.GetLimitRemainCount(CpCybos.LT_NONTRADE_REQUEST)
            if rcnt > 0:
                try:
                    desc_cnt = waitTick
                    # queue에서 가져옴
                    itm = q.get_nowait()
                    itm.Request()
                    ret = True
                except queue.Empty:
                    pass
            else:
                # wait more
                pass
        else:
            desc_cnt -= 1

        # generator
        yield ret


