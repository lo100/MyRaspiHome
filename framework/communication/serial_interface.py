"""
   module:: communication
   :synopsis: Wrapper class for serial interfaces.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""

from communication.exceptions import SerialConnectionError
from communication.serial_tarom import SerialTarom

class SerialInterface():

    """Interface instance.
    """
    _interface = None
    
    def __init__(self, interface):
        """Creates wrapped serial interface instance.
        
        :param interface: The serial interface to be wrapped.
        :type interface: string
        :raises: SerialConnectionError
        """
        if interface == 'tarom':
            self._interface = SerialTarom()
        else:
            raise SerialConnectionError('Serial interface not implemented! ' + 
                                        str(interface))
        
    def get_type(self):
        """Returns the initialized interface type
        
        :rtype: string
        """
        return self._interface.INTERFACE_TYPE
        
    def open(self):
        """ Opens the serial interface.
        
        :rtype: boolean
        """
        opened = False
        if self._interface != None:
            self._interface.open()
            opened = True
        return opened
        
    def close(self):
        """ Closes the serial interface.
        
        :rtype: boolean
        """
        closed = False
        if self._interface != None:
            self._interface.close()
            closed = True
        return closed
        
    def read(self):
        """Reads from serial interface until end of line detected.
        
        :rtype: string
        """
        data = None
        if self._interface != None:
            data = self._interface.read()
        return data
        
    def write(self, data=""):
        """Writes data to serial interface.
        
        :param data: The data to be sent
        :type data: string
        :rtype: integer
        """
        number_of_bytes = -1
        if self._interface != None:
            number_of_bytes = self._interface.write(data)
        return number_of_bytes
        
