'''
Created on Apr 3, 2017

@author: trevb
'''

import cv2
import numpy as np
import sys
from message import Message

class CameraProcess:
    """
    Facilitates communication with the arena camera.

    Args:
        options (dict): The dictionary containing the program settings.

    Attributes:
        cam_input (Queue): The queue for receiving messages in the camera process.
        com_input (Queue): The queue for sending messages to the communication level.
        keep_running (bool): Boolean that keeps the main event loop running.
        capture (img): The current image capture of the camera.
    """

    def __init__(self, options):
        self.options = options
        self.cam_input = None
        self.com_input = None
        self.keep_running = True
        self.capture = None
        

    def cam_process_main(self, cam_input, com_input):
        """
        The main function of a cam process.  It waits for a sensor check command and then processes
        the current state of the arena.

        Args:
            com_input (Queue): The queue for sending messages to the communication level.
            cam_input (Queue): The queue for receiving messages in the cam process.
        """

        self.cam_input = cam_input
        self.com_input = com_input
        self.capture = cv2.VideoCapture(self.options['CAMERA_ID'])

        self.com_input.put(Message('CAM_PROCESS', 'MAIN_LEVEL', 'info', {
            'message': 'CAM_PROCESS is running'
        }))

        while self.keep_running:

            # get items from queue until it's empty
            while not self.cam_input.empty():

                message = self.cam_input.get()

                # make sure the message is a Message object
                if isinstance(message, Message):

                    # Appropriately process the message depending on its category
                    if message.category == 'command':
                        self.process_command(message)

                    # check if the message is a movement command
                    elif message.category == 'movement':
                        self.process_movement(message)

            success, frame = self.capture.read()

            # Failed to red from the camera
            if not success:
                self.com_input.put(Message('CAM_PROCESS', 'MAIN_LEVEL', 'failure', {
                    'message': "Could not read from the camera, killing camera process"
                }))
                self.keep_running = False
                break

            # cv2.imshow('Raw Feed', frame)
            cv2.waitKey(1)
            img = frame

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            colors = ['Green', 'Purple', 'Yellow', 'Red', 'Blue', 'Light Blue']
            colorMin = [[48, 37, 1], [113, 85, 153], [43, 0, 177], [155, 37, 117], [108, 119, 170], [90, 102, 228]]
            colorMax = [[83, 255, 255], [134, 149, 202], [84, 41, 190], [179, 251, 255], [116, 183, 218], [114, 181, 255]]
            bw_imgs = []

            length = range(len(colors))
            for index in length:
                mask = cv2.inRange(hsv, tuple(colorMin[index]), tuple(colorMax[index]))
                res = cv2.bitwise_and(img, img, mask= mask)
                bw_imgs.append(mask)

            blobParams = cv2.SimpleBlobDetector_Params()

            blobParams.filterByColor = True
            blobParams.blobColor = 255
            blobParams.filterByArea = True
            blobParams.minArea = 10
            #blobParams.maxArea = 50
            blobParams.filterByCircularity = False
            blobParams.filterByConvexity = False
            blobParams.filterByInertia = False

            detector = cv2.SimpleBlobDetector_create(blobParams)

            keypoints = [[],[],[],[],[],[]]
            img_with_keypoints = img
            j = 0
            for im in bw_imgs:
                keypoints[j] = detector.detect(im)
                img_with_keypoints = cv2.drawKeypoints(img_with_keypoints, keypoints[j], np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                # Show keypoints
                cv2.imshow("Keypoints", img_with_keypoints)
                j += 1

    def process_command(self, message):
        """
        The command processor of the camera process.  It processes messages categorized as
        "commands".

        Args:
            message (Message): The message object to be processed.
        """

        if message.data['directive'] == 'shutdown' and message.origin == 'COM_LEVEL':
            # The level has been told to shutdown.
            self.com_input.put(Message('CAM_PROCESS', 'MAIN_LEVEL', 'info', {
                'message': 'Shutting down CAM_PROCESS'
            }))

            # Kill the windows
            self.capture.release()
            cv2.destroyAllWindows()

            # End the com_level
            self.keep_running = False
            sys.exit()

    def process_movement(self, message):
        """
        The movement processor of the camera process.  It processes messages categorized as
        "movements".

        Args:
            message (Message): The message object to be processed.
        """

        if message.data.command == 91:
            # Send back the sensor camera data
            print("asked for image")
