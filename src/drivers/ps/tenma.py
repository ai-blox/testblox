from src.drivers.driver_base import DriverBase
import serial
import time
import logging
import sys

class Tenma(DriverBase):

    def __init__(self, config):
        super().__init__(config)

        self.max_voltage = self.check_config_parameter('max_voltage', 24)
        self.serial_port = self.check_config_parameter('serial_port', mandatory=True)

        if (self.max_voltage is None) or (self.serial_port is None):
            self.logger.error('Failed to initialize Tenma driver')
            return

        self.logger.info('Opening port: %s' % self.serial_port)
        try:
            self.serial = serial.Serial(self.serial_port, 9600, timeout=None)
        except serial.SerialException:
            self.logger.error('Failed to open serial port %s' % self.serial_port)
            exit(1)

        self.initialized = True

    def set_voltage(self, voltage):
        if voltage > self.max_voltage:
            self.logger.warning('Try to set a voltage higher then allowed: %.2F' % voltage)
            return
        data = b'VSET1:%.2F' % voltage
        self.send(data)

    def set_current(self, current):
        data = b'ISET1:%.3F' % current
        self.send(data)

    def get_set_voltage(self):
        response = self.read(b'VSET1?')
        return float(response)

    def get_set_current(self):
        response = self.read(b'ISET1?')
        return float(response)

    def get_actual_voltage(self):
        response = self.read(b'VOUT1?')
        return float(response)

    def get_actual_current(self):
        response = self.read(b'IOUT1?')
        return float(response)

    def power_on(self):
        data = b'OUT1'
        self.send(data)

    def power_off(self):
        data = b'OUT0'
        self.send(data)

    def read_device(self):
        response = self.read(b'*IDN?')
        return response

    def is_connected(self):
        device = self.readDevice()
        if device.find('TENMA') < 0 and device.find("KORAD") < 0:
            return False
        else:
            return True

    def send(self, data):
        #self.logger.debug('Send: %s', str(data))
        self.serial.write(data)
        self.serial.flush()
        time.sleep(0.1)

    def read(self, data):
        self.send(data)
        rcvByte = self.serial.in_waiting
        response = self.serial.read(rcvByte)
        #self.logger.debug('Response: ' + response)
        return response


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    psu = Tenma("PS1", 15.00, "/dev/tty.usbmodem001C284402481")
    psu.setVoltage(12.34)
    time.sleep(1)
    psu.power_on()
    time.sleep(1)
    psu.power_off()
    time.sleep(1)
    psu.setVoltage(0.0)