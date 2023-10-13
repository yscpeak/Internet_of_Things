#***** Switching an LED on and off *****#

# First import the GPIO Zero library, and tell the Pi
#   which GPIO pin you are using - in this case pin 17.
# And press Enter on the keyboard.
from gpiozero import LED
import time
led = LED(13)

# To make the LED switch on, type the following and press Enter:
led.on()

time.sleep(3)
# To make it switch off you can type:
led.off()