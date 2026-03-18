import customtkinter as ctk

# --- 1. SETUP THE WINDOW ---
# Make it look sleek and modern!
ctk.set_appearance_mode("dark")  # "light", "dark", or "system"
ctk.set_default_color_theme("blue") # "blue", "green", or "dark-blue"

# Create the main window object (Think of this as your Pygame 'screen')
app = ctk.CTk()
app.geometry("400x420")
app.title("Focus Timer")

# --- 2. APP VARIABLES ---
WORK_TIME = 25 * 60  # 25 minutes in seconds
time_left = WORK_TIME
timer_running = False

# --- 3. THE LOGIC (Functions) ---
def start_timer():
    global timer_running
    if not timer_running:
        timer_running = True
        countdown()

def stop_timer():
    global timer_running
    timer_running = False

def reset_timer():
    global timer_running, time_left
    timer_running = False
    time_left = WORK_TIME
    update_timer_text()

def countdown():
    global time_left, timer_running
    if timer_running and time_left > 0:
        time_left -= 1
        update_timer_text()
        # .after() is the GUI magic trick! It tells the app to run this function again in 1000 milliseconds (1 second)
        app.after(1000, countdown) 
    elif time_left == 0:
        timer_running = False
        time_label.configure(text="Time's Up!", text_color="green")

def update_timer_text():
    # Convert total seconds into minutes and seconds
    minutes = time_left // 60
    seconds = time_left % 60
    # Format the text so it always shows two digits (e.g., 09:05)
    time_label.configure(text=f"{minutes:02d}:{seconds:02d}", text_color="white")

def set_custom_time():
    global WORK_TIME,time_left,timer_running
    try:
        user_minutes=int(time_entry.get())

        if user_minutes>0:
            timer_running=False
            WORK_TIME=user_minutes*60
            time_left=WORK_TIME
            update_timer_text()
            time_entry.delete(0,'end')
    except ValueError:
        print("Please enter A valid number.")

# --- 4. THE UI WIDGETS (Buttons and Text) ---
# Title
title_label = ctk.CTkLabel(app, text="Pomodoro Timer", font=("Arial", 24, "bold"))
title_label.pack(pady=20) # .pack() literally "packs" it onto the screen, leaving 20 pixels of padding above/below

# The Giant Clock Text
time_label = ctk.CTkLabel(app, text="25:00", font=("Arial", 80, "bold"))
time_label.pack(pady=20)

input_frame=ctk.CTkFrame(app,fg_color="transparent")
input_frame.pack(pady=10)

time_entry=ctk.CTkEntry(input_frame,placeholder_text="Minutes",width=80)
time_entry.grid(row=0,column=0,padx=5)

set_buttom=ctk.CTkButton(input_frame,text="Set Time",command=set_custom_time,width=80)
set_buttom.grid(row=0,column=1,padx=5)

# A frame to hold our buttons side-by-side
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=20)

# The Buttons
start_button = ctk.CTkButton(button_frame, text="Start", command=start_timer, width=100)
start_button.grid(row=0, column=0, padx=10) # .grid() lets us place things next to each other!

stop_button = ctk.CTkButton(button_frame, text="Stop", command=stop_timer, width=100, fg_color="gray", hover_color="darkgray")
stop_button.grid(row=0, column=1, padx=10)

reset_button = ctk.CTkButton(app, text="Reset", command=reset_timer, width=150, fg_color="#C0392B", hover_color="#922B21")
reset_button.pack(pady=10)

# --- 5. START THE APP LOOP ---
# This is the GUI version of "while running:"
app.mainloop()