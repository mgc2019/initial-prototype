# authors: Aiden Low Yew Woei

# This python script makes use of four ultrasound-vibration sensors.

from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
from math import e
from multiprocessing import Process
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
    distance = SPEED_OF_SOUND_CM * duration / 2

    if distance > ULTRASOUND_MAX_RANGE:
        return ULTRASOUND_MAX_RANGE
    if distance < ULTRASOUND_MIN_RANGE:
        return ULTRASOUND_MIN_RANGE
    
    return distance

# precondition: distance must be between ULTRASOUND_MIN_RANGE and ULTRASOUND_MAX_RANGE
def calculate_vibration(distance):
    vibration = e ** (-distance / VIBRATION_EXPONENTIAL_DECAY_CONSTANT)
    return vibration

def motor_ultrasound_pair_driver(trig, echo, motor):
    while True:
        duration = get_pulse_time(trig, echo)
        distance = calculate_distance(duration)
        print(distance)
        vibration_value = calculate_vibration(distance)
        print("vibration is: ", vibration_value)
        try:
            motor.value = vibration_value
            print("hello")
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    proc1 = Process(target=motor_ultrasound_pair_driver,
                    args=(front_trig, front_echo, front_motor))
    proc1.start()
