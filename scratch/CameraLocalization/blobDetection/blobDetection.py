'''
Created on Apr 3, 2017

@author: trevb
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

i = 0
cap = cv2.VideoCapture(1)  # @UndefinedVariable

while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)  # @UndefinedVariable
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # @UndefinedVariableq
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
            img_name = str(colors[num]) + str(i) + '.jpeg'
            cv2.imwrite(img_name, bw_imgs[num])  # @UndefinedVariable
            
        i += 1
        
        
#         blobParams = cv2.SimpleBlobDetector_Params()  # @UndefinedVariable
#         
#         blobParams.minThreshold(10)
#         blobParams.maxThreshold(200)
#         blobParams.filterByCircularity = True
#         blobParams.minCircularity = 0.780
#         blobParams.maxCircularity = 0.790
#         blobParams.filterByConvexity = True
#         blobParams.minConvexity = 0.34
#         blobParams.maxConvexity = 0.90
#         
#         detector = cv2.SimpleBlobDetector_create(blobParams)  # @UndefinedVariable
#          
#         keypoints = detector.detect(img)
#         for point in keypoints:
#             print(point, '\n')
#             for loc in point:
#                 print(loc)
#                 print(' ')
#              
#         img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # @UndefinedVariable
#         # Show keypoints
#         cv2.imshow("Keypoints", img_with_keypoints)  # @UndefinedVariable
#         cv2.waitKey(0)  # @UndefinedVariable
        
            

    
cap.release()
cv2.destroyAllWindows()  # @UndefinedVariable