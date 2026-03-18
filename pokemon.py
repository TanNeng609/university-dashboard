import customtkinter as ctk
import requests
from PIL import Image
import io
import threading

ctk.set_appearance_mode("dark")
app=ctk.CTk()
app.title("Python Pokedex")

current_normal_img=""
current_shiny_img=""
is_shiny=False

app.after(0,lambda:app.state('zoomed'))

def toggle_shiny():
    global is_shiny
    if current_normal_img=="":
        return
    
    is_shiny=not is_shiny

    target_url=current_shiny_img if is_shiny else current_normal_img

    if target_url:
        img_response=requests.get(target_url)
        img_data=Image.open(io.BytesIO(img_response.content))
        ctk_image=ctk.CTkImage(light_image=img_data,dark_image=img_data,size=(250,250))
        image_label.configure(image=ctk_image)

        shiny_button.configure(text="Show Normal" if is_shiny else "Show Shiny✨")

def search_pokemon(pokemon_name):
    global current_normal_img, current_shiny_img, is_shiny
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    try:
        response =requests.get(url)

        if response.status_code==200:
            data=response.json()
            name=data["name"].capitalize()
            weight=data["weight"]/10
            height=data["height"]/10

            type_lists=[t["type"]["name"].capitalize() for t in data["types"]]
            types_str= ", ".join(type_lists)

            abilities_list=[a["ability"]["name"].capitalize().replace("-"," ") for a in data["abilities"]]
            abilities_str=", ".join(abilities_list)

            stats_str=""
            for stat in data["stats"]:
                stat_name=stat["stat"]["name"].upper().replace("-"," ")
                stat_value=stat["base_stat"]
                stats_str += f"{stat_name}: {stat_value}\n"

            story_str="No story available."
            species_url=data["species"]["url"]
            species_response=requests.get(species_url)

            if species_response.status_code==200:
                species_data=species_response.json()
                for entry in species_data["flavor_text_entries"]:
                    if entry["language"]["name"]=="en":
                        story_str = entry["flavor_text"].replace("\n"," ").replace("\f"," ")
                        break


            full_info=(
                f"Name:{name}\n"
                f"Type:{types_str}\n"
                f"Height:{height}m | Weight:{weight}kg\n"
                f"Abilities:{abilities_str}\n\n"
                f"--- Background Story ---\n"
                f"{story_str}\n\n"
                f"--- Base Stats---\n"
                f"{stats_str}"
            )

            info_label.configure(text=full_info,text_color="white",justify="left")

            current_normal_img=data["sprites"]["other"]["official-artwork"]["front_default"]
            current_shiny_img=data["sprites"]["other"]["official-artwork"]["front_shiny"]

            is_shiny=False
            shiny_button.configure(text="Show Shiny ✨")

            if current_normal_img:
                img_response=requests.get(current_normal_img)
                img_data=Image.open(io.BytesIO(img_response.content))
                ctk_image=ctk.CTkImage(light_image=img_data,dark_image=img_data,size=(200,200))
                image_label.configure(image=ctk_image,text="")

        else:
            info_label.configure(text="Pokemon not found!\nCheck Your Spelling",text_color="#C0392B")
            image_label.configure(image="",text="?")
            current_normal_img=""

    except requests.exceptions.RequestException:
        info_label.configure(text="No internet connection!", text_color="#C0392B")

def search_btn_clicked():
    name=search_entry.get().strip()
    if name:
        threading.Thread(target=search_pokemon,args=(name,)).start()

title_label=ctk.CTkLabel(app,text="Pokedex Tracker",font=("Arial",28,"bold"))
title_label.pack(pady=20)

search_frame=ctk.CTkFrame(app,fg_color="transparent")
search_frame.pack(pady=10,fill="x",padx=20)

search_entry=ctk.CTkEntry(search_frame,placeholder_text="Enter pokemon...",width=200)
search_entry.pack(side="left",padx=10)

search_button=ctk.CTkButton(search_frame,text="Search",command=search_btn_clicked,width=80)
search_button.pack(side="left")

content_frame=ctk.CTkFrame(app,fg_color="transparent")
content_frame.pack(fill="both",expand=True,padx=20,pady=10)

scroll_frame=ctk.CTkScrollableFrame(content_frame,width=150,label_text="Gen 1 Pokemon")
scroll_frame.pack(side="left",fill="y",padx=(0,10))

detail_frame=ctk.CTkScrollableFrame(content_frame)
detail_frame.pack(side="left",fill="both",expand=True)

image_label=ctk.CTkLabel(detail_frame,text="?",font=("Arial",100),width=200,height=200,fg_color="gray20",corner_radius=15)
image_label.pack(pady=20)

shiny_button=ctk.CTkButton(detail_frame,text="Show Shiny ✨",command=lambda:threading.Thread(target=toggle_shiny).start(),width=150,fg_color="#D4AC0D",hover_color="#B7950B",text_color="black")
shiny_button.pack(pady=5)

info_label=ctk.CTkLabel(detail_frame,text="Type a name to begin!",font=("Arial",18),wraplength=700)
info_label.pack(pady=10)

def load_grid():
    url = "https://pokeapi.co/api/v2/pokemon?limit=300"
    try:
        response=requests.get(url).json()

        for pokemon in response["results"]:
            name=pokemon["name"].capitalize()

            btn=ctk.CTkButton(scroll_frame,text=name,command=lambda n=name:threading.Thread(target=search_pokemon,args=(n,)).start())
            btn.pack(pady=5,padx=5,fill="x")
    except:
        pass

load_grid()

app.mainloop()