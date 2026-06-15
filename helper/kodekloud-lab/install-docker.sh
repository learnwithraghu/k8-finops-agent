#!/bin/bash

#################################################################################
# Docker Installation Script
# Automatically detects OS and installs Docker
# Supports: Alpine Linux, Ubuntu/Debian, CentOS/RHEL, macOS
#################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        OS_VERSION=$VERSION_ID
        PRETTY_NAME=$PRETTY_NAME
    elif [ -f /etc/redhat-release ]; then
        OS="rhel"
        PRETTY_NAME=$(cat /etc/redhat-release)
    elif [ "$(uname)" = "Darwin" ]; then
        OS="macos"
        PRETTY_NAME="macOS"
    else
        OS="unknown"
        PRETTY_NAME="Unknown OS"
    fi
}

# Install Docker on Alpine Linux
install_docker_alpine() {
    print_header "Installing Docker on Alpine Linux"

    print_info "Updating package manager..."
    apk update

    print_info "Installing Docker..."
    apk add docker

    print_info "Installing Docker Compose..."
    apk add docker-compose

    print_success "Docker installed successfully"
}

# Install Docker on Ubuntu/Debian
install_docker_debian() {
    print_header "Installing Docker on Ubuntu/Debian"

    print_info "Updating package manager..."
    sudo apt-get update

    print_info "Installing prerequisites..."
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

    print_info "Adding Docker GPG key..."
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    print_info "Adding Docker repository..."
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    print_info "Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io

    print_success "Docker installed successfully"
}

# Install Docker on CentOS/RHEL
install_docker_rhel() {
    print_header "Installing Docker on CentOS/RHEL"

    print_info "Updating package manager..."
    sudo yum update -y

    print_info "Installing Docker..."
    sudo yum install -y docker

    print_success "Docker installed successfully"
}

# Install Docker on macOS
install_docker_macos() {
    print_header "Installing Docker on macOS"

    if ! command -v brew &> /dev/null; then
        print_error "Homebrew not found. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    print_info "Installing Docker via Homebrew..."
    brew install docker

    print_success "Docker installed successfully"
    print_info "Note: On macOS, Docker Desktop is recommended for best experience"
}

# Start Docker service
start_docker() {
    print_header "Starting Docker Service"

    case $OS in
        alpine)
            print_info "Starting Docker service with rc-service..."

            # Try to start Docker service with rc-service
            if rc-service docker start 2>&1 | grep -q "error\|failed"; then
                print_info "rc-service method encountered issues, trying dockerd daemon..."
                dockerd > /dev/null 2>&1 &
                sleep 3
            fi

            # Wait a moment and verify it started
            sleep 2

            if docker ps > /dev/null 2>&1; then
                print_success "Docker service started successfully"
            else
                print_error "Docker is not responding. Try running: rc-service docker start"
            fi

            print_info "Enabling Docker to start on boot..."
            rc-update add docker
            print_success "Docker enabled on boot"
            ;;
        ubuntu|debian)
            print_info "Starting Docker service..."
            sudo systemctl start docker
            print_success "Docker service started"

            print_info "Enabling Docker to start on boot..."
            sudo systemctl enable docker
            print_success "Docker enabled on boot"
            ;;
        rhel|centos)
            print_info "Starting Docker service..."
            sudo systemctl start docker
            print_success "Docker service started"

            print_info "Enabling Docker to start on boot..."
            sudo systemctl enable docker
            print_success "Docker enabled on boot"
            ;;
        macos)
            print_info "Docker Desktop must be started manually on macOS"
            print_info "You can start it from Applications > Docker"
            ;;
    esac
}

# Verify Docker installation
verify_docker() {
    print_header "Verifying Docker Installation"

    print_info "Checking Docker version..."
    docker --version

    print_info "Running hello-world container..."
    if docker run hello-world > /dev/null 2>&1; then
        print_success "Docker is working correctly!"
    else
        print_error "Docker test failed. There might be an issue with your installation."
    fi
}

# Main execution
main() {
    print_header "Docker Installation Script"

    detect_os

    echo -e "\n${BLUE}Detected OS:${NC} $PRETTY_NAME"
    echo -e "${BLUE}OS ID:${NC} $OS\n"

    case $OS in
        alpine)
            install_docker_alpine
            ;;
        ubuntu|debian)
            install_docker_debian
            ;;
        rhel|centos)
            install_docker_rhel
            ;;
        macos)
            install_docker_macos
            ;;
        *)
            print_error "Unsupported OS: $OS"
            print_info "Please install Docker manually from: https://docs.docker.com/get-docker/"
            exit 1
            ;;
    esac

    start_docker

    # Wait a moment for service to start
    sleep 2

    verify_docker

    print_header "Installation Complete!"
    echo -e "${GREEN}Docker has been successfully installed and configured.${NC}\n"
}

# Run main function
main
