# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sympy
import math
import os
# import opencv-python-contrib



# Разбор видео, поиск особых точек
capture = cv2.VideoCapture('20191119_1241_Cam_1_03_00.mp4')
counter = 0
Flag = True


# нахождение точек и их прослеживание
while(capture.isOpened() and Flag):
    counter += 1
    flag, frame = capture.read()  
    if not flag:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50, 150, 3)

    lines = cv2.HoughLinesP(canny, rho = 10,	theta = 5,	threshold = 10)#,	min_theta = 0,	max_theta = 90)
    print(lines)
    N = lines.shape[0]
    for i in range(N):
        x1 = lines[i][0][0]
        y1 = lines[i][0][1]    
        x2 = lines[i][0][2]
        y2 = lines[i][0][3]    
        cv2.line(I,(x1,y1),(x2,y2),(255,0,0),2)
        #for i in lines:
        #    string = str(counter) + '\t\t\t' + str(len(lines)) + '\t\t\t' + str(i[0][0]) + '\t\t\t' + str(i[0][1]) + '\n'
        #    file.write(string)
        #for x1,y1,x2,y2 in lines:        
        #    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)
    cv2.imshow('video', canny)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
file.close()
