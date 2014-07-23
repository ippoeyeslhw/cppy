cppy
====

cybosplus + python 을 이용하여 투자분석 및 시스템트레이딩을
편리하게 사용하기 위한 미니프로젝트 입니다.


###필요한것들

 * 윈도우 운영체제
 * python2.7
 * cybosplus
 * pywin32 라이브러리

###개념

cppy 패키지에는 adaptor모듈과 processor모듈이 있습니다. 
adaptor의 의미는 실시간으로 전달받는 각종 데이터를 변환하는 것이고
이를 processor에 있는 event처리기가 처리하게됩니다.
이러한 개념은 CEP를 본따 구성하였습니다([그림참조](http://www.idevnews.com/views/images/uploads/general/apama.gif)).

cppy 는 최소한의 요소만 사용하는 Micro Framework입니다.

