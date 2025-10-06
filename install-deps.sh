#!/bin/bash
set -e  # Exit on error

# Initialize conda for shell
eval "$(conda shell.bash hook)"

# Configure conda
echo "Configuring conda..."
conda config --set auto_activate_base false

# Accept Anaconda Terms of Service
echo "Accepting Anaconda Terms of Service..."
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Create PV25 environment
echo "Creating PV25 environment..."
conda create --name PV25 python=3.11 -y

# Activate environment and install packages
echo "Installing Python packages..."
conda activate PV25
