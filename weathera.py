import tkinter as tk
import requests

def start_weather_app():
    window =tk.Tk()
    window.title("Live Weather Dashboard")
    window.geometry("350x450")
    window.config(bg="#87CEEB")

    def fetch_weather():
        city=city_input.get()

        result_label.config(text="Fetching data... ⏳")
        window.update()

        try:
            url=f"https://wttr.in/{city}?format=j1"

            response = requests.get(url,timeout=5)

            weather_data= response.json()

            current = weather_data['current_condition'][0]

            
            temp_celsius = current['temp_C']
            feels_like = current['FeelsLikeC']  # NEW: Feels like temperature
            humidity = current['humidity']      # NEW: Humidity percentage
            description = current['weatherDesc'][0]['value']
            
            display_text = f"{city.title()}\n\n🌡️ Temp: {temp_celsius}°C\n🤔 Feels Like: {feels_like}°C\n💧 Humidity: {humidity}%\n🌤️ {description}"        
            result_label.config(text=display_text)
        except Exception:
            result_label.config(text="❌ City not found!\nPlease try again.")
    
    title_label=tk.Label(window, text="🌍 Weather App",font=("Arial",20,"bold"),bg="#87CEEB")
    title_label.pack(pady=20)

    instruction_label=tk.Label(window,text="Enter a city name:",font=("Arial",12),bg="#87CEEB")
    instruction_label.pack(pady=10)

    city_input= tk.Entry(window,font=("Arial",14),width=15)
    city_input.pack(pady=10)

    search_button= tk.Button(window,text="Get Weather",font=("Arial",12),bg="#87CEEB",command=fetch_weather)
    search_button.pack(pady=10)

    result_label=tk.Label(window,text="",font=("Arial",16),bg="#87CEEB",justify="center")
    result_label.pack(pady=30)

    window.mainloop()

start_weather_app()