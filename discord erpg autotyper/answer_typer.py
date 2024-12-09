from pynput.keyboard import Controller, Key
import os
import time
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Path to the text file
TEXT_FILE = r"discord erpg autotyper\storage.txt"

typing_delay = 0.05

keyboard = Controller()

def read_and_clear_text_file(file_path):
    """Reads content from the file and clears it."""
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            text = file.read()
            file.seek(0)
            file.truncate()  
            return text.strip()  
    except FileNotFoundError:
        return ""

def type_and_send_text(text):
    """Types the given text using the keyboard controller and presses Enter to send it."""
    print("Typing detected text. Please switch to Discord's typing space.")
    time.sleep(3)  

    for char in text:
        keyboard.type(char)
        time.sleep(typing_delay)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

if __name__ == "__main__":
    print(f"Monitoring {TEXT_FILE} for new text...")
    while True:
        text_to_type = read_and_clear_text_file(TEXT_FILE)

        if text_to_type:  
            print(f"New text detected: {text_to_type}")
            type_and_send_text(text_to_type)  
            print("Finished typing and sending.")
        else:
            time.sleep(2)  
