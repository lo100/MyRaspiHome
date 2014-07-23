"""
   module:: common
   :synopsis: Time functions.
   
   moduleauthor:: Bernhard Hari <github@taschenwerkstatt.ch>
"""

def get_offset(time=None, frequency=1):
    """ Calculates the offset for the given time.
    
    :param time: the time string, format: Hour:Minute:Second
    :type time: string
    :rtype: float
    """
    offset = -1

    if time != None:
        time_array = time.split(':')
        offset = ((int(time_array[0]) * 3600) + (int(time_array[1]) * 60) + (int(time_array[2]))) * frequency

    return int(offset)

