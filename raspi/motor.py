# this script tests your vibration motor wiring by stepping up in intensity from 0 to 100% voltage.

from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
from time import sleep, time

# gpio pin that controls the transistor gate
motor = PWMOutputDevice(14)
value = 0

while value <= 1:
    print("vibrating the motor at value", value)
    motor.value = value
    value = value + 0.1
    sleep(3)
