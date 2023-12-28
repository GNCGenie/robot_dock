import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds
from copy import deepcopy

def transform(inangles):
    theta = deepcopy(inangles)
    # Theta is in Radians
    l1 = 0.08285
    l2 = 0.08295
    l3 = 0.1842

    ##############################
    # Forward Kinematics
    ##############################
    alpha = np.array([0, np.pi/2, 0, 0, np.pi/2])
    a = np.array([0, 0, l1, l2, 0])
    d = np.array([0, 0, 0, 0, l3])
    theta[2] = theta[2] - np.pi/2
    theta[4] = theta[4] - np.pi/2

    T05 = np.eye(4)

    def fk1(alpha, a, d, theta, i):
        T = np.array([
            [np.cos(theta[i]), -np.sin(theta[i]), 0, a[i]],
            [np.sin(theta[i])*np.cos(alpha[i]),
             np.cos(theta[i])*np.cos(alpha[i]),
             -np.sin(alpha[i]), -np.sin(alpha[i])*d[i]],
            [np.sin(theta[i])*np.sin(alpha[i]),
             np.cos(theta[i])*np.sin(alpha[i]),
             np.cos(alpha[i]), np.cos(alpha[i])*d[i]],
            [0, 0, 0, 1]
            ])
        return T

    # T05 = T01 * T12 * T23 * T34 * T45
    for i in range(5):
        T = fk1(alpha, a, d, theta, i)
        T05 = np.dot(T05, T)

    return T05[0:3,3]

# Function to calculate angles by minimizing distance between arm and target
def get_angles(position):

    # Distance between arm and target
    def distance(theta):
        return np.linalg.norm(transform(theta) - position)

    # Bounds on angles the arm can take
    lower = [.0,    0.10*np.pi, 0.10*np.pi, 0.10*np.pi, .0,    .0]
    upper = [np.pi, 0.90*np.pi, 0.90*np.pi, 0.90*np.pi, np.pi, .0]

    init_guess = np.ones(6)*np.pi/2
    result = minimize(distance, init_guess, method='SLSQP',
            bounds = Bounds(lb=lower,ub=upper), tol=1e-9,
            options={'disp': True})

    return result.x # Theta is in Radians

##############################
# Testing
##############################

#targetpos = np.random.rand(3)/5
#print(targetpos)
#angles = getAngles(targetpos)
#print(angles)
#print(transform(angles))
