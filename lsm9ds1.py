from smbus import SMBus
b = SMBus(1) # 0 indicates /dev/i2c-0
mag_addy = 0x1e
acc_addy = 0x6b
gyr_addy = 0x6b

b.read_byte_data(0x2f,0x58)

