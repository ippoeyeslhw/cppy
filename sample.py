# coding: utf-8
from cppy.util import generateClass

'''
클래스 생성기로 코드를 생성하는 샘플코드 생성파일
1. helpTxt에 도움말 내용 전체 복사붙여넣기
2. 이파일 실행하여 출력코드를 복사하여 사용
'''

helpTxt = '''
StockChart

설명
 주식, 업종, ELW의 차트데이터를 수신합니다.

통신종류
 Request/Reply

연속여부
 X

관련 SB/PB
 StockCur

관련CYBOS
 [7400 통합챠트] 일,주,월,분,틱

모듈 위치
 cpsysdib.dll


Method
object.SetInputValue(type,value)

type에 해당하는 입력 데이터를 value 값으로 지정합니다

type: 입력 데이터 종류

0 - 종목코드(string): 주식(A003540), 업종(U001), ELW(J517016)의 종목코드

1 - 요청구분(char):

코드
 내용

'1'
 기간으로 요청

'2'
 개수으로 요청


2 - 요청종료일(ulong): YYYYMMDD형식으로 데이터의 마지막(가장 최근) 날짜 Default(0) - 최근 거래날짜

3 - 요청시작일(ulong): YYYYMMDD형식으로 데이터의 시작(가장 오래된) 날짜

4 - 요청개수(ulong): 요청할 데이터의 개수

5 - 필드(long or long array): 필드 또는 필드 배열

필드값

0: 날짜(ulong)

1:시간(long) - hhmm

2:시가(long or float)

3:고가(long or float)

4:저가(long or float)

5:종가(long or float)

6:전일대비(long or float) - 주) 대비부호(37)과 반드시 같이 요청해야 함

8:거래량(ulong or ulonglong) 주) 정밀도 만원 단위

9:거래대금(ulonglong)

10:누적체결매도수량(ulong or ulonglong) - 호가비교방식 누적체결매도수량
11:누적체결매수수량(ulong or ulonglong) - 호가비교방식 누적체결매수수량
 (주) 10, 11 필드는 분,틱 요청일 때만 제공

12:상장주식수(ulonglong)

13:시가총액(ulonglong)

14:외국인주문한도수량(ulong)

15:외국인주문가능수량(ulong)

16:외국인현보유수량(ulong)

17:외국인현보유비율(float)

18:수정주가일자(ulong) - YYYYMMDD

19:수정주가비율(float)

20:기관순매수(long)

21:기관누적순매수(long)

22:등락주선(long)

23:등락비율(float)

24:예탁금(ulonglong)

25:주식회전율(float)

26:거래성립률(float)

37:대비부호(char) - 수신값은 GetHeaderValue 8 대비부호와 동일

6 - 차트구분(char)

코드
 내용

'D'
 일

'W'
 주

'M'
 월

'm'
 분

'T'
 틱


7 - 주기(ushort): Default-1

8 - 갭보정여부(char)

코드
 내용

'0'
 갭무보정 [Default]

'1'
 갭보정


9 - 수정주가(char)

코드
 내용

'0'
 무수정주가 [Default]

'1'
 수정주가


10 - 거래량구분(char)

코드
 내용

'1'
 시간외거래량 모두 포함[Default]

'2'
 장종료시간외거래량만 포함

'3'
 시간외거래량 모두 제외

'4'
 장전시간외거래량만 포함


value: 새로 지정할 값

value = object.GetHeaderValue(type)

type에 해당하는 헤더 데이터를 반환합니다

type: 데이터 종류

0 - 종목코드(string)

1 - 필드개수(short)

2 - 필드명의 배열(string array): 필드는 요청한 필드 값의 오름차순으로 정렬되어 있음

3 - 수신개수(long)

4 - 마지막봉틱수(ushort)

5 - 최근거래일(ulong): YYYYMMDD

6 - 전일종가(ulong or float)

7 - 현재가(ulong or float)

8 - 대비부호(char)

코드
 내용

'1'
 상한

'2'
 상승

'3'
 보합

'4'
 하한

'5'
 하락

'6'
 기세상한

'7'
 기세상승

'8'
 기세하한

'9'
 기세하락


9 - 대비(long or float)

10 - 거래량(ulong or ulonglong)

11 - 매도호가(ulong or float)

12 - 매수호가(ulong or float)

13 - 시가(ulong or float)

14 - 고가(ulong or float)

15 - 저가(ulong or float)

16 - 거래대금(ulonglong)

17 - 종목상태(char)

'0' - 정상

'1' - 투자위험

'2' - 관리

'3' - 거래정지

'4' - 불성실공시

'5' - 불성실공시&관리

'6' - 불성실공시&거래정지

'7' - 불성실공시&투자위험

'8' - 투자위험&거래정지

'9' - 관리&거래정지

'A' - 불성실공시&관리&거래정지

'B' - 불성실공시&투자위험&거래정지

'C' - 투자위험예고

'D' - 투자주의

'E' - 투자경고

'F' - 불성실공시&투자위험예고

'G' - 불성실공시&투자주의

'H' - 불성실공시&투자경고

'I' - 투자위험예고&거래정지

'J' - 투자주의&거래정지

'K' - 투자경고&거래정지

'L' - 불성실공시&투자위험예고&거래정지

'M' - 불성실공시&투자주의&거래정지

'N' - 불성실공시&투자경고&거래정지

'Z' - ETF종목

18 - 상장주식수(ulonglong)

19 - 자본금[백만원](ulong)

20 - 전일거래량(ulong or ulonglong)

21 - 최근갱신시간(ulong): hhmm

22 - 상한가(ulong or float)

23 - 하한가(ulong or float)

반환값: 데이터 종류에 해당하는 값



value = object.GetDataValue (Type,index)

type에 해당하는 데이터를 반환합니다

type: 요청한 필드의 index - 필드는 요청한 필드 값으로 오름차순으로 정렬되어 있음

index: 요청한 종목의 index



object.Subscribe()

사용하지 않음

object.Unsubscribe()

사용하지 않음

object.Request()

해당하는 데이터를 요청한다

object.BlockRequest()

데이터 요청.Blocking Mode

Event

Object.Received

해당하는 데이터를 수신했을 때 발생하는 이벤트


'''

