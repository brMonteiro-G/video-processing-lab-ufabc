FROM ubuntu:20.04

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

# Configure conda
RUN conda config --set auto_activate_base false

# Create and activate PV25 environment
RUN conda create -n PV25 python -y

# Install OpenCV from source
WORKDIR /opencv_build
RUN git clone https://github.com/opencv/opencv.git && \
    git clone https://github.com/opencv/opencv_contrib.git

WORKDIR /opencv_build/opencv/build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON .. && \
    make -j$(nproc) && \
    make install

# Set up conda environment and install Python OpenCV packages
SHELL ["/bin/bash", "-c"]
RUN source /root/miniconda3/bin/activate PV25 && \
    pip install opencv-python opencv-contrib-python

# Set working directory
WORKDIR /workspace

# Create entrypoint script
RUN echo '#!/bin/bash\n\
source /root/miniconda3/bin/activate PV25\n\
exec "$@"' > /entrypoint.sh && \
chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]
