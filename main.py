import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time
import json
import textwrap


import asyncio
import aiohttp
import threading 


root = tk.Tk()
original_image = Image.open("template.png")
panel = None
label = None

def read_json():

    with open("overlay.json", "r") as json_file:
        json_data = json.load(json_file)

    return json_data


def get_overlay_image():
    image_with_text = original_image.copy()
    draw = ImageDraw.Draw(image_with_text)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf", 36, encoding="unic")
    js = read_json()

    for day, day_data in js.items():
        if day == "Monday":
            offset = 150
            if isinstance(day_data, dict):
                for user, events in day_data.items():
                    colour = "blue" if user == "user1" else "black"
                    for event in events:
                        wrapped_text = textwrap.fill(event, width=15)
                        draw.multiline_text((100, offset), wrapped_text, fill=colour, font=font)  
                        offset+= 50
                        offset += len(wrapped_text.split('\n')) * 25

        elif day == "Tuesday":
            offset = 150
            if isinstance(day_data, dict):
                for user, events in day_data.items():
                    colour = "blue" if user == "user1" else "black"
                    for event in events:
                        wrapped_text = textwrap.fill(event, width=15)
                        draw.multiline_text((450, offset), wrapped_text, fill=colour, font=font)  
                        offset+= 50
                        offset += len(wrapped_text.split('\n')) * 25
        
        elif day == "Wednesday":
            offset = 150
            if isinstance(day_data, dict):
                for user, events in day_data.items():
                    colour = "blue" if user == "user1" else "black"
                    for event in events:
                        wrapped_text = textwrap.fill(event, width=15)
                        draw.multiline_text((810, offset), wrapped_text, fill=colour, font=font)  
                        offset+= 50
                        offset += len(wrapped_text.split('\n')) * 25
        
        elif day == "Thursday":
            offset = 150
            if isinstance(day_data, dict):
                for user, events in day_data.items():
                    colour = "blue" if user == "user1" else "black"
                    for event in events:
                        wrapped_text = textwrap.fill(event, width=15)
                        draw.multiline_text((1175, offset), wrapped_text, fill=colour, font=font)  
                        offset+= 50
                        offset += len(wrapped_text.split('\n')) * 25


        elif day == "Friday":
            offset = 150
            if isinstance(day_data, dict):
                for user, events in day_data.items():
                    colour = "blue" if user == "user1" else "black"
                    for event in events:
                        wrapped_text = textwrap.fill(event, width=15)
                        draw.multiline_text((1530, offset), wrapped_text, fill=colour, font=font)  
                        offset+= 50
                        offset += len(wrapped_text.split('\n')) * 25


        elif day == "Saturday":
            offset = 750
            if isinstance(day_data, dict):
                for user, events in day_data.items():
                    colour = "blue" if user == "user1" else "black"
                    for event in events:
                        wrapped_text = textwrap.fill(event, width=40)
                        draw.multiline_text((90, offset), wrapped_text, fill=colour, font=font)  
                        offset+= 50
                        offset += len(wrapped_text.split('\n')) * 25


        elif day == "Sunday":
            offset = 750
            if isinstance(day_data, dict):
                for user, events in day_data.items():
                    colour = "blue" if user == "user1" else "black"
                    for event in events:
                        wrapped_text = textwrap.fill(event, width=40)
                        draw.multiline_text((990, offset), wrapped_text, fill=colour, font=font)  
                        offset+= 50
                        offset += len(wrapped_text.split('\n')) * 25

    return image_with_text

read_json()

def display_image(image_with_text):
    global root
    global label

    root.destroy(); root = tk.Tk()
    photo = ImageTk.PhotoImage(image_with_text)
    label = tk.Label(root, image=photo)
    label.pack()
    label.photo = photo
    root.mainloop()

def update_image(text_to_add):
    overlay = get_overlay_image(text_to_add)
    photo = ImageTk.PhotoImage(overlay)

    label.config(image=photo)
    label.image = photo

def main_thread():
    global root
    # Displaying initial state of GUI
    display_image(get_overlay_image())
    # Running tkinter main loop
    root.mainloop()

def async_loop():
    while True:
        print("Async loop is running!")
        time.sleep(5) 
        #to be implemented...
 
if __name__ == "__main__":
    t1 = threading.Thread(target=async_loop)
    t1.start()
    main_thread()