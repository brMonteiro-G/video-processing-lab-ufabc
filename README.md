# Video Processing Lab UFABC

This repository contains the environment setup for the UFABC Video Processing Laboratory using Docker.

## Using Docker Compose (Recommended)

### Starting the Environment

To start the video processing environment:

```bash
docker-compose up -d
```

### Accessing the Container

To enter the container with the PV25 environment activated:

```bash
docker-compose exec video-processing bash
```

### Stopping the Environment

To stop the environment:

```bash
docker-compose down
```

## Alternative: Using Docker Directly

### Building the Docker Image

To build the Docker image manually:

```bash
docker build -t video-processing-lab .
```

### Running the Container

To run the container with access to your local files:

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  video-processing-lab
```

Note: If you need to use OpenCV's GUI features or VLC, you'll need to add X11 forwarding:

```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd):/workspace \
  video-processing-lab
```

## Features

- Pre-configured Python environment (PV25) with OpenCV
- GUI support for OpenCV applications
- VLC media player installed
- Volume mounting for easy file access
- Resource management for optimal performance
- Webcam support (if available)

## Resource Configuration

The Docker Compose configuration includes resource limits to ensure stable performance:
- CPU: Limited to 4 cores, minimum 2 cores reserved
- Memory: Limited to 4GB, minimum 2GB reserved

You can adjust these values in the `docker-compose.yml` file according to your system's capabilities.


## Running Locally 

```
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```
