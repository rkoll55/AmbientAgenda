
# @Gil - R + T's systems need to be connected with this code. This is just the main architecture of the processes that are happening. 
# It will be easier to connect Rohans and Tobys systems IN PERSON during the studio, as I'm not currently sure how to connect to seperate Linux/Cloud. 
# Need to incorperate the 15 minute every morning ambient bell. Not sure which part of the code will need that section. 
# this code is rough lol 

# RUN pip install RPi.GPIO picamera requests ! !! 

import RPi.GPIO as GPIO
import time
import picamera
import requests

# Configure GPIO pins for light sensor and button This is the PI section. 
LIGHT_SENSOR_PIN = 17
BUTTON_PIN = 18

# Cloud storage endpoint URL ! Tobys link goes here ! 
CLOUD_URL = "https://your-cloud-service.com/upload"

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_SENSOR_PIN, GPIO.IN)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def take_photo():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)  # resolution
        camera.start_preview()
        time.sleep(2)  #  camera to adjust to light
        timestamp = time.strftime("%Y%m%d%H%M%S")
        photo_filename = f"photo_{timestamp}.jpg"
        camera.capture(photo_filename)
        return photo_filename

def upload_to_cloud(photo_filename):
    try:
        files = {'photo': open(photo_filename, 'rb')}
        response = requests.post(CLOUD_URL, files=files)
        if response.status_code == 200:
            print("Photo uploaded to the cloud successfully.")
        else:
            print("Failed to upload photo to the cloud.")
    except Exception as e:
        print(f"Error uploading to the cloud: {str(e)}")

def main():
    setup()
    while True:
        if GPIO.input(LIGHT_SENSOR_PIN) == GPIO.LOW:
            print("Light detected, turning on Linux code.")
            #  code here to trigger  Linux-based code, needs to be done during the studio 
            time.sleep(5)  
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed, taking a photo.")
            photo_filename = take_photo()
            upload_to_cloud(photo_filename)
            time.sleep(2)  

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Observer program terminated.")
    finally:
        GPIO.cleanup()
