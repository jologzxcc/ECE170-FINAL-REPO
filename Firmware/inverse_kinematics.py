import pyfabrik
import numpy as np
from vectormath import Vector2




initial_joint_positions = [Vector2(320, 480), Vector2(480, 240), Vector2(640, 0)]
tolerance = 0.02

fab = pyfabrik.Fabrik2D(initial_joint_positions, tolerance)

def inv(coordinate):
    fab.move_to(Vector2(coordinate))
    x = fab.angles_deg 
    return x, fab.joints

def get_angle(joints):

    hypotenuse_1 = np.sqrt((joints[1].x - joints[0].x) ** 2 + (joints[0].y - joints[1].y) ** 2)
    adjacent_1 = joints[1].x - joints[0].x
    angle_1 = 180 - np.arccos(adjacent_1/hypotenuse_1) * (180/np.pi)

    hypotenuse_2 = np.sqrt((joints[1].x - joints[2].x) ** 2 + (joints[1].y - joints[2].y) ** 2)
    adjacent_2 = joints[1].x - joints[2].x
    angle_2 = angle_1 - np.arccos(adjacent_2/hypotenuse_2) * (180/np.pi)

    if joints[2].y > joints[1].y:
        hypotenuse = np.sqrt((joints[1].x - joints[2].x) ** 2 + (joints[2].y - joints[1].y) ** 2)
        adjacent = joints[1].x - joints[2].x
        angle_2 = angle_1 + np.arccos(adjacent/hypotenuse) * (180/np.pi)

    if joints[1].y > 480:
        hypotenuse = np.sqrt((joints[1].x - joints[0].x) ** 2 + (joints[1].y - joints[0].y) ** 2)
        adjacent = joints[1].x - joints[0].x
        angle_1 = 180 + np.arccos(adjacent/hypotenuse) * (180/np.pi)

    

    return angle_1, angle_2

def normalized(value):
    normalized_value = 500 * np.tanh((1/1000) * value)
    return int(normalized_value)







