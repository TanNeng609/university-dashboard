import os

print("Installing PyInstaller to the correct location...")
# This forces the installation into the exact Python you are currently using
os.system("python -m pip install pyinstaller")

print("Building your app... Please wait a few moments.")
# This imports the PyInstaller tool directly and runs it inside Python
import PyInstaller.__main__

PyInstaller.__main__.run([
    'todolist.py', # Make sure this matches your actual To-Do list file name!
    '--onefile',
    '--windowed'
])

print("DONE! Check the 'dist' folder.")