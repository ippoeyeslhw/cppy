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



## processor
-----

adaptor 들에서 입력/출력 데이터들을 받고/내보내어 처리하는 부분입니다.
실시간으로 생성되는 데이터를 처리하기 위해 이벤트처리기를 지원합니다.
이는 Key/Value 스타일과 키의 패턴매칭을 지원하여 등록한 작은 프로그램들을 
자동으로 수행하게 해줍니다.

#### EventProcessor

간단한 이벤트처리기를 제공합니다. 
key와 함께 data를 전달을 하면 처리기는 순차적으로 처리합니다.
가장 마지막에 받은(최신) 데이터가 가장 앞에 있도록 
data를 받을때마다 key에 시계열로 저장합니다. 
이때 미리 등록한 패턴과 매칭시켜 일치하면 등록한 옵저버를 실행합니다.
옵저버는 실행가능한 함수 혹은 객체(__call__구현)이면 됩니다.
그리고 옵저버에서는 시계열을 인자로 받아 사용할수 있습니다.

간단한 사용례는 다음과 같습니다.

```python

    def echo(serieses, key, dat):
        print 'key:%s, dat:%s'%(key,dat)

    if __name__ == "__main__":
    
        evntproc = EventProcessor()
        evntproc.add_observer(['A003540*'], echo)
        evntproc.start()

```

add_observer 메서드에 패턴리스트와 옵저버(콜백)를 등록하였습니다. 
옵저버의 인자는 serieses, key, dat 으로서 시계열들의 집합에 접근할수 있고 
어떤 key와 dat 때문에 호출되었는지 알 수 있도록 합니다.
위에서는 A003540으로 시작하는 키를 받았을때 echo 를 수행하도록 지정하였습니다.
패턴은 Unix-shell 스타일의 패턴을 사용합니다.

그렇다면 adaptor 를 통해 이벤트처리기에 data를 전달해보겠습니다.

```python

    from cppy.adaptor import CpRqRpClass
    
    @CpRqRpClass('CpSysDib.StockChart')
    class StkChart(object):
        def request(self, com_obj):
            com_obj.SetInputValue(0, 'A003540')
            com_obj.SetInputValue(1, ord('2'))
            com_obj.SetInputValue(4, 100)
            com_obj.SetInputValue(5, [5])
            com_obj.SetInputValue(6, ord('D'))    
            com_obj.Request()
    
        def response(self, com_obj):
            cnt = com_obj.GetHeaderValue(3) #  수신개수
            for i in xrange(cnt):    
                # 키와 값을 인자로 하여 이벤트처리기에 전달
                evntproc.push('A003540_clpr', com_obj.GetDataValue(0,i))

```

push 메소드를 사용하여 데이터를 전달합니다. 인자는 key, data 순으로 넣습니다.


