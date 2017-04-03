from gpiozero import PWMLED
from signal import pause

led = PWMLED(17)
led02 = PWMLED(27)
led.pulse()
led02.pulse()
pause()
