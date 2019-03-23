# list of all functions in SMBus library can be found at 
# http://wiki.erazor-zone.de/wiki:linux:python:smbus:doc
from smbus import SMBus
b = SMBus(1) # instantiate I2C bus 1 for the raspberry pi
# addresses from datasheet for different parts of the sensor
mag_addy = 0x1c
acc_addy = 0x6a
gyr_addy = 0x6a

# complete list of register addresses on pages 38-40 of LSM9DS1 datasheet
# 0x18 = X axis gyroscope Low value
# 0x19 = X axis gyroscope High value
gyro_x_L = b.read_byte_data(gyr_addy, 0x18)
gyro_y_L = b.read_byte_data(gyr_addy, 0x1A)
gyro_z_L = b.read_byte_data(gyr_addy, 0x1C)
print("gyro_x_L =", gyro_x_L, "\tgyro_y_L =", gyro_y_L, "\tgryo_z_L =", gyro_z_L)