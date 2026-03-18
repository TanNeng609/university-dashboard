import tkinter as tk
import json

def start_todo_app():
    window = tk.Tk()
    window.title("Visual To-Do List")
    window.geometry("350x500")
    window.config(bg="#f0f0f0")

    def save_tasks():
        all_tasks=task_listbox.get(0,tk.END)
        with open("my_tasks.json","w") as file:
            json.dump(all_tasks,file)

    def load_tasks():
        try:
            with open("my_tasks.json","r")as file:
                saved_tasks= json.load(file)
                for task in saved_tasks:
                    task_listbox.insert(tk.END,task)
        except FileNotFoundError:
            pass

    def add_task():
        task=task_input.get()
        if task.strip() != "":
            task_listbox.insert(tk.END,task)
            task_input.delete(0,tk.END)
            save_tasks()

    def delete_task():
        task_listbox.delete(tk.ANCHOR)
        save_tasks()

    def mark_done():
        try:
            selected_index=task_listbox.curselection()[0]
            task=task_listbox.get(selected_index)

            task_listbox.delete(selected_index)
            
            if task.startswith("✓ "):
                unmarked_task= task[2:]
                task_listbox.insert(selected_index,unmarked_task)
            else:
                task_listbox.insert(selected_index,f"✓ {task}")
            
            save_tasks()

            task_listbox.selection_set(selected_index)
        except IndexError:
            pass

    title_label = tk.Label(window,text="📝 Daily Tasks", font=("Arial", 18, "bold"), bg="#f0f0f0")
    title_label.pack(pady=15)

    task_input= tk.Entry(window,font=("Arial",14), width=20)
    task_input.pack(pady=5)

    add_button = tk.Button(window, text="Add Task", font=("Arial",12),bg="lightgreen",command=add_task)
    add_button.pack(pady=5)

    task_listbox =tk.Listbox(window,font=("Arial",14),width=25,height=8,selectbackground="lightblue")
    task_listbox.pack(pady=15)

    done_button= tk.Button(window,text="Mark As Done ✓ " ,font=("Arial",12),bg="#ff9999",command=mark_done)
    done_button.pack(pady=5)

    delete_button= tk.Button(window,text="Delete Selected Task",font=("Arial",12),bg="#ff9999",command=delete_task)
    delete_button.pack(pady=5)

    load_tasks()
    window.mainloop()


start_todo_app()
