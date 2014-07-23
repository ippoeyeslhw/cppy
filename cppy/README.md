## adaptor
-----

cybosplus 및 각종 통신을 담당하는 부분입니다.
cybosplus의 Win32Com 객체와 연결하도록 하는 두가지의 클래스 데코레이터를 지원합니다.
이들은 Request/Response 통신, Subscribe/Publish 통신을 하기위해 작업해주어야 하는
번거로운 작업을 처리해줍니다.

#### CpRqRpClass

클래스 데코레이터입니다. Request/Response 통신방식을 
클래스로 구조화하여 사용합니다. 사용례는 다음과 같습니다.

```python

    from cppy.adaptor import CpRqRpClass

    @CpRqRpClass('dscbo1.StockMst')
    class StkMst(object):
        def request(self, com_obj):
            com_obj.SetInputValue(0, 'A122630')
            com_obj.Request()

        def response(self, com_obj):
            print com_obj.GetHeaderValue(1)
    
    if __name__ == '__main__':
    
        stkmst = StkMst()
        stkmst.request()
    
        import pythoncom, time
        while True:
            pythoncom.PumpWaitingMessages()
            time.sleep(0.01)
```
        
실행결과

    C:\Python27\python.exe C:/Users/lhw/Documents/GitHub/cppy/test/adaptor_test.py
    KODEX 레버리지
    

사용자 클래스는 request 메서드와 response 메서드를 반드시 구현하여야 하며 com_obj를 인자로
넣어주어야 제대로 동작합니다. 그리고 object를 반드시 상속하여야 합니다. 
com_obj는 내부적으로 Binding 된 Cybosplus의 COM객체를 의미합니다. 
cybosplus의 도움말을 이용하여 SetInputValue 메서드의 인자값과 GetHeaderValue, GetDataValue 의 인자값을 넣어
사용하면 됩니다.

response 는 request 메서드 내부에서 com_obj.Request로 비동기방식으로 요청했을시 서버로부터 응답을 받은 후 수행하는 부분입니다.
com_obj.BlockRequest로 동기방식으로 요청을 수행하면 직관적이고 이해하기 쉬우나 성능상 매우 비효율적으로 동작하므로 
가능한 Request를 사용하고 response에서 응답처리를 하는 방식을 권장합니다.


#### CpSubPubClass

클래스 데코레이터입니다. Subscribe/Publish 통신방식을 
클래스로 구조화하여 사용합니다. 사용례는 다음과 같습니다.


```python

    from cppy.adaptor import CpSubPubClass
    
    @CpSubPubClass('dscbo1.StockCur')
    class StkCur(object):
        def subscribe(self, com_obj):
            com_obj.SetInputValue(0, 'A122630')
            com_obj.Subscribe()

        def publish(self, com_obj):
            print 'nowpr: %s'%(com_obj.GetHeaderValue(13))   
                  
```

사용자 클래스는 subscribe 메서드와 publish 메서드를 반드시 구현하여야 하며 com_obj를 인자로
넣어주어야 제대로 동작합니다. 그리고 object를 반드시 상속하여야 합니다. 