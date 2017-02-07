# coding: utf-8
from cppy.CpUtil import CpCodeMgr


def getCommonStockCods():
    '''
    일반적인 종목코드를 리스트로 반환합니다.
    (거래소+코스닥, 경고위험제외, 관리종목제외, 거래정지중단제외, 리츠워런트ETFETN제외)
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

