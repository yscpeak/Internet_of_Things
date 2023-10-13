##### Blynk Slide V0 Control - A6FadingLED.py on Mu
## 記得點進去後，先點右下角的工具鈕，再"輕觸"Slide，就可以把Send on release關閉！
## 關閉才有漸進便亮便案的效果。

import BlynkLib
from gpiozero import PWMLED

BLYNK_TEMPLATE_ID = "TMPL2DObT2loX"
BLYNK_TEMPLATE_NAME = "First Blynk App Fading LED"
BLYNK_AUTH_TOKEN = "8GywavHavD98Fng6LYR7IJK0Wu0ZVZO_"

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
myLED = PWMLED(21)

@blynk.on("V0")
def v2_write_handler(value):
# def v2_event_handler(value):
    """Set LED hardware state."""
    try:
        brightness = int(value[0]) / 255.0
        myLED.value = brightness
    except Exception as e:
        print(e)

while True:
    try:
        blynk.run()
    except Exception as e:
        print(e)