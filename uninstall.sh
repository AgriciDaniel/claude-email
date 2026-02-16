#!/usr/bin/env bash
# uninstall.sh — Uninstall claude-email skill ecosystem
# Usage: bash uninstall.sh

set -euo pipefail

SKILLS_DIR="${HOME}/.claude/skills"
AGENTS_DIR="${HOME}/.claude/agents"

main() {
    echo "Uninstalling claude-email skill ecosystem..."
    echo ""

    REMOVED_COUNT=0

    # Remove main orchestrator skill
    if [[ -d "$SKILLS_DIR/email" ]]; then
        echo "Removing main orchestrator skill..."
        rm -rf "$SKILLS_DIR/email"
        echo "  ✓ email/"
        ((REMOVED_COUNT++))
    fi

    # Remove sub-skills
    echo "Removing sub-skills..."
    for skill_name in email-check email-write email-review email-audit email-sequence email-plan; do
        if [[ -d "$SKILLS_DIR/$skill_name" ]]; then
            rm -rf "$SKILLS_DIR/$skill_name"
            echo "  ✓ $skill_name/"
            ((REMOVED_COUNT++))
        fi
    done

    # Remove agent files
    echo "Removing agents..."
    for agent_file in "$AGENTS_DIR"/email-*.md; do
        if [[ -f "$agent_file" ]]; then
            agent_name=$(basename "$agent_file")
            rm -f "$agent_file"
            echo "  ✓ $agent_name"
            ((REMOVED_COUNT++))
        fi
    done

    echo ""
    if [[ $REMOVED_COUNT -eq 0 ]]; then
        echo "No claude-email skills found to remove."
    else
        echo "✓ Uninstallation complete!"
        echo "  Removed $REMOVED_COUNT skill(s) and agent(s)"
    fi
    echo ""
}

# Run main function
main "$@"
