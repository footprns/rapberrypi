from gpiozero import LED
from signal import pause

red = LED(17)
yellow = LED(27)

red.blink()
yellow.blink()

pause()
