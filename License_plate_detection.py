import numpy as np
import cv2

image = cv2.imread('/home/ankur/Downloads/9.jpg')	#reading the image
image = cv2.resize(image,(600,400))		#resizing the image	
	
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)		#grayscaling 
blur = cv2.GaussianBlur(gray, (5,5), 0)		#Gaussian blurring

sobely = cv2.Sobel(blur, -1, 1, 0)	#Applying sobel in y direction. Sobel is used for edge extraction

ret2,th2 = cv2.threshold(sobely,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)	#Thresholding 

se = cv2.getStructuringElement(cv2.MORPH_RECT,(16,4))	#morphology using rectangle
morph = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, se)  

ret, contours, hierarchy = cv2.findContours(morph,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #finding contours in the image
contours= sorted(contours, key = cv2.contourArea, reverse = True)  #arranging contours according to the decreasing order of their areas



for cnt in contours:
    rect = cv2.minAreaRect(cnt)   #finding the bounding box of each contour
    cx = rect[0][0]		#X coordinate of the center of the bounding box
    cy = rect[0][1]		#Y coordinate of the center of the bounding box
    width = rect[1][0]	#width of the bounding box
    height = rect[1][1]	#height of the bounding box	
    angle = rect[2]		#angle the bounding box makes with the horizontal
    area = width * height	#area of the box
    aspect_ratio = width/(height + 0.000001)	#aspect ratio of the triangle
    
    if (area > 500) and (area < 15000) and (aspect_ratio >= 2) and (aspect_ratio <= 10) and (angle > -15) :		#these contours have been found through trials
        
        
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)		#Poly DP gives the number of sides of the contour
        if len(approx) <= 15 and len(approx) >=3:
        	
        	row_2 = cy + height/2
        	row_1 = cy - height/2
        	col_1 = cx - width/2
        	col_2 = cx + width/2
        	cropped = image[int(row_1):int(row_2), int(col_1):int(col_2)]
        	cv2.imshow('Square',cropped)
        	cv2.waitKey(0)
        	cv2.destroyAllWindows()
        	break


