# coding: utf-8

from cppy.util import getDictPriceKey
from cppy.CpSysDib import StockChart

import matplotlib.pyplot as plt

class SampleStockChart(object):
    def __init__(self):
        self.com = StockChart(self.response)  # event handler
        self.cod = 'A003540'
        self.dt = 20170308
        self.dic = {}
        self.dic_keys_sort = []

    def request(self):
        self.com.SetInputValue(0, self.cod)  # 0 string : 주식(A003540), 업종(U001), ELW(J517016)의 종목코드
        self.com.SetInputValue(1, ord('1'))  # 1 char :
        self.com.SetInputValue(2, self.dt )  # 2 ulong : YYYYMMDD형식으로 데이터의 마지막(가장 최근) 날짜 Default(0) - 최근 거래날짜
        self.com.SetInputValue(3, self.dt )  # 3 ulong : YYYYMMDD형식으로 데이터의 시작(가장 오래된) 날짜
        self.com.SetInputValue(5, [1,2,3,4,5,8])  # 5 long or long array : 필드 또는 필드 배열
        self.com.SetInputValue(6, ord('m'))  # 6 char
        self.com.SetInputValue(10, ord('3'))  # 10 char

    def response(self):
        h3 = self.com.GetHeaderValue(3)  # 3 long
        h14 = self.com.GetHeaderValue(14) # high
        h15 = self.com.GetHeaderValue(15) # low

        self.dic_keys_sort = [x for x in self.dic_keys_sort if x >= h15 and x <= h14]

        for i in range(h3):
            tim = self.com.GetDataValue(0, h3-1-i)
            opn = self.com.GetDataValue(1, h3-1-i)
            hig = self.com.GetDataValue(2, h3-1-i)
            low = self.com.GetDataValue(3, h3-1-i)
            clr = self.com.GetDataValue(4, h3-1-i)
            vol = self.com.GetDataValue(5, h3-1-i)
            prs = [ x for x in self.dic_keys_sort if x >= low and x <= hig]

            avg = int(vol / len(prs))

            for j in prs:
                self.dic[j] += avg

            if i % 5 == 0:
                val_lists_by_sorted_key = [self.dic[x] for x in self.dic_keys_sort]
                plt.plot(val_lists_by_sorted_key, self.dic_keys_sort)
                plt.title(self.cod)
                plt.savefig('./pngs/%s%03d.png'%(self.cod, i))
                plt.close()




cod = 'A154040'
dt = 20170314

dicprs = getDictPriceKey(cod)
stkchart = SampleStockChart()

# init data
stkchart.cod = cod
stkchart.dt = dt
stkchart.dic = dicprs
stkchart.dic_keys_sort = sorted(dicprs.keys())

stkchart.request()
stkchart.com.BlockRequest()


print('done')


