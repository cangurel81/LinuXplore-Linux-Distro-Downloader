# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for Flet and other libs
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libavutil56 \
    libavcodec58 \
    libavformat58 \
    libswscale5 \
    libsecret-1-0 \
    libunwind8 \
    libnotify4 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Flet needs a way to display its window. For Docker, usually web mode is easier.
# To run in web mode:
# CMD ["flet", "run", "--web", "main.py"]

# Default command
CMD ["python", "main.py"]
