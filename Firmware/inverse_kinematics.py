from ntpath import join
import pyfabrik
import numpy as np
from vectormath import Vector2

def inv(coordinate):
    if(coordinate[0] < 320):
        initial_joint_positions = [Vector2(320, 480), Vector2(480, 240), Vector2(640, 0)] #[Vector2(320, 480), Vector2(380, 270), Vector2(440, 60)]
        tolerance = 0.02
        fab = pyfabrik.Fabrik2D(initial_joint_positions, tolerance)
        fab.move_to(Vector2(coordinate))
        x = fab.angles_deg

    else: 
        initial_joint_positions = [Vector2(320, 480), Vector2(160, 240), Vector2(0, 0)]#[Vector2(320, 480), Vector2(180, 270), Vector2(40, 60)]
        tolerance = 0.02
        fab = pyfabrik.Fabrik2D(initial_joint_positions, tolerance)
        fab.move_to(Vector2(coordinate))
        x = fab.angles_deg

    return x, fab.joints



def get_angle(joints, coordinate):
    if(coordinate[0] < 320):
        hypotenuse_1 = np.sqrt((joints[1].x - joints[0].x) ** 2 + (joints[0].y - joints[1].y) ** 2)
        adjacent_1 = joints[1].x - joints[0].x
        angle_0 = np.arccos(adjacent_1/hypotenuse_1) * (180/np.pi)
        angle_1 = 180 - angle_0

        if joints[2].y > joints[1].y:
            hypotenuse = np.sqrt((joints[1].x - joints[2].x) ** 2 + (joints[2].y - joints[1].y) ** 2)
            adjacent = joints[1].x - joints[2].x
            angle_12 = np.arccos(adjacent/hypotenuse) * (180/np.pi)
            angle_13 = angle_1 - 90
            angle_2 = 45 + angle_13 + 180 + angle_12
        
        else:
            hypotenuse_2 = np.sqrt((joints[1].x - joints[2].x) ** 2 + (joints[1].y - joints[2].y) ** 2)
            adjacent_2 = joints[1].x - joints[2].x
            angle_12 = np.arccos(adjacent_2/hypotenuse_2) * (180/np.pi)
            angle_13 = 180 - angle_0 - 90
            angle_2 = 45 + angle_13 + angle_0 + angle_1 - angle_12
        
    if(coordinate[0] >= 320):
        hypotenuse_1 = np.sqrt((joints[1].x - joints[0].x) ** 2 + (joints[0].y - joints[1].y) ** 2)
        adjacent_1 = joints[1].x - joints[0].x
        angle_0 = np.arccos(adjacent_1/hypotenuse_1) * (180/np.pi)
        angle_1 = 180 - angle_0

        if joints[2].y > joints[1].y:
            hypotenuse = np.sqrt((joints[2].x - joints[1].x) ** 2 + (joints[2].y - joints[1].y) ** 2)
            adjacent = joints[2].x - joints[1].x
            angle_12 = np.arccos(adjacent/hypotenuse) * (180/np.pi)
            angle_2 = angle_1 - angle_12 - 45

        else:
            hypotenuse_2 = np.sqrt((joints[2].x - joints[1].x) ** 2 + (joints[1].y - joints[2].y) ** 2)
            adjacent_2 = joints[2].x - joints[1].x
            angle_12 = np.arccos(adjacent_2/hypotenuse_2) * (180/np.pi)
            angle_2 = angle_12 + (180 - angle_0) - 45
        
        if angle_2 < 0:
            angle_2 = 0
        
    return angle_1, angle_2

def normalized(value):
    normalized_value = 100 * np.tanh((1/100) * value)
    if value < 0:
        normalized_value = 0
    return int(normalized_value)

def rotate(thumbtip, indextip):

    hypotenuse = np.sqrt((thumbtip[0] - indextip[0]) ** 2 + (thumbtip[1] - indextip[1]) ** 2)
    adjacent = thumbtip[0] - indextip[0]
    angle = np.arccos(adjacent/hypotenuse) * (180/np.pi)
    return angle

def distance_depth(wrist, base_finger):
    dist = np.sqrt((wrist[0] - base_finger[0]) ** 2 + (wrist[1] - base_finger[1]) ** 2) - 55
    return dist



    









