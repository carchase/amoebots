'''
Created on Apr 3, 2017

@author: trevb
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

i = 0
cap = cv2.VideoCapture(1)  # @UndefinedVariable 0 if no built in camera, 1 if there is

def black_white_conversion(img):
    for row in img:
        for column in row:
            if column > 0 and column < 255:
                print(column)
                
            if column >= 128:
                column = 255
            else:
                column = 0
                
    return img


while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)  # @UndefinedVariable
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # @UndefinedVariable
        break
    
    if cv2.waitKey(1) & 0xFF == ord('c'):  # @UndefinedVariable
        img = frame
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # @UndefinedVariable
        colors = ['Green', 'Purple', 'Yellow', 'Red', 'Blue', 'Light Blue']
        colorMin = [[48, 37, 1], [113, 85, 153], [43, 0, 177], [155, 37, 117], [108, 119, 170], [90, 102, 228]]
        colorMax = [[83, 255, 255], [134, 149, 202], [84, 41, 190], [179, 251, 255], [116, 183, 218], [114, 181, 255]]
        bw_imgs = []
        
        index = 0
        while index < 6:
            
            mask = cv2.inRange(hsv, tuple(colorMin[index]), tuple(colorMax[index]))  # @UndefinedVariable
            res = cv2.bitwise_and(img, img, mask= mask)  # @UndefinedVariable
            bw_imgs.append(mask)
            
            index += 1
        
        for num in range(6):
            img_name = str(colors[num]) + str(i) + '.png'
            cv2.imwrite(img_name, bw_imgs[num])  # @UndefinedVariable
            
        i += 1
        
        
        blobParams = cv2.SimpleBlobDetector_Params()  # @UndefinedVariable
        
        blobParams.filterByColor = True
        blobParams.blobColor = 255
        blobParams.filterByArea = True
        blobParams.minArea = 10
        #blobParams.maxArea = 50
        blobParams.filterByCircularity = False
        blobParams.filterByConvexity = False
        blobParams.filterByInertia = False
         
        detector = cv2.SimpleBlobDetector_create(blobParams)  # @UndefinedVariable
        
        keypoints = [[],[],[],[],[],[]]
        img_with_keypoints = img
        j = 0
        for im in bw_imgs:
            keypoints[j] = detector.detect(im)
            for points in keypoints[j]:
                print(points.pt)
            img_with_keypoints = cv2.drawKeypoints(img_with_keypoints, keypoints[j], np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # @UndefinedVariable
            # Show keypoints
            cv2.imshow("Keypoints", img_with_keypoints)  # @UndefinedVariable
            j += 1
            
        print('\n')
        
        

    
cap.release()
cv2.destroyAllWindows()  # @UndefinedVariable
