import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def button_callback(channel):
	print("button pushed")

GPIO.add_event_detect(11,GPIO.RISING,callback=button_callback)
message = input("Press button")

