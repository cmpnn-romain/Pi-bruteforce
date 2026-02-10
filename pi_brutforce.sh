#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Check if venv exists and is valid
check_venv() {
    if [ -d "venv" ] && [ -f "venv/bin/activate" ] && [ -f "venv/bin/python" ]; then
        return 0
    else
        return 1
    fi
}

# Setup environment
setup_environment() {
    echo -e "${CYAN}🥧 Pi Bruteforce Number Finder - Setup${NC}"
    echo "======================================"
    echo ""
    
    # Check Python3
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 is not installed!${NC}"
        echo "Please install Python3 first:"
        echo "  sudo apt update"
        echo "  sudo apt install python3"
        exit 1
    fi
    
    echo -e "${GREEN}✓${NC} Python3 found: $(python3 --version)"
    
    # Get Python version (e.g., 3.12)
    PYTHON_VERSION=$(python3 --version | grep -oP '\d+\.\d+' | head -1)
    
    # Test if we can create a venv (will fail if python3-venv not installed)
    if ! python3 -m venv /tmp/test_venv_$$ &> /dev/null; then
        echo -e "${YELLOW}⚠️  python3-venv is not installed.${NC}"
        echo "Installing python3-venv (requires sudo)..."
        
        sudo apt update -qq
        sudo apt install -y python3-venv python${PYTHON_VERSION}-venv
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Failed to install python3-venv${NC}"
            echo "Please install manually:"
            echo "  sudo apt install python3-venv python${PYTHON_VERSION}-venv"
            exit 1
        fi
        echo -e "${GREEN}✓${NC} python3-venv installed"
    fi
    
    # Clean up test venv
    rm -rf /tmp/test_venv_$$
    
    # Remove broken venv if exists
    if [ -d "venv" ] && [ ! -f "venv/bin/activate" ]; then
        echo -e "${YELLOW}⚠️  Removing broken virtual environment...${NC}"
        rm -rf venv
    fi
    
    # Create virtual environment
    if ! check_venv; then
        echo ""
        echo -e "${CYAN}📦 Creating virtual environment...${NC}"
        python3 -m venv venv
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Failed to create virtual environment${NC}"
            exit 1
        fi
        echo -e "${GREEN}✓${NC} Virtual environment created"
    fi
    
    # Activate and install dependencies
    echo ""
    echo -e "${CYAN}📦 Installing dependencies...${NC}"
    source venv/bin/activate
    
    pip install --upgrade pip -q
    pip install mpmath colorama msgpack -q
    
    # Install gmpy2 for maximum speed
    echo -e "${YELLOW}⚡ Installing high-performance math libraries (gmpy2)...${NC}"
    if command -v apt &> /dev/null; then
        echo "Requires sudo privileges to install system libraries:"
        sudo apt update -qq
        sudo apt install -y libgmp-dev libmpfr-dev libmpc-dev
        
        if [ $? -eq 0 ]; then
            pip install gmpy2 -q
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}🚀 Turbo mode ACTIVATED (gmpy2 installed)${NC}"
            else
                echo -e "${YELLOW}⚠️  gmpy2 pip install failed. Falling back to pure Python.${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️  System library install failed. Falling back to pure Python.${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  apt not found. Skipping gmpy2 auto-install.${NC}"
    fi

    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Dependencies installed"
        deactivate
        return 0
    else
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        deactivate
        exit 1
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] [NUMBER]"
    echo ""
    echo "Options:"
    echo "  --setup              Force setup/reinstall"
    echo "  --compute            Compute and cache Pi digits (run once, creates binary compressed cache)"
    echo "  --help, -h           Show this help message"
    echo ""
    echo "Search Options:"
    echo "  -l, --length N       Length of numbers to bruteforce"
    echo "  --starts-with P      Pattern(s) to start with (comma-separated for multiple)"
    echo "  --ends-with P        Pattern(s) to end with"
    echo "  --contains P         Pattern(s) to contain"
    echo "  --regex PATTERN      Regex pattern to match"
    echo "  --min N              Minimum value for range search"
    echo "  --max N              Maximum value for range search"
    echo "  -p, --precision N    Number of Pi digits (default: 10,000,000)"
    echo ""
    echo "Examples:"
    echo "  # Setup and cache"
    echo "  $0 --setup                           # Install dependencies"
    echo "  $0 --compute                         # Compute Pi cache (binary compressed)"
    echo ""
    echo "  # Basic bruteforce"
    echo "  $0 --length 9 --starts-with 123      # 9-digit numbers starting with 123"
    echo "  $0 --length 6 --ends-with 999        # 6-digit numbers ending with 999"
    echo "  $0 --length 8 --starts-with 42 --ends-with 24  # Combined filters"
    echo ""
    echo "  # Advanced features"
    echo "  $0 --regex \"12[0-9]{3}45\"            # Regex pattern matching"
    echo "  $0 --min 123000000 --max 123999999   # Range search"
    echo "  $0 --length 9 --starts-with 123,456,789  # Multiple patterns"
    echo ""
    echo "  # Legacy direct search"
    echo "  $0 123456                            # Search for specific number"
}

# Main logic
case "$1" in
    --help|-h)
        show_usage
        exit 0
        ;;
    --setup)
        setup_environment
        echo ""
        echo -e "${GREEN}✅ Setup complete!${NC}"
        echo ""
        exit 0
        ;;
    "")
        show_usage
        exit 0
        ;;
    *)
        # Check if setup is needed
        if ! check_venv; then
            echo -e "${YELLOW}⚠️  Virtual environment not found. Running setup...${NC}"
            echo ""
            setup_environment
            echo ""
        fi
        
        # Run main module with all arguments
        source venv/bin/activate
        python -m src "$@"
        EXIT_CODE=$?
        deactivate
        exit $EXIT_CODE
        ;;
esac
