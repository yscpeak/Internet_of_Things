# import time
# import network
# import webrepl

# def do_connect():
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     print('Connecting to network...')
#     while not wlan.isconnected():
#         wlan.connect('iPhone', '11281128')
#         time.sleep(5)
#     print('Network config:', wlan.ifconfig())

# do_connect()
# webrepl.start()


# Ignore "do_connect:connect:Wifi Internal Error" on Putty.
# The error resolved with the try except statements was preventing your board from working properly. 
# You can choose not to print the error to the screen if it makes you feel better.

import time
import network
import webrepl
 
def do_connect():
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        print('Connecting to network...')
        while not wlan.isconnected():
            try:
                wlan.connect('iPhone', '11281128')
            except Exception as e:
                print(f"do_connect:connect:{e}")
            time.sleep(5)
        print('Network config:', wlan.ifconfig())
    except Exception as e:
        print(f"do_connect:{e}")
 
do_connect()
webrepl.start()