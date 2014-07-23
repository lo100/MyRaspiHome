"""
   module:: data_mapper
   :synopsis: Exceptions raised by data mapper.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""

class DataMapperError(Exception):
    """Error handling for data mappers.
    """

    def __init__(self, message):
        """Data mapper error exception.
        
        :param message: Exception message
        :type message: string
        """
        self.message = message
        super(DataMapperError, self).__init__(message)
