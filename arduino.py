# Importing Libraries
import serial
import time

arduino = serial.Serial(port='COM3', baudrate=9600)
arduino.timeout = 1

while True:
    num = input("input(1 or 0): ")
    arduino.write(num.encode())