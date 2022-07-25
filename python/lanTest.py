import socket
from tkinter import *
from matplotlib import pyplot
import datetime

main = Tk()

host = StringVar()
host.set('10.0.0.97')
port = StringVar()
port.set('45454')
lbl = StringVar()
lastCmd = None
values = []
times = []

def query(cmd, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host.get(), int(port.get())))
    sock.sendall(cmd)
    data = sock.recv(1024)
    print("Received: ", repr(data))
    sock.close()
    return data

def getID():
    lbl.set(query(b'*idn?\r\n', host, port).strip())
    global lastCmd
    lastCmd = getID

def voltdc():
    resp = query(b'meas:volt:dc?\r\n', host, port)
    lbl.set(resp.strip())
    values.append(float(resp.decode()))
    times.append(datetime.datetime.now())
    global lastCmd
    lastCmd = voltdc

def lCmd():
    print(lastCmd)
    lastCmd()

def plot():
    pyplot.xkcd()
    pyplot.plot(times, values)
    pyplot.gcf().autofmt_xdate()
    pyplot.show()


Label(main, text="IP Addr").grid(row=2,column=1, sticky='e')
Entry(main, width=15, textvariable=host).grid(row=2,column=2, sticky='w')
Label(main, text="Port").grid(row=3,column=1, sticky='e')
Entry(main, width=6, textvariable=port).grid(row=3,column=2, sticky='w')
Label(main, textvariable=lbl, width=40, background='black', foreground='white', font=("courier bold", 20)).grid(row=1, column=1, columnspan=3)
Button(main, text="get ID", command=getID, width = 12).grid(row=4,column=1)
Button(main, text="volt dc", command=voltdc, width = 12).grid(row=4,column=2)
Button(main, text="run last", command=lCmd, width = 12).grid(row=5,column=1)
Button(main, text="plot", command=plot, width=12).grid(row=5,column=2)


main.mainloop()

