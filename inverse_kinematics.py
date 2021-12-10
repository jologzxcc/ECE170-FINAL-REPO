import pyfabrik
from vectormath import Vector2, Vector3

initial_joint_positions = [Vector2(0, 0), Vector2(350, 265), Vector2(550, 415), Vector2(650, 490)]
tolerance = 0.02

# Initialize the Fabrik class (Fabrik, Fabrik2D or Fabrik3D)
fab = pyfabrik.Fabrik2D(initial_joint_positions, tolerance)

def inv(coor):
    fab.move_to(Vector2(coor))
    x = fab.angles_deg # Holds [0.0, 0.0, 0.0]
    return x, fab.joints


