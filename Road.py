# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sympy
import math
import os
# import opencv-python-contrib

def len_between_dots(x1, y1, x2, y2):
    res = np.sqrt(pow(x2-x1,2)+pow(y2-y1,2))
    return res

def unions(lines, union_count, max_union_count_on_line):
    for i in lines:
        union_count_on_line = 0
        x11,y11,x12,y12 = i
        if x12 == x11:
            deg_1 = 90
        else:        
            deg_1 = math.degrees(math.atan(abs(y12-y11)/abs(x12-x11)))
        for j in lines:
            if i == j:
                continue
            x21,y21,x22,y22 = j
            if x22 == x21:
                deg_2 = 90
            else:
                deg_2 = math.degrees(math.atan(abs(y22-y21)/abs(x22-x21)))
            if abs(deg_2 - deg_1) <= 5:
                len13 = len_between_dots(x11, y11, x21, y21)
                len14 = len_between_dots(x11, y11, x22, y22)
                len23 = len_between_dots(x12, y12, x21, y21)
                len24 = len_between_dots(x12, y12, x22, y22)
                mas = [len13, len14, len23, len24]
                res = np.argmin(mas)
                if mas[res] > 10:
                    continue
                otr = len_between_dots(x11, y11, x12, y12)
                if res == 0:
                    len1 = len_between_dots(x12, y12, x21, y21)
                    dot_mas = [x12, y12, x22, y22]
                elif res == 1:
                    len1 = len_between_dots(x12, y12, x22, y22)
                    dot_mas = [x12, y12, x21, y21]
                elif res == 2:
                    len1 = len_between_dots(x11, y11, x21, y21)
                    dot_mas = [x11, y11, x22, y22]
                elif res == 3:
                    len1 = len_between_dots(x11, y11, x22, y22)
                    dot_mas = [x11, y11, x21, y21]
                
                if len1 > otr:
                    lines.remove([x11,y11,x12,y12])
                    lines.remove([x21,y21,x22,y22])
                    lines.append(dot_mas)
                    union_count += 1
                    union_count_on_line += 1
                    break
                else:
                    lines.remove([x21,y21,x22,y22])
                    union_count += 1
                    union_count_on_line += 1
        max_union_count_on_line = max(max_union_count_on_line, union_count_on_line)
    return (lines, union_count, max_union_count_on_line)
        
        

# Разбор видео, поиск особых точек
capture = cv2.VideoCapture('20191119_1241_Cam_1_03_00.mp4')
counter = 0
Flag = True

# Создание файла лога
#file = open('Lines.txt', 'w')
#string = 'frame number\t\tnumber of lines\t\tcoefficient 1\t\tcoefficient 2\n\n'
#file.write(string)

file2 = open('Debugging task before 4.txt', 'w')
string = '{:<10}{:<15}{:<15}{:<10}{:<15}{:<15}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}\n\n'.format('frame', 'start count', 'union count', 'avg', 'max union', 'end count', 'CountR', 'MinR', 'MaxR', 'CountL',  'MinL', 'MaxL','CountC', 'MinC', 'MaxC')
file2.write(string)
file2.close()

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
if not os.path.exists('.\\Files\\Color images with line union\\'):
    os.mkdir('.\\Files\\Color images with line union\\')
if not os.path.exists('.\\Files\\Different Canny\\'):
    os.mkdir('.\\Files\\Different Canny\\') 

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
    canny1, canny2 = 100, 200
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, canny1, canny2, 3)
    
    # Запись каждого 10 контурного изображения
#     if counter == 50:
#         os.chdir('.\\Files\\Different Canny\\')
#         cv2.imwrite('Canny {}x{}, img {}.jpeg'.format(canny1, canny2, counter), canny)
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
    canny_shape = canny.shape
    lines = cv2.HoughLinesP(canny, rho = 1, theta = 3*np.pi/180, threshold = 30, minLineLength = 15, maxLineGap=10)  
    lines_road_left, lines_road_right, lines_car = [], [], []      # точки отобранные по градусу
    for i in lines:
        x1,y1,x2,y2 = i[0]
        #if x1 in range(int(canny_shape[0]*0.2)):
        #    continue
#         if x2 in range(int(canny_shape[0]*0.9),int(canny_shape[0])):
#             continue
#         if y1 not in range(int(canny_shape[1]*0.6)):
#             continue
        deg = math.degrees(math.atan((y2-y1)/(x2-x1)))
        #print(deg)
        if (deg <= -30 and deg >= -70):
            if x1 not in range(int(canny_shape[0]*0.2)):
                lines_road_left.append(eval("[%d, %d, %d, %d]" %(x1,y1,x2,y2)))
                cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),3)
        elif (deg <= 70 and deg >= 30):
            lines_road_right.append(eval("[%d, %d, %d, %d]" %(x1,y1,x2,y2)))
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),3)
        elif ((deg <= 5 and deg >= -5)  or deg == 90 or deg == -90):
            if x1 in range(int(canny_shape[0]*0.6), int(canny_shape[0]*0.9)):
                lines_car.append(eval("[%d, %d, %d, %d]" %(x1,y1,x2,y2)))
                cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),3)
            #cv2.line(frame,(0,0),(1000, 500),(255,255,255),3)
    # Запись изображений разных размеров    
