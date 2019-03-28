# ported from "https://github.com/adafruit/Adafruit_CircuitPythonconst_9oF.git"

from smbus import SMBus
import time

# Internal constants and register values:
const_9oF = {
    "ADDRESS_XLG"            : 0x6B,
    "ADDRESS_MAG"            : 0x1E,
    "XG_ID"                  : 0b01101000,
    "MAG_ID"                 : 0b00111101,
    "ACCEL_MG_LSB_2G"        : 0.061,
    "ACCEL_MG_LSB_4G"        : 0.122,
    "ACCEL_MG_LSB_8G"        : 0.244,
    "ACCEL_MG_LSB_16G"       : 0.732,
    "MAG_MGAUSS_4GAUSS"      : 0.14,
    "MAG_MGAUSS_8GAUSS"      : 0.29,
    "MAG_MGAUSS_12GAUSS"     : 0.43,
    "MAG_MGAUSS_16GAUSS"     : 0.58,
    "GYRO_DPS_DIGIT_245DPS"  : 0.00875,
    "GYRO_DPS_DIGIT_500DPS"  : 0.01750,
    "GYRO_DPS_DIGIT_2000DPS" : 0.07000,
    "TEMP_LSB_DEGREE_CELSIUS": 8, # 1°C = 8, 25° = 200, etc.
    "WHO_AM_I_XG"   : 0x0F,
    "CTRL_REG1_G"   : 0x10,
    "CTRL_REG2_G"   : 0x11,
    "CTRL_REG3_G"   : 0x12,
    "TEMP_OUT_L"    : 0x15,
    "TEMP_OUT_H"    : 0x16,
    "STATUS_REG"    : 0x17,
    "OUT_X_L_G"     : 0x18,
    "OUT_X_H_G"     : 0x19,
    "OUT_Y_L_G"     : 0x1A,
    "OUT_Y_H_G"     : 0x1B,
    "OUT_Z_L_G"     : 0x1C,
    "OUT_Z_H_G"     : 0x1D,
    "CTRL_REG4"     : 0x1E,
    "CTRL_REG5_XL"  : 0x1F,
    "CTRL_REG6_XL"  : 0x20,
    "CTRL_REG7_XL"  : 0x21,
    "CTRL_REG8"     : 0x22,
    "CTRL_REG9"     : 0x23,
    "CTRL_REG10"    : 0x24,
    "OUT_X_L_XL"    : 0x28,
    "OUT_X_H_XL"    : 0x29,
    "OUT_Y_L_XL"    : 0x2A,
    "OUT_Y_H_XL"    : 0x2B,
    "OUT_Z_L_XL"    : 0x2C,
    "OUT_Z_H_XL"    : 0x2D,
    "WHO_AM_I_M"    : 0x0F,
    "CTRL_REG1_M"   : 0x20,
    "CTRL_REG2_M"   : 0x21,
    "CTRL_REG3_M"   : 0x22,
    "CTRL_REG4_M"   : 0x23,
    "CTRL_REG5_M"   : 0x24,
    "STATUS_REG_M"  : 0x27,
    "OUT_X_L_M"     : 0x28,
    "OUT_X_H_M"     : 0x29,
    "OUT_Y_L_M"     : 0x2A,
    "OUT_Y_H_M"     : 0x2B,
    "OUT_Z_L_M"     : 0x2C,
    "OUT_Z_H_M"     : 0x2D,
    "CFG_M"         : 0x30,
    "INT_SRC_M"     : 0x31,
    "SENSORS_GRAVITY_STANDARD"  : 9.80665,
    # User facing constants/module globals.
    "XL_RANGE_2G"   : (0b00 << 3),
    "XL_RANGE_16G"  : (0b01 << 3),
    "XL_RANGE_4G"   : (0b10 << 3),
    "XL_RANGE_8G"   : (0b11 << 3),
    "M_GAIN_4GAUSS" : (0b00 << 5), # +/- 4 gauss
    "M_GAIN_8GAUSS" : (0b01 << 5),  # +/- 8 gauss
    "M_GAIN_12GAUSS": (0b10 << 5),  # +/- 12 gauss
    "M_GAIN_16GAUSS": (0b11 << 5),  # +/- 16 gauss
    "G_SCALE_245DPS": (0b00 << 3),  # +/- 245 degrees/s rotation
    "G_SCALE_500DPS": (0b01 << 3),  # +/- 500 degrees/s rotation
    "G_SCALE_2000DPS": (0b11 << 3)  # +/- 2000 degrees/s rotation
}

def _twos_comp(val, bits):
    # Convert an unsigned integer in 2's compliment form of the specified bit
    # length to its signed integer value and return it.
    if val & (1 << (bits - 1)) != 0:
        return val - (1 << bits)
    return val


