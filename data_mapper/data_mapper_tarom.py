"""
   module:: data_mapper
   :synopsis: Data mapper for Solar Steca Tarom charge controller.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""

class DataMapperTarom():
    
    """Mapper type.
    """
    MAPPER_TYPE = 'tarom'

    def __init__(self):
        pass
        
    def map(self, data=None):
        """Returns data as a dictionary.
        
        :param data: data returned by charge controller
        :rtype: dictionary
        """
        return self._mapper.map(data)

