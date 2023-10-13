# Blynk app has been created with a nicely labeled button to turn relay on and off.
# Relay is wired correctly to the RPi, either directly or into the Grove base hat.
# Blynk app can successfully turn the relay on and off.

import time
import BlynkLib
from gpiozero import OutputDevice

BLYNK_TEMPLATE_ID = "TMPL2JnfQKgoY"
BLYNK_TEMPLATE_NAME = "First Blynk App"
BLYNK_AUTH_TOKEN = "u4Ak0mpBZovX-Yvysy0gSS9oTQQczFcn"

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
myRelay = OutputDevice(25)

@blynk.on("V2")
def v2_write_handler(value):
# def v2_event_handler(value):
    """Set Relay hardware state."""
    try:
        if int(value[0]):
            myRelay.on()
        else:
            myRelay.off()
    except Exception as e:
        print(e)

while True:
    try:
        blynk.run()
    except Exception as e:
        print(e)