#***** Manually controlling the LED *****#

# Create a new file by clicking New.
# Save the new file by clicking Save. Save the file as gpio_control.py.
# Save and run your program. When you push the button,
#    the LED should come on for three seconds.

from gpiozero import LED, Button
from time import sleep

led = LED(13)
button = Button(4)

button.wait_for_press()
led.on()
sleep(3)
led.off()