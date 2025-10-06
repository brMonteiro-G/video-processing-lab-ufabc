#include <opencv2/opencv.hpp>
using namespace cv;

int main(int argc, char** argv)
{
    // Check for valid command line arguments, print usage
    if (argc != 2) {
        std::cout << "Usage: DisplayImage <ImagePath>" << std::endl;
        return -1;
    }

    // Read the image
    Mat image = imread(argv[1], IMREAD_COLOR);

    if (!image.data) {
        std::cout << "Could not open or find the image" << std::endl;
        return -1;
    }

    // Display the image
    namedWindow("Display window", WINDOW_AUTOSIZE);
    imshow("Display window", image);

    waitKey(0);
    return 0;
}
