'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Nov 1, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

from serial import Serial
from message import Message

class COMListener:
    """
    Checks a COM port to see if there is a robot available.  If a robot is available, it
    sends an "add" message to the communication level.

    Args:
        options (dict): The dictionary containing the program settings.
    """

    def __init__(self, options):
        self.options = options

    def com_listener_main(self, address, com_input):
        """
        The main function of the COM listener.  The function tries to ping a robot on the com port,
        if it gets a response, then it tells the controller to add the robot.

        Args:
            address (str): The COM port to check for robots.
            com_input (Queue): The queue for sending messages to the communication level.
        """

        com_input.put(Message(address, 'MAIN_LEVEL', 'info', {
            'message': 'COM_LISTENER started on port ' + address
        }))

        try:
            with Serial(address, self.options["BAUD"], timeout=10) as port:

                # Call the ping command
                port.write(bytes("99 0 0", "utf-8"))

                response = port.readline().strip().decode()

                if not response == '':
                    # Clean out the buffer
                    while port.inWaiting() > 0:
                        response = response + port.read(port.inWaiting()).strip().decode()

                    com_input.put(Message(address, 'COM_LEVEL', 'command', {
                        'directive': 'add',
                        'message': 'Added a robot on port ' + address
                    }))
                else:
                    com_input.put(Message(address, 'COM_LEVEL', 'command', {
                        'directive': 'failure',
                        'message': 'Could not add robot on port ' + address
                    }))

                port.close()

        except Exception as err:
            # Catch any exceptions and return them as "failures" so the movement level can clean up.
            com_input.put(Message(address, 'COM_LEVEL', 'command', {
                'directive': 'failure',
                'message': 'Failed with the following error: ' + str(err)
            }))

            # Raise the exception again so it isn't lost.
            raise

        return 0
