# encoding=utf-8
import pandas
import threading
import time
import re
import tkinter
from tkinter import *
#from pandas.core.frame import DataFrame
from pandastable import Table, TableModel
from ping3 import ping, send_one_ping

pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')


class TestApp(Frame):
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('600x400+200+100')
        self.main.title('Ping Table')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        df = pandas.read_csv("default.csv")
        self.model = TableModel(dataframe=df)
        self.table = Table(f, model=self.model, showtoolbar=True, showstatusbar=True)
        self.table.show()
        self.running = True
        return

    def run(self):
        while self.running:
            print("running")
            col_red = []
            row_red = []
            for y in range(self.model.getColumnCount()):
                for x in range(self.model.getRowCount()):
                    text = self.model.getValueAt(x,y)
                    result = pattern.search(text)
                    if (result):
                        ret = ping(text)
                        if ret:
                            color = '#00FF00'
                        else:
                            color = '#FF0000'
                        self.table.setRowColors(cols=[y], rows=[x], clr=color)
                    else:
                        self.table.setRowColors(cols=[y], rows=[x], clr='#FFFFFF')   
                #time.sleep(3)

root = tkinter.Tk()
app = TestApp(root)
thread_ping = threading.Thread(target=app.run, daemon=True)
thread_ping.start()
#root.protocol('WM_DELETE_WINDOW', app.stop)

#launch the app
root.mainloop()
