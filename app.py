import RPi.GPIO as GPIO
import vlc
import requests
import time
# This was written super super quickly, but it works

GPIO.setmode(GPIO.BCM)

# Set pull up resistor in software
# Pin is set to high, when button is pressed it gets connected to ground, so goes low.
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# API key for Hue bridge
# Absolute path needed for running script as a service
f = open("/home/pi/christmas-box/api.key", "r")
key = f.read()
bridge_url = 'http://192.168.0.242/api/' + key + '/lights/' # use lights 2 and 4
state = '/state'

# Global variables are always good
song_player = vlc.MediaPlayer("/home/pi/christmas-box/music/song.mp3")
christmas_fm = vlc.MediaPlayer("https://ice31.securenetsystems.net/XMASFMM")

# JSON payloads for light colours
# Set Red
red = '{"on": true,"bri": 254,"hue": 65340,"sat": 251, "effect": "none","xy": [ 0.6822,0.3064]}'
# Transition Red
red_transition = '{"on": true,"bri": 254,"hue": 65340,"sat": 251, "effect": "none","xy": [ 0.6822,0.3064],"transitiontime":80}'
# Set Green
green = '{"on": true,"bri": 254,"hue": 24432,"sat": 254, "effect": "none","xy": [0.1938,0.6821]}'
# Transition Green
green_transition = '{"on": true,"bri": 254,"hue": 24432,"sat": 254, "effect": "none","xy": [0.1938,0.6821], "transitiontime":80}'
# Normal Lights
normal_light = '{"on":true,"bri":144,"hue":7676,"sat":199,"effect":"none","xy":[0.5016,0.4151],"ct":443}'


# Button control logic
def button_brb(channel):
    print("button_brb was pushed!")
    # play music
    do_music()

    # set lights looping
    do_lights()


def stop(channel):
    print("stop was pushed!")
    set_lights_normal()
    GPIO.cleanup()
    exit()


def button_christmasfm(channel):
    print("button_christmasfm was pushed!")
    do_christmas_fm()


# Music Logic
def do_music():
    christmas_fm.stop()
    if song_player.is_playing():
        song_player.stop()
    else:
        song_player.play()


def do_christmas_fm():
    song_player.stop()
    if christmas_fm.is_playing():
        christmas_fm.stop()
    else:
        christmas_fm.play()


# Sets lights to red and green, then transitions them to alternate colours for 4 minutes
def do_lights():
    # set light 2 to green
    set_light_green('2')
    # set light 4 to red
    set_light_red('4')

    # loop 29 times, sleep 8.5 seconds
    # 4 was set to red, want it to transition to green
    light_to_green = '4'
    # 2 was set to green, want it to transition it to red
    light_to_red = '2'
    for x in range(20):
        print("loop setting " + light_to_red + "to red")
        print("loop setting " + light_to_green + "to green")
        transition_light_red(light_to_red)
        transition_light_green(light_to_green)
        # Swap light identifiers for next loop
        temp = light_to_green
        light_to_green = light_to_red
        light_to_red = temp
        time.sleep(9)
        # Allow for button press interrupt
        #for y in range(9):
            # Todo: make this work with a button press interrupt
            #time.sleep(1)


# Functions below are used for setting lights to green or red, either immediately or with a transition
def set_light_green(light_number):
    print("setting light green")
    r = requests.put(url=build_url(light_number), data=green)
    print(r.text)


def set_light_red(light_number):
    print("setting light red")
    r = requests.put(url=build_url(light_number), data=red)


def transition_light_green(light_number):
    print("transition light green")
    r = requests.put(url=build_url(light_number), data=green_transition)
    print(r.text)


def transition_light_red(light_number):
    print("transition light red")
    r = requests.put(url=build_url(light_number), data=red_transition)


def set_lights_normal():
    r = requests.put(url=build_url('2'), data=normal_light)
    r = requests.put(url=build_url('4'), data=normal_light)


# Builds the full URL for setting light state.
# Returned value should be something like
# 192.168.0.5/[apikey]/2/state
def build_url(light_number):
    return bridge_url + light_number + state


# Logic to listen for button events
GPIO.add_event_detect(18,GPIO.FALLING,callback=button_brb)
GPIO.add_event_detect(14,GPIO.FALLING,callback=stop)
GPIO.add_event_detect(15,GPIO.FALLING,callback=button_christmasfm)


# Prevent program from ending
while True:
    num = 1 + 1
# GPIO.cleanup()
