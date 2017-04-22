'''
Created on Apr 12, 2017

@author: trevb
'''
import cv2
import numpy as np
import math

def arenaOrientation(points):

    #0 for first keypoint, 1 for second, 2 for third, -1 for uninitialized
    corner_index = -1
    front_index = -1
    left_index = -1
    
    line1 = np.sqrt((points[0].pt[0] - points[1].pt[0]) * (points[0].pt[0] - points[1].pt[0]) + (points[0].pt[1] - points[1].pt[1]) * (points[0].pt[1] - points[1].pt[1]))
    line2 = np.sqrt((points[1].pt[0] - points[2].pt[0]) * (points[1].pt[0] - points[2].pt[0]) + (points[1].pt[1] - points[2].pt[1]) * (points[1].pt[1] - points[2].pt[1]))
    line3 = np.sqrt((points[0].pt[0] - points[2].pt[0]) * (points[0].pt[0] - points[2].pt[0]) + (points[0].pt[1] - points[2].pt[1]) * (points[0].pt[1] - points[2].pt[1]))
    
    euclidean_distance = [[line1], [line2], [line3]]
    #print('\t\t\tEuclidean_distance:\t' + str(euclidean_distance))
    
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
    
    slope1 = (front[1] - corner[1]) / (front[0] - corner[0])
    slope2 = (left[1] - corner[1]) / (left[0] - corner[0])
    angle1 = math.degrees(-math.atan(slope1))
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
        
    if angle2 > 225:
        if angle1 < 135:
            angle = angle2
        else:
            angle = angle1
    else:
        angle= angle1
    
    center = [(front[0] + left[0]) / 2, (front[1] + left[1]) / 2]
    
    goal = [center[0], center[1], angle]

    return goal
    
def orientation(points, orange):

    #0 for first keypoint, 1 for second, 2 for third, -1 for uninitialized
    corner_index = -1
    front_index = -1
    left_index = -1
    
    line1 = np.sqrt((points[0].pt[0] - points[1].pt[0]) * (points[0].pt[0] - points[1].pt[0]) + (points[0].pt[1] - points[1].pt[1]) * (points[0].pt[1] - points[1].pt[1]))
    line2 = np.sqrt((points[1].pt[0] - points[2].pt[0]) * (points[1].pt[0] - points[2].pt[0]) + (points[1].pt[1] - points[2].pt[1]) * (points[1].pt[1] - points[2].pt[1]))
    line3 = np.sqrt((points[0].pt[0] - points[2].pt[0]) * (points[0].pt[0] - points[2].pt[0]) + (points[0].pt[1] - points[2].pt[1]) * (points[0].pt[1] - points[2].pt[1]))
    
    euclidean_distance = [[line1], [line2], [line3]]
    #print('\t\t\tEuclidean_distance:\t' + str(euclidean_distance))
    
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
    
    slope1 = (front[1] - corner[1]) / (front[0] - corner[0])
    slope2 = (left[1] - corner[1]) / (left[0] - corner[0])
    angle1 = math.degrees(-math.atan(slope1))
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
        
    if angle2 > 225:
        if angle1 < 135:
            angle = angle2
        else:
            angle = angle1
    else:
        angle= angle1
    
    center = [(front[0] + left[0]) / 2, (front[1] + left[1]) / 2]
    
    goal = [center[0], center[1], angle]
    
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
    
    return goal

i = 0
while True:
    img_name = 'original' + str(i) + '.png'
    
    try:
        img = cv2.imread(img_name)  # @UndefinedVariable
        #cv2.imshow(img_name, img)  # @UndefinedVariable
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # @UndefinedVariable
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
    
    orange = []
    locations = []
    
    for index in range(length):
        
        mask = cv2.inRange(hsv, tuple(colorMin[index]), tuple(colorMax[index]))  # @UndefinedVariable
        res = cv2.bitwise_and(img, img, mask= mask)  # @UndefinedVariable
    
        keypoints = detector.detect(mask)
        thePoints = '\t' + colors[index]
        
        k = 0
        for points in keypoints:
            #thePoints += ('\n\t\t' + str(points.pt))
            k += 1
            
        if len(keypoints) == 3:
            print(thePoints)
            img_with_keypoints = cv2.drawKeypoints(img_with_keypoints, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # @UndefinedVariable
            if colors[index] == 'Orange':
                orange = arenaOrientation(keypoints)
                print('\t\t\t' + str(orange))
            else:
                data = orientation(keypoints, orange)
                locations.append(data)
                print('\t\t\t' + str(data))

    # Show keypoints
    cv2.imshow(key_img, img_with_keypoints)  # @UndefinedVariable
    i += 1
    cv2.waitKey(0)  # @UndefinedVariable

cv2.waitKey(0)  # @UndefinedVariable
cv2.destroyAllWindows()  # @UndefinedVariable