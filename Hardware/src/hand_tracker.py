import cv2
import mediapipe as mp
import numpy as np
import time

from pySerialTransfer import pySerialTransfer as txfer
from inverse_kinematics import inv, scaled_angles


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
class_and_coordinates = ""

seconds = time.time()

if __name__ == '__main__':

    with mp_hands.Hands(
            max_num_hands = 1,
            model_complexity = 0,
            min_detection_confidence = 0.5,
            min_tracking_confidence = 0.5) as hands:

        try:
            link = txfer.SerialTransfer('COM3')
            link.open()
            time.sleep(2) 

            while cap.isOpened():
                send_size = 0
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
                        angle_depth = [int(angles[0]), int(angles[1]), depth, int(distance)]
                        cv2.imshow('Detected Hands', cv2.flip(image, 1))

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            cap.release()
                            break

                        list_ = angle_depth
                        list_size = link.tx_obj(list_)
                        send_size += list_size
                        link.send(send_size)

                        while not link.available():
                            if link.status < 0:
                                if link.status == txfer.CRC_ERROR:
                                    print('ERROR: CRC_ERROR')
                                elif link.status == txfer.PAYLOAD_ERROR:
                                    print('ERROR: PAYLOAD_ERROR')
                                elif link.status == txfer.STOP_BYTE_ERROR:
                                    print('ERROR: STOP_BYTE_ERROR')
                                else:
                                    print('ERROR: {}'.format(link.status))
                        
                        rec_list_  = link.rx_obj(obj_type=type(list_),
                                obj_byte_size=list_size,
                                list_format='i')

                        print('SENT: {}'.format(list_))
                        print('RCVD: {}'.format(rec_list_))
                        print(' ')  
    
        except KeyboardInterrupt:
            try:
                link.close()
            except:
                pass
        
        except:
            import traceback
            traceback.print_exc()
            
            try:
                link.close()
            except:
                pass

           