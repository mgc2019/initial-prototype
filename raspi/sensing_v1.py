# authors: Aiden Low Yew Woei

# constants
SPEED_OF_SOUND = 343000

# This python script makes use of four ultrasound-vibration sensors.

from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
from time import sleep, time

# front sensing control gpio pins
front_trig = OutputDevice(4)
front_echo = InputDevice(17)
front_motor = PWMOutputDevice(14)

sleep(1)

print("Set-up input and output devices")

def get_pulse_time(trig, echo):
    trig.on()
    # send a burst of ultrasound for 10 microsends
    sleep(0.00001)
    trig.off()
    
    while echo.is_active == False:
        pulse_start = time()

    while echo.is_active == True:
        pulse_end = time()

    # Let the ultrasound sleep for abit.
    sleep(0.10)

    # pulse_start or pulse_end may occasionally have problems with cycle of trigger
    # and echo on the ultrasound sensor.
    try:
        return pulse_end - pulse_start
    except:
        return 0.02

# calculate distance in metres
def calculate_distance(duration):
    distance = SPEED_OF_SOUND * duration / 2
    if distance
