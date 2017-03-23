# coding: utf-8
from cppy.CpUtil import CpCodeMgr
from cppy.CpUtil import CpCybos
from cppy.CpUtil import CpStockCode

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

class QuitCls:
    def __init__(self):
        self.quit =True

def generatorIntervalRequest(q, waitTick=250, limitType=CpCybos.LT_NONTRADE_REQUEST):
    '''
    Rq/Rp 균등시간 요청하기 위한 제네레이터
    :param q: Request 메서드가 있는 객체
    :param waitTick:  next 호출 횟수 간격
    :param limitType: 제한타입 Default: nontrade
    :return: Request호출시 True, 그외 False
    '''
    if q.__class__.__name__ != 'Queue':
        raise 'param queu error'

    cpcybos = CpCybos()
    desc_cnt = 0

    while True:
        ret = False
        # tick count 수가 없으면 (request 가능)
        if desc_cnt <= 0:
            # 가능 개수를 센다.
            rcnt = cpcybos.GetLimitRemainCount(limitType)
            if rcnt > 0:
                try:
                    # queue에서 가져옴
                    itm = q.get_nowait()
                    try:
                        if itm.quit:
                            return False
                    except AttributeError:
                        pass
                    itm.Request()
                    ret = True
                    desc_cnt = waitTick
                except queue.Empty:
                    pass
            else:
                # wait more
                pass
        else:
            desc_cnt -= 1

        # generator
        yield ret


def getDictPriceKey(cod):
    '''
    종목의 하한가부터 상한가까지 key(int)가 있는 dictionary를 반환합니다.
     value값은 0으로 초기화되어 있습니다.
    :param cod: 종목코드
    :return:  dictionary
    '''
    dic_pr = {}
    cpstkcod = CpStockCode()
    cpcodmgr = CpCodeMgr()
    min_pr = cpcodmgr.GetStockMinPrice(cod)
    max_pr = cpcodmgr.GetStockMaxPrice(cod)
    now_pr = min_pr
    dic_pr[min_pr] = 0
    while now_pr < max_pr:
        now_pr += cpstkcod.GetPriceUnit(cod, now_pr, 1)
        dic_pr[now_pr] = 0
    return dic_pr



import re

