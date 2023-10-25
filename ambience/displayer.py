import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time
import json
import textwrap
import os, uuid
from playsound import playsound
import threading 
import datetime
import re
import pygame
import weather
import tkinter as tk
import RPi.GPIO as GPIO



# added for google calendar 
import os.path
import datetime
from datetime import timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth import exceptions
from dateutil import parser
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


# Google calendar API link
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# Defines the tikinter image and panels
original_image = Image.open("images/template.png")
panel = None
label = None

pygame.mixer.init()

# Set up connection to Azure client
account_url = "https://cs110032002ba3931bf.blob.core.windows.net/"
default_credential = DefaultAzureCredential()
# Create the BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=default_credential)

# Download the blob to a local file
local_path = 'json'
local_file_name = 'overlay.json'
download_file_path = os.path.join(local_path, local_file_name)
container_client = blob_service_client.get_container_client(container="deco3801-storage")

#Pi configuration for GPIO ports
PHOTO_BUTTON_PIN = 11
CLEAR_BUTTON_PIN = 13
LIDR_PIN = 15
TRIGGER_READING = 1500
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PHOTO_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LIDR_PIN, GPIO.IN)
displayer_process = None

# Attempt to pull with azure and overwrite the json file
def cloud_update():
    try:
        #print("Azure data update")
        
        with open(file=download_file_path, mode="wb") as download_file:
            download_file.write(container_client.download_blob("overlay.json").readall())

    except Exception as ex:
        print('Exception:')
        print(ex)



# Play the corresponding type sound with pygame 
def play_sound(type="base"):
   # print(type)
    #playsound("sounds/chime.mp3") 
    if type == "base":
        pygame.mixer.music.load("sounds/chime.mp3")
    elif type == "weather":
        pygame.mixer.music.load("sounds/sunny.mp3")
    elif type == "food":
        pygame.mixer.music.load("sounds/cooking.mp3")
    elif type == "sport":
        pygame.mixer.music.load("sounds/sports.mp3")
    elif type == "work":
        pygame.mixer.music.load("sounds/work.mp3")
    elif type == "social":
        pygame.mixer.music.load("sounds/social.mp3")
    
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue



