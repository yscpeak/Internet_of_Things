import time
from grove.adc import ADC

aio = ADC(address=0x08)

while True:
	moisture = aio.read(0)
	print(moisture)
	time.sleep(1)