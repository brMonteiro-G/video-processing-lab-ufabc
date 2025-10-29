// lab3_rtmp_color.cpp
// Compile with CMake (use previous CMakeLists.txt). No CLI args; RTMP URL hardcoded.
// Features: RTMP capture, Gaussian blur, HSV color extraction (R/G/B), Canny, save images (s),
// start recording (k), stop recording (h), quit (q/ESC).

#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <iomanip>

using namespace cv;
using namespace std;

static string timestamp_filename() {
    auto now = chrono::system_clock::now();
    time_t tt = chrono::system_clock::to_time_t(now);
    std::tm tm;
#if defined(_WIN32) || defined(_WIN64)
    localtime_s(&tm, &tt);
#else
    localtime_r(&tt, &tm);
#endif
    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y%m%d_%H%M%S");
    return oss.str();
}

int main() {
    // Hardcoded RTMP stream (no args)
    const string stream_url = "rtmp://host.docker.internal:1935/stream/mystream";

    VideoCapture cap(stream_url);
    if (!cap.isOpened()) {
        cerr << "Error: cannot open video source: " << stream_url << endl;
        return -1;
    }

    // Get basic properties
    int frame_width = static_cast<int>(cap.get(CAP_PROP_FRAME_WIDTH));
    int frame_height = static_cast<int>(cap.get(CAP_PROP_FRAME_HEIGHT));
    double fps = cap.get(CAP_PROP_FPS);
    if (!(fps > 0)) fps = 20.0; // fallback

    cout << "Opened stream: " << frame_width << "x" << frame_height << " @ " << fps << " FPS\n";

    // Prepare windows
    const string win_side = "Original | Filtered";
    const string win_mask  = "Masks (B/G/R)";
    const string win_result = "Detected Objects";
    const string win_canny = "Canny";
    namedWindow(win_side, WINDOW_NORMAL);
    namedWindow(win_mask, WINDOW_NORMAL);
    namedWindow(win_result, WINDOW_NORMAL);
    namedWindow(win_canny, WINDOW_NORMAL);

    // HSV ranges (tune if necessary)
    Scalar red_lower1(0, 120, 70), red_upper1(10, 255, 255);
    Scalar red_lower2(170, 120, 70), red_upper2(180, 255, 255);
    Scalar green_lower(36, 50, 70), green_upper(89, 255, 255);
    Scalar blue_lower(90, 50, 70), blue_upper(128, 255, 255);

    // Gaussian parameters
    int ksize = 7; // odd
    double sigma = 1.5;

    // VideoWriter for recording (initialized on 'k')
    VideoWriter writer;
    bool recording = false;
    // We'll set writer size based on frame dims: record two panels side-by-side at original size
    Size writerSize(frame_width * 2, frame_height);

    cout << "Controls:\n  q or ESC: quit\n  s: save images\n  k: start recording\n  h: stop recording\n";

    Mat frame, filtered, hsv;
    Mat mask_r1, mask_r2, mask_red, mask_green, mask_blue, mask_all;
    Mat detected_red, detected_green, detected_blue, combined_detected, result, gray, canny;

    while (true) {
        if (!cap.read(frame) || frame.empty()) {
            cerr << "Warning: failed to grab frame (stream ended/disconnected)\n";
            break;
        }

        // Apply Gaussian blur before HSV
        GaussianBlur(frame, filtered, Size(ksize, ksize), sigma);

        // Convert to HSV
        cvtColor(filtered, hsv, COLOR_BGR2HSV);

        // Build masks
        inRange(hsv, red_lower1, red_upper1, mask_r1);
        inRange(hsv, red_lower2, red_upper2, mask_r2);
        mask_red = mask_r1 | mask_r2;
        inRange(hsv, green_lower, green_upper, mask_green);
        inRange(hsv, blue_lower, blue_upper, mask_blue);

        // Combined colored mask image (3-channel for display)
        vector<Mat> channels(3);
        channels[0] = mask_blue;   // B
        channels[1] = mask_green;  // G
        channels[2] = mask_red;    // R
        merge(channels, mask_all);

        // Extract detected regions (bitwise_and)
        bitwise_and(frame, frame, detected_red, mask_red);
        bitwise_and(frame, frame, detected_green, mask_green);
        bitwise_and(frame, frame, detected_blue, mask_blue);

        combined_detected = Mat::zeros(frame.size(), frame.type());
        add(combined_detected, detected_red, combined_detected);
        add(combined_detected, detected_green, combined_detected);
        add(combined_detected, detected_blue, combined_detected);

        // Find contours and draw bounding boxes & centers on result
        result = frame.clone();
        auto processMask = [&](const Mat &mask, const Scalar &color, const string &label) {
            vector<vector<Point>> contours;
            vector<Vec4i> hierarchy;
            Mat mask_tmp = mask.clone();
            findContours(mask_tmp, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
            for (size_t i = 0; i < contours.size(); ++i) {
                double area = contourArea(contours[i]);
                if (area < 400) continue; // filter noise - adjust threshold
                Rect bbox = boundingRect(contours[i]);
                rectangle(result, bbox, color, 2);
                Moments M = moments(contours[i]);
                if (M.m00 != 0) {
                    int cx = int(M.m10 / M.m00);
                    int cy = int(M.m01 / M.m00);
                    circle(result, Point(cx, cy), 4, color, -1);
                    putText(result, label, Point(bbox.x, bbox.y - 6), FONT_HERSHEY_SIMPLEX, 0.5, color, 1);
                }
            }
        };

        processMask(mask_red, Scalar(0,0,255), "RED");
        processMask(mask_green, Scalar(0,255,0), "GREEN");
        processMask(mask_blue, Scalar(255,0,0), "BLUE");

        // Canny on filtered image
        cvtColor(filtered, gray, COLOR_BGR2GRAY);
        int canny_low = 50, canny_high = 150;
        Canny(gray, canny, canny_low, canny_high);

        // Side-by-side original | filtered
        Mat side;
        // ensure same size
        Mat left = frame;
        Mat right = filtered;
        if (left.size() != right.size()) resize(right, right, left.size());
        hconcat(left, right, side);

        imshow(win_side, side);
        imshow(win_mask, mask_all);
        imshow(win_result, result);
        imshow(win_canny, canny);

        // Recording: compose frame (result | canny_color) at writerSize and write
        if (recording && writer.isOpened()) {
            Mat canny_color;
            cvtColor(canny, canny_color, COLOR_GRAY2BGR);
            Mat r_resized, c_resized;
            // Resize both to writer frame height (frame_height) and width frame_width
            resize(result, r_resized, Size(frame_width, frame_height));
            resize(canny_color, c_resized, Size(frame_width, frame_height));
            Mat composed;
            hconcat(r_resized, c_resized, composed); // size = (frame_width*2, frame_height)
            if (composed.size() == writerSize) {
                writer.write(composed);
            } else {
                // fallback: resize composed to writerSize
                Mat tmp;
                resize(composed, tmp, writerSize);
                writer.write(tmp);
            }
        }

        // key handling
        int key = waitKey(1);
        if (key == 27 || key == 'q') {
            cout << "Quit requested\n";
            break;
        } else if (key == 's') {
            string ts = timestamp_filename();
            string f_orig = "orig_" + ts + ".png";
            string f_filtered = "filtered_" + ts + ".png";
            string f_mask = "mask_" + ts + ".png";
            string f_result = "result_" + ts + ".png";
            string f_canny = "canny_" + ts + ".png";
            imwrite(f_orig, frame);
            imwrite(f_filtered, filtered);
            imwrite(f_mask, mask_all);
            imwrite(f_result, result);
            imwrite(f_canny, canny);
            cout << "Saved images: " << f_orig << ", " << f_filtered << ", " << f_mask << ", " << f_result << ", " << f_canny << "\n";
        } else if (key == 'k') {
            if (!recording) {
                string ts = timestamp_filename();
                string fname = "recording_" + ts + ".avi";
                int fourcc = VideoWriter::fourcc('M','J','P','G');
                bool ok = writer.open(fname, fourcc, fps, writerSize, true);
                if (!ok) {
                    cerr << "Error: could not open writer for file: " << fname << endl;
                } else {
                    recording = true;
                    cout << "Started recording -> " << fname << endl;
                }
            } else {
                cout << "Already recording\n";
            }
        } else if (key == 'h') {
            if (recording) {
                recording = false;
                writer.release();
                cout << "Stopped recording\n";
            }
        }
    } // while

    if (recording) {
        writer.release();
    }
    cap.release();
    destroyAllWindows();
    cout << "Finished.\n";
    return 0;
}
