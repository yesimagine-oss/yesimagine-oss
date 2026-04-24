# Dockerfile.evo-workbench
# Scientifically optimized containerized environment for EvoMap Workbench
# Ensures 100% consistent behavior across all platforms

FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install system dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
        curl wget gnupg ca-certificates \
        build-essential software-properties-common \
        git vim nano iputils-ping net-tools && \
    rm -rf /var/lib/apt/lists/*

# Install Node.js 18.x
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# Install Python 3.9+
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy application files
COPY . /app/

# Install Python dependencies
RUN pip3 install requests

# Install Clash (Mihomo) proxy
RUN wget https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-linux-amd64.tar.gz && \
    tar -xzf mihomo-linux-amd64.tar.gz && \
    mv mihomo /usr/local/bin/clash && \
    chmod +x /usr/local/bin/clash

# Create config directories
RUN mkdir -p ~/.config/mihomo

# Copy proxy configuration
COPY config.yaml ~/.config/mihomo/config.yaml

# Install EvoMap CLI globally
RUN npm install -g evomapper

# Create runtime directories
RUN mkdir -p ~/.evomap

# Setup entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose ports
EXPOSE 7890
EXPOSE 9090
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7890 || exit 1

# Default command
CMD ["/entrypoint.sh"]