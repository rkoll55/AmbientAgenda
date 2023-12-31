# Observer Script
import RPi.GPIO as GPIO
import subprocess
import cv2
import time
import recog
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json


# Button Setup
LIDR_PIN = 15
PHOTO_BUTTON_PIN = 11
TRIGGER_READING = 1500
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PHOTO_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LIDR_PIN, GPIO.IN)
displayer_process = None

# Cloud Storage Setup
account_url = "https://cs110032002ba3931bf.blob.core.windows.net"
default_credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(account_url, credential=default_credential)


# Camera Setup: 1 should indicate the first usb camera, 0 being picam port
def capture_photo():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    ret, frame = cap.read()
    if ret:
        photo_name = "capture.jpg"
        cv2.imwrite(photo_name, frame)
        # print(f"Photo captured and saved as {photo_name}")

    cap.release()

# The function called upon the button press to capture, run recognition and upload recognised text.
def button_callback(channel):
    print("button pressed")
    
    time.sleep(2)
    capture_photo()
    try:
        recog.write_to_temp(recog.box_recog('capture.jpg'), infile="json/template2.json", outfile="json/output.json")
        # push to cloud over here
        print("Successfully recognised text")
    except Exception as e:
        print("Failed to read text")

    # Send to container
    local_file_name = "json/template.json"
    upload_file_path = local_file_name

    blob_client = blob_service_client.get_blob_client(container="deco3801-storage", blob=local_file_name)
    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

if __name__ == "__main__":
    print("Program Start")
    GPIO.add_event_detect(PHOTO_BUTTON_PIN, GPIO.RISING, callback=button_callback)
    
    # Start the display.
    displayer_process = subprocess.Popen(["python3", "displayer.py"])
    
    # Continue running in wait for button press.
    while True:
        continue
