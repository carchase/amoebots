'''
This file is part of the amoebots project developed under the IPFW Senior Design Capstone.

Created on Nov 1, 2016

View the full repository here https://github.com/car-chase/amoebots
'''

import signal
import inspect
import socket
from main_level import MainLevel

# ***************** Constants used to configure the controller *****************
OPTIONS = {
    'DUMP_MSGS_TO_MAIN': True, # Show all messages in main log output
    'NUMBER_OF_DEVICES': 5, # The number of devices that the controller expects to use
    'BAUD': '115200', # The baud rate used by the com ports
    'TCP_LISTENER_IP': socket.gethostbyname(socket.gethostname()), # Hostname the TCP listener uses
    'TCP_LISTENER_PORT': 5000, # The port the TCP listener uses
    'TCP_LISTENER_START_PORT': 10000 # The starting port for TCP bots to use.
}
# ******************************************************************************

def signal_handler(sig, frame):
    """
    Handles the SIGINT when shutting down the controller.  Ensures that all processes exit
    gracefully.

    Args:
        signal (int): The number indicating the signal that was given.
        frame (frame): The object representing the frame where the signal originated.
    """
    # Get the origin of the SIGINT
    origin = inspect.getouterframes(frame)[0].function

    # Initilize shutdown only once, if the signal is from the main frame
    if __name__ == "__main__" and origin == "main_loop" and sig == 2:
        print("Initiating shutdown")

        MAIN_CONTROLLER.shutdown()

    # Don't do anything for the other frames

# Reigister the SIGINT signal handler
# This captures a ctrl+c and causes the controller to shutdown.
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    MAIN_CONTROLLER = MainLevel(OPTIONS)
    MAIN_CONTROLLER.main_loop()
