"""
   module:: communication
   :synopsis: Exceptions raised by serial interfaces.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""

class SerialConnectionError(Exception):
    """Error handling for serial interface connections.
    """

    def __init__(self, message):
        """Initializes serial connection error exception.
        
        :param message: Exception message
        :type message: string
        """
        self.message = message
        super(SerialConnectionError, self).__init__(message)
