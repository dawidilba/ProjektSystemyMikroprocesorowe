import serial
import time
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

# Testowane pod arduino Uno, któro wysyłało losowe dane imitujące dane otrzymywane z akcelerometru

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
        try:
            x, y, z = tmp.split() #jesli nie uda sie podzielic tmp to wykonuje sie except czyli nic
            self._data.append(tmp)
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
            #print(self.x, self.y, self.z)
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


uart = UartCommunication()
uart.openPort("COM3", 9600) # nazwa portu, predkosc transmisji

plt.style.use('seaborn-bright')
fig = plt.figure()
ax = fig.add_subplot(211, projection = '3d') # 3d chart
ax2 = fig.add_subplot(212) # x, y, z depending on time
ax2.set_ylim(-1000, 1300)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Amplitudes x,y,z")


toc = 0
xValues, yValues, zValues, timeValues = [], [], [], []

while True:
    tic = time.time() # time axis tmp
    timeValues.append(toc)

    uart.readPort(1, 0)
    x = uart.getX()
    xValues.append(x)
    y = uart.getY()
    yValues.append(y)
    z = uart.getZ()
    zValues.append(z)

    # x, y, z 3d chart
    ax.set_title("Real-Time data from accelerometer") #te parametry musza byc ustawiane w petli poniewaz cla() je kasuje
    ax.set_xlim(-1000, 1000)  # granice osi x
    ax.set_xlabel('X axis')  # nazwa osi x
    ax.set_ylim(-1000, 1000)
    ax.set_ylabel('Y axis')
    ax.set_zlim(-1000, 1000)
    ax.set_zlabel('Z axis')
    ax.scatter3D(x, y, z, c = 'r', marker = '^')

    ## x, y z depending on time chart
    ax2.set_xlim(left = max(0, toc-5), right = toc)
    ax2.plot(timeValues, xValues, 'b-',
             timeValues, yValues, 'g-',
             timeValues, zValues, 'r-',)
    plt.show(block=False) # block na false zeby dane byly wciaz wyswietlane na wykresie
    plt.pause(0.01) #czas odswiezania wykresu
    ax.cla()    # clear axes
    toc += time.time()-tic







