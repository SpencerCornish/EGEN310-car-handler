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
    pi.set_servo_pulsewidth(pinout.FRONT_STEERING, 1000)


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
    pi.set_servo_pulsewidth(pinout.FRONT_STEERING, 1000)
    sleep(.1)


# connect to the
pi = pigpio.pi()


redisClient = redis.StrictRedis()

arm()

try:
    while True:
        # 100 Hz data refresh rate
        sleep(.01)
        # if we're connected but we think we aren't update.
        if redisClient.exists("tele.heartbeat"):
            if not isConnected:
                isConnected = True
                print("reconnection event. isConnected changing to True")
        # if we're disconnected but we think we are update
        else:
            if isConnected:
                isConnected = False
                emergency_stop()
                print("disconnection event. isConnected changing to False")

        if isConnected:
            frontMotorSpeed = redisClient.get("move.speed.front")
            rearMotorSpeed = redisClient.get("move.speed.rear")
            steeringAngle = redisClient.get("move.steer")

            if steeringAngle is None:
                steeringAngle = 1000
            if frontMotorSpeed is None:
                frontMotorSpeed = 1000
            if rearMotorSpeed is None:
                rearMotorSpeed = 1000
            # If we have a new front speed from the app
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
    pi.stop()
