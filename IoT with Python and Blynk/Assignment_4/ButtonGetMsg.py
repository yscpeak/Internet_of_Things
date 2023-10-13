#***** Using buttons to get input *****#

# Create a new file by clicking New.
# Save the new file by clicking Save. Save the file as gpio_button.py.
# This time you’ll need the Button class,
#     and to tell it that the button is on pin 2.
# Save and run the code.
# Press the button and your text will appear.

from gpiozero import Button
button = Button(4)
button.wait_for_press()
print('You pushed me')