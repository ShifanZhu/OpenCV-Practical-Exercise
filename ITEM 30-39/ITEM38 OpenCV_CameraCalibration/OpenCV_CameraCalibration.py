#!/usr/bin/env python

import cv2
import numpy as np
import glob

def get_frames(video_file):
    cap = cv2.VideoCapture(video_file)
    
    if not cap.isOpened():
        print("Error opening video stream or file")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame

    cap.release()
    cv2.destroyAllWindows()

# Defining the dimensions of checkerboard
CHECKERBOARD = (8,6)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Creating vector to store vectors of 3D points for each checkerboard image
objpoints = []
# Creating vector to store vectors of 2D points for each checkerboard image
imgpoints = [] 


# Defining the world coordinates for 3D points
objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

gray = None

images = glob.glob('./images/*.jpg')

# Extracting path of individual image stored in a given directory


# From video
cnt_save = 0
for fname in get_frames('chessboard.avi'):
    cnt_save = cnt_save + 1
    if cnt_save % 10 != 0:
        continue
    print('cnt = ', cnt_save)
    # img = cv2.imread(fname)
    img = fname
    

# From images
# for fname in images:
#     img = cv2.imread(fname)




    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # If desired number of corners are found in the image then ret = true
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+
    	cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
    
    """
    If desired number of corner are detected,
    we refine the pixel coordinates and display 
    them on the images of checker board
    """
    if ret == True:
        objpoints.append(objp)
        # refining pixel coordinates for given 2d points.
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2,ret)
    
    #cv2.imshow('img',img)
    #cv2.waitKey(0)

cv2.destroyAllWindows()

# h,w = img.shape[:2]

"""
Performing camera calibration by 
passing the value of known 3D points (objpoints)
and corresponding pixel coordinates of the 
detected corners (imgpoints)
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
print("rvecs : \n")
print(rvecs)
print("tvecs : \n")
print(tvecs)


# 0 -- this
# [[377.15617416   0.         314.37004072]
#  [  0.         377.04656492 244.82744548]
#  [  0.           0.           1.        ]]
# [[-0.05555919  0.02769264 -0.00136252 -0.00150069  0.00753809]]

# 1
# [[379.68442303   0.         315.4618254 ]
#  [  0.         379.36436083 245.56179639]
#  [  0.           0.           1.        ]]
# [[-0.05432558  0.036466   -0.00151437 -0.0015278  -0.00126632]]

# 2
# [[381.68926054   0.         317.5112728 ]
#  [  0.         381.37352646 249.54567462]
#  [  0.           0.           1.        ]]
# [[-0.0628898   0.0613293   0.00019191  0.00052524 -0.01467109]]

# 0 -- kalibr
# distortion_coeffs: [-0.09890296366599262, 0.30114215986711335, -0.00032231761415806894, 0.002357310348509497]
# intrinsics: [376.68023480196206, 376.65799408400954, 318.5991620301586, 245.2711702226122]

# 1
# distortion_coeffs: [-0.13015291545901225, 0.1995964953236916, -0.0034277465087109702, -0.016953927207494137]
# intrinsics: [382.7009632324603, 384.88861703104453, 315.31649834927583, 243.4097426969524]

# 2
# distortion_coeffs: [-0.060378158504629166, 0.0420190504988976, -0.00021827163036562553, 0.0010279151127056275]
# intrinsics: [381.8885309653513, 381.51960052390865, 318.6555011308029, 249.72661960229894]


# Realsense
#   PPX:        	316.609558105469
#   PPY:        	248.536376953125
#   Fx:         	380.225982666016
#   Fy:         	379.800872802734
#   Distortion: 	Inverse Brown Conrady
#   Coeffs:     	-0.0582379177212715  	0.0692759975790977  	0.000362122984370217  	-0.000120137752674054  	-0.0220816992223263




# [[434.61422334   0.         476.89422231]
#  [  0.         433.09332771 285.38447351]
#  [  0.           0.           1.        ]]
# dist : 

# [[-3.04116802e-01  1.35821112e-01  8.61264005e-04 -7.56463380e-05
#   -3.45892737e-02]]



# [[434.61684768   0.         476.70014749]
#  [  0.         433.25361169 286.44239539]
#  [  0.           0.           1.        ]]
# dist : 

# [[-3.04633266e-01  1.38192568e-01  7.91648999e-04 -1.71549566e-04
#   -3.64213918e-02]]