#!/usr/bin/env pwsh
# claude-email uninstaller for Windows

$ErrorActionPreference = "Stop"

function Main {
    $SkillDir = Join-Path $env:USERPROFILE ".claude" "skills"
    $AgentDir = Join-Path $env:USERPROFILE ".claude" "agents"

    Write-Host "=== Uninstalling claude-email ===" -ForegroundColor Cyan
    Write-Host ""

    # Remove main skill
    $mainDir = Join-Path $SkillDir "email"
    if (Test-Path $mainDir) {
        Remove-Item -Recurse -Force $mainDir
        Write-Host "  Removed: $mainDir" -ForegroundColor Green
    }

    # Remove sub-skills
    $subSkills = @("email-audit", "email-check", "email-plan", "email-review", "email-sequence", "email-write")
    foreach ($skill in $subSkills) {
        $skillPath = Join-Path $SkillDir $skill
        if (Test-Path $skillPath) {
            Remove-Item -Recurse -Force $skillPath
            Write-Host "  Removed: $skillPath" -ForegroundColor Green
        }
    }

    # Remove agents
    $agents = @("email-compliance", "email-content", "email-deliverability", "email-inbox")
    foreach ($agent in $agents) {
        $agentPath = Join-Path $AgentDir "$agent.md"
        if (Test-Path $agentPath) {
            Remove-Item -Force $agentPath
            Write-Host "  Removed: $agentPath" -ForegroundColor Green
        }
    }

    Write-Host ""
    Write-Host "=== claude-email uninstalled ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Restart Claude Code to complete removal." -ForegroundColor Yellow
}

Main