# For setting up google calendar credentials
def OAuthHandler():
    creds = None
    if os.path.exists('json/token.json'):
        creds = Credentials.from_authorized_user_file('json/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except exceptions.RefreshError:
                creds = None 
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file('json/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('json/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


# Read JSON file
def read_json():
    with open("json/overlay.json", "r") as json_file:
        json_data = json.load(json_file)
    return json_data


# Make a different sound based on the type of event
def make_sound(event):
    event = event.lower()
    # sounds for food
    if (event.find("dinner") != -1 or event.find("lunch") != -1 or event.find("breakfast") != -1 or event.find("food") != -1 or event.find("brunch") != -1):
        play_sound("food")
    # sounds for sports
    elif (event.find("sport") != -1 or event.find("game") != -1 or event.find("match") != -1 or event.find("training") != -1 or event.find("gym") != -1):
        play_sound("sport")
    # work / school
    elif (event.find("uni") != -1 or event.find("school") != -1 or event.find("work") != -1 or event.find("meeting") != -1 or event.find("class") != -1 or event.find("lecture") != -1):
        play_sound("work")
    # social
    elif (event.find("friend") != -1 or event.find("hang") != -1 or event.find("meet") != -1 or event.find("meet") != -1 or event.find("date") != -1 or event.find("party") != -1):
        play_sound("social")
    # sound for other stuff
    else:
        play_sound("base")


# Gets the events out of the JSON file
def get_all_existing_events(js):
    existing_events = set()
    for day, day_data in js.items():
        for user, events in day_data.items():
            for event in events:
                existing_events.add(event)

    return existing_events


# Gets the image and applies text overlay based in the overlay.json file
def get_overlay_image():
    sound_played = False
    image_with_text = original_image.copy()
    draw = ImageDraw.Draw(image_with_text)

    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf", 36, encoding="unic")
    js = read_json()
    
    # Logic flow for each potential day
    for day, day_info in js.items():
        if day == "Monday":
            offset = 150
            for info, day_data in day_info.items():
                if isinstance(day_data, dict):
                    for user, events in day_data.items():
                        colour = "#0070C1" if user == "user1" else "#008080"
                        for event in events:
                            wrapped_text = textwrap.fill(event, width=15)
                            draw.multiline_text((100, offset), wrapped_text, fill=colour, font=font)  
                            offset+= 50
                            offset += len(wrapped_text.split('\n')) * 25

        elif day == "Tuesday":
            offset = 150
            for info, day_data in day_info.items():
                if isinstance(day_data, dict):
                    for user, events in day_data.items():
                        colour = "#0070C1" if user == "user1" else "#008080"
                        for event in events:
                            wrapped_text = textwrap.fill(event, width=15)
                            draw.multiline_text((450, offset), wrapped_text, fill=colour, font=font)  
                            offset+= 50
                            offset += len(wrapped_text.split('\n')) * 25
        
        elif day == "Wednesday":
            offset = 150
            for info, day_data in day_info.items():
                if isinstance(day_data, dict):
                    for user, events in day_data.items():
                        colour = "#0070C1" if user == "user1" else "#008080"
                        for event in events:
                            wrapped_text = textwrap.fill(event, width=15)
                            draw.multiline_text((810, offset), wrapped_text, fill=colour, font=font)  
                            offset+= 50
                            offset += len(wrapped_text.split('\n')) * 25
        
        elif day == "Thursday":
            offset = 150
            for info, day_data in day_info.items():
                if isinstance(day_data, dict):
                    for user, events in day_data.items():
                        colour = "#0070C1" if user == "user1" else "#008080"
                        for event in events:
                            wrapped_text = textwrap.fill(event, width=15)
                            draw.multiline_text((1175, offset), wrapped_text, fill=colour, font=font)  
                            offset+= 50
                            offset += len(wrapped_text.split('\n')) * 25


        elif day == "Friday":
            offset = 150
            for info, day_data in day_info.items():
                if isinstance(day_data, dict):
                    for user, events in day_data.items():
                        colour = "#0070C1" if user == "user1" else "#008080"
                        for event in events:
                            wrapped_text = textwrap.fill(event, width=15)
                            draw.multiline_text((1540, offset), wrapped_text, fill=colour, font=font)  
                            offset+= 50
                            offset += len(wrapped_text.split('\n')) * 25


        elif day == "Saturday":
            offset = 750
            for info, day_data in day_info.items():
                if isinstance(day_data, dict):
                    for user, events in day_data.items():
                        colour = "#0070C1" if user == "user1" else "#008080"
                        for event in events:
                            wrapped_text = textwrap.fill(event, width=40)
                            draw.multiline_text((90, offset), wrapped_text, fill=colour, font=font)  
                            offset+= 50
                            offset += len(wrapped_text.split('\n')) * 25


        elif day == "Sunday":
            offset = 750
            for info, day_data in day_info.items():
                if isinstance(day_data, dict):
                    for user, events in day_data.items():
                        colour = "#0070C1" if user == "user1" else "#008080"
                        for event in events:
                            wrapped_text = textwrap.fill(event, width=40)
                            draw.multiline_text((990, offset), wrapped_text, fill=colour, font=font)  
                            offset+= 50
                            offset += len(wrapped_text.split('\n')) * 25

    return image_with_text


# initialses the base display onto the screen
def init_display():
    global root, label, screen_brightness
    root = tk.Tk()
    image_with_text = get_overlay_image()
    photo = ImageTk.PhotoImage(image_with_text.resize((640,455)))
    label = tk.Label(root, image=photo)
    label.pack()
    label.photo = photo
    screen_brightness = 1.0  # 100% brightness by default
    root.attributes("-alpha", screen_brightness)
    
    
# Function that pulls json data from google calendar
def google_calendar_handler():
    try:
        service = OAuthHandler()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        one_week_from_now = (datetime.datetime.utcnow() + timedelta(weeks=1)).isoformat() + 'Z'
        events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=one_week_from_now,
                                              singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        js = read_json()  # read the existing JSON data
        existing_events = get_all_existing_events(js)

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            date_obj = parser.parse(start)
            day_of_week = date_obj.strftime("%A")

            formatted_time = date_obj.strftime('%I%p').lower().lstrip('0')
            event_summary = f"{formatted_time} {event['summary']}".lower()
            hour_key = date_obj.strftime('%H')

            user = 'user1'
            if event_summary not in existing_events:
                if day_of_week not in js:
                    js[day_of_week] = {hour_key: {user: [event_summary]}}
                else:
                    if hour_key not in js[day_of_week]:
                        js[day_of_week][hour_key] = {user: [event_summary]}
                    elif user not in js[day_of_week][hour_key]:
                        js[day_of_week][hour_key][user] = [event_summary]
                    else:
                        if event_summary not in js[day_of_week][hour_key][user]:
                            js[day_of_week][hour_key][user].append(event_summary)
                    existing_events.add(event_summary)
        
        with open("json/overlay.json", "w") as json_file:
            print("POINT")
            json.dump(js, json_file)
        print("point 2")
    except HttpError as error:
        print('An error occurred: %s' % error)



# Daemon thread that polls the cloud for updates
def async_loop():
    while True:
        time.sleep(5)
        

        #if the buttor is pressed
        # clear_image()
        #else
        cloud_update()
        print("cloud update")
        time.sleep(1)
        google_calendar_handler()
        print("calendar update")
        time.sleep(1)
        update_image()
        print("image update")


# Make tkinter reload the display 
def update_image():
    overlay = get_overlay_image()
    photo = ImageTk.PhotoImage(overlay.resize((640,455)))


    label.config(image=photo)
    label.image = photo
    

# Clear the tkinter display to make it ready to take photo
def clear_image(channel):
    overlay = original_image.copy()
    photo = ImageTk.PhotoImage(overlay.resize((640,455)))

    label.config(image=photo)
    label.image = photo
    time.sleep(3)


# Seperate thread to play sound if there is an event in the next hour
def time_thread():
    played = False
    numplayed = 0
    counter = 0
    pattern = r'([1-9]|1[0-2])(am|pm)'

    while True:
        current_datetime = datetime.datetime.now()
        day_of_week = current_datetime.strftime("%A")
        current_hour_24 = int(current_datetime.strftime("%H"))
        current_minute = current_datetime.minute
        
        json_file = read_json()
        #rread the JSON for the day and find the relevant events
        # play the relevant sounds for them and track how many were played
        # if numplayed > 0 and number events > numlpayed play the difference 
        times =  json_file.get(day_of_week, {})       
        counter = 0

        for ctime, user_events in times.items():
            for user, events_list in user_events.items():
                cur_time = int(ctime)  
                for event in events_list:
                        if (((cur_time - current_hour_24) == 1) and (counter >= numplayed)):
                            make_sound(event)
                        counter = counter + 1
                        print(counter)
        numplayed = counter
        print(numplayed)

        time.sleep(30)
       
        
# Code that initialises the lidar. 
def init_display_light():
    global root, label, screen_brightness
    root = tk.Tk()
    image_with_text = get_overlay_image()
    photo = ImageTk.PhotoImage(image_with_text)
    label = tk.Label(root, image=photo)
    label.pack()
    label.photo = photo
    screen_brightness = 1.0  # 100% brightness by default
    root.attributes("-alpha", screen_brightness)


# Increase and decrease brighness of screen depening on light detected by lidar
def monitor_light_sensor():
    global screen_brightness
    try:
        while True:
            sensor_value = GPIO.input(LIDR_PIN)

            if sensor_value == GPIO.LOW:
              #  print("Dark")
                if screen_brightness > 0.2:
                    screen_brightness -= 0.1  # Reduce brightness by 20% when it's dark
            else:
           #     print("Light")
                if screen_brightness < 1.0:
                # Increase brightness by 20% when it's light
                    screen_brightness += 0.1
                    if screen_brightness >= 1:
                        weather.play_weather()
                    
            root.attributes("-alpha", screen_brightness)
            time.sleep(0.1)  

    except KeyboardInterrupt:
        GPIO.cleanup()        
 
 
# Main function and tkinter loop
if __name__ == "__main__":
    start_time = time.time()
    GPIO.add_event_detect(PHOTO_BUTTON_PIN, GPIO.RISING, callback=clear_image)
    cloud_update()
    read_json()
    init_display()
    t1 = threading.Thread(target=async_loop)
    t1.start()
    t2 = threading.Thread(target=time_thread)
    t2.start()
    t4 = threading.Thread(target=monitor_light_sensor)  
    t4.start()
    root.mainloop()

