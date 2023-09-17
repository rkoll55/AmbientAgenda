# Observer Script
import RPi as GPIO #Need to install "Microsoft C++ Build Tools first"
import subprocess
from picamera import PiCamera
import time
import recog

GPIO.setmode(GPIO.BCM)

LIDR_PIN = 1
PHOTO_BUTTON_PIN = 2
TRIGGER_READING = 1500

GPIO.setup(LIDR_PIN, GPIO.IN)
GPIO.setup(PHOTO_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera()

displayer_process = None
button_pressed = False

try:
    while True:
        light_reading = GPIO.input(LIDR_PIN)
        if light_reading >= TRIGGER_READING and displayer_process is None:
            displayer_process = subprocess.Popen(["python3", "displayer_program.py"])
            break
        
    camera.start_preview()
    time.sleep(3)
    while True:
        
        button_state = GPIO.input(PHOTO_BUTTON_PIN)
        '''
        if light_reading >= TRIGGER_READING and displayer_process is None:
            displayer_process = subprocess.Popen(["python3", "displayer_program.py"])
        elif light_reading < TRIGGER_READING and displayer_process is not None:
            displayer_process.terminate()
            displayer_process = None
        '''
        if button_state == GPIO.LOW and not button_pressed:
            camera.capture('capture.jpg')
            json = recog.write_to_temp(recog.box_recog('capture.jpg'), infile="template.json", outfile="output.json") #has default file paths
            # push to cloud over here
            button_pressed = True
        elif button_state == GPIO.HIGH:
            button_pressed = False

except KeyboardInterrupt:
    if displayer_process is not None:
        displayer_process.terminate()
    camera.stop_preview()
    GPIO.cleanup()