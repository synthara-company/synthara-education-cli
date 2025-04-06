#!/bin/bash
# Setup script for Synthara Education CLI

echo "Setting up Synthara Education CLI..."

# Create installation directory
INSTALL_DIR="$HOME/synthara-cli"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download necessary files
echo "Downloading files..."
curl -s -O https://raw.githubusercontent.com/synthara-company/synthara-education-cli/main/simple_gemini_cli/gemini_chat.py
mkdir -p simple_gemini_cli
mv gemini_chat.py simple_gemini_cli/

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Create wrapper script
echo "Creating launcher..."
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
echo "Installing dependencies..."
source venv/bin/activate
pip install google-generativeai rich --quiet

echo ""
echo "✅ Installation complete!"
echo "✅ To run Synthara Education CLI, use the following command:"
echo "   cd $INSTALL_DIR && ./gemini-chat"
echo ""
echo "⭐ The application is now installed and ready to use!"
echo "⭐ Run the command above to start using Synthara Education CLI."
echo ""
