#!/bin/bash
# Setup script for Synthara Education CLI

# Print colorful header
echo -e "\033[1;36m"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║          Synthara | The Education Times CLI                ║"
echo "║                  Installation Script                       ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "\033[0m"

# Create installation directory
INSTALL_DIR="$HOME/synthara-cli"
echo -e "\033[1;33m[1/4]\033[0m Creating installation directory at $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download necessary files
echo -e "\033[1;33m[2/4]\033[0m Downloading files..."
curl -s -O https://raw.githubusercontent.com/bniladridas/gemini_cli/main/simple_gemini_cli/gemini_chat.py
mkdir -p simple_gemini_cli
mv gemini_chat.py simple_gemini_cli/

# Create virtual environment
echo -e "\033[1;33m[3/4]\033[0m Setting up Python virtual environment..."
python3 -m venv venv

# Create launcher script
echo -e "\033[1;33m[4/4]\033[0m Creating launcher script..."
cat > gemini-chat << 'EOF'
#!/bin/bash

# Change to the installation directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed, install if needed
if ! python -c "import google.generativeai" &>/dev/null || ! python -c "import rich" &>/dev/null; then
    echo "Installing dependencies..."
    pip install google-generativeai rich --quiet
fi

# Run the application
python simple_gemini_cli/gemini_chat.py
EOF

chmod +x gemini-chat

# Install dependencies in the virtual environment
echo -e "\033[1;33m[Bonus]\033[0m Installing dependencies..."
source venv/bin/activate
pip install google-generativeai rich --quiet

# Print success message
echo -e "\033[1;32m"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║               Installation Complete!                       ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "\033[0m"

echo -e "\033[1;36mTo run Synthara Education CLI, use this command:\033[0m"
echo -e "\033[1;37m   cd $INSTALL_DIR && ./gemini-chat\033[0m"
echo ""
echo -e "\033[1;33mTip:\033[0m You'll need a Gemini API key from https://aistudio.google.com/app/apikey"
echo ""
