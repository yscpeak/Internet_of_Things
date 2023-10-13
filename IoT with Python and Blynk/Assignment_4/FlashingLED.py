#***** Flashing an LED *****#

# Create a new file by clicking New.
# Save the new file by clicking Save. Save the file as gpio_led.py

# Save the file and run the code with by clicking on Run.
# The LED should be flashing on and off. To exit the program click Stop.

from gpiozero import LED
from time import sleep

led = LED(13)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)