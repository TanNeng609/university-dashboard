import tkinter as tk
import json

class Pet:
    def __init__(self,name):
        self.name=name
        self.hunger=50
        self.happiness=50
        self.energy=100
        self.is_sleeping=True
        self.is_alive=True

    def feed(self):
        if self.is_alive and not self.is_sleeping:
            self.hunger-=15
            if self.hunger<0:
                self.hunger=0

    def play(self):
        if self.is_alive and not self.is_sleeping:
            self.happiness+=15
            self.energy-=10
            if self.happiness>100:
                self.happiness=100

    def toggle_sleep(self):
        if self.is_alive:
            self.is_sleeping=not self.is_sleeping

my_pet = Pet("Babo")

def save_pet():
    pet_data={
        "name":my_pet.name,
        "hunger":my_pet.hunger,
        "happiness":my_pet.happiness,
        "energy":my_pet.energy,
        "is_sleeping":my_pet.is_sleeping,
        "is_alive":my_pet.is_alive
    }

    with open("babo_save_file.json","w")as file:
        json.dump(pet_data,file)

def load_pet():
    try:
        with open("babo_save_file.json","r")as file:
            savedData=json.load(file)

            my_pet.name=savedData["name"]
            my_pet.hunger=savedData["hunger"]
            my_pet.happiness=savedData["happiness"]
            my_pet.energy=savedData["energy"]
            my_pet.is_sleeping=savedData["is_sleeping"]
            my_pet.is_alive=savedData["is_alive"]
    except FileNotFoundError:
        pass

def start_game():
    window= tk.Tk()
    window.title("Virtual pet")
    window.geometry("350x450")
    window.config(bg="#FFFACD")
    
    load_pet()

    def update_pet():
        if my_pet.is_alive:

            if my_pet.is_sleeping:
                my_pet.energy+=5
                my_pet.hunger+=1
                if my_pet.energy>100:
                    my_pet.energy=100
                    my_pet.toggle_sleep()
                    sleep_button.config(text="🌙 Sleep")
                
                window.config(bg="#2C3E50")
                name_label.config(bg="#2C3E50",fg="white")
                pet_face.config(text="😴",bg="#2C3E50")
                stats_label.config(bg="#2C3E50",fg="white")
                button_frame.config(bg="#2C3E50")

            else:
                my_pet.hunger+=2
                my_pet.happiness-=2
                my_pet.energy-=1
                if my_pet.energy<0:
                    my_pet.energy=0
                    my_pet.toggle_sleep()
                    sleep_button.config(text="☀️ Wake")

                window.config(bg="#FFFACD")
                name_label.config(bg="#FFFACD", fg="black")
                pet_face.config(bg="#FFFACD")
                stats_label.config(bg="#FFFACD", fg="black")
                button_frame.config(bg="#FFFACD")

                if my_pet.hunger>=100 or my_pet.happiness<=0:
                    my_pet.is_alive=False
                    pet_face.config(text="😵")
                    stats_label.config(text=f"Oh no! {my_pet.name}didn't make it")
                elif my_pet.energy <20:
                    pet_face.config(text="🥱")
                elif my_pet.happiness>70 and my_pet.hunger<30:
                    pet_face.config(text="😸")
                elif my_pet.hunger>70:
                    pet_face.config(text="🤤")
                elif my_pet.happiness<30:
                    pet_face.config(text="😿")
                else:
                    pet_face.config(text="😺")

            stats_label.config(text=f"Hunger: {my_pet.hunger}/100\nHappiness:{my_pet.happiness}/100\nEnergy: {my_pet.energy}/100")

            save_pet()    

            if my_pet.is_alive:
                window.after(3000,update_pet)

    def on_feed():
        my_pet.feed()
        stats_label.config(text=f"Hunger: {my_pet.hunger}/100\nHappiness: {my_pet.happiness}/100\nEnergy: {my_pet.energy}/100")
        save_pet()

    def on_play():
        my_pet.play()
        stats_label.config(text=f"Hunger: {my_pet.hunger}/100\nHappiness: {my_pet.happiness}/100\nEnergy: {my_pet.energy}/100")
        save_pet()

    def on_sleep():
        my_pet.toggle_sleep()
        if my_pet.is_sleeping:
            sleep_button.config(text="☀️ Wake")
        else:
            sleep_button.config(text="🌙 Sleep")
        save_pet()

    name_label = tk.Label(window,text=f"{my_pet.name} the Cat",font=("Arial",18,"bold"),bg="#FFFACD")
    name_label.pack(pady=10)

    pet_face=tk.Label(window,text="🐱",font=("Arial",60),bg="#FFFACD")
    pet_face.pack(pady=10)
    
    stats_label=tk.Label(window,text="",font=("Arial",14),bg="#FFFACD")
    stats_label.pack(pady=10)

    button_frame=tk.Frame(window,bg="#FFFACD")
    button_frame.pack(pady=10)

    feed_button=tk.Button(button_frame, text="🐟 Feed",font=("Arial",12),bg="lightgreen",command=on_feed)
    feed_button.grid(row=0,column=0,padx=10)

    play_button=tk.Button(button_frame, text="🪀 Play",font=("Arial",12),bg="lightgreen",command=on_play)
    play_button.grid(row=0,column=1,padx=10)    

    initial_sleep_text="☀️ Wake" if my_pet.is_sleeping else "🌙 Sleep"
    sleep_button= tk.Button(button_frame,text=initial_sleep_text, font=("Arial", 12), bg="mediumpurple", command=on_sleep)
    sleep_button.grid(row=0,column=2,padx=5)

    update_pet()

    window.mainloop()

start_game()