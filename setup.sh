#!/bin/bash
#
# K8s FinOps Agent - Setup Script
# Validates prerequisites and prepares the environment
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CLUSTER_NAME="finops-cluster"
NAMESPACE="airline"
IMAGE_NAME="k8-finops-agent"

# Helper functions
print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Validate prerequisites
validate_prerequisites() {
    print_header "Step 1: Validating Prerequisites"

    local missing=()

    # Check Docker
    if command_exists docker; then
        DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
        print_success "Docker installed: $DOCKER_VERSION"
    else
        print_error "Docker not found"
        missing+=("docker")
    fi

    # Check Kind
    if command_exists kind; then
        KIND_VERSION=$(kind version | awk '{print $2}')
        print_success "Kind installed: $KIND_VERSION"
    else
        print_error "Kind not found"
        missing+=("kind")
    fi

    # Check kubectl
    if command_exists kubectl; then
        KUBECTL_VERSION=$(kubectl version --client -o json 2>/dev/null | grep '"gitVersion"' | head -1 | awk -F: '{print $2}' | sed 's/[",]//g' | tr -d ' ')
        print_success "kubectl installed: $KUBECTL_VERSION"
    else
        print_error "kubectl not found"
        missing+=("kubectl")
    fi

    # Check Python (optional, for local dev)
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | awk '{print $2}')
        print_success "Python installed: $PYTHON_VERSION"
    else
        print_warning "Python not found (optional for local development)"
    fi

    # Report missing
    if [ ${#missing[@]} -ne 0 ]; then
        echo ""
        print_error "Missing prerequisites: ${missing[*]}"
        echo ""
        echo "Install instructions:"
        echo "  Docker: https://docs.docker.com/get-docker/"
        echo "  Kind: https://kind.sigs.k8s.io/docs/user/quick-start/#installation"
        echo "  kubectl: https://kubernetes.io/docs/tasks/tools/"
        exit 1
    fi

    print_success "All required prerequisites validated"
}

# Check Docker is running
check_docker_running() {
    print_header "Step 2: Checking Docker Daemon"

    if docker info >/dev/null 2>&1; then
        print_success "Docker daemon is running"
    else
        print_error "Docker daemon is not running"
        echo ""
        echo "Please start Docker:"
        echo "  macOS: Open Docker Desktop"
        echo "  Linux: sudo systemctl start docker"
        exit 1
    fi
}

# Check for existing Kind cluster
check_existing_cluster() {
    print_header "Step 3: Checking for Existing Kind Cluster"

    if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
        print_warning "Kind cluster '${CLUSTER_NAME}' already exists"
        echo ""
        read -p "Do you want to delete and recreate it? (y/N): " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Deleting existing cluster..."
            kind delete cluster --name "${CLUSTER_NAME}"
            print_success "Cluster deleted"
        else
            print_info "Keeping existing cluster"
            return 0
        fi
    else
        print_info "No existing Kind cluster found"
    fi
}

# Check for existing resources in cluster
check_existing_resources() {
    print_header "Step 4: Checking for Existing Resources"

    local has_resources=false

    # Check if kubectl can connect
    if kubectl cluster-info >/dev/null 2>&1; then
        # Check for deployments
        DEPLOYMENTS=$(kubectl get deployments --all-namespaces -o name 2>/dev/null | grep -v "kube-system" | grep -v "local-path-storage" | wc -l)
        if [ "$DEPLOYMENTS" -gt 0 ]; then
            print_warning "Found $DEPLOYMENTS deployments in cluster"
            has_resources=true
        fi

        # Check for services
        SERVICES=$(kubectl get services --all-namespaces -o name 2>/dev/null | grep -v "kube-system" | grep -v "default/kubernetes" | wc -l)
        if [ "$SERVICES" -gt 0 ]; then
            print_warning "Found $SERVICES services in cluster"
            has_resources=true
        fi

        # Check for PVCs
        PVCS=$(kubectl get pvc --all-namespaces -o name 2>/dev/null | wc -l)
        if [ "$PVCS" -gt 0 ]; then
            print_warning "Found $PVCS PVCs in cluster"
            has_resources=true
        fi

        if [ "$has_resources" = true ]; then
            echo ""
            read -p "Do you want to clean up all existing resources? (y/N): " -n 1 -r
            echo ""

            if [[ $REPLY =~ ^[Yy]$ ]]; then
                cleanup_resources
            else
                print_warning "Keeping existing resources (may affect scan results)"
            fi
        else
            print_success "No existing resources found"
        fi
    else
        print_info "Cannot connect to cluster (will create new one)"
    fi
}

# Clean up existing resources
cleanup_resources() {
    print_header "Cleaning Up Existing Resources"

    # Delete all deployments except system ones
    print_info "Deleting deployments..."
    kubectl delete deployments --all --all-namespaces --ignore-not-found=true 2>/dev/null || true

    # Delete all services except system ones
    print_info "Deleting services..."
    kubectl delete services --all --all-namespaces --ignore-not-found=true 2>/dev/null || true
    # Recreate default/kubernetes service if deleted
    kubectl expose service kubernetes --namespace=default 2>/dev/null || true

    # Delete all PVCs
    print_info "Deleting PVCs..."
    kubectl delete pvc --all --all-namespaces --ignore-not-found=true 2>/dev/null || true

    # Delete all configmaps except system ones
    print_info "Deleting ConfigMaps..."
    kubectl delete configmap --all --all-namespaces --ignore-not-found=true 2>/dev/null || true

    # Delete namespace if exists
    if kubectl get namespace "${NAMESPACE}" >/dev/null 2>&1; then
        print_info "Deleting namespace ${NAMESPACE}..."
        kubectl delete namespace "${NAMESPACE}" --ignore-not-found=true 2>/dev/null || true
    fi

    print_success "Cleanup complete"
}

# Create Kind cluster
create_cluster() {
    print_header "Step 5: Creating Kind Cluster"

    if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
        print_info "Using existing cluster '${CLUSTER_NAME}'"
    else
        print_info "Creating Kind cluster '${CLUSTER_NAME}'..."
        kind create cluster --name "${CLUSTER_NAME}" --wait 60s
        print_success "Cluster created"
    fi

    # Verify cluster
    kubectl cluster-info
    kubectl get nodes
    print_success "Cluster is ready"
}

# Check for existing Docker image
check_existing_image() {
    print_header "Step 6: Checking for Existing Docker Image"

    if docker images | grep -q "^${IMAGE_NAME}"; then
        print_warning "Docker image '${IMAGE_NAME}' already exists"
        echo ""
        read -p "Do you want to rebuild it? (y/N): " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            build_image
        else
            print_info "Using existing image"
        fi
    else
        print_info "No existing image found"
        build_image
    fi
}

# Build Docker image
build_image() {
    print_header "Building Docker Image"

    print_info "Building ${IMAGE_NAME}:latest..."
    docker build -t "${IMAGE_NAME}:latest" .

    print_success "Docker image built successfully"
    docker images | grep "${IMAGE_NAME}"
}

# Check environment file
check_env_file() {
    print_header "Step 7: Checking Environment Configuration"

    if [ -f ".env" ]; then
        print_success ".env file found"

        # Check required variables
        local missing_vars=()

        if ! grep -q "^AWS_ACCESS_KEY_ID=" .env 2>/dev/null || \
           [ -z "$(grep "^AWS_ACCESS_KEY_ID=" .env | cut -d= -f2)" ]; then
            missing_vars+=("AWS_ACCESS_KEY_ID")
        fi

        if ! grep -q "^AWS_SECRET_ACCESS_KEY=" .env 2>/dev/null || \
           [ -z "$(grep "^AWS_SECRET_ACCESS_KEY=" .env | cut -d= -f2)" ]; then
            missing_vars+=("AWS_SECRET_ACCESS_KEY")
        fi

        if ! grep -q "^GITHUB_TOKEN=" .env 2>/dev/null || \
           [ -z "$(grep "^GITHUB_TOKEN=" .env | cut -d= -f2)" ]; then
            missing_vars+=("GITHUB_TOKEN")
        fi

        if ! grep -q "^GITHUB_REPO=" .env 2>/dev/null || \
           [ -z "$(grep "^GITHUB_REPO=" .env | cut -d= -f2)" ]; then
            missing_vars+=("GITHUB_REPO")
        fi

        if [ ${#missing_vars[@]} -ne 0 ]; then
            print_warning "Missing or empty variables in .env: ${missing_vars[*]}"
            echo ""
            echo "You can still run in mock mode:"
            echo "  ./setup.sh --mock"
        fi
    else
        print_warning ".env file not found"
        echo ""
        echo "Please create .env file:"
        echo "  cp .env.example .env"
        echo "  # Edit .env with your credentials"
        echo ""
        echo "Or run in mock mode (no AWS/GitHub required):"
        echo "  ./setup.sh --mock"
    fi
}

# Print next steps
print_next_steps() {
    print_header "Setup Complete!"

    echo "Your environment is ready. Next steps:"
    echo ""
    echo "1. Deploy airline services:"
    echo -e "   ${YELLOW}kubectl apply -k airline-k8-deployment/${NC}"
    echo ""
    echo "2. Verify deployments:"
    echo -e "   ${YELLOW}kubectl get all -n airline${NC}"
    echo ""
    echo "3. Run the FinOps agent:"
    echo -e "   ${YELLOW}docker run --rm -v ~/.kube/config:/home/finops/.kube/config:ro --env-file .env k8-finops-agent:latest${NC}"
    echo ""
    echo "4. Or run in mock mode:"
    echo -e "   ${YELLOW}docker run --rm -v ~/.kube/config:/home/finops/.kube/config:ro -e USE_MOCK=true -e USE_MOCK_GITHUB=true k8-finops-agent:latest${NC}"
    echo ""
    echo "For more options, see USAGE.md"
}

# Full cleanup
full_cleanup() {
    print_header "Full Cleanup Mode"

    echo "This will delete:"
    echo "  - Kind cluster: ${CLUSTER_NAME}"
    echo "  - Docker image: ${IMAGE_NAME}"
    echo ""
    read -p "Are you sure? (y/N): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Delete Kind cluster
        if kind get clusters | grep -q "^${CLUSTER_NAME}$"; then
            print_info "Deleting Kind cluster..."
            kind delete cluster --name "${CLUSTER_NAME}" || true
            print_success "Cluster deleted"
        fi

        # Delete Docker image
        if docker images | grep -q "^${IMAGE_NAME}"; then
            print_info "Deleting Docker image..."
            docker rmi "${IMAGE_NAME}:latest" || true
            print_success "Image deleted"
        fi

        print_success "Cleanup complete"
    else
        print_info "Cleanup cancelled"
    fi
}

# Main function
main() {
    # Parse arguments
    local mock_mode=false
    local cleanup_mode=false
    local skip_build=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --mock)
                mock_mode=true
                shift
                ;;
            --cleanup)
                cleanup_mode=true
                shift
                ;;
            --skip-build)
                skip_build=true
                shift
                ;;
            --help|-h)
                echo "K8s FinOps Agent Setup Script"
                echo ""
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --mock         Run in mock mode (no AWS/GitHub required)"
                echo "  --cleanup      Full cleanup (cluster + image)"
                echo "  --skip-build   Skip Docker image build"
                echo "  --help, -h     Show this help message"
                echo ""
                echo "Examples:"
                echo "  $0                    # Full setup"
                echo "  $0 --mock             # Setup for mock mode"
                echo "  $0 --cleanup          # Clean everything"
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                echo "Run '$0 --help' for usage"
                exit 1
                ;;
        esac
    done

    # Handle cleanup mode
    if [ "$cleanup_mode" = true ]; then
        full_cleanup
        exit 0
    fi

    # Print banner
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                ║${NC}"
    echo -e "${GREEN}║     K8s FinOps Agent - Setup Script            ║${NC}"
    echo -e "${GREEN}║                                                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
    echo ""

    # Run setup steps
    validate_prerequisites
    check_docker_running
    check_existing_cluster
    check_existing_resources
    create_cluster

    if [ "$skip_build" = false ]; then
        check_existing_image
    else
        print_info "Skipping Docker build (--skip-build)"
    fi

    check_env_file

    # Print next steps
    print_next_steps

    # Print mock mode info if requested
    if [ "$mock_mode" = true ]; then
        echo ""
        print_header "Mock Mode Enabled"
        echo "To run without AWS/GitHub credentials:"
        echo -e "   ${YELLOW}docker run --rm -v ~/.kube/config:/home/finops/.kube/config:ro -e USE_MOCK=true -e USE_MOCK_GITHUB=true k8-finops-agent:latest${NC}"
    fi
}

# Run main function
main "$@"