#     if counter%10 == 0 and counter<=10:
#         os.chdir('.\\Files\\Different sizes\\')
#         cv2.imwrite('size {}x{}, img {} lines.jpeg'.format(canny.shape[:2][1], canny.shape[:2][0], counter), frame)
#         os.chdir('..')
#         os.chdir('..')
    
    union_count, max_union_count_on_line = 0, 0
    len_lines = int(len(lines_road_left)) + int(len(lines_road_right)) + int(len(lines_car))
    lines_road_left, union_count, max_union_count_on_line = unions(lines_road_left, union_count, max_union_count_on_line)
    lines_road_right, union_count, max_union_count_on_line = unions(lines_road_right, union_count, max_union_count_on_line)
    lines_car, union_count, max_union_count_on_line = unions(lines_car, union_count, max_union_count_on_line)

    len_lines_new = int(len(lines_road_left)) + int(len(lines_road_right)) + int(len(lines_car))
    
    lines_road_left_min, lines_road_left_max = len_between_dots(0, 0, canny_shape[0], canny_shape[1]), 0
    lines_road_right_min, lines_road_right_max = len_between_dots(0, 0, canny_shape[0], canny_shape[1]), 0
    lines_car_min, lines_car_max = len_between_dots(0, 0, canny_shape[0], canny_shape[1]), 0

    for i in lines_road_left:
        x1,y1,x2,y2 = i
        lenn = len_between_dots(x1,y1,x2,y2)
        if lenn >= 20:
            lines_road_left_min = min(lines_road_left_min, lenn)
            lines_road_left_max = max(lines_road_left_max, lenn)
            cv2.line(frame,(x1,y1),(x2,y2),(150,150,255),2)
            cv2.circle(frame, (x1,y1), 5, (150,150,255),2)
            cv2.circle(frame, (x2,y2), 5, (150,150,255),2)
    for i in lines_road_right:
        x1,y1,x2,y2 = i
        lenn = len_between_dots(x1,y1,x2,y2)
        if lenn >= 20:
            lines_road_right_min = min(lines_road_right_min, lenn)
            lines_road_right_max = max(lines_road_right_max, lenn)
            cv2.line(frame,(x1,y1),(x2,y2),(150,255,150),2)
            cv2.circle(frame, (x1,y1), 5, (150,255,150),2)
            cv2.circle(frame, (x2,y2), 5, (150,255,150),2)
    for i in lines_car:
        x1,y1,x2,y2 = i
        lenn = len_between_dots(x1,y1,x2,y2)
        if lenn >= 20:
            lines_car_min = min(lines_car_min, lenn)
            lines_car_max = max(lines_car_max, lenn)
            cv2.line(frame,(x1,y1),(x2,y2),(255,150,150),2)
            cv2.circle(frame, (x1,y1), 5, (255,150,150),2)
            cv2.circle(frame, (x2,y2), 5, (255,150,150),2)
        
        
     
    file2 = open('Debugging task before 4.txt', 'a')
    string = '{:<10}{:<15}{:<15}{:<10}{:<15}{:<15}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}\n'.format(counter, len_lines, union_count, round(len_lines/union_count, 2), max_union_count_on_line, len_lines_new, len(lines_road_right), round(lines_road_right_min,2), round(lines_road_right_max,2), len(lines_road_left), round(lines_road_left_min,2), round(lines_road_left_max,2), len(lines_car), round(lines_car_min,2), round(lines_car_max,2))
    file2.write(string)
    file2.close()
    #file2.write(string)
    if counter%10 == 0:
        os.chdir('.\\Files\\Color images with line union\\')
        cv2.imwrite('img {}.jpeg'.format(counter), frame)
        os.chdir('..')
        os.chdir('..')
        
        # запись в файл Lines.txt
#     if counter%10 == 0:
#         for i in lines_road_left:
#             # Запись строк в лог
#             x1,y1,x2,y2 = i[0]
#             if x2 != x1:
#                 k = round(((y2-y1)/(x2-x1)), 3)
#                 b = round(((y1*x2-x1*y2)/(x2-x1)), 3)
#                 string = str(counter) + '\t\t\t' + str(len(lines_road_left)) + '\t\t\t' + str(k) + '\t\t\t' + str(b) + '\n'
#                 file.write(string)
            
#             # Запись каждого 10 изображения с прямыми
#             os.chdir('.\\Files\\Color images with Hough\\')
#             cv2.imwrite('img {}.jpeg'.format(counter), frame)
#             os.chdir('..')
#             os.chdir('..')

    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
#file.close()
file2.close()
