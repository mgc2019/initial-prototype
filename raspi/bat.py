# authors: Aiden Low Yew Woei

# This python script uses the ultrasound sensor to calculate distance.
# it also includes a script that generates a vibration setting for the vibration motor.

from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
from time import sleep, time

# ultrasound gpio pins
trig = OutputDevice(4)
echo = InputDevice(17)

# pin to control the vibration motor with pulse-width modulation
motor = PWMOutputDevice(14)

sleep(2)

print("Set-up input and output devices")

def get_pulse_time():
    trig.on()
    # send a burst of ultrasound for 10 microseconds
    sleep(0.00001)
    trig.off()
    other_start_time = time()

    while echo.is_active == False:
        pulse_start = time()

    while echo.is_active == True:
        pulse_end = time()
    
    # Let the ultrasound sleep for abit?
    sleep(0.10)
    try:
        return pulse_end - pulse_start
    except:
        return 0.02


# calculate distance in metres
def calculate_distance(duration):
    speed = 34300
    distance = speed * duration / 2
    return distance

def calculate_vibration(distance):
    vibration = (((distance - 0.02) * -1) / (3 - 0.02)) + 1
    print("vibration is: ", vibration)
    return vibration

while True:
    duration = get_pulse_time()
    distance = calculate_distance(duration)
    print(distance)
    
