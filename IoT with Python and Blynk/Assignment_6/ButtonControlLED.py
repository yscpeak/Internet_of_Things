##### Blynk Button V2 Control - A6First_blynk.py on Mu

import BlynkLib
from gpiozero import LED

BLYNK_TEMPLATE_ID = "TMPL2JnfQKgoY"
BLYNK_TEMPLATE_NAME = "First Blynk App"
BLYNK_AUTH_TOKEN = "u4Ak0mpBZovX-Yvysy0gSS9oTQQczFcn"

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
myLED = LED(21)

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

while True:
    try:
        blynk.run()
    except Exception as e:
        print(e)