import serial
import time
from tkinter import *
import struct
import functools
import operator
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import matplotlib.pyplot as plt


class UartCommunication:
    def __init__(self):
        self.uartPort = serial.Serial()
        self._data = list()
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def openPort(self, portName, baudRate):
        if self.uartPort.is_open == False:
            self.uartPort.port = portName
            self.uartPort.baudrate = baudRate
            try:
                self.uartPort.open()
            except:
                print("Failed to open port")

    def isPortOpen(self):
        if self.uartPort.is_open == False:
            return False
        else:
            return True

    def closePort(self):
        if self.uartPort.is_open == True:
            try:
                self.uartPort.close()
            except:
                print("Failed to close port")

    def openLogFile(self):
        with open("logs/data.log", 'r') as file:
            try:
                self._data = file.read()
            except:
                print("Failed to open log file")

    def saveLogFile(self):
        with open("logs/data.log", 'w') as file:
            file = file.write(''.join(self._data)) #join, zeby polaczyc liste

    def appendToLogFile(self, txt):
        with open("logs/data.log", 'a') as file:
            file = file.write(''.join(txt))

    def readPort(self, doLogFile, saveOrAppend ): #doLogFile=1->zrob log, saveOrAppend : 0 - zapisz na nowo, 1 - dopisz
        line = self.uartPort.readline() # unicode znaki np b'1'
        tmp = str(line, 'utf-8') # conversion from byte to string
        #KL46
        #tmpX = self.uartPort.read(4)
        #tmpY = self.uartPort.read(4)
        #tmpZ = self.uartPort.read(4)
        #tmpX = struct.unpack('f', tmpX) #byte to tuple
        #tmpY = struct.unpack('f', tmpY)
        #tmpZ = struct.unpack('f', tmpZ)
        #self.x = functools.reduce(operator.add, tmpX) #tuple to float
        #self.y = functools.reduce(operator.add, tmpY)
        #self.z = functools.reduce(operator.add, tmpZ)
        try:
            x, y, z = tmp.split() #jesli nie uda sie podzielic tmp to wykonuje sie except czyli nic
            self._data.append(tmp)
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
            if doLogFile == 1:
                if saveOrAppend == 0:
                    self.saveLogFile()
                else:
                    self.appendToLogFile(tmp)
        except:
            pass

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getZ(self):
        return self.z



# obj UartCommunication
uart = UartCommunication()

def dtw_dist(x, y):
    distance, path = fastdtw(x, y, dist = euclidean)
    return distance

def liveData():
    button1.configure(text="Zamknij wykres", command=closeAll)
    uart.openPort("COM3", 9600)  # nazwa portu, predkosc transmisji
    plt.style.use('seaborn-bright')
    fig = plt.figure()
    ax = fig.add_subplot(211, projection='3d')  # 3d chart
    ax2 = fig.add_subplot(212)  # x, y, z depending on time
    ax2.set_ylim(-2, 2)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Amplitudes x,y,z")

    xValues, yValues, zValues, timeValues = [], [], [], []
    toc = 0
    while uart.isPortOpen() == True:
        tic = time.time() # time axis tmp
        timeValues.append(toc)

        uart.readPort(0, 0)
        x = uart.getX()
        xValues.append(x)
        y = uart.getY()
        yValues.append(y)
        z = uart.getZ()
        zValues.append(z)

    # x, y, z 3d chart
        ax.set_title("Real-Time data from accelerometer") #te parametry musza byc ustawiane w petli poniewaz cla() je kasuje
        ax.set_xlim(-2, 2)  # granice osi x
        ax.set_xlabel('X axis')  # nazwa osi x
        ax.set_ylim(-2, 2)
        ax.set_ylabel('Y axis')
        ax.set_zlim(-2, 2)
        ax.set_zlabel('Z axis')
        ax.scatter3D(x, y, z, c = 'r', marker = '^')

    ## x, y z depending on time chart
        ax2.set_xlim(left = max(0.01, toc-5), right = toc)
        ax2.plot(timeValues, xValues, 'b-',
                timeValues, yValues, 'g-',
                timeValues, zValues, 'r-',)
        plt.show(block=False) # block na false zeby dane byly wciaz wyswietlane na wykresie
        plt.pause(0.01) #czas odswiezania wykresu
        ax.cla()    # clear axes
        toc += time.time()-tic

def saveGesture():
    from matplotlib.widgets import Button
    button2.configure(text="Zamknij wykres", command=closeAll)
    uart.openPort("COM3", 9600)  # nazwa portu, predkosc transmisji
    plt.style.use('seaborn-bright')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(-2, 2)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitudes x,y,z")
    def Start(event):
        xValues, yValues, zValues, timeValues = [], [], [], []
        toc = 0
        while toc < 3:
            tic = time.time()  # time axis tmp
            timeValues.append(toc)
            uart.readPort(1, 0)
            x = uart.getX()
            xValues.append(x)
            y = uart.getY()
            yValues.append(y)
            z = uart.getZ()
            zValues.append(z)
            ## x, y z depending on time chart
            ax.set_xlim(left=max(0.01, toc - 5), right=toc)
            ax.plot(timeValues, xValues, 'b-',
                    timeValues, yValues, 'g-',
                    timeValues, zValues, 'r-', )
            plt.show(block = False)
            plt.pause(0.01)  # czas odswiezania wykresu
            toc += time.time() - tic
        uart.closePort()

    axButtonStart = plt. axes([0.2, 0.90, 0.6, 0.05])
    buttonStart = Button(axButtonStart, "START")
    buttonStart.on_clicked(Start)
    plt.show()

def recognizeGesture():
    pass

def closeAll():
    plt.close("all")
    uart.closePort()
    button1.configure(text="Wyswietlaj dane z akcelerometru", command = liveData)
    button2.configure(text="Zapisz gest", command = saveGesture)

def exitButton():
    plt.close("all")
    uart.closePort()
    window.quit()


# Main menu
window = Tk()
window.title("KL46 Project")
window.geometry("370x220")
window.resizable(0,0)
window.configure(background = "white")
button1 = Button(window, text = "Wyswietlaj dane z akcelerometru", width = 30, height = 2, font = 'Verdana 13 bold italic', background = "white", command = liveData)
button1.grid(row = 3, column = 1, sticky = W)
button2 = Button(window, text = "Zapisz gest", width = 30, height = 2, font = 'Verdana 13 bold italic', background = "white", command = saveGesture)
button2.grid(row = 4, column = 1, sticky = W)
Button(window, text = "Rozpoznaj gest", width = 30, height = 2, font = 'Verdana 13 bold italic', background = "white", command = recognizeGesture).grid(row = 5, column = 1, sticky = W)
Button(window, text = "Wyjdz", width = 30,height = 2, font = 'Verdana 13 bold italic', background = "white", command = exitButton).grid(row = 6, column = 1, sticky = W)
window.mainloop()











