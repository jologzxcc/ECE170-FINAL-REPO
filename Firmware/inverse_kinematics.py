import pyfabrik
from vectormath import Vector2
initial_joint_positions = [Vector2(0, 0), Vector2(350, 265), Vector2(550, 415), Vector2(650, 490)]
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
            new_angles.append(angle + 90)
        else: 
            new_angles.append(angle + 90)
    
    str_angles = ' '.join([str(elem) for elem in new_angles])
    
    return str_angles




