import cv2 as cv
import mediapipe as mp
from collections import deque

coordinates = deque(maxlen=1024)
cam = cv.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils
while True:
    ret, frame = cam.read()
    imgrgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    res = hands.process(imgrgb)
    if res.multi_hand_landmarks:
        for handLMS in res.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame,handLMS,mphands.HAND_CONNECTIONS)
        for id, lm in enumerate(handLMS.landmark):
            h,w,c = frame.shape
            x,y = int(lm.x*w), int(lm.y*h)
            if id == 8:
                coordinates.append([x,y])
    for coord in coordinates:
        cv.circle(frame, coord, 5, (255, 0, 0), -1)
    cv.imshow('Hand', frame)
    if cv.waitKey(1) == ord('q'):
        break
'''import cv2
from collections import deque

# Initialize a deque to store coordinates
coordinates = deque(maxlen=100)  # Adjust the maximum length as needed
coordinates.extend([(100, 100), (200, 200), (300, 300), (400, 400)])

# Function to draw blue dots on the image at the specified coordinates
def draw_dots(image, coords):
    for coord in coords:
        cv2.circle(image, coord, 5, (255, 0, 0), -1)  # Draw blue dot at the coordinate

# Main function to capture video from the camera and draw blue dots
def main():
    cap = cv2.VideoCapture(0)  # Initialize camera capture
    while True:
        ret, frame = cap.read()  # Capture frame from camera
        if not ret:
            break

        # Draw blue dots on the frame
        draw_dots(frame, coordinates)

        cv2.imshow('Camera', frame)  # Display the frame

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
'''