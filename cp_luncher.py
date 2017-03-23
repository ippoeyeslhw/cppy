# coding: utf-8

import pywinauto
import pyautogui
import time

print(pywinauto.__version__)

# 비번
pw = '1234'
cert = '1234'

# 파일에서 비번들 로드할경우
with open('./ignores/pw.txt') as f:
    itms = list(f.readlines())
    pw = itms[0].strip()
    cert = itms[1].strip()


# 어플리케이션 실행
app = pywinauto.Application()
app.start(r'C:\DAISHIN\STARTER\ncStarter.exe /prj:cp')
print('cp load done')

# wait
time.sleep(1)

# 엔터
pyautogui.typewrite('\n', interval=0.1)
print('enter done')

# 다이얼로그
def ret_wind():
    return app.window(title='CYBOS Starter')
dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, ret_wind)
print('done dlg')

# pass edit
pass_edit = dlg.Edit2
pass_edit.SetFocus()
pass_edit.TypeKeys(pw)
print('done pw')

# cert edit
cert_edit = dlg.Edit3
cert_edit.SetFocus()
cert_edit.TypeKeys(cert)
print('done cert')

# login
btn = dlg.Button
btn.Click()
print('done login click')
