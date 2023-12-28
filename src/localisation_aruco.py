import numpy as np
import cv2 as cv
import time

def get_position():

    # Open camera connected to device 0
    video_file = '/dev/video0'
    video = cv.VideoCapture(video_file)
    assert video.isOpened(), "Camera Stream Error"

    # K and d matrices for IMX335
    K = np.float32([[1.23637547e+03, 0.00000000e+00, 2.94357998e+02],
                    [0.00000000e+00, 1.22549758e+03, 2.20521015e+02],
                    [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    d = np.float32([-1.5209742,   2.46986782,  0.07634431,  0.07220847,  1.9630171 ])

    # Define marker size and dictionary for aruco detection
    markersize = 0.03
    aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
    aruco_params = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(aruco_dict, aruco_params)

    ##############################
    # Aruco detection
    ##############################
    '''
    The code runs for 1 second and then stops. The average position of the
    markers is taken as the target position.
    
    On the first run, the code sets the target position equal to the average
    Later on it takes moving average of the target position
    '''
    t = np.zeros(3) # Initial target position, on first run, will be overwritten
    alpha = 0.9 # Kalman filter parameter (Moving average)
    start_time = time.time()

    ##############################
    # Take readings for 1 second
    ##############################
    while time.time() - start_time < 1:
        valid, image = video.read()
        if not valid:
            break

        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # Convert to grayscale
        corners, ids, rejected = detector.detectMarkers(gray_image) # Detect markers
        tobs = np.zeros(3)
        if ids is not None: # If markers are detected
            for i in range(len(corners)): # For each marker
                _, tvec, _ = cv.aruco.estimatePoseSingleMarkers(corners[i], markersize, K, d)
                tobs += tvec.flatten() # Add marker position to total

            tobs /= len(corners) # Average marker positions
            if not np.any(t): # If first run set target equal to position
                t = tobs
            t = alpha*t + (1-alpha)*tobs # Moving average

    video.release() # Close camera
    t[2] = 0.3942*t[2] + 0.02 # Z position Calibrated for IMX335 lens
    return t
