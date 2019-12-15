import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Set pull up resistor in software
# Pin is set to high, when button is pressed it gets connected to ground, so goes low.
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_callback(channel):
    print("Button was pushed!")

#GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
#GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(18,GPIO.FALLING,callback=button_callback)