import pigpio
import pinout
from time import sleep

# connect to the
pi = pigpio.pi()
# loop forever
while True:

    pi.set_servo_pulsewidth(pinout.FRONT_STEERING, 0)    # off
    pi.set_servo_pulsewidth(pinout.REAR_STEERING, 0)    # off
    sleep(1)
    # position anti-clockwise
    pi.set_servo_pulsewidth(pinout.FRONT_STEERING, 600)
    # position anti-clockwise
    pi.set_servo_pulsewidth(pinout.REAR_STEERING, 600)
    sleep(1)
    pi.set_servo_pulsewidth(pinout.FRONT_STEERING, 1500)  # middle
    pi.set_servo_pulsewidth(pinout.REAR_STEERING, 1500)  # middle
    sleep(1)
    pi.set_servo_pulsewidth(pinout.FRONT_STEERING, 2300)  # position clockwise
    pi.set_servo_pulsewidth(pinout.REAR_STEERING, 2300)  # position clockwise
    sleep(1)
