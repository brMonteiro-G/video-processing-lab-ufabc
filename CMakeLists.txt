cmake_minimum_required(VERSION 2.8)

# Top-level project
project(OpenCVExamples)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

# ---- First executable ----
add_executable(DisplayImage DisplayImage.cpp)
target_link_libraries(DisplayImage ${OpenCV_LIBS})

# ---- Second executable ----
add_executable(ConvertFormatImage ConvertFormatImage.cpp)
target_link_libraries(ConvertFormatImage ${OpenCV_LIBS})
