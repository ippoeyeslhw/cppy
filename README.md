cppy
====

cybosplus + python 을 이용하여 투자분석 및 시스템트레이딩을
편리하게 사용하기 위한 미니프로젝트 입니다.


### 필요한것들

 * 윈도우 운영체제
 * cybosplus
 * pywin32 라이브러리

### Modules
사이보스 플러스 Type Library에 정의된 coclass 모음
 * cppy/CpDib.py:
 * cppy/CpSysDib.py:
 * cppy/CpTrade.py:
 * cppy/CpUtil.py:
 * cppy/util.py : 위 라이브러리를 활용한 간단한 함수 모음



### Example
 * cp_luncher.py : 자동로그인 스크립트, pywinauto, pyautogui 필요
 * sample.py : cppy.util.generateClass 메서드를 이용하여 도움말을 이용하여
 샘플클래스를 생성하는 템플릿 (코드생성용)
 * scraper.py : 5~10% 상승한 종목을 0.25초 간격으로
 감시하다가 종목이 검출되면 바로 실시간 체결과 호가정보를
 구독하여 Sqlite DB에 데이터를 저장하는 스크립트
 * player.py : 위 scraper.py로 저장된 DB를 사용하여 호가창을
 리플레이 해볼수 있는 플레이어 (TK-GUI)