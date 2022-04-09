import cv2
import mediapipe as mp
import numpy as np
import time

from inverse_kinematics import inv, scaled_angles
from transmit import transmit

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
class_and_coordinates = ""

seconds = time.time()

def estimate_hands():
  with mp_hands.Hands(
      max_num_hands = 1,
      model_complexity = 0,
      min_detection_confidence = 0.5,
      min_tracking_confidence = 0.5) as hands:

    try:
      while cap.isOpened():
        success, image = cap.read()
        img_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        img_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if not success:
          print("Ignoring empty camera frame.")
          continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks != None:

          for handLandmarks in results.multi_hand_landmarks:
            normalized_landmark_index_fingertip = handLandmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP.value]
            pixel_coordinates_landmark_index_fingertip = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark_index_fingertip.x, 
                                                                                                     normalized_landmark_index_fingertip.y, 
                                                                                                     img_width, 
                                                                                                     img_height)
            z_axis = normalized_landmark_index_fingertip.z
            depth = abs(int(float(z_axis) * 1000))
            normalized_landmark_thumbtip = handLandmarks.landmark[mp_hands.HandLandmark.THUMB_TIP.value]
            pixel_coordinates_landmark_thumbtip = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark_thumbtip.x, 
                                                                                              normalized_landmark_thumbtip.y, 
                                                                                              img_width, 
                                                                                              img_height)

            distance = np.sqrt(np.square(pixel_coordinates_landmark_index_fingertip[0] - pixel_coordinates_landmark_thumbtip[0])+np.square(pixel_coordinates_landmark_index_fingertip[1] - pixel_coordinates_landmark_thumbtip[1]))
    
            if distance <= 30:
              class_and_coordinates = "CLOSE"
            else:
              class_and_coordinates = "OPEN"

            dot = (int(pixel_coordinates_landmark_index_fingertip[0]), int(pixel_coordinates_landmark_index_fingertip[1]))
          
            inverse = inv((dot))
            joints = inverse[1]
            angles = scaled_angles(inverse[0])

            image = cv2.line(image, (int(joints[0].x), 
                          int(joints[0].y)), 
                          (int(joints[1].x), 
                          int(joints[1].y)), 
                          color=(0, 255, 0), 
                          thickness=2)

            image = cv2.line(image, (int(joints[1].x), 
                          int(joints[1].y)), 
                          (int(joints[2].x), 
                          int(joints[2].y)), 
                          color=(0, 255, 0), 
                          thickness=2)
        
            image = cv2.circle(image, dot[:2], radius=10, color=(0, 0, 255), thickness=-1)
            
            # print(class_and_coordinates + 
            # f", coordinates {dot}" + 
            # f", angles: {inverse[0]}" + 
            # f", new angles: {angles}" + 
            # f", time: {time.time() - seconds}" + 
            # f", depth: {abs(int(float(z_axis) * 1000))}")

            angle_depth = [angles[0], angles[1], depth, distance]
            # print(angle_depth)
            transmit(angle_depth)

        cv2.imshow('Detected Hands', cv2.flip(image, 1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
          cap.release()
          break
        
    except:
      print("OUT OF BOUNDS RERUN THE PROGRAM")
      pass
    
