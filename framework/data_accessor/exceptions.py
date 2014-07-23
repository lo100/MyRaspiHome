"""
   module:: data_accessor
   :synopsis: Exceptions raised by data accessor.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""

class DataAccessorError(Exception):
    """Error handling for data accessor.
    """

    def __init__(self, message):
        """Initializes data accessor error exception.
        
        :param message: Exception message
        :type message: string
        """
        self.message = message
        super(DataAccessorError, self).__init__(message)
