# Observer Script
import RPi.GPIO as GPIO #Need to install "Microsoft C++ Build Tools first"
import subprocess
import cv2
import time
import recog
from azure.iot.device import IoTHubDeviceClient, Message
import json

CONNECTION_STRING = "HostName=deco3801.azure-devices.net;DeviceId=raspberrypi1;SharedAccessKey=jZKYxNL3AY5EuMBZF/p9YDUy54ClsFYStjhp/v8E4yg="
GPIO.setmode(GPIO.BCM)

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def capture_photo(cap):
    #cap = cv2.VideoCapture(1)  # 1 for the USB camera, change as needed

    ret, frame = cap.read()
    if ret:
        photo_name = "capture.jpg"
        cv2.imwrite(photo_name, frame)
        #print(f"Photo captured and saved as {photo_name}")

    cap.release()

LIDR_PIN = 6
PHOTO_BUTTON_PIN = 7
TRIGGER_READING = 1500

GPIO.setup(LIDR_PIN, GPIO.IN)
GPIO.setup(PHOTO_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 1 should indicate the first usb camera, 0 being picam port
camera = cv2.VideoCapture(0) 

if not camera.isOpened():
    print("Could not open camera.")
    
capture_photo(camera) #remove this
json_object = recog.write_to_temp(recog.box_recog('capture.jpg'), infile="json/template.json", outfile="json/output.json") #delete this


displayer_process = None
button_pressed = False

try:
    while True:
        print("In LIDR loop.")
        #Following three lines to be deleted for proper functionality.
        print("Attempting to run displayer.")
        displayer_process = subprocess.Popen(["python3", "displayer.py"])
        break
        light_reading = GPIO.input(LIDR_PIN)
        if light_reading >= TRIGGER_READING and displayer_process is None:
            print("Attempting to run displayer.")
            displayer_process = subprocess.Popen(["python3", "displayer_program.py"])
            break
        
    while True:
        print("polling buttons")
        
        button_state = GPIO.input(PHOTO_BUTTON_PIN)
        '''
        if light_reading >= TRIGGER_READING and displayer_process is None:
            displayer_process = subprocess.Popen(["python3", "displayer_program.py"])
        elif light_reading < TRIGGER_READING and displayer_process is not None:
            displayer_process.terminate()
            displayer_process = None
        '''
        if button_state == GPIO.LOW and not button_pressed:
            print("Attempting Capture.")
            capture_photo(camera)
            #Sending to text recognition script
            json_object = recog.write_to_temp(recog.box_recog('capture.jpg'), infile="json/template.json", outfile="json/output.json") #has default file paths
            # push to cloud over here
            print("Successfully recognised text")
            
            print("Connecting to IoT Hub...")
            client = iothub_client_init()
            client.connect()
            print("Successfully connected to IoT hub")

            #the code to send
            print(json_object)
            print(str(json_object))
            message = Message(str(json_object))
            print("Sending capture to IoT Hub...")
            message.content_encoding = "utf-8"
            message.content_type = "application/json"
            client.send_message(message)
            print("Sent.")
            #no idea if it works

            button_pressed = True
        elif button_state == GPIO.HIGH:
            button_pressed = False
        break

except KeyboardInterrupt:
    if displayer_process is not None:
        displayer_process.terminate()
    GPIO.cleanup()
    cv2.destroyAllWindows()
