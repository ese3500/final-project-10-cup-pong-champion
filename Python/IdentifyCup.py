import cv2
import numpy as np

img = cv2.imread("Images/try3.png")

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    pixelCoords = np.array([-1,-1])
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if(area>300):
            cv2.drawContours(imgContour, cnt, -1, (255,0,0),3)
            peri = cv2.arcLength(cnt, True)
            approxPoints = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approxPoints) 
            cv2.rectangle(imgContour, (x,y), (x+w,y+h),(0,255,0),3)
            print("x: " + str(x+w/2))
            print("y: " + str(y+h/2))
            pixelVals = np.array([x+w/2, y+h/2])
            pixelCoords = np.append(pixelCoords,pixelVals)
    return pixelCoords[2:len(pixelCoords)]

def pixelToCM(pixels):
    cm_coords = np.zeros_like(pixels)
    i = 0
    for v in pixels:
        if i%2 == 0:
            cm_coords[i] = v*.206 - 61
        else:
            cm_coords[i] = 160
        i += 1
    return cm_coords    
#Crop Image
imgResize = cv2.resize(img,(1000,1000))
#first one is y and second one is x
imgCropped = imgResize[170:600,100:600] 
#imgCropped = imgResize
#cv2.imshow("Image Resize",imgResize)
cv2.imshow("Image Cropped",imgCropped)

"""
width,height = 1184,638
pts1 = np.float32([[44,560],[1850,24],[0,1260],[1850,1260]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgWarp = cv2.warpPerspective(imgCropped,matrix,(width,height))
cv2.imshow("Output",imgWarp)
"""
#Color Masking
imgHSV = cv2.cvtColor(imgCropped,cv2.COLOR_BGR2HSV)

#Red Mask
h_min = 0
h_max = 179
sat_min = 150
sat_max = 255
val_min = 51
val_max = 255

lower = np.array([h_min, sat_min, val_min])
upper = np.array([h_max, sat_max, val_max])


mask = cv2.inRange(imgHSV, lower, upper)
img_result = cv2.bitwise_and(imgCropped, imgCropped, mask=mask)
#cv2.imshow("Red Mask", img_result)

#White Mask
h_min = 0
h_max = 255
sat_min = 0
sat_max = 90
val_min = 180
val_max = 255

lower = np.array([h_min, sat_min, val_min])
upper = np.array([h_max, sat_max, val_max])


mask = cv2.inRange(imgHSV, lower, upper)
img_result2 = cv2.bitwise_and(imgCropped, imgCropped, mask=mask)
cv2.imshow("White Mask", img_result2)

img_final_mask = cv2.add(img_result, img_result2)

#cv2.imshow("Final Mask", img_final_mask)

#Detect cup circles
imgContour = img_result2.copy()
imgGray = cv2.cvtColor(img_final_mask,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur, 300, 300)

arr = getContours(imgCanny)
arr2 = pixelToCM(arr)
cv2.imshow("Show Contours", imgContour)
cv2.waitKey(0)



