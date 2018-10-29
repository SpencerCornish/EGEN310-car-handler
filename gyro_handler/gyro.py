
from mpu6050 import mpu6050
import redis
from time import sleep


redisClient = redis.StrictRedis()

sensor = mpu6050(0x68)


while True:
    gyro_dict = sensor.get_accel_data()
    redisClient.set("tele.gyro.x", gyro_dict["x"])
    redisClient.set("tele.gyro.y", gyro_dict["y"])
    redisClient.set("tele.gyro.z", gyro_dict["z"])
    redisClient.set("tele.temp", sensor.get_temp())
    sleep(1)
