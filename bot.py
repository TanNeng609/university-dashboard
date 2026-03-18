import pyautogui
import keyboard
import time

print("🤖 Auto Bot is online")
print("HOLD the 's' key to spam click")
print("PRESS the 'q' key to quit the program")

while True:
    if keyboard.is_pressed('q'):
        print("Bot shutting down....")
        break

    if keyboard.is_pressed('s'):
        pyautogui.click()

        time.sleep(0.001)