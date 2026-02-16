#!/usr/bin/env bash
# install.sh — Install claude-email skill ecosystem
# Usage: curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-email/main/install.sh | bash

set -euo pipefail

REPO_URL="https://github.com/AgriciDaniel/claude-email"
SKILLS_DIR="${HOME}/.claude/skills"
AGENTS_DIR="${HOME}/.claude/agents"

main() {
    echo "Installing claude-email skill ecosystem..."
    echo ""

    # Check prerequisites
    check_prerequisites

    # Create target directories
    mkdir -p "$SKILLS_DIR"
    mkdir -p "$AGENTS_DIR"

    # Clone repo to temp directory
    TEMP_DIR=$(mktemp -d)
    trap 'rm -rf "$TEMP_DIR"' EXIT

    echo "Cloning repository..."
    git clone --depth 1 "$REPO_URL" "$TEMP_DIR" >/dev/null 2>&1

    # Copy main orchestrator skill
    echo "Installing main orchestrator skill..."
    cp -r "$TEMP_DIR/email" "$SKILLS_DIR/"

    # Copy sub-skills
    echo "Installing sub-skills..."
    for skill_dir in "$TEMP_DIR/skills"/email-*; do
        if [[ -d "$skill_dir" ]]; then
            skill_name=$(basename "$skill_dir")
            cp -r "$skill_dir" "$SKILLS_DIR/"
            echo "  ✓ $skill_name"
        fi
    done

    # Copy agents
    echo "Installing agents..."
    if [[ -d "$TEMP_DIR/agents" ]]; then
        for agent_file in "$TEMP_DIR/agents"/email-*.md; do
            if [[ -f "$agent_file" ]]; then
                agent_name=$(basename "$agent_file")
                cp "$agent_file" "$AGENTS_DIR/"
                echo "  ✓ $agent_name"
            fi
        done
    fi

    # Copy scripts (if exists)
    if [[ -d "$TEMP_DIR/scripts" ]]; then
        echo "Installing scripts..."
        cp -r "$TEMP_DIR/scripts" "$SKILLS_DIR/email/"
        chmod +x "$SKILLS_DIR/email/scripts"/*.py 2>/dev/null || true
    fi

    # Copy hooks and make executable
    if [[ -d "$TEMP_DIR/hooks" ]]; then
        echo "Installing hooks..."
        cp -r "$TEMP_DIR/hooks" "$SKILLS_DIR/email/"
        chmod +x "$SKILLS_DIR/email/hooks"/*.sh 2>/dev/null || true
        chmod +x "$SKILLS_DIR/email/hooks"/*.py 2>/dev/null || true
    fi

    # Install Python dependencies
    if [[ -f "$TEMP_DIR/requirements.txt" ]]; then
        echo "Installing Python dependencies..."
        if command -v pip3 >/dev/null 2>&1; then
            pip3 install -q -r "$TEMP_DIR/requirements.txt" 2>/dev/null || {
                echo "  ⚠️  pip install failed — you may need to run: pip3 install -r requirements.txt"
            }
        elif command -v pip >/dev/null 2>&1; then
            pip install -q -r "$TEMP_DIR/requirements.txt" 2>/dev/null || {
                echo "  ⚠️  pip install failed — you may need to run: pip install -r requirements.txt"
            }
        else
            echo "  ⚠️  pip not found — skipping Python dependencies"
        fi
    fi

    echo ""
    echo "✓ Installation complete!"
    echo ""
    echo "Usage:"
    echo "  /email                    — Interactive email assistant menu"
    echo "  /email check              — Validate email before sending"
    echo "  /email write              — Compose professional emails"
    echo "  /email review             — Review and improve email drafts"
    echo "  /email audit              — Analyze email deliverability"
    echo "  /email sequence           — Build multi-email campaigns"
    echo "  /email plan               — Design email strategy"
    echo ""
    echo "Skills installed at: $SKILLS_DIR/email*"
    echo "Agents installed at: $AGENTS_DIR/email-*.md"
    echo ""
}

check_prerequisites() {
    if ! command -v python3 >/dev/null 2>&1; then
        echo "Error: python3 not found. Please install Python 3.7+."
        exit 1
    fi

    if ! command -v git >/dev/null 2>&1; then
        echo "Error: git not found. Please install git."
        exit 1
    fi
}

# Run main function (prevents partial execution on curl pipe)
main "$@"
