cppy
====

cybosplus + python 을 이용하여 투자분석 및 시스템트레이딩을
하는 목적의 프로젝트 입니다.

### adaptor
-----
cybosplus 및 각종 통신을 담당하는 부분입니다.
cybosplus의 경우 Win32Com 객체와 연결 두가지의 클래스 데코레이터를 지원합니다.
Request/Response 통신, Subscribe/Publish 통신을 하기위해 작업해주어야 하는
번거로운 작업을 처리해줍니다.

#### CpRqRpClass

클래스 데코레이터입니다. 사용례는 다음과 같습니다.

    from cppy.adaptor import CpRqRpClass

    @CpRqRpClass('dscbo1.StockMst')
    class StkMst(object):
        def request(self, com_obj):
            com_obj.SetInputValue(0, 'A122630')
            com_obj.Request()

        def response(self, com_obj):
            print com_obj.GetHeaderValue(1)
