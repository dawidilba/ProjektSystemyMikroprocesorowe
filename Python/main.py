import serial
import time


class UartCommunication:
    def __init__(self):
        self.uartPort = serial.Serial()
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
                print("Nie udało się otworzyć portu")

    def closePort(self):
        if self.uartPort.is_open == True:
            try:
                self.uartPort.close()
            except:
                print("Nie udało się zamknąć portu")

    def readPort(self):
        while 1:
            try:    # bez sprawdzania portu i w taki sposob zeby nie bylo bledow z danymi
                line = self.uartPort.readline() # unicode znaki np b'1'
                tmp = str(line, 'utf-8') # conversion from byte to string
                x, y, z = tmp.split()
                self.x = float(x)
                self.y = float(y)
                self.z = float(z)
                print(self.x, self.y, self.z)
                time.sleep(0.5) # czas odswiezania
            except:
                continue


uart = UartCommunication()
uart.openPort("COM3", 9600) # nazwa portu, predkosc transmisji, timeout
uart.readPort()




