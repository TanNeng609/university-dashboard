import tkinter as tk

def start_app():
    window = tk.Tk()
    window.title("The first GUI")
    window.geometry("350x250")


    def on_button_click():
        user_name = name_input.get()

        if user_name.strip()== "":
            message_label.config(text="Hello There, stranger!")
        else:
            message_label.config(text=f"Hello, {user_name} !")

        name_input.delete(0,tk.END)

    instruction_label= tk.Label(window,text="Please enter your name: ",font=("Arial",12))
    instruction_label.pack(pady=(20,5))

    name_input=tk.Entry(window,font=("Arial",14),width=15)
    name_input.pack(pady=5)

    message_label=tk.Label(window,text="", font=("Arial", 16,"bold"),fg="darkgreen")
    message_label.pack(pady=10)

    click_button=tk.Button(window, text="Greet Me!",font=("Arial",14),bg="lightblue",command=on_button_click)
    click_button.pack(pady=30)


    window.mainloop()

start_app()
