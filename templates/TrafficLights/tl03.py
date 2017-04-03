from gpiozero import Button, LED
from time import sleep
import random

led = LED(17)

player_1 = Button(2)
player_2 = Button(27)

time = random.uniform(5, 10)
sleep(time)
led.on()

while True:
    if player_1.is_pressed:
        print("Winona wins!")
        break
    if player_2.is_pressed:
        print("Papa Iman wins!")
        break

led.off()
