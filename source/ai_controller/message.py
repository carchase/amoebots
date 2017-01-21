'''
The class that defines messages sent between processes.

Created on Jan 20, 2017
View the full repository here https://github.com/car-chase/amoebots
'''

import json

class Message:

    def __init__(self, origin, destination, category, data ):
        self.origin = origin
        self.destination = destination
        self.category = category
        self.data = data

    def toString(self):
        category = "{:<8}".format((self.category.upper())[:8])
        destination = "{:<17}".format(('To: ' + self.destination.upper())[:17]) 
        source = "{:<19}".format(('From: ' + self.origin.upper())[:19])
        if type(self.data) is dict:
            if(self.data.get("message") != None):
                data = self.data.get("message")
            else:
                data = json.dumps(self.data)
        elif type(self.data) is str:
            data = self.data
        else:
            data = "Bad Data Type"

        return "[" + category + "][" + destination + "][" + source + "] " + data