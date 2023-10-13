#***** Making a switch *****#

# Save and run the program. Now when the button is pressed, the LED
#     will light up. It will turn off again when the button is released.

from gpiozero import LED, Button
from signal import pause

led = LED(13)
button = Button(4)

button.when_pressed = led.on
button.when_released = led.off

pause()