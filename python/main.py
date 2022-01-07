# stolen from https://github.com/murtazahassan/Learn-OpenCV-in-3-hours/blob/master/chapter9.py
import cv2
import sys
import numpy
# import json
import struct
# import os
from pathlib import Path
# print(os.getcwd())
# print(sys.stdin.encoding)

# raw = json.load(sys.stdin).get('data')
def to_buffer(l):
    return struct.pack('I' * len(l), *l)

def read_from_buffer(buff):
    bytes = numpy.asarray(bytearray(buff), dtype=numpy.uint8).tobytes()
    return cv2.imdecode(bytes, 0)

faceCascade = cv2.CascadeClassifier("python/Resources/haarcascade_frontalface_default.xml") 
# Пути следует прописывать именно так - как если бы мы находились в корневой папке проекта! Фактически, мы в ней и находимся, что подтверждает вывод os.getcwd()

# img = read_from_buffer(to_buffer(raw))
# Как правильно преобразовать list в buffer? Это позволило бы хранить данные изображения в  multer.memoryStorage()
img_path = Path().joinpath('uploads', sys.argv[1])
img = cv2.imread(str(img_path))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

# cv2.imshow("Result", img)
try:
    res = cv2.imencode(img_path.suffix, img)[1]
except:
    res = cv2.imencode('.jpg', img)[1]
print(list(res))
print('end')
cv2.waitKey(0) 
