# Claude Email — Comprehensive Email Management & Marketing

## Project Overview

This repository contains **Claude Email**, a Tier 4 Claude Code skill for inbox
management, email composition, quality review, deliverability auditing, automation
sequences, and email marketing strategy. It follows the Agent Skills open standard
and the 3-layer architecture (directive, orchestration, execution).

## Architecture

```
claude-email/
  CLAUDE.md                          # This file (project instructions)
  email/                             # Main orchestrator skill (Tier 4)
    SKILL.md                         # Entry point, routing table, user profile, quality gates
    references/                      # On-demand knowledge files (6 files)
      deliverability-rules.md       # SPF/DKIM/DMARC thresholds, bulk sender requirements
      benchmarks.md                 # KPI benchmarks by industry, scoring tables
      compliance.md                 # CAN-SPAM, GDPR, CCPA, RFC 8058
      copy-frameworks.md           # PAS, AIDA, BAB, FAB, 4Ps frameworks
      technical-standards.md        # HTML email rendering, dark mode, responsive
      mcp-integration.md           # Setup guides for Gmail, Outlook, SendGrid, etc.
  skills/                            # Sub-skills
    email-check/SKILL.md            # Inbox triage, categorization, reply suggestions
    email-write/SKILL.md            # Email composition with frameworks and templates
    email-review/SKILL.md           # Pre-send quality scoring (0-100)
    email-audit/SKILL.md            # Domain deliverability audit (SPF/DKIM/DMARC)
    email-sequence/SKILL.md         # Automation sequence designer
    email-plan/SKILL.md             # Email marketing strategy with industry templates
      assets/                       # Industry templates (local-business, saas, ecommerce, etc.)
  agents/                            # Subagent definitions
    email-deliverability.md         # Deliverability analysis agent
    email-compliance.md             # Compliance checking agent
    email-content.md                # Copy quality scoring agent
    email-inbox.md                  # Inbox categorization agent
  scripts/                           # Python execution scripts
    check_deliverability.py         # SPF/DKIM/DMARC checks via checkdmarc + dig
    analyze_email_html.py           # HTML email validation
    score_subject_line.py           # Subject line scoring algorithm
  hooks/                             # Quality gate hooks
    pre-send-check.sh              # Pre-send quality gate
    validate-email-html.py         # Post-edit HTML validation
  install.sh                         # Installation script
```

## Key Principles

1. **User Profile System**: First-run onboarding generates email-profile.md for personalized behavior
2. **MCP-First**: Integrates with Gmail/Outlook MCP for live inbox access
3. **Progressive Disclosure**: Metadata always loaded, instructions on activation, references on demand
4. **Quality Gates**: Score emails 0-100 before sending, audit domains before campaigns
5. **Industry Adaptation**: Templates and recommendations adapt to business type

## Development Rules

- Test with `python scripts/check_deliverability.py <domain> --json` after changes
- Keep SKILL.md files under 500 lines / 5000 tokens
- Reference files should be focused and under 200 lines
- Scripts must have docstrings, CLI interface, JSON output
- Follow kebab-case naming for all skill directories

## Commands

| Command | Purpose |
|---------|---------|
| `/email` | Interactive mode with inbox summary or menu |
| `/email check` | Inbox triage and reply suggestions |
| `/email write` | Compose emails with frameworks |
| `/email review` | Pre-send quality scoring |
| `/email audit <domain>` | Deliverability and compliance audit |
| `/email sequence <type>` | Design automation sequences |
| `/email plan <business>` | Email marketing strategy |

## MCP Dependencies

- **Required**: Gmail MCP (taylorwilsdon/google_workspace_mcp)
- **Optional**: Microsoft 365, SendGrid, Mailchimp, Kit.com
