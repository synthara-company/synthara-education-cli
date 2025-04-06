#!/bin/bash
# Setup script for Synthara Education CLI

echo "Setting up Synthara Education CLI..."

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Download necessary files
echo "Downloading files..."
curl -s -O https://raw.githubusercontent.com/bniladridas/gemini_cli/main/simple_gemini_cli/gemini_chat.py
mkdir -p simple_gemini_cli
mv gemini_chat.py simple_gemini_cli/

# Create wrapper script
echo "Creating launcher..."
cat > gemini-chat << 'EOF'
#!/bin/bash
# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is required but not installed. Please install pip3 and try again."
    exit 1
fi

# Install required packages if not already installed
echo "Checking dependencies..."
pip3 install google-generativeai rich --quiet

# Run the application
python3 simple_gemini_cli/gemini_chat.py
EOF

chmod +x gemini-chat

# Create installation directory
INSTALL_DIR="$HOME/synthara-cli"
mkdir -p "$INSTALL_DIR"

# Move files to installation directory
mv simple_gemini_cli "$INSTALL_DIR"
mv gemini-chat "$INSTALL_DIR"

echo "Installation complete!"
echo "To run Synthara Education CLI, use the following command:"
echo "cd $INSTALL_DIR && ./gemini-chat"

# Run the application directly
cd "$INSTALL_DIR"
./gemini-chat
