import cv2
import numpy as np
import os
from datetime import datetime

# Define color ranges (initial values)
colors = {
    'red': {
        'name': 'Red',
        'ranges': [(0, 50, 50), (10, 255, 255)],  # Red has two ranges in HSV
        'ranges2': [(170, 50, 50), (180, 255, 255)],
        'color': (0, 0, 255),  # BGR color for visualization
        'mask': None
    },
    'blue': {
        'name': 'Blue',
        'ranges': [(100, 50, 50), (130, 255, 255)],
        'color': (255, 0, 0),
        'mask': None
    },
    'green': {
        'name': 'Green',
        'ranges': [(40, 50, 50), (80, 255, 255)],
        'color': (0, 255, 0),
        'mask': None
    },
    'yellow': {
        'name': 'Yellow',
        'ranges': [(20, 50, 50), (40, 255, 255)],
        'color': (0, 255, 255),
        'mask': None
    }
}

# Recording state
is_recording = False
out_original = None
out_threshold = None

# Create output directories
output_dir = os.path.join(os.path.dirname(__file__), 'output')
images_dir = os.path.join(output_dir, 'images')
videos_dir = os.path.join(output_dir, 'videos')
os.makedirs(images_dir, exist_ok=True)
os.makedirs(videos_dir, exist_ok=True)

def create_trackbars(color_name, color_data):
    window_name = f'{color_data["name"]} Controls'
    cv2.namedWindow(window_name)
    
    def on_trackbar(val, param):
        range_id = 0 if param.startswith('low') else 1
        channel = param[-1]
        channel_id = {'H': 0, 'S': 1, 'V': 2}[channel]
        
        if param.startswith('low'):
            colors[color_name]['ranges'][0][channel_id] = val
        else:
            colors[color_name]['ranges'][1][channel_id] = val
    
    # Create trackbars for each HSV channel
    for param in ['low_H', 'high_H', 'low_S', 'high_S', 'low_V', 'high_V']:
        initial_value = (colors[color_name]['ranges'][0] if param.startswith('low') else colors[color_name]['ranges'][1])[0 if param.endswith('H') else 1 if param.endswith('S') else 2]
        max_value = 180 if param.endswith('H') else 255
        cv2.createTrackbar(param, window_name, initial_value, max_value, lambda x, p=param: on_trackbar(x, p))

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def save_frame(frame, window_name):
    timestamp = get_timestamp()
    filename = f"{window_name}_{timestamp}.jpg"
    filepath = os.path.join(images_dir, filename)
    cv2.imwrite(filepath, frame)
    print(f"Saved {filename}")

def start_recording(frame_size):
    global out_original, out_threshold, is_recording
    timestamp = get_timestamp()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    original_path = os.path.join(videos_dir, f'original_{timestamp}.avi')
    threshold_path = os.path.join(videos_dir, f'threshold_{timestamp}.avi')
    out_original = cv2.VideoWriter(original_path, fourcc, 20.0, frame_size)
    out_threshold = cv2.VideoWriter(threshold_path, fourcc, 20.0, frame_size)
    is_recording = True
    print("Started recording...")

def stop_recording():
    global out_original, out_threshold, is_recording
    if is_recording:
        out_original.release()
        out_threshold.release()
        out_original = None
        out_threshold = None
        is_recording = False
        print("Stopped recording...")

# Create video capture object
vid_capture = cv2.VideoCapture("rtmp://localhost:1935/stream/mystream")

if not vid_capture.isOpened():
    print("Error opening video stream")
    exit(0)

# Create trackbars for each color
for color_name, color_data in colors.items():
    create_trackbars(color_name, color_data)

print("Controls:")
print("Press 's' to save current frames")
print("Press 'k' to start recording")
print("Press 'h' to stop recording")
print("Press 'q' to quit")

while vid_capture.isOpened():
    ret, frame = vid_capture.read()
    if not ret:
        break

    # Convert to HSV
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a copy for visualization
    result_frame = frame.copy()
    combined_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    
    # Process each color
    for color_name, color_data in colors.items():
        window_name = f'{color_data["name"]} Controls'
        
        # Get current trackbar values
        low_H = cv2.getTrackbarPos('low_H', window_name)
        high_H = cv2.getTrackbarPos('high_H', window_name)
        low_S = cv2.getTrackbarPos('low_S', window_name)
        high_S = cv2.getTrackbarPos('high_S', window_name)
        low_V = cv2.getTrackbarPos('low_V', window_name)
        high_V = cv2.getTrackbarPos('high_V', window_name)
        
        # Create mask for this color
        mask = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
        
        # For red color, add second range
        if color_name == 'red':
            mask2 = cv2.inRange(frame_HSV, colors['red']['ranges2'][0], colors['red']['ranges2'][1])
            mask = cv2.bitwise_or(mask, mask2)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw contours and add text for each detected object
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Filter small contours
                cv2.drawContours(result_frame, [contour], -1, color_data['color'], 2)
                M = cv2.moments(contour)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    cv2.putText(result_frame, color_data['name'], (cx-20, cy), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_data['color'], 2)
        
        # Show individual color detection
        cv2.imshow(f'{color_data["name"]} Detection', mask)
        
        # Add to combined mask
        combined_mask = cv2.bitwise_or(combined_mask, mask)
    
    # Show results
    cv2.imshow('Original', frame)
    cv2.imshow('Multiple Color Detection', result_frame)
    cv2.imshow('Combined Mask', combined_mask)

    # Record frames if recording is active
    if is_recording:
        out_original.write(frame)
        out_threshold.write(cv2.cvtColor(combined_mask, cv2.COLOR_GRAY2BGR))

        

    # Handle key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        save_frame(frame, 'original')
        save_frame(result_frame, 'detection')
        save_frame(combined_mask, 'mask')
    elif key == ord('k') and not is_recording:
        start_recording(frame.shape[1::-1])
    elif key == ord('h'):
        stop_recording()

# Cleanup
stop_recording()
vid_capture.release()
cv2.destroyAllWindows()