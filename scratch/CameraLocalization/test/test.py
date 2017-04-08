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
        colorMin = [[48, 37, 1], [113, 85, 153], [43, 0, 177], [155, 37, 117], [108, 119, 170], [90, 102, 228]]
        colorMax = [[83, 255, 255], [134, 149, 202], [84, 41, 190], [179, 251, 255], [116, 183, 218], [114, 181, 255]]
        index = 0
        while index < 6:
            
            #decrease minHue
            if cv2.waitKey(1) & 0xFF == ord('s'):  # @UndefinedVariable
                colorMin[index][0] -= 1
                print('ColorMin:')
                print(colorMin[index])
                
            #increase minHue
            if cv2.waitKey(1) & 0xFF == ord('w'):  # @UndefinedVariable
                if colorMin[index][0] < colorMax[index][0]:
                    colorMin[index][0] += 1
                    print('ColorMin:')
                    print(colorMin[index])
                            
            #decrease minSat
            if cv2.waitKey(1) & 0xFF == ord('d'):  # @UndefinedVariable
                colorMin[index][1] -= 1
                print('ColorMin:')
                print(colorMin[index])
                
            #increase minSat
            if cv2.waitKey(1) & 0xFF == ord('e'):  # @UndefinedVariable
                if colorMin[index][1] < colorMax[index][1]:
                    colorMin[index][1] += 1
                    print('ColorMin:')
                    print(colorMin[index])
            
            #decrease minVal
            if cv2.waitKey(1) & 0xFF == ord('f'):  # @UndefinedVariable
                colorMin[index][2] -= 1
                print('ColorMin:')
                print(colorMin[index])
                
            #increase minVal
            if cv2.waitKey(1) & 0xFF == ord('r'):  # @UndefinedVariable
                if colorMin[index][2] < colorMax[index][2]:
                    colorMin[index][2] += 1
                    print('ColorMin:')
                    print(colorMin[index])
                            
            #decrease maxHue
            if cv2.waitKey(1) & 0xFF == ord('g'):  # @UndefinedVariable
                if colorMin[index][0] < colorMax[index][0]:
                    colorMax[index][0] -= 1
                    print('ColorMax:')
                    print(colorMax[index])
                
            #increase maxHue
            if cv2.waitKey(1) & 0xFF == ord('t'):  # @UndefinedVariable
                colorMax[index][0] += 1
                print('ColorMax:')
                print(colorMax[index])
                            
            #decrease maxSat
            if cv2.waitKey(1) & 0xFF == ord('h'):  # @UndefinedVariable
                if colorMin[index][1] < colorMax[index][1]:
                    colorMax[index][1] -= 1
                    print('ColorMax:')
                    print(colorMax[index])
                
            #increase maxSat
            if cv2.waitKey(1) & 0xFF == ord('y'):  # @UndefinedVariable
                colorMax[index][1] += 1
                print('ColorMax:')
                print(colorMax[index])
                
            #decrease maxVal
            if cv2.waitKey(1) & 0xFF == ord('j'):  # @UndefinedVariable
                if colorMin[index][2] < colorMax[index][2]:
                    colorMax[index][2] -= 1
                    print('ColorMax:')
                    print(colorMax[index])
                
            #increase maxVal
            if cv2.waitKey(1) & 0xFF == ord('u'):  # @UndefinedVariable
                colorMax[index][2] += 1
                print('ColorMax:')
                print(colorMax[index])
                
            #nextColor
            if cv2.waitKey(1) & 0xFF == ord('a'):  # @UndefinedVariable
                index += 1
                
            mask = cv2.inRange(hsv, tuple(colorMin[index]), tuple(colorMax[index]))  # @UndefinedVariable
            res = cv2.bitwise_and(img, img, mask= mask)  # @UndefinedVariable
            cv2.imshow('purple mask', mask)  # @UndefinedVariable
        
        f = open('colors.txt', 'w')
        f.write('ColorMin')
        f.write(str(colorMin))
        f.write('\nColorMax')
        f.write(str(colorMax))
        
        print('ColorMin')
        print(colorMin)
        print('\nColorMax')
        print(colorMax)
        
        img_name = 'img' + str(i) + '.jpeg'
        cv2.imwrite(img_name, img)  # @UndefinedVariable
        cv2.imshow('target', img)  # @UndefinedVariable
        i += 1
        
#         filename = 'outfile'
#         filename += str(i)
#         
#         f = open(filename, 'w')
#         num_pixels = 0
#         for arr in img:
#             for num in arr:
#                 for value in num:
#                     f.write(str(value))
#                     f.write(' ')
#                 f.write(',')
#                 num_pixels += 1
#             f.write('\n')
#                 
#         print(str(num_pixels))
#         i += 1
        
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