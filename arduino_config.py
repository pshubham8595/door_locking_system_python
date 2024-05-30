import time
import serial

SERIAL_PORT = 'COM8'  # Change this to the appropriate port
BAUD_RATE = 9600


# Initialize serial communication
def openLock(sleepingSeconds):
    print("Opening lock")
    serialPort = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    try:
        keepItOn = True
        while keepItOn:
            # Send '1' to turn on the LED
            time.sleep(2)
            serialPort.write(b'1')
            time.sleep(sleepingSeconds)
            serialPort.write(b'0')
            # Wait for 1 second
            serialPort.close()
            keepItOn = False
        return
    except KeyboardInterrupt:
        # Close the serial connection when the program is terminated
        serialPort.close()


# openLock(10)