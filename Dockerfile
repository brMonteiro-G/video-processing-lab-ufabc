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

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir \
    opencv-python \
    opencv-contrib-python \
    numpy

# Set working directory
WORKDIR /workspace

# Create entrypoint script
# RUN echo '#!/bin/bash\n\
# source /root/miniconda3/bin/activate PV25\n\
# exec "$@"' > /entrypoint.sh && \
# chmod +x /entrypoint.sh

CMD ["tail", "-f", "/dev/null"]