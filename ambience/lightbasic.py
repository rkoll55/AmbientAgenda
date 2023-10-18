import RPi.GPIO as GPIO
import time

# Disable GPIO warnings
GPIO.setwarnings(False)

# Set the GPIO mode and channel
GPIO.setmode(GPIO.BCM)
light_sensor_pin = 17  # Adjust this to the GPIO pin you've connected to the sensor

# Setup the GPIO pin as an input
GPIO.setup(light_sensor_pin, GPIO.IN)

try:
    while True:
        # Read the light sensor value
        sensor_value = GPIO.input(light_sensor_pin)

        if sensor_value == GPIO.LOW:
            print("Dark")
        else:
            print("Light")

        time.sleep(3.5)  # Read the sensor every 1 second

except KeyboardInterrupt:
    GPIO.cleanup()
