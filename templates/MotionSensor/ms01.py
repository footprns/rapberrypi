from gpiozero import MotionSensor, LED
from signal import pause

pir = MotionSensor(17)
led = LED(2)

# pir.when_motion = led.on
# pir.when_no_motion = led.off
while True:
    pir.wait_for_motion()
    print("Motion detected!")
    led.on()

# pause()
