import cv2
import mediapipe as mp
import numpy as np
import time

from inverse_kinematics import inv, normalized, get_angle, rotate, distance_depth

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# url = "http://192.168.50.168:8080/video"
# cap = cv2.VideoCapture(url)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
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
  
            normalized_landmark_thumbtip = handLandmarks.landmark[mp_hands.HandLandmark.THUMB_TIP.value]
            pixel_coordinates_landmark_thumbtip = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark_thumbtip.x, 
                                                                                              normalized_landmark_thumbtip.y, 
                                                                                              img_width, 
                                                                                              img_height)

            normalized_landmark_wrist = handLandmarks.landmark[mp_hands.HandLandmark.WRIST.value]
            pixel_coordinates_landmark_wrist = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark_wrist.x, 
                                                                                              normalized_landmark_wrist.y, 
                                                                                              img_width, 
                                                                                              img_height)

            normalized_landmark_mcp = handLandmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP.value]
            pixel_coordinates_landmark_mcp = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark_mcp.x, 
                                                                                              normalized_landmark_mcp.y, 
                                                                                              img_width, 
                                                                                              img_height)

            normalized_landmark_pinky = handLandmarks.landmark[mp_hands.HandLandmark.PINKY_MCP.value]
            pixel_coordinates_landmark_pinky = mp_drawing._normalized_to_pixel_coordinates(normalized_landmark_pinky.x, 
                                                                                              normalized_landmark_pinky.y, 
                                                                                              img_width, 
                                                                                              img_height)                                                                                  
            # z_axis = normalized_landmark_mcp.z
            # depth = normalized(abs(int(float(z_axis) * 1500)))

            depth_distance = normalized(distance_depth(pixel_coordinates_landmark_pinky, pixel_coordinates_landmark_wrist))

            distance = np.sqrt(np.square(pixel_coordinates_landmark_index_fingertip[0] - pixel_coordinates_landmark_thumbtip[0])+np.square(pixel_coordinates_landmark_index_fingertip[1] - pixel_coordinates_landmark_thumbtip[1]))
            centroid = (int((pixel_coordinates_landmark_mcp[0] + pixel_coordinates_landmark_wrist[0])/2),
                        int((pixel_coordinates_landmark_mcp[1] + pixel_coordinates_landmark_wrist[1])/2))

            # dot = (int(pixel_coordinates_landmark_index_fingertip[0]), int(pixel_coordinates_landmark_index_fingertip[1]))
          
            inverse = inv((centroid))
            joints = inverse[1]
            angles = get_angle(joints, centroid)
            rotation = rotate(pixel_coordinates_landmark_thumbtip, pixel_coordinates_landmark_index_fingertip)

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
        
            image = cv2.circle(image, centroid[:2], radius=10, color=(0, 0, 255), thickness=-1)
            # image = cv2.putText(image, "Swivel angle:" + str(int(rotation)), (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            angle_depth = [int(angles[0]), int(angles[1]), depth_distance, distance, rotation]
            # print(f"Angle 1: {int(angles[0])}, Angle 2: {int(angles[1])}")
            print(f"Depth: {int(depth_distance)}")

        cv2.imshow('Detected Hands', cv2.flip(image, 1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
          cap.release()
          break
        
    except:
      print("OUT OF BOUNDS RERUN THE PROGRAM")
      pass

