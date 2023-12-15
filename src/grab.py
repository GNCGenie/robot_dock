import numpy as np
from time import sleep
from localisation_aruco import getPosition
from arm_angle_calc import getAngles, transform
from armcontrol import ArmMove

home = np.array([np.pi/2,.0,np.pi/2,np.pi/2,np.pi/2])
print("Home Postion : ", home)
ArmMove(home)
sleep(5)

pos = np.array([0.35,0.0,0.0])
#pos = getPosition()
#print("Target Position : ", pos)
angles = getAngles(pos)
angles = np.array(angles)

print("Arm angles   : ", angles)
print("Arm final position : ", transform(angles))
ArmMove(angles)
