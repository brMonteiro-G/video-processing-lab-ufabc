Lab_3_Color Space

(1) Study the theory of color conversion.
Color conversions :
https://docs.opencv.org/4.x/de/d25/imgproc_color_conversions.html

Most commonly used conversions: RGB <-> GRAY, RGB <-> YCrCb, RGB <-> HSV, and Bayer -> RGB

(2) Study this program which performs the change from RGB to HSV color space, and run the program with the webcam and colored objects. Additionally, carefully study the inRange function in the program:
Thresholding Operations using inRange
https://docs.opencv.org/4.x/da/d97/tutorial_threshold_inRange.html

Analyze the detection of at least three colored objects, the HSV value range for each case, and the corresponding RGB value.

(2.a) Modify this program to filter the webcam input image with a Gaussian filter before converting it to HSV space. Additionally, the program should create an extra window to show the unfiltered and filtered images side-by-side. Analyze the effect of the Gaussian filter with at least three colored objects.

 

(2.b) Develop a new program (new folder), modifying the program created in item (2.a) so that the filtered image is submitted to the CANNY detector. Therefore, the team must first study the Canny detector.

https://docs.opencv.org/4.x/da/d5c/tutorial_canny_detector.html

Therefore, the new program should create an additional window to display the filtered image and the image from the Canny detector. Analyze the best Canny detector configuration, with at least three colored objects.


(2.c) Modify the program from item (2.b) to include the function to save the image of open windows when the [s] key is pressed, and the function to record videos of the windows using the [k] key to start recording and the [h] key to stop recording these videos. These videos should demonstrate the tracking of the movement of colored objects. Analyze these videos.


(3) Team exercise:
Develop a program to find and extract more than one colored object in an image, for example, extract red, blue and green objects simultaneously (or any other color combinations).