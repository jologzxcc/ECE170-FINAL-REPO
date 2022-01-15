import cv2
import mediapipe as mp
import numpy as np
import serial
import time

from inverse_kinematics import inv, scaled_angles
from arduino import send_to_arduino

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
class_and_coordinates = ""

arduino = serial.Serial(port='COM3', baudrate=9600)
arduino.timeout = 1

def estimate_hands():
  with mp_hands.Hands(
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
          
          # for hand_landmarks in results.multi_hand_landmarks:
          #   mp_drawing.draw_landmarks(
          #       image,
          #       hand_landmarks,
          #       mp_hands.HAND_CONNECTIONS,
          #       mp_drawing_styles.get_default_hand_landmarks_style(),
          #       mp_drawing_styles.get_default_hand_connections_style())

          for handLandmarks in results.multi_hand_landmarks:
            
            normalized_landmark_index_fingertip = handLandmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP.value]
            pixel_coordinates_landmark_index_fingertip = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark_index_fingertip.x, normalized_landmark_index_fingertip.y, img_width, img_height)
            
            normalized_landmark_thumbtip = handLandmarks.landmark[mp_hands.HandLandmark.THUMB_TIP.value]
            pixel_coordinates_landmark_thumbtip = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark_thumbtip.x, normalized_landmark_thumbtip.y, img_width, img_height)
            
            distance = np.sqrt(np.square(pixel_coordinates_landmark_index_fingertip[0] - pixel_coordinates_landmark_thumbtip[0])+np.square(pixel_coordinates_landmark_index_fingertip[1] - pixel_coordinates_landmark_thumbtip[1]))
    
            if distance <= 30:
              class_and_coordinates = "CLOSE"
            else:
              class_and_coordinates = "OPEN"

            # Centroid
            # normalized_landmark_wrist = handLandmarks.landmark[mp_hands.HandLandmark.WRIST.value]
            # pixel_coordinates_landmark_wrist = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark_wrist.x, normalized_landmark_wrist.y, img_width, img_height)
            
            # normalized_landmark_5 = handLandmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP.value]
            # pixel_coordinates_landmark_5 = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark_5.x, normalized_landmark_5.y, img_width, img_height)
            
            # cx = int((pixel_coordinates_landmark_wrist[0] + pixel_coordinates_landmark_5[0])/2)
            # cy = int((pixel_coordinates_landmark_wrist[1] + pixel_coordinates_landmark_5[1])/2)

            # centroid = (cx, cy, 0 )
            
            dot = (int(pixel_coordinates_landmark_index_fingertip[0]), int(pixel_coordinates_landmark_index_fingertip[1]))
          
            inverse = inv((dot))
            joints = inverse[1]
            new_angles = scaled_angles(inverse[0])

            image = cv2.line(image, (int(joints[0].x), int(joints[0].y)), (int(joints[1].x), int(joints[1].y)), color=(0, 255, 0), thickness=2)
            image = cv2.line(image, (int(joints[1].x), int(joints[1].y)), (int(joints[2].x), int(joints[2].y)), color=(0, 255, 0), thickness=2)
            image = cv2.line(image, (int(joints[2].x), int(joints[2].y)), (int(joints[3].x), int(joints[3].y)), color=(0, 255, 0), thickness=2)
            image = cv2.circle(image, dot[:2], radius=10, color=(0, 0, 255), thickness=-1)
            
            print(class_and_coordinates + f", coordinates {dot}" + f", angles: {inverse[0]}" + f", new angles: {new_angles}")

            arduino.write(new_angles.encode())

        cv2.imshow('Detected Hands', cv2.flip(image, 1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
          cap.release()
          break
        
    except:
      print("OUT OF BOUNDS RERUN THE PROGRAM")
      pass
