# Use the latest Amazon Linux 2023 as base image
FROM public.ecr.aws/amazonlinux/amazonlinux:2023

# Set metadata
LABEL maintainer="Network Testing Tool"
LABEL description="Container image for network testing with Python and network utilities"

# Install Python 3, network tools, and utilities
RUN dnf update -y && \
    dnf install -y \
    python3 \
    python3-pip \
    iputils \
    bind-utils \
    net-tools \
    iproute \
    tcpdump \
    traceroute \
    nmap-ncat \
    telnet \
    wget \
    # curl \ # Curl package from DNF conflicts with AL2023 included Curl package
    nano \
    && dnf clean all

# Create app directory
WORKDIR /app

# Copy the network tester script
COPY network_tester.py /app/

# Make the script executable
RUN chmod +x /app/network_tester.py

# Create output directory
RUN mkdir -p /app/output

# Set Python to run in unbuffered mode for better logging
ENV PYTHONUNBUFFERED=1

# Set the entrypoint to the network tester
ENTRYPOINT ["python3", "/app/network_tester.py"]

# Default command (can be overridden)
CMD ["--help"]
