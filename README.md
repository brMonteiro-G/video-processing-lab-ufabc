# Video Processing Lab UFABC

This repository contains the environment setup for the UFABC Video Processing Laboratory using Docker.

## Setup Instructions

### macOS Setup (Required for GUI Applications)

1. **Install XQuartz**
   - Download and install XQuartz from [xquartz.org](https://www.xquartz.org/)
   - After installation, restart your computer

2. **Configure XQuartz**
   - Open XQuartz
   - Go to XQuartz → Preferences → Security
   - Check "Allow connections from network clients"
   - Restart XQuartz

3. **Enable X11 Forwarding**
   - Open terminal and run:
   ```bash
   xhost +localhost
   ```

4. **Set Display Environment Variable**
   - Add this to your `~/.zshrc` or `~/.bashrc`:
   ```bash
   export DISPLAY=host.docker.internal:0
   ```
   - Then reload your shell:
   ```bash
   source ~/.zshrc  # or source ~/.bashrc
   ```

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





### to use video from wbcam 



Step 1: Set up OBS to stream your webcam

Open OBS Studio on your Mac.

Add your webcam as a video source.

Go to Settings → Stream:

Set Service: Custom...

/stream is the default path configured on nginx of rmtp 

Server: rtmp://localhost:1935/stream (we’ll run a local RTMP server)

Stream Key: mystream

Apply and start streaming.