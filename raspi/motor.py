from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
from time import sleep, time

motor = PWMOutputDevice(23)

sleep(1)
print("motor set up")

motor.value = 1

while True:
    motor.on()
