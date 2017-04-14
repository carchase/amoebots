'''
Created on Apr 12, 2017

@author: trevb
'''
import cv2
import numpy as np

def arenaOrientation(points):

    #0 for first keypoint, 1 for second, 2 for third, -1 for uninitialized
    corner = -1
    front = -1
    left = -1
    
    line1 = np.sqrt((points[0].pt[0] - points[1].pt[0]) * (points[0].pt[0] - points[1].pt[0]) + (points[0].pt[1] - points[1].pt[1]) * (points[0].pt[1] - points[1].pt[1]))
    line2 = np.sqrt((points[1].pt[0] - points[2].pt[0]) * (points[1].pt[0] - points[2].pt[0]) + (points[1].pt[1] - points[2].pt[1]) * (points[1].pt[1] - points[2].pt[1]))
    line3 = np.sqrt((points[0].pt[0] - points[2].pt[0]) * (points[0].pt[0] - points[2].pt[0]) + (points[0].pt[1] - points[2].pt[1]) * (points[0].pt[1] - points[2].pt[1]))
    
    euclidean_distance = [[line1], [line2], [line3]]
    print('\t\t\tEuclidean_distance:\t' + str(euclidean_distance))
    
    if euclidean_distance[0] > euclidean_distance[1]:
        front = 0
        if euclidean_distance[0] > euclidean_distance[2]:
            corner = 2
            left = 1
        else:
            corner = 1
            left = 2
    elif euclidean_distance[1] > euclidean_distance[2]:
        corner = 0
        front = 1
        left = 2
    else:
        corner = 1
        front = 0
        left = 2
        
    print('\t\t\tCorner:\t' + str(points[corner].pt[0]) + ', ' + str(points[corner].pt[1]))
        
    return 'yea'
    
def orientation(points):

    #0 for first keypoint, 1 for second, 2 for third, -1 for uninitialized
    corner_index = -1
    front_index = -1
    left_index = -1
    
    line1 = np.sqrt((points[0].pt[0] - points[1].pt[0]) * (points[0].pt[0] - points[1].pt[0]) + (points[0].pt[1] - points[1].pt[1]) * (points[0].pt[1] - points[1].pt[1]))
    line2 = np.sqrt((points[1].pt[0] - points[2].pt[0]) * (points[1].pt[0] - points[2].pt[0]) + (points[1].pt[1] - points[2].pt[1]) * (points[1].pt[1] - points[2].pt[1]))
    line3 = np.sqrt((points[0].pt[0] - points[2].pt[0]) * (points[0].pt[0] - points[2].pt[0]) + (points[0].pt[1] - points[2].pt[1]) * (points[0].pt[1] - points[2].pt[1]))
    
    euclidean_distance = [[line1], [line2], [line3]]
    print('\t\t\tEuclidean_distance:\t' + str(euclidean_distance))
    
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
    front = []
    left = []
    
    
    if points[front_index].pt[0] > corner[0] and points[left_index].pt[0] > corner[0]:
        if points[front_index].pt[1] > points[left_index].pt[1]:
            front = [points[front_index].pt[0],points[front_index].pt[1]]
            left = [points[left_index].pt[0], points[left_index].pt[1]]
        else:
            left = [points[front_index].pt[0],points[front_index].pt[1]]
            front = [points[left_index].pt[0], points[left_index].pt[1]]
    elif points[front_index].pt[0] < corner[0] and points[left_index].pt[0] < corner[0]:
        if points[front_index].pt[1] > points[left_index].pt[1]:
            left = [points[front_index].pt[0],points[front_index].pt[1]]
            front = [points[left_index].pt[0], points[left_index].pt[1]]
        else:
            front = [points[front_index].pt[0],points[front_index].pt[1]]
            left = [points[left_index].pt[0], points[left_index].pt[1]]
    elif points[front_index].pt[1] > corner[1] and points[left_index].pt[1] > corner[1]:
        if points[front_index].pt[0] > points[left_index].pt[0]:
            left = [points[front_index].pt[0],points[front_index].pt[1]]
            front = [points[left_index].pt[0], points[left_index].pt[1]]
        else:
            front = [points[front_index].pt[0],points[front_index].pt[1]]
            left = [points[left_index].pt[0], points[left_index].pt[1]]
    elif points[front_index].pt[1] < corner[1] and points[left_index].pt[1] < corner[1]:
        if points[front_index].pt[0] > points[left_index].pt[0]:
            front = [points[front_index].pt[0],points[front_index].pt[1]]
            left = [points[left_index].pt[0], points[left_index].pt[1]]
        else:
            left = [points[front_index].pt[0],points[front_index].pt[1]]
            front = [points[left_index].pt[0], points[left_index].pt[1]]
    else:
        print("You're fucked!")
        left = [points[left_index].pt[0], points[left_index].pt[1]]
        front = [points[front_index].pt[0],points[front_index].pt[1]]
        
    
    print('\t\t\tCorner:\t' + str(corner[0]) + ', ' + str(corner[1]))
    print('\t\t\tFront:\t' + str(front[0]) + ', ' + str(front[1]))
    print('\t\t\tLeft:\t' + str(left[0]) + ', ' + str(left[1]))
    return 'naw'

i = 0
while True:
    img_name = 'original' + str(i) + '.png'
    
    try:
        img = cv2.imread(img_name)  # @UndefinedVariable
        #cv2.imshow(img_name, img)  # @UndefinedVariable
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # @UndefinedVariable
        i += 1
    except:
        break
    
    colors = ['Orange', 'Green', 'Purple', 'Yellow', 'Red', 'Blue', 'Light Blue']
    colorMin = [[0, 67, 122], [48, 37, 1], [113, 85, 153], [43, 0, 177], [155, 37, 117], [108, 119, 170], [90, 102, 228]]
    colorMax = [[20, 255, 255], [83, 255, 255], [134, 149, 202], [84, 41, 190], [179, 251, 255], [116, 183, 218], [114, 181, 255]]
        
    blobParams = cv2.SimpleBlobDetector_Params()  # @UndefinedVariable
        
    blobParams.filterByColor = True
    blobParams.blobColor = 255
    blobParams.filterByArea = True
    blobParams.minArea = 10
    blobParams.filterByCircularity = False
    blobParams.filterByConvexity = False
    blobParams.filterByInertia = False
     
    detector = cv2.SimpleBlobDetector_create(blobParams)  # @UndefinedVariable
    
    length = len(colors)
    img_with_keypoints = img
    keypoints = [[], [], [], [], [], [], []]
    key_img = 'Keypoints' + str(i) + '.png'
    
    for index in range(length):
        
        mask = cv2.inRange(hsv, tuple(colorMin[index]), tuple(colorMax[index]))  # @UndefinedVariable
        res = cv2.bitwise_and(img, img, mask= mask)  # @UndefinedVariable
    
        keypoints = detector.detect(mask)
        thePoints = '\t' + colors[index]
        
        k = 0
        for points in keypoints:
            thePoints += ('\n\t\t' + str(points.pt))
            k += 1
            
        if k >= 3:
            print(thePoints)
            img_with_keypoints = cv2.drawKeypoints(img_with_keypoints, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # @UndefinedVariable
            if colors[index] == 'Orange':
                print(arenaOrientation(keypoints))
            else:
                print(orientation(keypoints))

    # Show keypoints
    cv2.imshow(key_img, img_with_keypoints)  # @UndefinedVariable
    cv2.waitKey(0)  # @UndefinedVariable

cv2.waitKey(0)  # @UndefinedVariable
cv2.destroyAllWindows()  # @UndefinedVariable