def generateClass(txt, description=True):
    '''
        코드생성해주는 유틸리티 펑션
        Help 파일의 페이지의 설명을 읽어 샘플클래스로 생성,
        정확하지 않으니 제대로 생성이 안될 경우 직접 작성하세요
        '''

    # 라인별 종류 반환
    def token(line):
        if line.find('설명') != -1:
            return ('CLS_DESC', None)
        if line.find('통신종류') != -1:
            return ('COMU_TYP', None)
        if line.find('모듈 위치') != -1:
            return ('MOD_POS', None)
        if line.find('연속여부') != -1:
            return ('CONT_YN', None)
        if line.find('object.SetInputValue') != -1:
            return ('INPUT_VAL', None)
        if line.find('object.GetHeaderValue') != -1:
            return ('HEAD_VAL', None)
        if line.find('object.GetDataValue') != -1:
            return ('DATA_VAL', None)
        if line.find('object.Subscribe') != -1:
            return ('SUB', None)
        m = re.search(r'^\s*(\d+)\s*-\s*.*?\(\s*([^)]+)\s*\)(.*)', line)
        if m:
            return ('TYP_VAL', m)

        m = re.search(r'(type|value|반환값):', line)
        if m:
            return ('SKIP', None)
        if line.find('사용하지 않음') != -1:
            return ('SKIP', None)
        if line.strip() == '':
            return ('SKIP', None)

        return ('ANYTHING', None)

    # 클래스명 추출
    lines = txt.strip().split('\n')
    cls_nm = lines[0].strip()

    tok = None

    cls_desc = ''  # 클래스설명
    isrqrp = False  # RQRP 여부
    mod_pos = ''  # 모듈위치
    iscont = False  # 연속여부
    input_val_list = []  # inputvalue 메서드의 각 type 및 value
    head_val_list = []  # headervalue 메서드의 각 type 및 value
    data_val_list = []  # datavalue 메서드의 각 type 및 value
    anything = ''

    # tok 현재토큰,  lookahead 다음 토큰
    # 두 토큰의 관계에 따라 rule에 의해 parsing
    for i, line in enumerate(lines[1:]):
        lookahead = token(line)
        #print (lookahead, line)
        if lookahead == None:
            continue
        if lookahead[0] == 'SKIP':
            continue
        if tok == None:
            pass
        else:
            # 토큰이 있을 경우

            # 클래스 설명
            if tok[0] == 'CLS_DESC':
                cls_desc = line.strip()
            # 통신종류
            if tok[0] == 'COMU_TYP':
                if line.find('Request') != -1:
                    isrqrp = True
                else:
                    isrqrp = False
            # 모듈위치
            if tok[0] == 'MOD_POS':
                if line.find('cpdib') != -1:
                    mod_pos = 'CpDib'
                elif line.find('cpsysdib') != -1:
                    mod_pos = 'CpSysDib'
                elif line.find('cptrade') != -1:
                    mod_pos = 'CpTrade'
                elif line.find('CpUtil') != -1:
                    mod_pos = 'CpUtil'
                else:
                    mod_pos = 'NOTMODULE'
            # 연속여부
            if tok[0] == 'CONT_YN':
                if line.find('X') != -1:
                    iscont = False
                else:
                    iscont = True
            # SetInputValue 메서드
            if tok[0] == 'INPUT_VAL':
                if lookahead[0] == 'TYP_VAL':
                    # 설명 넣기
                    if len(input_val_list) > 0:
                        input_val_list[-1][3] = anything
                    # 필드넣기
                    input_val_list.append([lookahead[1].group(1),
                                           lookahead[1].group(2),
                                           lookahead[1].group(3),
                                           ''])
                    anything = ''
                    continue
                elif lookahead[0] == 'ANYTHING':
                    anything += line + '\n\t\t\t'
                    continue
                elif lookahead[0] == 'SKIP':
                    continue
                else:
                    if len(input_val_list) > 0:
                        input_val_list[-1][3] = anything
                    anything = ''

            # GetHeaderValue 메서드
            if tok[0] == 'HEAD_VAL':
                if lookahead[0] == 'TYP_VAL':
                    # 설명 넣기
                    if len(head_val_list) > 0:
                        head_val_list[-1][3] = anything
                    # 필드넣기
                    head_val_list.append([lookahead[1].group(1),
                                          lookahead[1].group(2),
                                          lookahead[1].group(3),
                                          ''])
                    anything = ''
                    continue
                elif lookahead[0] == 'ANYTHING':
                    anything += line + '\n\t\t\t'
                    continue
                elif lookahead[0] == 'SKIP':
                    continue
                else:
                    if len(head_val_list) > 0:
                        head_val_list[-1][3] = anything
                    anything = ''
            # GetDataValue 메서드
            if tok[0] == 'DATA_VAL':
                if lookahead[0] == 'TYP_VAL':
                    # 설명 넣기
                    if len(data_val_list) > 0:
                        data_val_list[-1][3] = anything
                    # 필드넣기
                    data_val_list.append([lookahead[1].group(1),
                                          lookahead[1].group(2),
                                          lookahead[1].group(3),
                                          ''])
                    anything = ''
                    continue
                elif lookahead[0] == 'ANYTHING':
                    anything += line + '\n\t\t\t'
                    continue
                elif lookahead[0] == 'SKIP':
                    continue
                else:
                    if len(data_val_list) > 0:
                        data_val_list[-1][3] = anything
                    anything = ''

        # 룩어헤드를 현재토큰으로 변경
        tok = lookahead

    # print(cls_desc,isrqrp,mod_pos,iscont,input_val_list,head_val_list,data_val_list)

    # 코드 생성부

    code_format = '''
from cppy.%s import %s

class Sample%s(object):
\tdef __init__(self):
\t\tself.com = %s(self.%s) # event handler

\tdef %s(self):
\t\t%s

\tdef %s(self):
\t\t%s

\t\t%s
    '''

    # input value code
    input_code = ''
    for itm in input_val_list:
        if itm[1] == 'char':
            val = 'ord(v%s)' % itm[0]
        else:
            val = 'v%s' % itm[0]
        if itm[3] != '' and description:
            desc = '"""%s"""\n\t\t' % itm[3]
        else:
            desc = ''
        input_code += 'self.com.SetInputValue(%s, %s) # %s %s %s\n\t\t%s' % (
            itm[0],
            val,
            itm[0],
            itm[1],
            itm[2],
            desc
        )
    # header value code
    head_cod = ''
    for itm in head_val_list:
        if itm[3] != ''and description:
            desc = '"""%s"""\n\t\t' % itm[3]
        else:
            desc = ''
        head_cod += 'h%s = self.com.GetHeaderValue(%s) # %s %s %s\n\t\t%s' % (
            itm[0],
            itm[0],
            itm[0],
            itm[1],
            itm[2],
            desc
        )

    # data value code
    data_code = ''
    if len(data_val_list) > 0:
        data_code = 'for i in range(cnt): # cnt 값을 넣어주세요\n\t\t\t'
    for itm in data_val_list:
        if itm[3] != ''and description:
            desc = '"""%s"""\n\t\t\t' % itm[3]
        else:
            desc = ''
        data_code += 'd%s = self.com.GetDataValue(%s, i) # %s %s %s\n\t\t\t%s' % (
            itm[0],
            itm[0],
            itm[0],
            itm[1],
            itm[2],
            desc
        )

    # 파라미터 생성
    params = None

    if isrqrp == True:
        params = (
            mod_pos,
            cls_nm,
            cls_nm,
            cls_nm,
            'response',
            'request',
            input_code,
            'response',
            head_cod,
            data_code
        )
    else:
        params = (
            mod_pos,
            cls_nm,
            cls_nm,
            cls_nm,
            'publish',
            'subscribe',
            input_code,
            'publish',
            head_cod,
            data_code
        )

    return code_format % params