# coding: utf-8

import re

def parseHelpPage(txt):
    '''
    코드생성해주는 유틸리티 펑션
    Help 파일의 페이지의 설명을 읽어 샘플클래스로 생성,
    정확하지 않으니 제대로 생성이 안될 경우 직접 작성하세요
    '''
    #start parse
    lines = txt.strip().split('\n')
    cls_nm = lines[0].strip()
    #print('클래스명: ', cls_nm)

    desc_cls = '' # 클래스 설명
    comu_typ = 'Request/Reply' # 통신종류
    module_nm = '' # 모듈위치

    # cut idx
    setinput_line = 0
    getheader_line = 0
    getdata_line = 0
    getsub_line = 0
    lines = lines[1:]

    # 메서드 위치 찾기
    for i, line in enumerate(lines):
        if line.find('설명') != -1:
            desc_cls = lines[i+1]
        if line.find('통신종류') != -1:
            comu_typ = lines[i+1]
        if line.find('모듈 위치') != -1:
            module_nm = lines[i+1]
        if line.find('object.SetInputValue') != -1:
            setinput_line = i
        if line.find('object.GetHeaderValue') != -1:
            getheader_line = i
        if line.find('object.GetDataValue') != -1:
            getdata_line = i
        if line.find('object.Subscribe') != -1:
            getsub_line = i

    #print(desc_cls, comu_typ, module_nm,setinput_line, getheader_line, getdata_line)

    # setinputvalue extract
    setinput_list = []
    is_exist_prev = False
    prev_field_no = 0
    prev_field_type = ''
    prev_field_nm = ''
    prev_field_desc = ''
    for i , line in enumerate(lines[setinput_line: getheader_line]):
        #print(i, line)
        m = re.search(r'^(\d+)\s*-\s*\(\s*(\w+)\s*\)(.*)', line)
        if m:
            if is_exist_prev == False:
                is_exist_prev = True
            else:
                #print(prev_field_no, prev_field_type, prev_field_nm, prev_field_desc)
                setinput_list.append((prev_field_no, prev_field_type, prev_field_nm, prev_field_desc))
            prev_field_no = m.group(1)
            prev_field_type = m.group(2)
            prev_field_nm = m.group(3)
            prev_field_desc = ''

        else:
            if is_exist_prev == False:
                prev_field_desc = ''
            else:
                prev_field_desc += line.strip()
                if line.strip() != '':
                    prev_field_desc += '\n'

    # last
    if is_exist_prev == True:
        setinput_list.append((prev_field_no, prev_field_type, prev_field_nm, prev_field_desc))

    #setheadervalue extract
    getheader_list = []
    is_exist_prev = False
    prev_field_no = 0
    prev_field_type = ''
    prev_field_nm = ''
    prev_field_desc = ''
    for i , line in enumerate(lines[getheader_line: getdata_line]):
        #print(i, line)
        m = re.search(r'^(\d+)\s*-\s*\(\s*(\w+)\s*\)(.*)', line)
        if m:
            if is_exist_prev == False:
                is_exist_prev = True
            else:
                #print(prev_field_no, prev_field_type, prev_field_nm, prev_field_desc)
                getheader_list.append((prev_field_no, prev_field_type, prev_field_nm, prev_field_desc))

            prev_field_no = m.group(1)
            prev_field_type = m.group(2)
            prev_field_nm = m.group(3)
            prev_field_desc = ''

        else:
            if is_exist_prev == False:
                prev_field_desc = ''
            else:
                prev_field_desc += line.strip()
                if line.strip() != '':
                    prev_field_desc += '\n'

    # last
    #print(prev_field_no, prev_field_type, prev_field_nm, prev_field_desc)
    if is_exist_prev == True:
        getheader_list.append((prev_field_no, prev_field_type, prev_field_nm, prev_field_desc))

    # getdatavalue extract
    getdata_list = []
    is_exist_prev = False
    prev_field_no = 0
    prev_field_type = ''
    prev_field_nm = ''
    prev_field_desc = ''
    for i , line in enumerate(lines[getdata_line: getsub_line]):
        #print(i, line)
        m = re.search(r'^(\d+)\s*-\s*\(\s*(\w+)\s*\)(.*)', line)
        if m:
            if is_exist_prev == False:
                is_exist_prev = True
            else:
                #print(prev_field_no, prev_field_type, prev_field_nm, prev_field_desc)
                getdata_list.append((prev_field_no, prev_field_type, prev_field_nm, prev_field_desc))

            prev_field_no = m.group(1)
            prev_field_type = m.group(2)
            prev_field_nm = m.group(3)
            prev_field_desc = ''

        else:
            if is_exist_prev == False:
                prev_field_desc = ''
            else:
                prev_field_desc += line.strip()
                if line.strip() != '':
                    prev_field_desc += '\n'

    # last
    #print(prev_field_no, prev_field_type, prev_field_nm, prev_field_desc)
    if is_exist_prev == True:
        getdata_list.append((prev_field_no, prev_field_type, prev_field_nm, prev_field_desc))


    # module rename
    if module_nm.find('cpdib') != -1:
        module_nm = 'CpDib'
    if module_nm.find('cpsysdib') != -1:
        module_nm = 'CpSysDib'
    if module_nm.find('cptrade') != -1:
        module_nm = 'CpTrade'
    if module_nm.find('cputil') != -1:
        module_nm = 'CpUtil'

    # 요청 통신 종류
    send_nm = ''
    send_nm_u = ''
    recv_nm = ''
    if comu_typ.strip() == 'Request/Reply':
        send_nm = 'request'
        send_nm_u = 'Request'
        recv_nm = 'response'
    else:
        send_nm = 'subscribe'
        send_nm_u = 'Subscribe'
        recv_nm = 'publish'


    basic_format = """
from cppy.%s import %s

class Sample%s(object):
    '''%s'''
    def __init__(self):
        self.com = %s(self.%s)
    def %s(self):
        %s
        self.com.%s()
    def %s(self):
        %s

        %s
    """

    input_format = '\n\t\t'.join(["self.com.SetInputValue(%s, s%s) # %s %s"%(itm[0],itm[0], itm[1], itm[2]) for itm in setinput_list])
    header_format = '\n\t\t'.join(
        ["h%s = self.com.GetHeaderValue(%s) # %s %s " % (itm[0], itm[0], itm[1], itm[2]) for itm in getheader_list])

    data_format = ''
    if len(getdata_list) > 0:
        data_format = 'for i in range(cnt): # 조회할 건수를 세팅하세요\n\t\t\t'
        data_format += '\n\t\t\t'.join(["d%s = self.com.GetDataValue(%s, i) # %s %s"%(itm[0],itm[0], itm[1], itm[2]) for itm in getdata_list])

    return (basic_format%(
        module_nm, cls_nm,
        cls_nm,
        desc_cls,
        cls_nm, recv_nm,
        send_nm,
        input_format,
        send_nm_u,
        recv_nm,
        header_format,
        data_format
        ))

