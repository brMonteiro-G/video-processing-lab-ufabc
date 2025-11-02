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

def CannyThreshold(val):
    if frame_gray is None or current_frame is None:
        return
    
    low_threshold = val
    img_blur = cv2.blur(frame_gray, (3,3))
    detected_edges = cv2.Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)
    mask = detected_edges != 0
    dst = current_frame * (mask[:,:,None].astype(current_frame.dtype))
    cv2.imshow(window_name, dst)

# Create video capture object
vid_capture = cv2.VideoCapture("rtmp://localhost:1935/stream/mystream")
ksize, sigma = 7, 1.5

if (vid_capture.isOpened() == False):
    print("Error opening the video stream")
    exit(0)

# Create windows and trackbar
cv2.namedWindow('Original')
cv2.namedWindow(window_name)
cv2.createTrackbar(title_trackbar, window_name, 0, max_lowThreshold, CannyThreshold)

while(vid_capture.isOpened()):
    ret, frame = vid_capture.read()
    if ret == True:
        # Update global frames for Canny processing
        current_frame = cv2.GaussianBlur(frame, (ksize, ksize), sigma)
        frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        
        # Show original frame
        cv2.imshow('Original', frame)
        
        # Update Canny edge detection
        CannyThreshold(cv2.getTrackbarPos(title_trackbar, window_name))
        
        # Wait for key press
        k = cv2.waitKey(20)
        if k == 113:  # 'q' key
            break
    else:
        break

# Release resources
vid_capture.release()
cv2.destroyAllWindows()