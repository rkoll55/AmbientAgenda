import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import time
import json
import textwrap
import os
from playsound import playsound
import threading 
import datetime
import re
import pygame
import weather



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

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


original_image = Image.open("images/template.png")
panel = None
label = None

pygame.mixer.init()


def play_sound(type="base"):
    print(type)
    #playsound("sounds/chime.mp3") 

    pygame.mixer.music.load("sounds/chime.mp3")
    pygame.mixer.music.play()

# for initial setup of access tokens for google calendar
def OAuthHandler():
    creds = None
    if os.path.exists('json/token.json'):
        creds = Credentials.from_authorized_user_file('json/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except exceptions.RefreshError:
                creds = None  # Set creds to None so that new authentication flow will be triggered
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file('json/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('json/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def read_json():
    with open("json/overlay.json", "r") as json_file:
        json_data = json.load(json_file)
    return json_data


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


# method to get all the existing events to check duplicate events 
def get_all_existing_events(js):
    existing_events = set()
    # may need js = read_json() here 
    for day, day_data in js.items():
        for user, events in day_data.items():
            for event in events:
                existing_events.add(event)

    return existing_events

def get_overlay_image():
    sound_played = False
    image_with_text = original_image.copy()
    draw = ImageDraw.Draw(image_with_text)
    font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf", 36, encoding="unic")
    # font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf", 36, encoding="unic")
    js = read_json()

    for day, day_info in js.items():
        if day == "Monday":
            offset = 150
            for info, day_data in day_info.items():
                if isinstance(day_data, dict):
                    for user, events in day_data.items():
                        colour = "blue" if user == "user1" else "green"
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
                        colour = "blue" if user == "user1" else "green"
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
                        colour = "blue" if user == "user1" else "green"
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
                        colour = "blue" if user == "user1" else "green"
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
                        colour = "blue" if user == "user1" else "green"
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
                        colour = "blue" if user == "user1" else "green"
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
                        colour = "blue" if user == "user1" else "green"
                        for event in events:
                            wrapped_text = textwrap.fill(event, width=40)
                            draw.multiline_text((990, offset), wrapped_text, fill=colour, font=font)  
                            offset+= 50
                            offset += len(wrapped_text.split('\n')) * 25

    return image_with_text

read_json()

#initialises Tkinter window once with the label to display the image, rather than recreating the window every time the image is updated.
def init_display():
    global root, label
    root = tk.Tk()
    image_with_text = get_overlay_image()
    photo = ImageTk.PhotoImage(image_with_text)

    label = tk.Label(root, image=photo)
    label.pack()
    label.photo = photo
    
def async_loop():
    while True:
        #print("Async loop is running!")
        time.sleep(5) 

        #if the buttor is pressed
        # clear_image()
        #else
        update_image()

# for google calendar
def google_calendar_handler():
    while True:  # keep this thread always running
        try:
            service = OAuthHandler()
            
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            one_week_from_now = (datetime.datetime.utcnow() + timedelta(weeks=1)).isoformat() + 'Z'
            
            #print('Getting all events for the upcoming week')
            
            events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=one_week_from_now,
                                                  singleEvents=True, orderBy='startTime').execute()
            
            events = events_result.get('items', [])
            
            if not events:
                #print('No upcoming events found.')
                continue  # go to next iteration of the loop
            
            js = read_json()  # read the existing JSON data
            existing_events = get_all_existing_events(js)

            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                # Parsing the date string to datetime object
                date_obj = parser.parse(start)
                # Get the day of the week
                day_of_week = date_obj.strftime("%A")
    
                formatted_time = date_obj.strftime('%I%p').lower().lstrip('0')  # e.g., "12pm" or "2am"
                event_summary = f"{formatted_time} {event['summary']}"
                hour_key = date_obj.strftime('%H')  # This gives the hour in the format "00" to "23"

                # Events for user 1
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
    
            # Write updated data back to JSON file
            with open("json/overlay.json", "w") as json_file:
                json.dump(js, json_file)
            
        except HttpError as error:
            print('An error occurred: %s' % error)
        
        # sleep for 100 seconds before rechecking for events added to google calendar 
        time.sleep(100)


def update_image():
    overlay = get_overlay_image()
    photo = ImageTk.PhotoImage(overlay)

    label.config(image=photo)
    label.image = photo

def clear_image():
    overlay = original_image.copy()
    photo = ImageTk.PhotoImage(overlay)

    label.config(image=photo)
    label.image = photo

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
        #print(current_datetime)

        
        json_file = read_json()
        #rread the JSON for the day and find the relevant events
        # play the relevant sounds for them and track how many were played
        # if numplayed > 0 and number events > numlpayed play the difference 
        times =  json_file.get(day_of_week, {})       
        counter = 0


        # for ctime in times:
        #     events = times[ctime]
        #     if events:
        #         for user in events:
        #             cur_time = int(ctime)   
                    
        #             for event in events[user]:  

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
 
if __name__ == "__main__":
    weather.play_weather()
    init_display()
    t1 = threading.Thread(target=async_loop)
    t1.start()
    t2 = threading.Thread(target=time_thread)
    t2.start()
    t3 = threading.Thread(target=google_calendar_handler)
    t3.start()
    root.mainloop()