helpstring = '''
CpSvr9842S

설명
 투자 주체별로 어느 종목을 얼마만큼 매수잔고로 보유하고 있고, 혹은 매도잔고로 보유하고 있는지 직관적으로 파악할수 있으며, 이를 투자주체별로 비교할수 있다
(고객 등급 제한 오브젝트 입니다.)

통신종류
 Subscribe/Publish

관련 RQ/RP
 CpSvr9842

관련CYBOS
 [9842 투자주체별 종목 비교] 실시간

모듈 위치
 cpsysdib.dll


Method
object.SetInputValue(type,value)

type에 해당하는 입력 데이터를 value 값으로 지정합니다

type: 입력 데이터 종류

0 - (char) 장구분

코드
 내용

'1'
 선물

'2'
 콜옵션

'3'
 풋옵션


1 - (char) 월물구분

코드
 내용

'1'
 최근월물

'2'
 차근월물


2 - (char) 일자구분

코드
 내용

'1'
 당일

'2'
 기간


3- (short) 투자자 구분 코드

코드
 내용

0
 개인

1
 외국인

2
 기관계

3
 증권

4
 보험

5
 투신

6
 은행

7
 종금/신금

8
 기금/연금

9
 기타(국가)

10
 선물회사

11
 기타(법인)


value: 새로 지정할 값



value = object.GetHeaderValue(type)

type에 해당하는 헤더 데이터를 반환합니다

type: 데이터 종류

0- (short) 투자자 구분 코드

1 - (ulong) 수신 시간

2 - (short) 종목갯수

반환값: 데이터 종류에 해당하는 값

value = object.GetDataValue (Type,index)

type에 해당하는 데이터를 반환합니다

type: 데이터 종류

0-( string) 대상종목코드
 1-( long ) 보유계약

2-( float ) 평균단가

3-( long) 보유금액

4-( float ) 확정손익

index: data index

반환값: 데이터 종류의 index번째 data

object.Subscribe()

실시간 데이터 수신을 신청한다

object.Unsubscribe()

실시간 데이터 수신를 해지한다

object.Request()

사용하지 않음

object.BlockRequest()

사용하지 않음

Event

Object.Received

해당하는 데이터를 수신했을 때 발생하는 이벤트


'''



print(parseHelpPage(helpstring))
