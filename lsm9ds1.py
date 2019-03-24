# list of all functions in SMBus library can be found at 
# http://wiki.erazor-zone.de/wiki:linux:python:smbus:doc
from smbus import SMBus
b = SMBus(1) # instantiate I2C bus 1 for the raspberry pi
# addresses from datasheet for different parts of the sensor
mag = 0x1c
xlg = 0x6a

# complete list of register addresses on pages 38-40 of LSM9DS1 datasheet
reg = {
    # BEGIN ACCELEROMETER/GYROSCOPE REGISTERS
    # Reserved 0x00-0x03
    'ACT_THS':0x04,
    'ACT_DUR':0x05,
    'INT_GEN_CFG_XL':0x06,
    'INT_GEN_THS_X_XL':0x07,
    'INT_GEN_THS_Y_XL':0x08,
    'INT_GEN_THS_Z_XL':0x09,
    'INT_GEN_DUR_XL':0x0a,
    'REFERENCE_G':0x0b,
    'INT1_CTRL':0x0c,
    'INT2_CTRL':0x0d,
    # Reserved 0x0e,
    'WHO_AM_I':0x0f,
    'CTRL_REG1_G':0x10,
    'CTRL_REG2_G':0x11,
    'CTRL_REG3_G':0x12,
    'ORIENT_CFG_G':0x13,
    'INT_GEN_SRC_G':0x14,
    'OUT_TEMP_L':0x15,
    'OUT_TEMP_H':0x16,
    'STATUS_REG_G':0x17,
    'OUT_X_L_G':0x18,
    'OUT_X_H_G':0x19,
    'OUT_Y_L_G':0x1a,
    'OUT_Y_H_G':0x1b,
    'OUT_Z_L_G':0x1c,
    'OUT_Z_H_G':0x1d,
    'CTRL_REG4':0x1e,
    'CTRL_REG5_XL':0x1f,
    'CTRL_REG6_XL':0x20,
    'CTRL_REG7_XL':0x21,
    'CTRL_REG8':0x22,
    'CTRL_REG9':0x23,
    'CTRL_REG10':0x24,
    # Reserved 0x25,
    'INT_GEN_SRC_XL':0x26,
    'STATUS_REG_XL':0x27,
    'OUT_X_L_XL':0x28,
    'OUT_X_H_XL':0x29,
    'OUT_Y_L_XL':0x2a,
    'OUT_Y_H_XL':0x2b,
    'OUT_Z_L_XL':0x2c,
    'OUT_Z_H_XL':0x2d,
    'FIFO_CTRL':0x2e,
    'FIFO_SRC':0x2f,
    'INT_GEN_CFG_G':0x30,
    'INT_GEN_THS_XH_G':0x31,
    'INT_GEN_THS_XL_G':0x32,
    'INT_GEN_THS_YH_G':0x33,
    'INT_GEN_THS_YL_G':0x34,
    'INT_GEN_THS_ZH_G':0x35,
    'INT_GEN_THS_ZL_G':0x36,
    'INT_GEN_DUR_G':0x37,
    # Reserved 0x38-0x7f
    # BEGIN MAGNETOMETER REGISTERS
    # Reserved 0x00-0x04
    'OFFSET_X_REG_L_M':0x05,
    'OFFSET_X_REG_H_M':0x06,
    'OFFSET_Y_REG_L_M':0x07,
    'OFFSET_Y_REG_H_M':0x08,
    'OFFSET_Z_REG_L_M':0x09,
    'OFFSET_Z_REG_H_M':0x0a,
    # Reserved 0x0b-0x0e
    'WHO_AM_I_M':0x0f,
    # Reserved 0x10=0x1f
    'CTRL_REG1_M':0x20,
    'CTRL_REG2_M':0x21,
    'CTRL_REG3_M':0x22,
    'CTRL_REG4_M':0x23,
    'CTRL_REG5_M':0x24,
    # Reserved 0x25-0x26
    'STATUS_REG_M':0x27,
    'OUT_X_L_M':0x28,
    'OUT_X_H_M':0x29,
    'OUT_Y_L_M':0x2a,
    'OUT_Y_H_M':0x2b,
    'OUT_Z_L_M':0x2c,
    'OUT_Z_H_M':0x2d,
    # Reserved 0x2e-0x2f
    'INT_CFG_M':0x30,
    'INT_SRC_M':0x31,
    'INT_THS_L_M':0x32,
    'INT_THS_H_M':0x33
}
# data is split up into 2 bytes, thus the H & L suffix in register names.
# data is organized in little endian format by default
gyro_x = b.read_byte_data(xlg, reg['OUT_X_L_G']) | ( b.read_byte_data(xlg, reg['OUT_X_L_H_G']) << 8 )
gyro_y = b.read_byte_data(xlg, reg['OUT_Y_L_G']) | ( b.read_byte_data(xlg, reg['OUT_Y_L_H_G']) << 8 )
gyro_z = b.read_byte_data(xlg, reg['OUT_Z_L_G']) | ( b.read_byte_data(xlg, reg['OUT_Z_L_H_G']) << 8 )
accel_x = b.read_byte_data(xlg, reg['OUT_X_L_XL']) | ( b.read_byte_data(xlg, reg['OUT_X_L_H_XL']) << 8 )
accel_y = b.read_byte_data(xlg, reg['OUT_Y_L_XL']) | ( b.read_byte_data(xlg, reg['OUT_Y_L_H_XL']) << 8 )
accel_z = b.read_byte_data(xlg, reg['OUT_Z_L_XL']) | ( b.read_byte_data(xlg, reg['OUT_Z_L_H_XL']) << 8 )
mag_x = b.read_byte_data(xlg, reg['OUT_X_L_M']) | ( b.read_byte_data(xlg, reg['OUT_X_H_M']) << 8 )
mag_y = b.read_byte_data(xlg, reg['OUT_Y_L_M']) | ( b.read_byte_data(xlg, reg['OUT_Y_H_M']) << 8 )
mag_z = b.read_byte_data(xlg, reg['OUT_Z_L_M']) | ( b.read_byte_data(xlg, reg['OUT_Z_H_M']) << 8 )
print("gyro_x =", gyro_x, "\tgyro_y =", gyro_y, "\tgryo_z =", gyro_z)
print("accel_x =", accel_x, "\taccel_y =", accel_y, "\taccel_z =", accel_z)
print("mag_x =", mag_x, "\tmag_y =", mag_y, "\tmag_z =", mag_z)
