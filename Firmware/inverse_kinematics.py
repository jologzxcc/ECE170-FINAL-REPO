import pyfabrik
import numpy as np
from vectormath import Vector2




initial_joint_positions = [Vector2(320, 480), Vector2(610, 240), Vector2(900, 0)]
tolerance = 0.02

fab = pyfabrik.Fabrik2D(initial_joint_positions, tolerance)

def inv(coor):
    fab.move_to(Vector2(coor))
    x = fab.angles_deg 
    return x, fab.joints

def scaled_angles(orig_angles):
    new_angles = []
    for angle in orig_angles:
        if angle >= 0: 
            new_angles.append(round(angle + 90))
        else: 
            new_angles.append(round(angle + 90))
    
    # str_angles = ' '.join([str(elem) for elem in new_angles[:-1]])
    
    return new_angles


def normalized(value):
    normalized_value = 500 * np.tanh((1/1000) * value)
    return int(normalized_value)







