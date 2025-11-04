import cv2
import numpy as np

# Window names
original_window = 'Original'
blur_window = 'GaussianBlur'

# Trackbar names
kernel_trackbar = 'Kernel Size (must be odd)'
sigma_trackbar = 'Sigma'

# Initial values
max_kernel = 21  # Maximum kernel size
max_sigma = 10   # Maximum sigma value
initial_kernel = 3  # Starting with less blur
initial_sigma = 1.0

def update_blur(frame):
    # Get current values (kernel must be odd)
    k = cv2.getTrackbarPos(kernel_trackbar, blur_window)
    k = k if k % 2 == 1 else k + 1
    s = cv2.getTrackbarPos(sigma_trackbar, blur_window) / 10.0
    
    # Apply blur
    blurred = cv2.GaussianBlur(frame, (k, k), s)
    return blurred

# Create video capture object
vid_capture = cv2.VideoCapture("rtmp://localhost:1935/stream/mystream")

if not vid_capture.isOpened():
    print("Error opening video stream")
    exit(0)

# Create windows and trackbars
cv2.namedWindow(original_window)
cv2.namedWindow(blur_window)

# Create trackbars
cv2.createTrackbar(kernel_trackbar, blur_window, initial_kernel, max_kernel, lambda x: None)
cv2.createTrackbar(sigma_trackbar, blur_window, int(initial_sigma * 10), max_sigma * 10, lambda x: None)

print("\nGaussian Blur Controls:")
print("- Kernel Size: Controls the blur area (bigger = more blur)")
print("- Sigma: Controls blur intensity (bigger = more blur)")
print("\nTry moving colorful objects and observe:")
print("1. Small kernel (3x3) + small sigma (0.5): Slight noise reduction")
print("2. Medium kernel (7x7) + medium sigma (1.5): Motion blur")
print("3. Large kernel (21x21) + large sigma (5.0): Heavy blur")
print("\nPress 'q' to quit")

while vid_capture.isOpened():
    ret, frame = vid_capture.read()
    if ret:
        # Apply Gaussian blur with current parameters
        blurred = update_blur(frame)
        
        # Show difference between original and blurred
        difference = cv2.absdiff(frame, blurred)
        
        # Show all frames
        cv2.imshow(original_window, frame)
        cv2.imshow(blur_window, blurred)
        cv2.imshow('Difference', difference)
        
        # Wait for key press
        k = cv2.waitKey(20)
        if k == ord('q'):
            break
    else:
        break

vid_capture.release()
cv2.destroyAllWindows()