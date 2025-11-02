import cv2




def timestamp_filename():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def process_mask(mask, color, label, result):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 400:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(result, (x, y), (x + w, y + h), color, 2)
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(result, (cx, cy), 4, color, -1)
            cv2.putText(result, label, (x, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)



# Create a video capture object
# vid_capture = cv2.VideoCapture(0) will work fine, but generates a warning.
# A bug, Direct show flag solves it.
vid_capture = cv2.VideoCapture("rtmp://host.docker.internal:1935/stream/mystream")


if(vid_capture.isOpened() == False):
	print("Error opening video stream")

# Get height and width of the frame
#CAP_PROP_FRAME_WIDTH =3, CAP_PROP_FRAME_HEIGHT =4
frame_width = int(vid_capture.get(3))
frame_height = int(vid_capture.get(4))
frame_size = (frame_width,frame_height)
fps = 20
ksize, sigma = 7, 1.5


# Create a video writer object
output = cv2.VideoWriter('Resources/output_video_from_web_cam.avi', cv2.VideoWriter_fourcc('M','J','P','G'), fps, frame_size)

while(vid_capture.isOpened()):
	# vCapture.read() methods returns a tuple, first element is a bool 
	# and the second is frame
	ret, frame = vid_capture.read()

	if ret == True:
		output.write(frame)


		cv2.imshow("Frame",cv2.Canny(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 50, 150))

		# k == 113 is ASCII code for q key. You can try to replace that 
		# with any key with its corresponding ASCII code, try 27 which is for ESCAPE
		key = cv2.waitKey(20)
		if key == ord('q'):
			break
	else:
		print('Web camera is disconnected')
		break
# Release the video capture and output objects.
vid_capture.release()
output.release()
cv2.destroyAllWindows()