from gpiozero import LED
from time import sleep

red = LED(17)
yellow = LED(27)

while True:
    red.on()
    yellow.off()
    sleep(1)
    red.off()
    yellow.on()
    sleep(1)
