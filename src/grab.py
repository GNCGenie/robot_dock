import numpy as np
from time import sleep
from localisation_aruco import get_position
from arm_angle_calc import get_angles, transform
from Arm_Lib import Arm_Device

Arm = Arm_Device()
Arm.Arm_reset()
sleep(0.1)

home = np.array([90,90,90,90,90,0]) # Upright position
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
print("Arm angles (ang) : ", anglesdeg)

input("Press any key to go to position...")
Arm.Arm_serial_servo_write6_array(anglesdeg, 2000)
input("Press any key to close arm...")
Arm.Arm_serial_servo_write(6, 180, 1000)
