import cv2
import numpy as np

# HSV range variables
max_value = 255
max_value_H = 180
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_detection_name = 'HSV Color Detection'

# Trackbar callback functions
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos('Low H', window_detection_name, low_H)

def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos('High H', window_detection_name, high_H)

def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos('Low S', window_detection_name, low_S)

def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos('High S', window_detection_name, high_S)

def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos('Low V', window_detection_name, low_V)

def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos('High V', window_detection_name, high_V)

# Create video capture object
vid_capture = cv2.VideoCapture("rtmp://localhost:1935/stream/mystream")

if not vid_capture.isOpened():
    print("Error opening video stream")
    exit(0)

# Create windows and trackbars
cv2.namedWindow(window_detection_name)
cv2.createTrackbar('Low H', window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
cv2.createTrackbar('High H', window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
cv2.createTrackbar('Low S', window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
cv2.createTrackbar('High S', window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
cv2.createTrackbar('Low V', window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
cv2.createTrackbar('High V', window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)

while vid_capture.isOpened():
    ret, frame = vid_capture.read()
    if not ret:
        break

    # Convert to HSV
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get current trackbar values
    low_H = cv2.getTrackbarPos('Low H', window_detection_name)
    high_H = cv2.getTrackbarPos('High H', window_detection_name)
    low_S = cv2.getTrackbarPos('Low S', window_detection_name)
    high_S = cv2.getTrackbarPos('High S', window_detection_name)
    low_V = cv2.getTrackbarPos('Low V', window_detection_name)
    high_V = cv2.getTrackbarPos('High V', window_detection_name)

    # Create HSV mask
    frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    print(f"Low HSV: ({low_H}, {low_S}, {low_V}) - High HSV: ({high_H}, {high_S}, {high_V})")
    rgb = cv2.cvtColor(np.uint8([[[low_H, low_S, low_V]]]), cv2.COLOR_HSV2BGR)[0][0]
    print(f"Low HSV in RGB: ({rgb[2]}, {rgb[1]}, {rgb[0]})")


    # Show results
    cv2.imshow('Original', frame)
    cv2.imshow(window_detection_name, frame_threshold)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid_capture.release()
cv2.destroyAllWindows()