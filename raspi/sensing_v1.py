"""Environment sensing script for the blind, version one.

This python script is written modularly and allows the use of
multiple ultrasound-vibration sensors.

Multithreading is used to minimise downtime between each ultrasound detection loop.

Why multithreading instead of multiprocessing?
    Multithreading has lower overhead. All threads share the same memory space.
    No new ones have to be allocated and managed for new commands.
    The above also means that there won't be issues controlling different GPIO
    pins tied to global variables, as compared to using processes which will
    operate on a different memory.

Todo:
    * implement threads for all other directions in line with prototype.
    * decide on feedback algorithm for ceiling feedback.
"""

from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
from math import e
from threading import Thread
from time import sleep, time

# constants
SPEED_OF_SOUND_CM = 34300
ULTRASOUND_MAX_RANGE = 400
ULTRASOUND_MIN_RANGE = 2

# see wolfram alpha for the decay curve.
VIBRATION_EXPONENTIAL_DECAY_CONSTANT = 200


# front sensing control gpio pins
front_trig = OutputDevice(4)
front_echo = InputDevice(17)
front_motor = PWMOutputDevice(14)

sleep(1)

print("Set-up input and output devices")

def get_pulse_time(trig, echo):
    """Find the time of flight using ultrasound.
    
    Keyword arguments:
    trig -- the GPIO pin controlling the ultrasound trigger
    echo -- the GPIO pin that gives the return signal of the reflected echo

    An ultrasound burst of 10 microseconds is used.
    """
    
    # send the ultrasound burst
    trig.on()
    sleep(0.00001)
    trig.off()
    
    # calculate time of flight
    while echo.is_active == False:
        pulse_start = time()

    while echo.is_active == True:
        pulse_end = time()

    # Let the ultrasound sleep to 
    sleep(0.10)

    # pulse_start or pulse_end may occasionally have problems with cycle of trigger
    # and echo on the ultrasound sensor.
    try:
        return pulse_end - pulse_start
    except:
        return 0.02

def calculate_distance(duration):
    """Calculates distance and returns it in centimetres"""
    distance = SPEED_OF_SOUND_CM * duration / 2

    # accounting for ultrasound time of flight range errors
    if distance > ULTRASOUND_MAX_RANGE:
        return ULTRASOUND_MAX_RANGE
    if distance < ULTRASOUND_MIN_RANGE:
        return ULTRASOUND_MIN_RANGE
    
    return distance

# precondition: distance must be between ULTRASOUND_MIN_RANGE and ULTRASOUND_MAX_RANGE
def calculate_vibration(distance):
    """Calculates the vibration intensity for the vibration motor.

    Preconditions:
    distance -- must be in centimetres
    between ULTRASOUND_MIN_RANGE and ULTRASOUND_MAX_RANGE

    An exponential decay formula is used for a stronger feedback response
    the closer objects are.
    """

    vibration = e ** (-distance / VIBRATION_EXPONENTIAL_DECAY_CONSTANT)
    return vibration

def motor_ultrasound_pair_driver(trig, echo, motor):
    """Drives an ultrasound-motor pair."""
    while True:
        duration = get_pulse_time(trig, echo)
        distance = calculate_distance(duration)
        vibration_value = calculate_vibration(distance)
        print("vibration is: ", vibration_value)
        try:
            motor.value = vibration_value
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':

    front_detection = Thread(target=motor_ultrasound_pair_driver, 
                    args=(front_trig, front_echo, front_motor))
    front_detection.start()

