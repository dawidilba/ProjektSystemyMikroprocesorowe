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
            print(self.x, self.y, self.z)
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
fig = plt.figure()
ax = plt.axes(projection='3d')

while True:
    uart.readPort(1, 0)
    x = uart.getX()
    y = uart.getY()
    z = uart.getZ()
    plt.title("Real-Time data from accelerometer") #musi byc ustawiany w petli poniewaz cla() go kasuje
    ax.scatter3D(x,y,z, c = 'r', marker = 'o')
    plt.show(block=False) # block zeby dane byly wciaz pobierane
    plt.pause(1) #czas odswiezania wykresu
    plt.cla() # clear axes





