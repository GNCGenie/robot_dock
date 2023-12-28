##################################################
# Load all libraries required for grabbing target
##################################################
# Ensure numpy as available in virtual environment
import numpy as np
from time import sleep

# Import library for arm control, specific to DOFBOT
from Arm_Lib import Arm_Device

# All local files should be in same directory for import
'''
/src/localisation_aruco.py
/src/arm_angle_calc.py
/src/grab.py
'''
from localisation_aruco import get_position
from arm_angle_calc import get_angles, transform

Arm = Arm_Device() # Create arm object for moving arm
Arm.Arm_reset() # Reset arm
sleep(0.1) # Wait for arm to reset

home = np.array([90,90,90,90,90,0]) # Upright position
'''
Robot angles are defined as :
    theta[0] : Joint 1, base rotation
    theta[1] : Joint 2, shoulder
    theta[2] : Joint 3, elbow
    theta[3] : Joint 4, wrist
    theta[4] : Joint 5, gripper rotation
    theta[5] : Joint 6, gripper close and open
'''
Arm.Arm_serial_servo_write6_array(home, 1000) # Return arm to home position
sleep(1)

pos = get_position() # Position w.r.t. Camera origin
pos[1],pos[2] = pos[2], pos[1] # Switch Y & Z axis
pos[0] = -pos[0] # Flip X axis sign
pos += [0.03, 0.04, -0.08] # Position of camera w.r.t. Robot Arm Base
print("Target Position : ", pos)

anglesrad = get_angles(pos) # Minimise distance between arm and target
anglesdeg = np.array(anglesrad) * 180/np.pi # Robot arm takes angles in degrees
print("Going to position : " , transform(anglesrad))
print("Arm angles (deg) : ", anglesdeg)

input("Press any key to go to position...")
Arm.Arm_serial_servo_write6_array(anglesdeg, 2000) # Go to target position
input("Press any key to close arm...")
Arm.Arm_serial_servo_write(6, 180, 1000)
