cmake_minimum_required(VERSION 3.5)
project(ExtractColors)

find_package(OpenCV REQUIRED)
if(NOT OpenCV_FOUND)
  message(FATAL_ERROR "OpenCV not found")
endif()

add_executable(ExtractColors ExtractColors.cpp)
target_link_libraries(ExtractColors ${OpenCV_LIBS})
set_target_properties(ExtractColors PROPERTIES
  CXX_STANDARD 11
  CXX_STANDARD_REQUIRED ON
)