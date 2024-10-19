# Use the base image for Raspberry Pi (arm architecture)
FROM arm32v7/python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    lsb-release \
    software-properties-common

# Add Docker’s official GPG key and Docker APT repo for Raspberry Pi
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=armhf] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list

# Install Docker
RUN apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io

# Start Docker daemon in the container (you will need privileged mode to run the container)
CMD ["dockerd"]
