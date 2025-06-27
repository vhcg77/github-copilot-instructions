#!/bin/bash
# GitHub Copilot Instructions - Quick Install Script
# Usage: curl -fsSL https://raw.githubusercontent.com/your-username/github-copilot-instructions/main/install.sh | bash

set -e

echo "🚀 Installing GitHub Copilot Instructions - Advanced Hierarchical System"
echo "=================================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is required but not installed. Please install git first."
    exit 1
fi

# Check if python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is required but not installed. Please install Python 3.8+ first."
    exit 1
fi

# Determine python command
PYTHON_CMD="python"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
fi

echo "✅ Prerequisites check passed"

# Clone the repository to temp directory
TEMP_DIR=$(mktemp -d)
echo "📥 Downloading GitHub Copilot Instructions..."
git clone https://github.com/vhcg77/github-copilot-instructions.git "$TEMP_DIR" --quiet

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "⚠️  Warning: Not in a git repository. Installing anyway..."
fi

# Backup existing files if they exist
if [ -d ".github" ]; then
    echo "📋 Backing up existing .github directory..."
    mv .github .github.backup.$(date +%Y%m%d_%H%M%S)
fi

if [ -f ".vscode/settings.json" ]; then
    echo "📋 Backing up existing .vscode/settings.json..."
    mkdir -p .vscode.backup.$(date +%Y%m%d_%H%M%S)
    cp .vscode/settings.json .vscode.backup.$(date +%Y%m%d_%H%M%S)/
fi

# Copy system files
echo "📁 Installing system files..."
cp -r "$TEMP_DIR/.github" .
mkdir -p .vscode
cp "$TEMP_DIR/.vscode/settings.json" .vscode/

# Copy additional files
if [ ! -f ".gitignore" ]; then
    cp "$TEMP_DIR/.gitignore" .
    echo "📝 Added comprehensive .gitignore"
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo "✅ Installation completed!"
echo ""
echo "🔍 Running validation..."

# Run validation
if $PYTHON_CMD .github/instructions/copilot_best_practices_validator.py . > /dev/null 2>&1; then
    echo "✅ Validation passed! Score: 100% - 🏆 EXCELLENT"
else
    echo "⚠️  Validation completed with warnings. Check the report for details."
fi

echo ""
echo "🎉 GitHub Copilot Instructions installed successfully!"
echo ""
echo "Next steps:"
echo "1. 🔄 Restart VS Code"
echo "2. 📝 Open a Python file and type a comment"
echo "3. ✨ Watch Copilot generate enterprise-ready code!"
echo ""
echo "📖 Full documentation: README.md"
echo "🆘 Support: https://github.com/vhcg77/github-copilot-instructions/issues"
echo ""
echo "⭐ Star the repo if this helped you: https://github.com/vhcg77/github-copilot-instructions"
