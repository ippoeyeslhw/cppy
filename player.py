# coding: utf-8
import sqlite3

'''
scraper.py 로 수집된 db를 기반으로 tk로 만든 호가창 플레이어
'''

class DbControl:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
    def select_list(self, cod=None):
        cursor = self.conn.cursor()
        if cod == None:
            cursor.execute('''SELECT * FROM codlist''')
        else:
            cursor.execute('''
            SELECT * FROM codlist WHERE cod = ?
            ''', (cod,))
        return cursor.fetchall()

    def select_cur(self, cod, tim):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT * FROM curtbl WHERE cod=? AND tim > ?
        LIMIT 1000
        ''', (cod, tim))
        return cursor.fetchall()

    def select_bid(self, cod, tim):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT * FROM bidtbl WHERE cod=? AND tim > ?
        LIMIT 1000
        ''', (cod, tim))
        return cursor.fetchall()

import threading
import time
import queue

class PlayBuffer(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path
        self.cur_q = queue.Queue()
        self.bid_q = queue.Queue()
        self.cod = None
        self.cur_tim = ''
        self.bid_tim = ''
        self.isstop = False

    def reset(self, cod, tim):
        # call by main thread
        self.cur_q = queue.Queue()
        self.bid_q = queue.Queue()
        self.cod = cod
        self.cur_tim = tim
        self.bid_tim = tim

    def stop(self):
        self.isstop = True

    def run(self):
        self.dbcont = DbControl(self.path)
        while True:
            if self.isstop:
                break
            if self.cod == None:
                pass
            else:
                # append cur
                curs = self.dbcont.select_cur(self.cod, self.cur_tim)
                if len(curs) > 0:
                    self.cur_tim = curs[-1][2] # lase element tim
                    for cur in curs:
                        self.cur_q.put(cur)
                    print ('[IO THREAD] cur append buffer', self.cur_tim)

                # append bid
                bids = self.dbcont.select_bid(self.cod, self.bid_tim)
                if len(bids) > 0:
                    self.bid_tim = bids[-1][2] # last element tim
                    for bid in bids:
                        self.bid_q.put(bid)
                    print ('[IO THREAD] bid append buffer', self.bid_tim)

            time.sleep(0.2)

from tkinter import *
import datetime

def make_timeset():
    dtim = datetime.datetime(2017,3,20,9,0,0)
    ddel = datetime.timedelta(minutes=1)
    ret = {}

    for i in range(390):
        mkey =  '%02d%02d'%(
            dtim.hour,
            dtim.minute
        )
        ret[mkey] = i
        ret[i] = mkey
        dtim = dtim + ddel

    #print sorted(ret.keys())
    return ret


class Application(Frame):
    def createWidgets(self):
        # 1. 코드 리스트 (0, 1 컬럼)
        self.cod_scroll = Scrollbar(self.master)
        self.cod_listbox = Listbox(self.master, width=35, yscrollcommand=self.cod_scroll.set)
        # position
        self.cod_listbox.grid(row=0, column=0, rowspan=12, sticky=W+E+N+S)
        self.cod_scroll.grid(row=0, column=1, rowspan=12, sticky=W+E+N+S)
        # action
        self.cod_scroll.config(command=self.cod_listbox.yview)
        # data load
        self.cod_list = self.dbcontrol.select_list()
        for cod in self.cod_list:
            self.cod_listbox.insert(END, '%s %s %s'%(cod[0],cod[2], cod[1]))
        # bind event
        self.cod_listbox.bind('<<ListboxSelect>>', self.cod_listbox_click)

        # 2. 호가창 (2,3,4 컬럼)
        pos = [
            (4,3),(5,3),(4,2),(5,4),
            (3,3),(6,3),(3,2),(6,4),
            (2,3),(7,3),(2,2),(7,4),
            (1,3),(8,3),(1,2),(8,4),
            (0,3),(9,3),(0,2),(9,4)
        ]
        self.lbls = []
        for i in range(20):
            self.lbls.append(Label(self.master, width=10, anchor="e"))
            self.lbls[i].config(text="0")
            self.lbls[i].grid(row=pos[i][0], column=pos[i][1])

        # 3. 체결내역 (5,6 컬럼)
        self.cur_scroll = Scrollbar(self.master)
        self.cur_listbox = Listbox(self.master, width=40, yscrollcommand=self.cur_scroll.set, font=(u'굴림체', 10))
        # position
        self.cur_listbox.grid(row=0, column=5, rowspan=10, sticky=W+E+N+S)
        self.cur_scroll.grid(row=0, column=6, rowspan=10, sticky=W+E+N+S)
        # action
        self.cur_scroll.config(command=self.cur_listbox.yview)

        # 4. play bar
        self.play_bar = Scale(self.master,  orient=HORIZONTAL, from_=0, to_=389,  showvalue=0)
        self.play_bar_lbl = Label(self.master, width=10, anchor="e", text='0900')
        self.play_tim_set = make_timeset()
        # position
        self.play_bar.grid(row=11, column=3, columnspan=3, sticky=W+E+N+S)
        self.play_bar_lbl.grid(row=11,column=2)
        # event
        self.play_bar.bind('<Button-1>', self.play_bar_press)
        self.play_bar.bind('<B1-Motion>', self.play_bar_move)
        self.play_bar.bind('<ButtonRelease-1>', self.play_bar_release)

        # 5. timer
        self.play_on = False


    # 이벤트
    def cod_listbox_click(self, evnt):
        print ('select cod')
        select_idx = self.cod_listbox.curselection()[0]
        itm = self.cod_list[int(select_idx)]
        cod = itm[0]
        tim = itm[2]
        print (cod,tim)
        self.play_set(cod, tim)
    def play_bar_press(self, evnt):
        print ('play-bar press')
        self.play_on = False
    def play_bar_move(self, evnt):
        idx = self.play_bar.get()
        show_val = self.play_tim_set[idx]
        self.play_bar_lbl.config(text=show_val)
    def play_bar_release(self, evnt):
        print ('play-bar release')
        select_idx = self.cod_listbox.curselection()[0]
        itm = self.cod_list[int(select_idx)]
        cod = itm[0]
        idx = self.play_bar.get()
        tim = '%s00000'%(self.play_tim_set[idx])
        print (cod,tim)
        self.play_set(cod, tim)

    def play_set(self, cod, tim):
        self.n_cur = None
        self.n_bid = None
        self.cur_listbox.delete(0,END)
        self.frm_tim = datetime.datetime(
            2017,3,21,
            int(tim[0:2]), #hour
            int(tim[2:4]), #minuate
            int(tim[4:6]), # sec
            int(tim[6:]) # millisec
        )
        # buffer reset
        self.play_buffer.reset(cod, tim)
        # play
        self.play_on = True
        self.tick()

    def tick(self):
        # 0.01sec 마다 한번씩
        play_tim = '%02d%02d%02d%03d'%(
            self.frm_tim.hour,
            self.frm_tim.minute,
            self.frm_tim.second,
            self.frm_tim.microsecond/1000
        )
        # cur
        try:
            while True:
                if self.n_cur == None:
                    self.n_cur = self.play_buffer.cur_q.get_nowait()
                if self.n_cur[2] <= play_tim:
                    # cur update
                    # set
                    sll_buy = u'매도'
                    sll_qty = '%9d'%self.n_cur[5]
                    buy_qty = '         '
                    # buy set
                    if self.n_cur[3] == '2':
                        sll_buy = u'매수'
                        sll_qty = '         '
                        buy_qty = '%9d'%self.n_cur[5]
                    self.cur_listbox.insert(0, '%s,%s,%s,%s,%s'%(
                        self.n_cur[2], #tim
                        sll_buy, # sll buy
                        self.n_cur[4],
                        sll_qty,
                        buy_qty)
                    )
                    self.n_cur = None
                else:
                    break
        except queue.Empty:
            pass

        # bid
        try:
            while True:
                if self.n_bid == None:
                    self.n_bid = self.play_buffer.bid_q.get_nowait()
                if self.n_bid[2] <= play_tim:
                    # bid update
                    for i in range(20):
                        self.lbls[i].config(text=self.n_bid[i+3])
                    self.n_bid = None
                else:
                    break
        except queue.Empty:
            pass

        # scale update
        play_bar_idx = self.play_tim_set[play_tim[0:4]]
        self.play_bar.set(play_bar_idx)
        self.play_bar_lbl.config(text=play_tim[0:4])

        # time update
        self.frm_tim = self.frm_tim + self.frm_tim_delta
        if self.play_on:
            self.root.after(10, self.tick)


    def __init__(self, master=None, path=None):
        Frame.__init__(self, master)
        self.root = master
        # db conn
        dt = datetime.datetime.now()
        dt_nm = 'test_%s%s%s.db'%(dt.year, dt.month, dt.day)
        if path == None:
            path = dt_nm
        self.dbcontrol = DbControl(path)
        # ui init
        self.grid()
        self.createWidgets()
        self.play_buffer = PlayBuffer(path)
        self.play_buffer.start() # load thread start
        # time def
        self.frm_tim = None # 프레임 시간
        self.frm_tim_delta = datetime.timedelta(milliseconds=10)
        #
        self.n_cur = None
        self.n_bid = None

        #self.root.protocol("WM_DELETE_WINDOW", self.destory_tk)

    def destroy(self):
        self.play_buffer.stop()





root = Tk()
path_ = None
#path_ = 'test_2017322.db'
app = Application(master=root, path=path_)
app.mainloop()
#root.destroy()