import random
import time
import shutil
import sys

GREEN = '\033[92m'
RESET = '\033[0m'

matrix_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&* "

print(GREEN)
print("Initializing Matrix connection... Press Ctrl+C in the terminal to exit.")
time.sleep(2)

try:
    while True:
        columns=shutil.get_terminal_size().columns

        line="".join(random.choice(matrix_chars)for _ in range(columns))

        sys.stdout.write(line+'\n')
        sys.stdout.flush()

        time.sleep(0.04)

except KeyboardInterrupt:
    print(RESET)
    print("\n[Connevtion Seveered]")