# 설명 false
print(generateClass(helpTxt, False))


















########## 생성된 코드 ############
'''
from cppy.CpDib import StockMst


class SampleStockMst(object):
    def __init__(self):
        self.com = StockMst(self.response)  # event handler

    def request(self):
        self.com.SetInputValue(0, '')  # 0 string  종목 코드

    def response(self):
        h0 = self.com.GetHeaderValue(0)  # 0 string  종목 코드
        h1 = self.com.GetHeaderValue(1)  # 1 string  종목 명
        h2 = self.com.GetHeaderValue(2)  # 2 string  대신 업종코드
        h3 = self.com.GetHeaderValue(3)  # 3 string  그룹 코드
        h4 = self.com.GetHeaderValue(4)  # 4 short  시간
        h5 = self.com.GetHeaderValue(5)  # 5 string  소속 구분(문자열)
        h6 = self.com.GetHeaderValue(6)  # 6 string  대형,중형,소형
        h8 = self.com.GetHeaderValue(8)  # 8 long  상한가
        h9 = self.com.GetHeaderValue(9)  # 9 long  하한가
        h10 = self.com.GetHeaderValue(10)  # 10 long  전일종가
        h11 = self.com.GetHeaderValue(11)  # 11 long  현재가
        h12 = self.com.GetHeaderValue(12)  # 12 long  전일대비
        h13 = self.com.GetHeaderValue(13)  # 13 long  시가
        h14 = self.com.GetHeaderValue(14)  # 14 long  고가
        h15 = self.com.GetHeaderValue(15)  # 15 long  저가
        h16 = self.com.GetHeaderValue(16)  # 16 long  매도호가
        h17 = self.com.GetHeaderValue(17)  # 17 long  매수호가
        h18 = self.com.GetHeaderValue(18)  # 18 long  누적거래량 [주의] 기준 단위를 확인하세요
        """시장구분
             기준 단위
            거래소,코스닥,프리보드
             단주
            거래소 지수
             천주
            코스닥 지수 프리보드 지수
             단주
            """
        h19 = self.com.GetHeaderValue(19)  # 19 long  누적거래대금 [주의] 기준 단위를 확인하세요
        """시장구분
             기준 단위
            거래소
             만원
            코스닥,프리보드
             천원
            거래소 지수, 코스닥 지수
             백만원
            프리보드지수
             천원
            """
        h20 = self.com.GetHeaderValue(20)  # 20 long  EPS
        h21 = self.com.GetHeaderValue(21)  # 21 long  신고가
        h22 = self.com.GetHeaderValue(22)  # 22 long  신고가일
        h23 = self.com.GetHeaderValue(23)  # 23 long  신저가
        h24 = self.com.GetHeaderValue(24)  # 24 long  신저가일
        h25 = self.com.GetHeaderValue(25)  # 25 short  신용시장(전체)
        h26 = self.com.GetHeaderValue(26)  # 26 short  결산월
        h27 = self.com.GetHeaderValue(27)  # 27 long  basis price (기준가)
        h28 = self.com.GetHeaderValue(28)  # 28 float  PER
        h31 = self.com.GetHeaderValue(31)  # 31 decimal  상장주식수 [주의] 기준 단위를 확인하세요
        """시장구분
             기준 단위
            거래소
             천주->단주
            코스닥,프리보드
             단주
            """
        h32 = self.com.GetHeaderValue(32)  # 32 long  상장자본금
        h33 = self.com.GetHeaderValue(33)  # 33 long  외국인 DATA 일자
        h34 = self.com.GetHeaderValue(34)  # 34 short  외국인 TIME 일자
        h35 = self.com.GetHeaderValue(35)  # 35 decimal  외국인 상장주식수
        h36 = self.com.GetHeaderValue(36)  # 36 decimal  외국인 주문주식수
        h37 = self.com.GetHeaderValue(37)  # 37 long  외국인 한도수량
        h38 = self.com.GetHeaderValue(38)  # 38 float  외국인 한도비율
        h39 = self.com.GetHeaderValue(39)  # 39 decimal  외국인 주문가능수량
        h40 = self.com.GetHeaderValue(40)  # 40 float  외국인 주문가능비율
        h42 = self.com.GetHeaderValue(42)  # 42 string  증권 전산 업종코드
        h43 = self.com.GetHeaderValue(43)  # 43 short  매매 수량 단위
        h44 = self.com.GetHeaderValue(44)  # 44 char  정상/이상급등/관리/거래 정지 등등 구분(코드)
        """이 구분값 대신에 66, 67, 68번 구분값을 조합해서 사용하시기 바랍니다.
            [거래소 +코스닥]
            '0' - 정상
            '1' - 투자위험
            '2' - 관리
            '3' - 거래정지
            '4' - 불성실공시
            '5' - 불성실공시&관리
            '6' - 불성실공시&거래정지
            '7' - 불성실공시&투자위험
            '8' - 투자위험&거래정지
            '9' - 관리&거래정지
            'A' - 불성실공시&관리&거래정지
            'B' - 불성실공시&투자위험&거래정지
            'C' - 투자위험예고
            'D' - 투자주의
            'E' - 투자경고
            'F' - 불성실공시&투자위험예고
            'G' - 불성실공시&투자주의
            'H' - 불성실공시&투자경고
            'I' - 투자위험예고&거래정지
            'J' - 투자주의&거래정지
            'K' - 투자경고&거래정지
            'L' - 불성실공시&투자위험예고&거래정지
            'M' - 불성실공시&투자주의&거래정지
            'N' - 불성실공시&투자경고&거래정지
            'Z' - ETF종목
            [프리보드]
            '0' - 정상
            '3' - 거래정지
            '4' - 불성실공시 1회
            '5' - 불성실공시 2회
            '6' - 불성실공시 1회 & 거래정지
            '7' - 불성실공시 2회 & 거래정지
            """
        h45 = self.com.GetHeaderValue(45)  # 45 char  소속 구분(코드)
        """코드
             내용
            '1'
             거래소
            '4'
             증권투자
            '5'
             코스닥
            '6'
             프리보드
            '7'
             리츠
            """
        h46 = self.com.GetHeaderValue(46)  # 46 long  전일 거래량
        """시장구분
             기준 단위
            거래소,코스닥,프리보드
             단주
            거래소지수
             천주
            코스닥지수,프리보드지수
             단주
            """
        h47 = self.com.GetHeaderValue(47)  # 47 long  52주 최고가
        h48 = self.com.GetHeaderValue(48)  # 48 long  52주 최고일
        h49 = self.com.GetHeaderValue(49)  # 49 long  52주 최저가
        h50 = self.com.GetHeaderValue(50)  # 50 long  52주 최저일
        """51 - 지원하지 않음
            """
        h52 = self.com.GetHeaderValue(52)  # 52 string  벤처기업 구분
        """ [코스닥과 프리보드만 해당됨]
            시장구분
             내용
            거래소
             해당사항없음
            코스닥
             일반기업/벤처기업
            프리보드
             일반기업/벤처기업/테크노파크일반/테크노파크벤쳐
            """
        h53 = self.com.GetHeaderValue(53)  # 53 string  KOSPI200 채용 여부
        """시장구분
             내용
            거래소
             미분류/제조업/전기통신/건설/유통서비스/금융
             2011년 4월 1일부터 아래 값으로 변경
            시장구분
             내용
            거래소
             미채용/건설기계/조선운송/철강소재/에너지화학/정보통신/금융/필수소비재/자유소비재
            """
        h54 = self.com.GetHeaderValue(54)  # 54 short  액면가
        h55 = self.com.GetHeaderValue(55)  # 55 long  예상 체결가
        h56 = self.com.GetHeaderValue(56)  # 56 long  예상 체결가 전일 대비
        h57 = self.com.GetHeaderValue(57)  # 57 long  예상 체결 수량
        h58 = self.com.GetHeaderValue(58)  # 58 char  예상 체결가 구분 플래그
        """코드
             내용
            '0'
             동시호가와 장중이외의 시간
            '1'
             동시호가시간
            (예상체결가 들어오는 시간)
            '2'
             장중
            """
        h59 = self.com.GetHeaderValue(59)  # 59 char  장 구분 플래그
        """코드
             내용
            '1'
             장전예상체결
            '2'
             장중
            '3'
             장전시간외
            '4'
             장후 시간외
            '5'
             장후 예상체결
            """
        h60 = self.com.GetHeaderValue(60)  # 60 char  자사주 신청여부
        """코드
             내용
            '1'
             신청
            '0'
             미신청
            """
        h61 = self.com.GetHeaderValue(61)  # 61 long  자사주 신청 수량
        h62 = self.com.GetHeaderValue(62)  # 62 long  거래원 외국계매도총합
        h63 = self.com.GetHeaderValue(63)  # 63 long  거래원 외국계매수총합
        h64 = self.com.GetHeaderValue(64)  # 64 float  신용잔고비율
        h65 = self.com.GetHeaderValue(65)  # 65 char  CB여부
        """코드
             내용
            '0'
             초기
            '1'
             CB발동
            '2'
             CB해제
            """
        h66 = self.com.GetHeaderValue(66)  # 66 char  관리구분
        """코드
             내용
            'Y'
             관리종목
            'N'
             정상종목
            """
        h67 = self.com.GetHeaderValue(67)  # 67 char 투자경고구분
        """코드
             내용
            '1'
             정상
            '2'
             주의
            '3'
             경고
            '4'
             위험예고
            '5'
             위험
            """
        h68 = self.com.GetHeaderValue(68)  # 68 char 거래정지구분
        """코드
             내용
            'Y'
             거래정지종목
            'N'
             정상종목
            """
        h69 = self.com.GetHeaderValue(69)  # 69 char  불성실 공시구분
        """[거래소/코스닥]
            코드
             내용
            '0'
             정상
            '1'
             불성실 공시
            [프리보드]
            코드
             내용
            '0'
             정상
            '1'
             불성실공시1회
            '2'
             불성실공시2회
            """
        h70 = self.com.GetHeaderValue(70)  # 70 long  BPS
'''
