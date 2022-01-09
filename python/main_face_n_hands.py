import cv2
import sys
import numpy
import mediapipe as mp
import struct
from pathlib import Path


faceCascade = cv2.CascadeClassifier(
    "python/Resources/haarcascade_frontalface_default.xml")

img_path = Path().joinpath('uploads', sys.argv[1])
img = cv2.imread(str(img_path))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# face:
faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

# hands:
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

results = hands.process(imgRGB)
if results.multi_hand_landmarks:
    for handLms in results.multi_hand_landmarks:
        for id, lm in enumerate(handLms.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 3, (255, 0, 0), cv2.FILLED)

        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, mpDraw.DrawingSpec(
            color=(0, 0, 255)), mpDraw.DrawingSpec(color=(255, 255, 0)))

try:
    res = cv2.imencode(img_path.suffix, img)[1]
except:
    res = cv2.imencode('.jpg', img)[1]
print(list(res))
print('end')
cv2.waitKey(0)
