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

# Create non-root user for running the application
RUN groupadd -r nettest && \
    useradd -r -g nettest -u 1000 -m -s /bin/bash nettest

# Create app directory and set ownership
WORKDIR /app

# Copy the network tester script
COPY network_tester.py /app/

# Create output directory and set permissions
RUN mkdir -p /app/output && \
    chown -R nettest:nettest /app && \
    chmod +x /app/network_tester.py

# Grant ping capability to the ping binary (allows non-root ping)
# This is more secure than running the entire container as root
RUN setcap cap_net_raw+ep /usr/bin/ping

# Set Python to run in unbuffered mode for better logging
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER nettest

# Set the entrypoint to the network tester
ENTRYPOINT ["python3", "/app/network_tester.py"]

# Default command (can be overridden)
CMD ["--help"]
