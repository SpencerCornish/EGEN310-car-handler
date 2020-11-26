#!/usr/bin/python3

import pigpio
import pinout
import redis
from time import sleep


# global variables
isConnected = False
frontSpeed = 1000
rearSpeed = 1000
steerAngle = 1000


def emergency_stop():
    pi.set_servo_pulsewidth(pinout.FRONT_MOTOR, 1000)
    pi.set_servo_pulsewidth(pinout.REAR_MOTOR, 1000)
    pi.set_servo_pulsewidth(pinout.FRONT_STEERING, 1500)


def arm():
    # Arm the ESCs
    pi.set_servo_pulsewidth(pinout.FRONT_MOTOR, 0)
    pi.set_servo_pulsewidth(pinout.REAR_MOTOR, 0)
    sleep(.1)
    pi.set_servo_pulsewidth(pinout.FRONT_MOTOR, 2000)
    pi.set_servo_pulsewidth(pinout.REAR_MOTOR, 2000)
    sleep(.1)
    pi.set_servo_pulsewidth(pinout.FRONT_MOTOR, 1000)
    pi.set_servo_pulsewidth(pinout.REAR_MOTOR, 1000)
    sleep(.1)
    # Zero the servos
    pi.set_servo_pulsewidth(pinout.FRONT_STEERING, 1500)
    sleep(.1)


# connect to the
pi = pigpio.pi()


redisClient = redis.StrictRedis()
redisClient.publish()

arm()

try:
    while True:
        # 100 Hz data refresh rate
        sleep(.01)
        # if we're connected but we think we aren't, update.
        if redisClient.exists("tele.heartbeat"):
            if not isConnected:
                isConnected = True
                print("reconnected to control app")
        # if we're disconnected but we think we are, update
        else:
            if isConnected:
                isConnected = False
                emergency_stop()
                print("disconnected from control app")

        if isConnected:
            frontMotorSpeed = redisClient.get("move.speed.front")
            rearMotorSpeed = redisClient.get("move.speed.rear")
            steeringAngle = redisClient.get("move.steer")
            #  Initialize defaults, if they haven't been set by the app yet
            if steeringAngle is None:
                steeringAngle = 1500
            if frontMotorSpeed is None:
                frontMotorSpeed = 1000
            if rearMotorSpeed is None:
                rearMotorSpeed = 1000

            # If we have a new speed/steering setting from the app
            if frontMotorSpeed != frontSpeed:
                frontSpeed = frontMotorSpeed
                pi.set_servo_pulsewidth(pinout.FRONT_MOTOR, frontSpeed)
            if rearMotorSpeed != rearSpeed:
                rearSpeed = rearMotorSpeed
                pi.set_servo_pulsewidth(pinout.REAR_MOTOR, rearSpeed)
            if steeringAngle != steerAngle:
                steerAngle = steeringAngle
                pi.set_servo_pulsewidth(pinout.FRONT_STEERING, steerAngle)
finally:
    # Reset everything to default
    pi.set_servo_pulsewidth(pinout.FRONT_MOTOR, 0)
    pi.set_servo_pulsewidth(pinout.REAR_MOTOR, 0)
    pi.set_servo_pulsewidth(pinout.FRONT_STEERING, 0)
    pi.stop()
