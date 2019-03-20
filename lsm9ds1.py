# list of all functions in SMBus library can be found at 
# http://wiki.erazor-zone.de/wiki:linux:python:smbus:doc
from smbus import SMBus
b = SMBus(1) # instantiate I2C bus 1 for the raspberry pi
# addresses from datasheet for different parts of the sensor
mag_addy = 0x1e
acc_addy = 0x6b
gyr_addy = 0x6b

# complete list of register addresses on pages 38-40 of LSM9DS1 datasheet
# 0x18 = X axis gyroscope Low value
# 0x19 = X axis gyroscope High value
gyro_x = ( b.read_byte_data(gyr_addy, 0x19) - b.read_byte_data(gyr_addy, 0x18) ) / 2
gyro_y = ( b.read_byte_data(gyr_addy, 0x1B) - b.read_byte_data(gyr_addy, 0x1A) ) / 2
gyro_z = ( b.read_byte_data(gyr_addy, 0x1D) - b.read_byte_data(gyr_addy, 0x1C) ) / 2
print("gyro_x =", gyro_x, "\tgyro_y =", gyro_y, "\tgryo_z =", gyro_z)