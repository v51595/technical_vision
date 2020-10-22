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

# Создание файла лога
file = open('Lines.txt', 'w')
string = 'frame number\t\tnumber of lines\t\tcoefficient 1\t\t\t\tcoefficient 1\n\n'
file.write(string)

# Создание папок для изображений
if not os.path.exists('.\\Files\\'):
    os.mkdir('.\\Files\\')
if not os.path.exists('.\\Files\\Color images\\'):
    os.mkdir('.\\Files\\Color images\\')
if not os.path.exists('.\\Files\\Contour images\\'):
    os.mkdir('.\\Files\\Contour images\\')
if not os.path.exists('.\\Files\\Color images with Hough\\'):
    os.mkdir('.\\Files\\Color images with Hough\\')  
if not os.path.exists('.\\Files\\Different sizes\\'):
    os.mkdir('.\\Files\\Different sizes\\') 

while(capture.isOpened() and Flag):
    counter += 1
    flag, frame = capture.read()  
    if not flag:
        break
    
    #for i in range(5):
    #    frame = cv2.resize(frame, (int(1600/pow(2,i)), int(1200/pow(2,i))))
    
    # Запись первых 50 изображений из видео
#    if counter <= 50:
#        os.chdir('.\\Files\\Color images\\')
#        cv2.imwrite('img {}.jpeg'.format(counter), frame)
#        os.chdir('..')
#        os.chdir('..')
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50, 150, 3)
    
    # Запись каждого 10 контурного изображения
#     if counter%10 == 0:
#         os.chdir('.\\Files\\Contour images\\')
#         cv2.imwrite('img {}.jpeg'.format(counter), canny)
#         os.chdir('..')
#         os.chdir('..')
    
    # Запись 10 изображений с разными размерами
    # (меньше 800х600 контуры уже почти неразличимы, а ниже 400х300 ничего и не выделяется)
#     if counter%10 == 0 and counter<=100:
#         os.chdir('.\\Files\\Different sizes\\')
#         cv2.imwrite('size {}x{}, img {}.jpeg'.format(canny.shape[:2][1], canny.shape[:2][0], counter), canny)
#         os.chdir('..')
#         os.chdir('..')
        
    #lines = cv2.HoughLinesP(canny, rho = 5,	theta = 1, threshold = 10, minLineLength = 10)#, maxLineGap=90)    #N = lines.shape[0]
    lines = cv2.HoughLinesP(canny, rho = 1, theta = 3*np.pi/180, threshold = 30, minLineLength = 25, maxLineGap=10)  
    for i in lines:
        x1,y1,x2,y2 = i[0]
        cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),3)
        
    # Запись изображений разных размеров    
#     if counter%10 == 0 and counter<=10:
#         os.chdir('.\\Files\\Different sizes\\')
#         cv2.imwrite('size {}x{}, img {} lines.jpeg'.format(canny.shape[:2][1], canny.shape[:2][0], counter), frame)
#         os.chdir('..')
#         os.chdir('..')

    if counter%10 == 0:
        for i in lines:
            # Запись строк в лог
            x1,y1,x2,y2 = i[0]
            if x2 != x1:
                string = str(counter) + '\t\t\t' + str(len(lines)) + '\t\t\t' + str((y2-y1)/(x2-x1)) + '\t\t\t\t\t' + str((y1*x2-x1*y2)/(x2-x1)) + '\n'
                file.write(string)
            
            # Запись каждого 10 изображения с прямыми
            os.chdir('.\\Files\\Color images with Hough\\')
            cv2.imwrite('img {}.jpeg'.format(counter), frame)
            os.chdir('..')
            os.chdir('..')
    #cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
file.close()
