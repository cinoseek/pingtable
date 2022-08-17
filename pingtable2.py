from tkinter import *
import csv
import re
import time
import threading
from ping3 import ping, send_one_ping
"""
row0: [BTN        ]
row1: IP      PING
row2: [    ] [    ]
"""

file = "ip_list.csv"
ip_list = []
ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

window = Tk()
entry_ip = []
entry_ping = []
startline = 2

running = True

def load_file():
    ip_list.clear()
    f = open(file, 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        ip_list.append(line)
    f.close()

def make_entry():
    for i,p in zip(entry_ip, entry_ping):
        i.destroy()
        p.destroy()
    for i in range(startline, len(ip_list)):
        e1 = Entry(window)
        e2 = Entry(window)
        e1.grid(row=i, column=0)
        e2.grid(row=i, column=1)
        e1.insert(0,ip_list[i-startline])
        e2.insert(0,"")
        entry_ip.append(e1)
        entry_ping.append(e2)



def draw_default():
    Label(window, text='IP').grid(row=1, column=0)
    Label(window, text='PING').grid(row=1, column=1)
    #Button(window, text='reload', command=reload).grid(row=0, column=0, sticky= W, pady=4)

def update():
    global running
    while running:
        for i, p in zip(entry_ip, entry_ping):
            iptext = i.get()
            result = ip_pattern.search(iptext)
            if (result):
                ret = ping(iptext, timeout=1)
                # return NoneType or float
                if type(float(0.0)) == type(ret):
                    i['fg'] = 'black'
                    p['fg'] = 'green'
                    p.delete(0,10)
                    p.insert(0,int(ret*1000))
                else:
                    i['fg'] = 'red'
                    p['fg'] = 'red'
                    p.delete(0,10)
                    p.insert(0,"999")
            else:
                p.delete(0,10)
        time.sleep(1)

def start_update():
    running = True
    thread_ping = threading.Thread(target=update, daemon=True)
    thread_ping.start()

def load():
    load_file()
    make_entry()

def main():
    draw_default()
    load()
    start_update()
    window.mainloop()

if __name__ == "__main__":
    main()