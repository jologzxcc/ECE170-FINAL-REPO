import cv2
from vectormath import Vector3

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while cap.isOpened():
        success, image = cap.read()
        img_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        img_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        vect = Vector3(100, 100, 0)

        image = cv2.line(image, (0,0), (int(vect.x), int(vect.y)), color=(0, 255, 0), thickness=2)


        cv2.imshow('Detected Hands', cv2.flip(image, 1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
          cap.release()
          break