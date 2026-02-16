# install.ps1 — Install claude-email skill ecosystem (Windows)
# Usage:
#   iwr -useb https://raw.githubusercontent.com/AgriciDaniel/claude-email/main/install.ps1 | iex
# Or:
#   powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"

$RepoUrl = "https://github.com/AgriciDaniel/claude-email"
$SkillsDir = Join-Path $env:USERPROFILE ".claude\skills"
$AgentsDir = Join-Path $env:USERPROFILE ".claude\agents"

function Main {
    Write-Host "Installing claude-email skill ecosystem..." -ForegroundColor Cyan
    Write-Host ""

    # Check prerequisites
    Check-Prerequisites

    # Create target directories
    New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null
    New-Item -ItemType Directory -Force -Path $AgentsDir | Out-Null

    # Clone repo to temp directory
    $TempDir = Join-Path $env:TEMP "claude-email-$(Get-Random)"
    try {
        Write-Host "Cloning repository..."
        git clone --depth 1 $RepoUrl $TempDir 2>&1 | Out-Null

        # Copy main orchestrator skill
        Write-Host "Installing main orchestrator skill..."
        $EmailSkillDir = Join-Path $SkillsDir "email"
        Copy-Item -Path (Join-Path $TempDir "email") -Destination $EmailSkillDir -Recurse -Force

        # Copy sub-skills
        Write-Host "Installing sub-skills..."
        $SubSkillsPath = Join-Path $TempDir "skills"
        if (Test-Path $SubSkillsPath) {
            Get-ChildItem -Path $SubSkillsPath -Directory -Filter "email-*" | ForEach-Object {
                $SkillName = $_.Name
                Copy-Item -Path $_.FullName -Destination (Join-Path $SkillsDir $SkillName) -Recurse -Force
                Write-Host "  ✓ $SkillName" -ForegroundColor Green
            }
        }

        # Copy agents
        Write-Host "Installing agents..."
        $AgentsPath = Join-Path $TempDir "agents"
        if (Test-Path $AgentsPath) {
            Get-ChildItem -Path $AgentsPath -File -Filter "email-*.md" | ForEach-Object {
                $AgentName = $_.Name
                Copy-Item -Path $_.FullName -Destination (Join-Path $AgentsDir $AgentName) -Force
                Write-Host "  ✓ $AgentName" -ForegroundColor Green
            }
        }

        # Copy scripts
        $ScriptsPath = Join-Path $TempDir "scripts"
        if (Test-Path $ScriptsPath) {
            Write-Host "Installing scripts..."
            $TargetScriptsDir = Join-Path $EmailSkillDir "scripts"
            Copy-Item -Path $ScriptsPath -Destination $TargetScriptsDir -Recurse -Force
        }

        # Copy hooks
        $HooksPath = Join-Path $TempDir "hooks"
        if (Test-Path $HooksPath) {
            Write-Host "Installing hooks..."
            $TargetHooksDir = Join-Path $EmailSkillDir "hooks"
            Copy-Item -Path $HooksPath -Destination $TargetHooksDir -Recurse -Force
        }

        # Install Python dependencies
        $RequirementsFile = Join-Path $TempDir "requirements.txt"
        if (Test-Path $RequirementsFile) {
            Write-Host "Installing Python dependencies..."
            try {
                if (Get-Command pip3 -ErrorAction SilentlyContinue) {
                    pip3 install -q -r $RequirementsFile 2>$null
                } elseif (Get-Command pip -ErrorAction SilentlyContinue) {
                    pip install -q -r $RequirementsFile 2>$null
                } else {
                    Write-Host "  ⚠️  pip not found — skipping Python dependencies" -ForegroundColor Yellow
                }
            } catch {
                Write-Host "  ⚠️  pip install failed — you may need to run: pip install -r requirements.txt" -ForegroundColor Yellow
            }
        }

        Write-Host ""
        Write-Host "✓ Installation complete!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Usage:"
        Write-Host "  /email                    — Interactive email assistant menu"
        Write-Host "  /email check              — Validate email before sending"
        Write-Host "  /email write              — Compose professional emails"
        Write-Host "  /email review             — Review and improve email drafts"
        Write-Host "  /email audit              — Analyze email deliverability"
        Write-Host "  /email sequence           — Build multi-email campaigns"
        Write-Host "  /email plan               — Design email strategy"
        Write-Host ""
        Write-Host "Skills installed at: $SkillsDir\email*"
        Write-Host "Agents installed at: $AgentsDir\email-*.md"
        Write-Host ""
    }
    finally {
        # Cleanup temp directory
        if (Test-Path $TempDir) {
            Remove-Item -Path $TempDir -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

function Check-Prerequisites {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
            Write-Host "Error: Python not found. Please install Python 3.7+." -ForegroundColor Red
            exit 1
        }
    }

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "Error: git not found. Please install git." -ForegroundColor Red
        exit 1
    }
}

# Run main function
Main
