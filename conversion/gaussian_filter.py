import cv2
import numpy as np

# Global variables for Canny edge detection
max_lowThreshold = 100
window_name = 'Edge Map'
title_trackbar = 'Min Threshold:'
ratio = 3
kernel_size = 3
frame_gray = None
current_frame = None

# Create video capture object
vid_capture = cv2.VideoCapture("rtmp://localhost:1935/stream/mystream")
ksize, sigma = 7, 1.5

if (vid_capture.isOpened() == False):
    print("Error opening the video stream")
    exit(0)

# Create windows and trackbar
cv2.namedWindow('Original')
cv2.namedWindow(window_name)

while(vid_capture.isOpened()):
    ret, frame = vid_capture.read()
    if ret == True:
        # Update global frames for Canny processing
        current_frame = cv2.GaussianBlur(frame, (ksize, ksize), sigma)

        # Show original frame
        cv2.imshow('Original', frame)

        # Show original frame
        cv2.imshow('GaussianBlur', current_frame)
        
        
        # Wait for key press
        k = cv2.waitKey(20)
        if k == 113:  # 'q' key
            break
    else:
        break

# Release resources
vid_capture.release()
cv2.destroyAllWindows()