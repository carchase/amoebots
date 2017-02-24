'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Jan 20, 2017

View the full repository here: https://github.com/car-chase/amoebots
'''

import json

class Message:
    '''
    The class that defines messages sent between processes.

    Full details are documented here:
    https://github.com/car-chase/amoebots/wiki/Controller-Interprocess-API

    Args:
        origin (str): The level where the interprocess message originated.
        destination (str): The level where the interprocess message is destined.
        category (str): The category of the message.
        data (dict): The dictionary containing the data of the message.

    Attributes:
        origin (str): The level where the interprocess message originated.
        destination (str): The level where the interprocess message is destined.
        category (str): The category of the message.
        data (dict): The dictionary containing the data of the message.
    '''

    def __init__(self, origin, destination, category, data):
        self.origin = origin.upper()
        self.destination = destination.upper()
        self.category = category.lower()
        self.data = data

    def to_string(self):
        """
        Converts the message into a human-readable string.
        """
        category = "{:<8}".format((self.category)[:8])
        destination = "{:<17}".format(('To: ' + self.destination)[:17])
        source = "{:<19}".format(('From: ' + self.origin)[:19])
        if isinstance(self.data, dict):
            if self.data.get("message") != None:
                data = self.data.get("message")
            else:
                data = json.dumps(self.data)
        elif isinstance(self.data, str):
            data = self.data
        else:
            data = str(self.data)

        return "[" + category + "][" + destination + "][" + source + "] " + data
