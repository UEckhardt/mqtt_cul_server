import sys
import logging
import os
import serial


class Cul(object):
    """Helper class to encapsulate serial communication with CUL device"""

    def __init__(self, serial_port : str, baud_rate=115200, test=False):
        """Create instance with a given serial port"""
        if test:
            self.serial = sys.stderr
            self.test = True
        else:
            self.test = False
            if not os.path.exists(serial_port):
                raise ValueError("cannot find CUL device %s" % serial_port)
            try:
                self.serial = serial.Serial(
                    port=serial_port, baudrate=baud_rate, timeout=1
                )
             
            except serial.SerialException as e:
                logging.error("Could not open CUL device: %s", e)

    def get_cul_version(self) -> str:
        """Get CUL version"""
        self.serial.write("V\n")
        self.serial.flush()
        return self.serial.readline().decode()
    
    def read(self) -> str:
        return self.serial.readline().decode()

    def send_command(self, command_string : bytes) -> None:
        """Send command string to serial port with CUL device"""
        if self.test:
            print(command_string)
        else:
            try:
                self.serial.write(command_string)
                self.serial.flush()
            except serial.SerialException as e:
                logging.error("Could not send command to CUL device %s", e)
                sys.exit(1)


    def listen(self, callback) -> None:
        while True:
            # readline() blocks until message is available
            try:
                message = self.serial.readline().decode("utf-8")
                if message:
                    logging.debug("Received RF message: %s", message)
                callback(message)
            except:
                pass
