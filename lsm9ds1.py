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
gyro_x_H = b.read_byte_data(gyr_addy, 0x19)
gyro_y_H = b.read_byte_data(gyr_addy, 0x1B)
gyro_z_H = b.read_byte_data(gyr_addy, 0x1D)
accel_x_L = b.read_byte_data(acc_addy, 0x28)
accel_y_L = b.read_byte_data(acc_addy, 0x29)
accel_z_L = b.read_byte_data(acc_addy, 0x2A)
accel_x_H = b.read_byte_data(acc_addy, 0x2B)
accel_y_H = b.read_byte_data(acc_addy, 0x2C)
accel_z_H = b.read_byte_data(acc_addy, 0x2D)
mag_x_L = b.read_byte_data(mag_addy, 0x28)
mag_y_L = b.read_byte_data(mag_addy, 0x29)
mag_z_L = b.read_byte_data(mag_addy, 0x2A)
mag_x_H = b.read_byte_data(mag_addy, 0x2B)
mag_y_H = b.read_byte_data(mag_addy, 0x2C)
mag_z_H = b.read_byte_data(mag_addy, 0x2D)
print("gyro_x_L =", gyro_x_L, "\tgyro_y_L =", gyro_y_L, "\tgryo_z_L =", gyro_z_L)
print("gyro_x_H =", gyro_x_H, "\tgyro_y_H =", gyro_y_H, "\tgryo_z_H =", gyro_z_H)
print("accel_x_L =", accel_x_L, "\taccel_y_L =", accel_y_L, "\taccel_z_L =", accel_z_L)
print("accel_x_H =", accel_x_H, "\taccel_y_H =", accel_y_H, "\taccel_z_H =", accel_z_H)
print("mag_x_L =", mag_x_L, "\tmag_y_L =", mag_y_L, "\tmag_z_L =", mag_z_L)
print("mag_x_H =", mag_x_H, "\tmag_y_H =", mag_y_H, "\tmag_z_H =", mag_z_H)