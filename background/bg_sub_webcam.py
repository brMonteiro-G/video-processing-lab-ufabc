import cv2
import numpy as np
import os

def process_video(video_path, mode="fast"):
    """
    mode: "fast" or "slow"
    """

    # Define configuration presets
    if mode == "fast":
        config = {
            "min_brightness": 30,
            "max_brightness": 220,
            "min_area": 800,
            "learning_rate": 0.7,   # higher = fast adaptation
            "bg_thresh": 900,       # sensitive to motion
            "morph_kernel": (3, 3)
        }
    elif mode == "slow":
        config = {
            "min_brightness": 40,
            "max_brightness": 180,
            "min_area": 1200,
            "learning_rate": 0.05,  # slower background adaptation
            "bg_thresh": 300,       # less sensitive to background variation
            "morph_kernel": (7, 7)
        }
    else:
        raise ValueError("Mode must be 'fast' or 'slow'.")

    # Load video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Cannot open video: {video_path}")
        return

    # Get frame size and FPS
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
    frame_size = (frame_width, frame_height)

    # Ensure output directory exists
    os.makedirs("./outputs", exist_ok=True)

    # Define output path and writer
    output_path = f'./outputs/webcam_output_video.avi'
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')    
    output = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    # Initialize background subtractor
    mog = cv2.createBackgroundSubtractorKNN(detectShadows=False)
    mog.setDist2Threshold(config["bg_thresh"])

    print(f"▶ Processing {mode.upper()} mode... Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Brightness mask
        mask = cv2.inRange(gray, config["min_brightness"], config["max_brightness"])
        gray_masked = cv2.bitwise_and(gray, gray, mask=mask)

        # Apply background subtraction
        fgmask = mog.apply(gray_masked, learningRate=config["learning_rate"])

        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, config["morph_kernel"])
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        fgmask = cv2.dilate(fgmask, kernel, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw results
        result = frame.copy()
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < config["min_area"]:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(result, f'Area: {int(area)}', (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convert fgmask to BGR before saving
        fg_bgr = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
        output.write(fg_bgr)

        # Display
        cv2.imshow(f'Motion Detection ({mode.upper()})', fgmask)
        cv2.imshow(f'Result ({mode.upper()})', result)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    output.release()
    cv2.destroyAllWindows()
    print(f"✅ Output saved to {output_path}")


# -----------------------------
# Run both modes separately
# -----------------------------

process_video("rtmp://localhost:1935/stream/mystream", mode="fast")
