import cv2
import numpy as np
import pandas as pd

from positions_module import EyeDataModule, PositionsModule
from face_adjustments_module import FaceAdjuster
from face_mesh_module import FaceMeshDetector
from eye_feature_detector_module import EyeModule
from definitions import *


def draw_face_box(image,face_border):
    top, left, bottom, right = face_border
    image = cv2.rectangle(image,(left,top),(right,bottom),(0,255,0,1))
    return image

def draw_iris_circles(image,left_iris,right_iris):
    if(left_iris == 0 or right_iris == 0 or left_iris == None or right_iris == None):
        return image
    if(left_iris):
        cv2.circle(image, left_iris[0],left_iris[1], (255,0,255), 1, cv2.LINE_AA)
    if(right_iris):
        cv2.circle(image, right_iris[0],right_iris[1], (255,0,255), 1, cv2.LINE_AA)
    return image

def draw_pupil_circles(image,left_pupil,right_pupil):
    if(left_pupil == 0 or right_pupil == 0 or left_pupil == None or right_pupil == None):
        return image
    if(left_pupil):
        cv2.circle(image, left_pupil[0],left_pupil[1], (0,0,255), 1, cv2.LINE_AA)
    if(right_pupil):
        cv2.circle(image, right_pupil[0],right_pupil[1], (0,0,255), 1, cv2.LINE_AA)
    return image

def draw_past_positions_iris_center(image,positions_data,max_number_draw):
    left_eye,right_eye = positions_data.get_past_n_positions(max_number_draw)

    left_eye_printable = [] # tirei os 0,0 que eu coloco quando não acho nada
    for i in range(1,len(left_eye)):
        if(left_eye[i]==0 or left_eye[i]==None or left_eye[i]=="" ):
            continue
        else:
            left_eye_printable.append(left_eye[i])
    right_eye_printable = [] # tirei os 0,0 que eu coloco quando não acho nada
    for i in range(1,len(right_eye)):
        if(right_eye[i]==0 or right_eye[i]==None or right_eye[i]=="" ):
            continue
        else:
            right_eye_printable.append(right_eye[i])

    for i in range(1,len(left_eye_printable)):
        end_point=left_eye_printable[i]
        start_point=left_eye_printable[i-1]
        if(start_point == [None,None] or end_point == [None,None]):
            continue
        if i == 1:
            color = (255,0,0)
        else:
            color = (0,0,255)
        thickness =int(max_number_draw/(2*i+max_number_draw/3))+1
        image = cv2.line(image, start_point, end_point, color, thickness)
        #print(f'Left eye Line start: {start_point} | Line end: {end_point}')

    for i in range(1,len(right_eye_printable)):
        end_point=right_eye_printable[i]
        start_point=right_eye_printable[i-1]
        if(start_point == [None,None] or end_point == [None,None]):
            continue
        if i ==1:
            color = (255,0,0)
        else:
            color = (0,0,255)
        thickness =int(max_number_draw/(2*i+max_number_draw/3))+1
        image = cv2.line(image, start_point, end_point, color, thickness)
        #print(f'Right eye Line start: {start_point} | Line end: {end_point}')
    return image

def draw_face_mesh_points(image, lms,color = (0,255,0)):
    for lm in lms:
        image = cv2.circle(image, (lm), radius=1, color=color, thickness=-1)
    return image
