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
LIDR_PIN = 11
PHOTO_BUTTON_PIN = 13
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


def button_callback(channel):
    print("button pressed")
    capture_photo()

    recog.write_to_temp("user2", recog.box_recog('capture.jpg', real=True, debug=True), infile="json/template.json", outfile="json/output.json")
    # push to cloud over here
    print("Successfully recognised text")

    # Send to container
    local_file_name = "json/template.json"
    upload_file_path = local_file_name

    blob_client = blob_service_client.get_blob_client(container="deco3801-storage", blob=local_file_name)
    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

def button_callblack(channel):
    print("hi")
    
    
if __name__ == "__main__":
    GPIO.add_event_detect(PHOTO_BUTTON_PIN, GPIO.RISING, callback=button_callback)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        if displayer_process is not None:
            displayer_process.terminate()
        GPIO.cleanup()
        cv2.destroyAllWindows()
