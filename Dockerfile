FROM --platform=linux/amd64 ubuntu:20.04

# Avoid timezone prompt during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    wget \
    sudo \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    gfortran \
    openexr \
    libatlas-base-dev \
    python3-dev \
    python3-numpy \
    libtbb-dev \
    libdc1394-dev \
    libopenexr-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev \
    vlc \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN mkdir -p /root/miniconda3 && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda3/miniconda.sh && \
    bash /root/miniconda3/miniconda.sh -b -u -p /root/miniconda3 && \
    rm /root/miniconda3/miniconda.sh

# Add conda to path
ENV PATH="/root/miniconda3/bin:${PATH}"


# Install OpenCV from source
WORKDIR /opencv_build
RUN git clone https://github.com/opencv/opencv.git && \
    git clone https://github.com/opencv/opencv_contrib.git

WORKDIR /opencv_build/opencv/build


# Before OpenCV build, add these environment variables
ENV MAKEFLAGS="-j8"
ENV OPENCV_BUILD_TYPE=RELEASE
ENV DEBIAN_FRONTEND=noninteractive


# Update the build commands
RUN cmake \
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    # Disable unnecessary features
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_DOCS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_JAVA=OFF \
    -D BUILD_opencv_apps=OFF \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    # Enable only necessary modules
    -D BUILD_opencv_python3=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_build/opencv_contrib/modules \
    # Performance optimizations
    -D WITH_TBB=ON \
    -D WITH_OPENMP=ON \
    -D ENABLE_FAST_MATH=ON \
    -D CPU_BASELINE=AVX2 \
    -D CMAKE_C_FLAGS="-O3 -march=native" \
    -D CMAKE_CXX_FLAGS="-O3 -march=native" \
    # Disable unnecessary dependencies
    -D WITH_1394=OFF \
    -D WITH_GSTREAMER=OFF \
    -D WITH_IPP=OFF .. && \
    make -j"$(nproc)" && \
    make install


# Set working directory
WORKDIR /workspace

# Create entrypoint script
# RUN echo '#!/bin/bash\n\
# source /root/miniconda3/bin/activate PV25\n\
# exec "$@"' > /entrypoint.sh && \
# chmod +x /entrypoint.sh

CMD ["tail", "-f", "/dev/null"]