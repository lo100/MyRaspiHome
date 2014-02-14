"""
   module:: serial
   :synopsis: Serial interface for Solar Steca Tarom charge controller.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""
import serial

class SerialTarom():

    """RS-232 serial port instance.
    """
    _serial = None
    
    """Interface type.
    """
    INTERFACE_TYPE = 'tarom'

    def __init__(self):
        pass
        
    def open(self):
        """ Opens the RS-232 serial interface to solar charge controller.
        
        :rtype: boolean
        """        
        try:
            self._serial = serial.Serial(port='/dev/ttyAMA0', baudrate=4800)
            self._serial.parity = 'N'
            self._serial.stoppbits = 1
            self._serial.bytesize = 8
            self._serial.flowcontrol = 'off'
        except:
            raise SerialConnectionError('Serial port could not be opened! /dev/ttyAMA0')

    def close(self):
        """ Closes the serial interface.
        
        :rtype: boolean
        """        
        self._serial.close()
        return False
        
    def read(self):
        """Reads from serial interface until end of line detected.
        
        :rtype: string
        """        
        return self._serial.readline()
        
    def write(self, data):
        """Writes data to serial interface.
        
        :param data: The data to be sent
        :type data: string
        :rtype: integer
        """        
        return self._serial.write(data)
