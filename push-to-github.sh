#!/bin/bash
# Quick GitHub Push Script
# Save this as push-to-github.sh and run with: bash push-to-github.sh

# Configuration
REPO_NAME="health-chatbot"
GITHUB_USERNAME="YOUR-USERNAME"

echo "=========================================="
echo "GitHub Push Setup for $REPO_NAME"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized. Run: git init"
    exit 1
fi

echo "✓ Git repository found"
echo ""

# Instructions
echo "📋 FOLLOW THESE STEPS:"
echo ""
echo "1️⃣  Create a new repository on GitHub:"
echo "    Visit: https://github.com/new"
echo "    Name: $REPO_NAME"
echo "    Make it PUBLIC"
echo "    Don't initialize with README"
echo "    Click 'Create repository'"
echo ""

echo "2️⃣  Run these commands:"
echo ""
echo "    git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo "    git branch -m master main"
echo "    git push -u origin main"
echo ""

echo "3️⃣  Check GitHub:"
echo "    https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""

echo "=========================================="
echo "Ready to push? Update GITHUB_USERNAME above"
echo "Then run the commands in step 2!"
echo "=========================================="
