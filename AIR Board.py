import cv2
import mediapipe as mp
import math
from collections import deque


mp_drawing = mp.solutions.drawing_utils
mphands = mp.solutions.hands

coordinates = deque(maxlen=1024)
temp_coordinates = deque(maxlen=1024)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
hands = mphands.Hands()

def euclidian(x1,y1,x2,y2):
    d = int(math.sqrt((x1 - x2)**2 + (y1 - y2)**2)*100)
    return d


while True:
    data, image = cap.read()
    # Flip the image
    image = cv2.cvtColor(cv2.flip(image,1), cv2.COLOR_BGR2RGB)

    # Storing the result
    result = hands.process(image)
    image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mphands.HAND_CONNECTIONS)
            index_finger_y = hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP].y
            middle_finger_y = hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_TIP].y
            index_finger_x = hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP].x
            middle_finger_x = hand_landmarks.landmark[mphands.HandLandmark.MIDDLE_FINGER_TIP].x
            pinky_x = hand_landmarks.landmark[mphands.HandLandmark.PINKY_TIP].x
            pinky_y = hand_landmarks.landmark[mphands.HandLandmark.PINKY_TIP].y
            d_draw = euclidian(index_finger_x,index_finger_y,middle_finger_x,middle_finger_y)
            d_erase = euclidian(index_finger_x,index_finger_y,pinky_x,pinky_y)
            if d_draw>7:
                h,w,c = image.shape
                x,y = int(index_finger_x*w), int(index_finger_y*h)
                temp_coordinates.append([x,y])
                for i in range(1,len(temp_coordinates)):
                    cv2.line(image,temp_coordinates[i],temp_coordinates[i-1],(255,0,0),2)
            elif d_draw<7:
                coordinates.append(temp_coordinates)
                temp_coordinates=[]
            if d_erase<=13 and d_erase>=8:
                temp_coordinates=[]
                coordinates=[]
    for j in range(1,len(coordinates)):
        for i in range(1,len(coordinates[j])):
            cv2.line(image,coordinates[j][i],coordinates[j][i-1],(0,255,0),2)
    cv2.imshow('Lines', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

#ucliden
#l2nomes