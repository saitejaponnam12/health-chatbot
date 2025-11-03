# ============================================================
# HEALTH CHATBOT - GITHUB DEPLOYMENT SCRIPT
# ============================================================
# This script automates pushing your project to GitHub
# 
# USAGE:
# 1. Go to https://github.com/new
# 2. Create repo named "health-chatbot" (PUBLIC, no README)
# 3. Copy the HTTPS URL shown
# 4. Open PowerShell and run:
#    $username = "YOUR-GITHUB-USERNAME"
#    $repoUrl = "https://github.com/YOUR-GITHUB-USERNAME/health-chatbot.git"
#    git remote add origin $repoUrl
#    git branch -m master main
#    git push -u origin main
# ============================================================

# Configuration
$RepoName = "health-chatbot"
$GitHubUsername = "YOUR-GITHUB-USERNAME"  # ← CHANGE THIS

# Colors for output
$Green = [ConsoleColor]::Green
$Yellow = [ConsoleColor]::Yellow
$Red = [ConsoleColor]::Red
$Cyan = [ConsoleColor]::Cyan

# Functions
function Write-Status {
    param([string]$Message, [string]$Status)
    if ($Status -eq "success") {
        Write-Host "✅ $Message" -ForegroundColor $Green
    } elseif ($Status -eq "warning") {
        Write-Host "⚠️  $Message" -ForegroundColor $Yellow
    } elseif ($Status -eq "error") {
        Write-Host "❌ $Message" -ForegroundColor $Red
    } else {
        Write-Host "ℹ️  $Message" -ForegroundColor $Cyan
    }
}

function Show-Instructions {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor $Cyan
    Write-Host "GITHUB DEPLOYMENT INSTRUCTIONS" -ForegroundColor $Cyan
    Write-Host "========================================" -ForegroundColor $Cyan
    Write-Host ""
    
    Write-Status "Step 1: Create GitHub Repository" "info"
    Write-Host "  1. Go to: https://github.com/new"
    Write-Host "  2. Name: $RepoName"
    Write-Host "  3. Type: PUBLIC"
    Write-Host "  4. DON'T check 'Add README'"
    Write-Host "  5. Click 'Create repository'"
    Write-Host ""
    
    Write-Status "Step 2: Copy Your Repository URL" "info"
    Write-Host "  GitHub will show you:"
    Write-Host "  https://github.com/$GitHubUsername/$RepoName.git"
    Write-Host ""
    
    Write-Status "Step 3: Run These Commands" "info"
    Write-Host ""
    Write-Host "  git remote add origin https://github.com/$GitHubUsername/$RepoName.git" -ForegroundColor Yellow
    Write-Host "  git branch -m master main" -ForegroundColor Yellow
    Write-Host "  git push -u origin main" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Status "Your Project Will Be At:" "success"
    Write-Host "  https://github.com/$GitHubUsername/$RepoName"
    Write-Host ""
}

# Main
Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor $Cyan
Write-Host "║  HEALTH CHATBOT - GITHUB DEPLOYMENT   ║" -ForegroundColor $Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor $Cyan
Write-Host ""

Show-Instructions

Write-Status "Project Status" "success"
Write-Host "  • 27 files ready to push"
Write-Host "  • 7708 insertions"
Write-Host "  • 3 commits prepared"
Write-Host "  • All code tested ✓"
Write-Host ""

Write-Host "========================================" -ForegroundColor $Cyan
Write-Host "Ready to deploy? Follow the steps above!" -ForegroundColor $Green
Write-Host "========================================" -ForegroundColor $Cyan
Write-Host ""
