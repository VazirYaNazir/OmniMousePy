import serial
import pyautogui

BAUD_RATE = 9600
SERIAL_PORT = '8C-55-4A-45-DF-57'


def bridge():
    with serial.Serial(SERIAL_PORT, BAUD_RATE) as ser:
        print("Connected to Android, controlling mouse...")
        while True:
            data = ser.readline().decode("utf-8").strip()
            if data.startswith("MOVE:"):
                dx, dy = map(float, data[5:].split(","))
                pyautogui.moveRel(dx, dy)
            elif data.startswith("CLICK:"):
                if data[6:] == "LEFT":
                    pyautogui.click()
                elif data[6:] == "RIGHT":
                    pyautogui.rightClick()


bridge()