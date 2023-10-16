# Demonstrate that you can use a virtual button in a Blynk app to
# turn on & off a physical LED wired to your RPi.

# Demonstrate that you can use a physical button wired to your RPi to
# turn on & off a virtual LED in a Blynk app.

import BlynkLib
from gpiozero import LED, Button

BLYNK_TEMPLATE_ID = "TMPL2JnfQKgoY"
BLYNK_TEMPLATE_NAME = "First Blynk App"
BLYNK_AUTH_TOKEN = "u4Ak0mpBZovX-Yvysy0gSS9oTQQczFcn"

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

myLED = LED(18)
myButton = Button(4)

def led_on():
    """Turn on LED"""
    blynk.virtual_write(3, 255)

def led_off():
    """Turn off LED"""
    blynk.virtual_write(3, 0)

@blynk.on("V2")
def v2_write_handler(value):
# def v2_event_handler(value):
    """Set LED hardware state."""
    try:
        if int(value[0]):
            myLED.on()
        else:
            myLED.off()
    except Exception as e:
        print(e)

myButton.when_pressed = led_on
myButton.when_released = led_off

while True:
    try:
        blynk.run()
    except Exception as e:
        print(e)