'''
Created on Apr 3, 2017

@author: trevb
'''

import cv2
import numpy as np
import math
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
        #options as defined in main.py
        self.options = options
        #stores the number of robots available
        self.length = len(self.options['colors'])
        #blob detection
        self.detector = None
        #dictionary that holds the data to be sent back to the movement_level
        self.robots = {}
        #value to scale the pixel data properly
        self.scaler = 0
        #distance between orange squares
        self.arena_size = self.options['ARENA_SIZE_CM']
        #temporary storage for recieved messages
        self.movement_message = {}
        #number of iterations the camera should do before responding with data
        self.camera_iterations = self.options['CAMERA_ITERATIONS']
        #stores the number of iterations completed
        self.iterations = 0
        #flag that is set to True when a message is recieved and false when a response has been sent
        self.get_message = False
        #left/front translations for grid
        self.translate = {}
        self.cam_input = None
        self.com_input = None
        self.keep_running = True
        self.capture = None
        
    #capture the location and orientation of the arena
    def arenaOrientation(self, points):

        if len(points) != 3:
            return None

        # 0 for first keypoint, 1 for second, 2 for third, -1 for uninitialized
        corner_index = -1
        front_index = -1
        left_index = -1
    
        line1 = np.sqrt((points[0].pt[0] - points[1].pt[0]) * (points[0].pt[0] - points[1].pt[0]) + (points[0].pt[1] - points[1].pt[1]) * (points[0].pt[1] - points[1].pt[1]))
        line2 = np.sqrt((points[1].pt[0] - points[2].pt[0]) * (points[1].pt[0] - points[2].pt[0]) + (points[1].pt[1] - points[2].pt[1]) * (points[1].pt[1] - points[2].pt[1]))
        line3 = np.sqrt((points[0].pt[0] - points[2].pt[0]) * (points[0].pt[0] - points[2].pt[0]) + (points[0].pt[1] - points[2].pt[1]) * (points[0].pt[1] - points[2].pt[1]))
    
        euclidean_distance = [line1, line2, line3]
    
        if euclidean_distance[0] > euclidean_distance[1]:
            front_index = 0
            self.scaler = float(euclidean_distance[1]) / self.arena_size
            if euclidean_distance[0] > euclidean_distance[2]:
                corner_index = 2
                left_index = 1
            else:
                corner_index = 1
                left_index = 2
        elif euclidean_distance[1] > euclidean_distance[2]:
            self.scaler = float(euclidean_distance[0]) / self.arena_size
            corner_index = 0
            front_index = 1
            left_index = 2
        else:
            self.scaler = float(euclidean_distance[0]) / self.arena_size
            corner_index = 1
            front_index = 0
            left_index = 2
        
        corner = [points[corner_index].pt[0], points[corner_index].pt[1]]
        front = [points[front_index].pt[0], points[front_index].pt[1]]
        left = [points[left_index].pt[0], points[left_index].pt[1]]
        
        try:
            slope1 = (front[1] - corner[1]) / (front[0] - corner[0])
        except ZeroDivisionError as err:
            angle1 = 0
        else:
            angle1 = math.degrees(-math.atan(slope1))

        try:
            slope2 = (left[1] - corner[1]) / (left[0] - corner[0])
        except ZeroDivisionError as err:
            angle2 = 0
        else:
            angle2 = math.degrees(-math.atan(slope2))
        
        angle = 0
        
        if angle1 > 0:
            if front[1] < corner[1]:
                angle1 += 270
            else:
                angle1 += 90
        else:
            if front[1] < corner[1]:
                angle1 = 90 + angle1
            else:
                angle1 = 270 + angle1
                
        if angle2 > 0:
            if left[1] < corner[1]:
                angle2 += 270
            else:
                angle2 += 90
        else:
            if left[1] < corner[1]:
                angle2 = 90 + angle2
            else:
                angle2 = 90 + 270
                
        if angle1 > angle2:
            angle2, angle1 = angle1, angle2
            front, left = left, front
            
        if angle2 > 225:
            if angle1 < 135:
                angle = angle2
                front, left = left, front
            else:
                angle = angle1
        else:
            angle = angle1
        
        center = [(front[0] + left[0]) / 2, (front[1] + left[1]) / 2]
        
        goal = [center[0], center[1], angle]
        
        matrix = [[math.cos(math.radians(angle)), math.sin(math.radians(angle))], [-math.sin(math.radians(angle)), math.cos(math.radians(angle))]]

        front[0] -= center[0]
        left[0] -= center[0]
        front[1] -= center[1]
        left[1] -= center[1]

        front[0] = (front[0] * matrix[0][0]) + (front[1] * matrix[0][1])
        front[1] = (front[0] * matrix[1][0]) + (front[1] * matrix[1][1])
        left[0] = (left[0] * matrix[0][0]) + (left[1] * matrix[0][1])
        left[1] = (left[0] * matrix[1][0]) + (left[1] * matrix[1][1])

        front[0] += center[0]
        left[0] += center[0]
        front[1] += center[1]
        left[1] += center[1]
        
        self.translate['front'] = front
        self.translate['left'] = left

        return goal
        
    #capture the location and orientation of the robots
    def orientation(self, points, orange):
    
        # 0 for first keypoint, 1 for second, 2 for third, -1 for uninitialized
        corner_index = -1
        front_index = -1
        left_index = -1

        
        line1 = np.sqrt((points[0].pt[0] - points[1].pt[0]) * (points[0].pt[0] - points[1].pt[0]) + (points[0].pt[1] - points[1].pt[1]) * (points[0].pt[1] - points[1].pt[1]))
        line2 = np.sqrt((points[1].pt[0] - points[2].pt[0]) * (points[1].pt[0] - points[2].pt[0]) + (points[1].pt[1] - points[2].pt[1]) * (points[1].pt[1] - points[2].pt[1]))
        line3 = np.sqrt((points[0].pt[0] - points[2].pt[0]) * (points[0].pt[0] - points[2].pt[0]) + (points[0].pt[1] - points[2].pt[1]) * (points[0].pt[1] - points[2].pt[1]))
        
        euclidean_distance = [[line1], [line2], [line3]]
        
        if euclidean_distance[0] > euclidean_distance[1]:
            front_index = 0
            if euclidean_distance[0] > euclidean_distance[2]:
                corner_index = 2
                left_index = 1
            else:
                corner_index = 1
                left_index = 2
        elif euclidean_distance[1] > euclidean_distance[2]:
            corner_index = 0
            front_index = 1
            left_index = 2
        else:
            corner_index = 1
            front_index = 0
            left_index = 2
        
        corner = [points[corner_index].pt[0], points[corner_index].pt[1]]
        front = [points[front_index].pt[0], points[front_index].pt[1]]
        left = [points[left_index].pt[0], points[left_index].pt[1]]
        
        try:
            slope1 = (front[1] - corner[1]) / (front[0] - corner[0])
        except ZeroDivisionError as err:
            angle1 = 0
        else:
            angle1 = math.degrees(-math.atan(slope1))

        try:
            slope2 = (left[1] - corner[1]) / (left[0] - corner[0])
        except ZeroDivisionError as err:
            angle2 = 0
        else:
            angle2 = math.degrees(-math.atan(slope2))
        
        angle = 0
        
        if angle1 > 0:
            if front[1] < corner[1]:
                angle1 += 270
            else:
                angle1 += 90
        else:
            if front[1] < corner[1]:
                angle1 = 90 + angle1
            else:
                angle1 = 270 + angle1
                
        if angle2 > 0:
            if left[1] < corner[1]:
                angle2 += 270
            else:
                angle2 += 90
        else:
            if left[1] < corner[1]:
                angle2 = 90 + angle2
            else:
                angle2 = 90 + 270
                
        if angle1 > angle2:
            angle2, angle1 = angle1, angle2
            front, left = left, front
            
        if angle2 > 225:
            if angle1 < 135:
                angle = angle2
                front, left = left, front
            else:
                angle = angle1
        else:
            angle = angle1
        
        center = [(front[0] + left[0]) / 2, (front[1] + left[1]) / 2]
        
        goal = [center[0], center[1], 360 - angle]
        
        x = goal[0] - orange[0]
        y = goal[1] - orange[1]
        goal[2] -= orange[2]
        if goal[2] < 0:
            goal[2] += 360
        elif goal[2] >= 360:
            goal[2] -= 360
        
        matrix = [[math.cos(math.radians(orange[2])), math.sin(math.radians(orange[2]))], [-math.sin(math.radians(orange[2])), math.cos(math.radians(orange[2]))]]
        goal[0] = (x * matrix[0][0]) + (y * matrix[0][1])
        goal[1] = (x * matrix[1][0]) + (y * matrix[1][1])
        
        goal[0] += orange[0]
        goal[1] += orange[1]


        goal[1] -= self.translate['front'][1]
        goal[0] -= self.translate['left'][0]


        dic = {}
        dic['x'] = goal[0] / self.scaler
        dic['y'] = goal[1] / self.scaler
        dic['heading'] = goal[2]

        return dic
        
    def blobDetector(self):
        blobParams = cv2.SimpleBlobDetector_Params()
        blobParams.filterByColor = True
        blobParams.blobColor = 255
        blobParams.filterByArea = True
        blobParams.minArea = 10
        blobParams.filterByCircularity = False
        blobParams.filterByConvexity = False
        blobParams.filterByInertia = False
        return cv2.SimpleBlobDetector_create(blobParams)
        

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
        self.detector = self.blobDetector()

        self.com_input.put(Message('CAM_PROCESS', 'MAIN_LEVEL', 'info', {
            'message': 'CAM_PROCESS is running'
        }))

        while self.keep_running:

            if self.get_message:
                if self.iterations == 0:
                    self.process_movement(self.movement_message)
                    self.get_message = False
                    self.movement_message = None
                else:
                    self.iterations -= 1

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
                        self.get_message = True
                        self.robots = {}
                        self.movement_message = message
                        self.iterations = self.camera_iterations

            success, img = self.capture.read()

            # Failed to read from the camera
            if not success:
                self.com_input.put(Message('CAM_PROCESS', 'MAIN_LEVEL', 'failure', {
                    'message': "Could not read from the camera, killing camera process"
                }))
                self.keep_running = False
                break

            #image processing
            img_with_keypoints = img
            orange = []
            locations = []
            
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            for index in range(self.length):
                mask = cv2.inRange(hsv, tuple(self.options['minColors'][index]), tuple(self.options['maxColors'][index]))
                res = cv2.bitwise_and(img, img, mask= mask)
                keypoints = self.detector.detect(mask)
                
                #checks if the index is for the arena then checks if there
                #are enough points to calculate the orientation of the arena
                #if there are not, set index to the length to break out of this
                #loop because robot positions can't be calculated
                img_with_keypoints = cv2.drawKeypoints(img_with_keypoints, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

                if index == 0:
                    orange = self.arenaOrientation(keypoints)
                    if  orange is None:
                        index = self.length

                else:
                    #if there are 3 keypoints then calculate the location
                    #and orientation for that object
                    if len(keypoints) == 3 and orange is not None:
                        self.robots[self.options['colors'][index]] = self.orientation(keypoints, orange)

            cv2.imshow('frame', img_with_keypoints)
            cv2.waitKey(1)

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

        if message.data['command'] == 90:
            # Send back the sensor camera data
            self.com_input.put(Message('CAM_PROCESS', 'MOV_LEVEL', 'response', {
                'content': 'robot-info', 
                'data': { 'type': 'camera' }
            }))

        elif message.data['command'] == 91:
            # Send back the sensor camera data
            self.com_input.put(Message('CAM_PROCESS', 'MOV_LEVEL', 'response', {
                'content': 'sensor-camera', 
                'data': self.robots
            }))
