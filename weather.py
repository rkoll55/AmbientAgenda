import requests
import pygame


# OpenWeatherMap API key  /home/deco3801/Desktop/weather.py
api_key = "273bc3d19d048c1238798c7e29ff54ef"


city_id = 2174003  # Brisbane, Australia


weather_url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}"


sunny_sound = "sunny.mp3"
rainy_sound = "rainy.mp3"
cloudy_sound = "sunny.mp3"

pygame.mixer.init()

def get_weather():
    try:
        response = requests.get(weather_url)
        data = response.json()
        weather_main = data["weather"][0]["main"]
        return weather_main
    except Exception as e:
        print("Error fetching weather data:", e)
        return None

def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def main():
    while True:
        weather = get_weather()
        
        if weather:
            if "Clear" in weather:
                play_sound(sunny_sound)
            elif "Rain" in weather or "Drizzle" in weather:
                play_sound(rainy_sound)
            else:
                play_sound(cloudy_sound)
        
        time.sleep(1800)

if __name__ == "__main__":
    main()