class LSM9DS1:
    """Driver for the LSM9DS1 accelerometer, magnetometer, gyroscope."""

    def __init__(self):
        # Class-level buffer for reading and writing data with the sensor.
        # This reduces memory allocations but means the code is not re-entrant or
        # thread safe!
        self.buf = bytearray(6)
        self.b = SMBus(1) # instantiate I2C bus 1 for the raspberry pi
        
        # Check ID registers.
        if self.b.read_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["WHO_AM_I_XG"]) != const_9oF["_XG_ID"] or self.b.read_byte_data(const_9oF["ADDRESS_MAG"], const_9oF["WHO_AM_I_M"]) != const_9oF["MAG_ID"]:
            raise RuntimeError('Could not find LSM9DS1, check wiring!')

        # soft reset & reboot accel/gyro
        self.b.write_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["CTRL_REG8"], 0x05)
        # soft reset & reboot magnetometer
        self.b.write_byte_data(const_9oF["ADDRESS_MAG"], const_9oF["CTRL_REG2_M"], 0x0C)
        time.sleep(0.01)
        # enable gyro continuous
        self.b.write_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["CTRL_REG1_G"], 0xC0) # on XYZ
        # Enable the accelerometer continous
        self.b.write_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["CTRL_REG5_XL"], 0x38)
        self.b.write_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["CTRL_REG6_XL"], 0xC0)
        # enable mag continuous
        self.b.write_byte_data(const_9oF["ADDRESS_MAG"], const_9oF["CTRL_REG3_M"], 0x00)
        # Set default ranges for the various sensors
        self._accel_mg_lsb = const_9oF["ACCEL_MG_LSB_2G"]
        self._mag_mgauss_lsb = const_9oF["MAG_MGAUSS_4GAUSS"]
        self._gyro_dps_digit = const_9oF["GYRO_DPS_DIGIT_245DPS"]
        self.accel_range = const_9oF["XL_RANGE_2G"]
        self.mag_gain = const_9oF["M_GAIN_4GAUSS"]
        self.gyro_scale = const_9oF["G_SCALE_245DPS"]

    def get_accel_range(self):
        """The accelerometer range.  Must be a value of:
          - XL_RANGE_2G
          - XL_RANGE_4G
          - XL_RANGE_8G
          - XL_RANGE_16G
        """
        reg = self.b.read_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["CTRL_REG6_XL"])
        return (reg & 0b00011000) & 0xFF

    def set_accel_range(self, val):
        if const_9oF.get(val) != None:
            val = const_9oF.get(val)
        else: 
            print('"', val, '" is not defined', sep = '')
            return
        reg = self.get_accel_range()
        reg |= val
        self.b.write_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["CTRL_REG6_XL"], reg)
        if val == const_9oF["XL_RANGE_2G"]:
            self._accel_mg_lsb = const_9oF["ACCEL_MG_LSB_2G"]
        elif val == const_9oF["XL_RANGE_4G"]:
            self._accel_mg_lsb = const_9oF["ACCEL_MG_LSB_4G"]
        elif val == const_9oF["XL_RANGE_8G"]:
            self._accel_mg_lsb = const_9oF["ACCEL_MG_LSB_8G"]
        elif val == const_9oF["XL_RANGE_16G"]:
            self._accel_mg_lsb = const_9oF["ACCEL_MG_LSB_16G"]

    def get_mag_gain(self):
        """The magnetometer gain.  Must be a value of:
          - M_GAIN_4GAUSS
          - M_GAIN_8GAUSS
          - M_GAIN_12GAUSS
          - M_GAIN_16GAUSS
        """
        reg = self.b.read_byte_data(const_9oF["ADDRESS_MAG"], const_9oF["CTRL_REG2_M"])
        return (reg & 0b01100000) & 0xFF

    def set_mag_gain(self, val):
        if const_9oF.get(val) != None:
            val = const_9oF.get(val)
        else: 
            print('"', val, '" is not defined', sep = '')
            return
        reg = self.b.read_byte_data(const_9oF["ADDRESS_MAG"], const_9oF["CTRL_REG2_M"])
        reg = (reg & ~(0b01100000)) & 0xFF
        reg |= val
        self.b.write_byte_data(const_9oF["ADDRESS_MAG"], const_9oF["CTRL_REG2_M"], reg)
        if val == const_9oF["M_GAIN_4GAUSS"]:
            self._mag_mgauss_lsb = const_9oF["MAG_MGAUSS_4GAUSS"]
        elif val == const_9oF["M_GAIN_8GAUSS"]:
            self._mag_mgauss_lsb = const_9oF["MAG_MGAUSS_8GAUSS"]
        elif val == const_9oF["M_GAIN_12GAUSS"]:
            self._mag_mgauss_lsb = const_9oF["MAG_MGAUSS_12GAUSS"]
        elif val == const_9oF["M_GAIN_16GAUSS"]:
            self._mag_mgauss_lsb = const_9oF["MAG_MGAUSS_16GAUSS"]

    def get_gyro_scale(self):
        """The gyroscope scale.  Must be a value of:
          - G_SCALE_245DPS
          - G_SCALE_500DPS
          - G_SCALE_2000DPS
        """
        reg = self.b.read_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["CTRL_REG1_G"])
        return (reg & 0b00011000) & 0xFF

    def set_gyro_scale(self, val):
        if const_9oF.get(val) != None:
            val = const_9oF.get(val)
        else: 
            print('"', val, '" is not defined', sep = '')
            return
        reg = self.b.read_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["CTRL_REG1_G"])
        reg = (reg & ~(0b00011000)) & 0xFF
        reg |= val
        self.b.write_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["CTRL_REG1_G"], reg)
        if val == const_9oF["G_SCALE_245DPS"]:
            self._gyro_dps_digit = const_9oF["GYRO_DPS_DIGIT_245DPS"]
        elif val == const_9oF["G_SCALE_500DPS"]:
            self._gyro_dps_digit = const_9oF["GYRO_DPS_DIGIT_500DPS"]
        elif val == const_9oF["G_SCALE_2000DPS"]:
            self._gyro_dps_digit = const_9oF["GYRO_DPS_DIGIT_2000DPS"]

    def read_accel_raw(self):
        """Read the raw accelerometer sensor values and return it as a
        3-tuple of X, Y, Z axis values that are 16-bit unsigned values.  If you
        want the acceleration in nice units you probably want to use the
        accelerometer property!
        """
        # Read the accelerometer
        self.buf = self.b.read_i2c_block_data(const_9oF["ADDRESS_XLG"], const_9oF["OUT_X_L_XL"])
        raw_x, raw_y, raw_z = struct.unpack_from('<hhh', self.buf[0:6])
        return (_twos_comp(raw_x, 16), _twos_comp(raw_y, 16), _twos_comp(raw_z, 16))

    def acceleration(self):
        """The accelerometer X, Y, Z axis values as a 3-tuple of
        m/s^2 values.
        """
        raw = self.read_accel_raw()
        return map(lambda x: x * self._accel_mg_lsb / 1000.0 * const_9oF["SENSORS_GRAVITY_STANDARD"], raw)

    def read_mag_raw(self):
        """Read the raw magnetometer sensor values and return it as a
        3-tuple of X, Y, Z axis values that are 16-bit unsigned values.  If you
        want the magnetometer in nice units you probably want to use the
        magnetometer property!
        """
        # Read the magnetometer
        self.buf = self.b.read_i2c_block_data(const_9oF["ADDRESS_MAG"], const_9oF["OUT_X_L_M"])
        raw_x, raw_y, raw_z = struct.unpack_from('<hhh', self.buf[0:6])
        return (_twos_comp(raw_x, 16), _twos_comp(raw_y, 16), _twos_comp(raw_z, 16))

    def magnetic(self):
        """The magnetometer X, Y, Z axis values as a 3-tuple of
        gauss values.
        """
        raw = self.read_mag_raw()
        return map(lambda x: x * self._mag_mgauss_lsb / 1000.0, raw)

    def read_gyro_raw(self):
        """Read the raw gyroscope sensor values and return it as a
        3-tuple of X, Y, Z axis values that are 16-bit unsigned values.  If you
        want the gyroscope in nice units you probably want to use the
        gyroscope property!
        """
        # Read the gyroscope
        self.buf = self.b.read_i2c_block_data(const_9oF["ADDRESS_XLG"], const_9oF["OUT_X_L_G"])
        raw_x, raw_y, raw_z = struct.unpack_from('<hhh', self.buf[0:6])
        return (_twos_comp(raw_x, 16), _twos_comp(raw_y, 16), _twos_comp(raw_z, 16))

    def gyro(self):
        """The gyroscope X, Y, Z axis values as a 3-tuple of
        degrees/second values.
        """
        raw = self.read_gyro_raw()
        return map(lambda x: x * self._gyro_dps_digit, raw)

    def read_temp_raw(self):
        """Read the raw temperature sensor value and return it as a 12-bit
        signed value.  If you want the temperature in nice units you probably
        want to use the temperature property!
        """
        # Read temp sensor
        return _twos_comp(self.b.read_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["TEMP_OUT_L"]) | ( (self.b.read_byte_data(const_9oF["ADDRESS_XLG"], const_9oF["TEMP_OUT_H"]) & 0x0F) << 8 ), 12)

    def temperature(self):
        """The temperature of the sensor in degrees Celsius."""
        # This is just a guess since the starting point (21C here) isn't documented :(
        # See discussion from:
        #  https://github.com/kriswiner/LSM9DS1/issues/3
        temp = self.read_temp_raw()
        temp = 27.5 + temp/16
        return temp
