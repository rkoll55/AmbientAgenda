from picamera2 import Picamera2
import time


camera = Picamera2()

camera.start_preview()
camera.start()
time.sleep(2)
camera.capture_file('test_image.jpg')
camera.stop_preview()
