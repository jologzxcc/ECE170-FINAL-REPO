# Importing Libraries
import serial
import time


def send_to_arduino(data): 
    arduino = serial.Serial(port='COM3', baudrate=9600)
    arduino.timeout = 1

    while True:
        arduino.write(data.encode())
