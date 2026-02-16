# Changelog

All notable changes to Claude Email will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-16

### Added
- Initial release of Claude Email skill ecosystem
- Main orchestrator skill (`email/SKILL.md`) with routing table and interactive mode
- User profile system with adaptive learning (`~/.claude/profiles/email/profile.json`)
- 6 sub-skills:
  - `email-check`: Inbox triage with AI importance scoring and reply suggestions
  - `email-write`: Email composition using proven copywriting frameworks
  - `email-review`: Pre-send quality review with 0-100 scoring system
  - `email-audit`: Domain deliverability audit (SPF/DKIM/DMARC, blacklists, compliance)
  - `email-sequence`: Automation sequence design (welcome, nurture, cart, etc.)
  - `email-plan`: Email marketing strategy with 90-day roadmap
- 4 subagent definitions:
  - `email-deliverability.md`: Technical DNS and authentication validation
  - `email-compliance.md`: Legal and regulatory compliance checks (CAN-SPAM, GDPR, CASL)
  - `email-content.md`: Copywriting analysis and framework application
  - `email-inbox.md`: Intelligent inbox triage logic
- 3 Python scripts:
  - `check_deliverability.py`: SPF/DKIM/DMARC DNS validation
  - `analyze_email_html.py`: HTML quality scoring and rendering analysis
  - `score_subject_line.py`: Subject line effectiveness scoring
- 6 reference files:
  - `deliverability-rules.md`: DNS configuration, authentication, reputation management
  - `benchmarks.md`: Industry-specific email marketing metrics
  - `compliance.md`: Legal requirements and best practices
  - `copy-frameworks.md`: PAS, AIDA, BAB, FAB, 4Ps framework guides
  - `technical-standards.md`: HTML/CSS email standards, accessibility
  - `mcp-integration.md`: Platform-specific MCP integration guides
- 6 industry strategy templates:
  - `local-business.md`: Local service business email strategy
  - `saas.md`: SaaS product email strategy
  - `ecommerce.md`: E-commerce email strategy
  - `creator.md`: Creator/influencer email strategy
  - `agency.md`: Agency/B2B email strategy
  - `generic.md`: General business email strategy
- 2 quality gate hooks:
  - `pre-send-check.sh`: Bash hook for pre-send validation
  - `validate-email-html.py`: Python hook for HTML quality validation
- Installation scripts:
  - `install.sh`: Unix/macOS installation (bash)
  - `install.ps1`: Windows installation (PowerShell)
  - `uninstall.sh`: Unified uninstallation script
- MCP integration support:
  - Gmail (taylorwilsdon/google_workspace_mcp) - Primary
  - Microsoft 365 (Softeria/ms-365-mcp-server) - Optional
  - SendGrid (Garoth/sendgrid-mcp) - Optional
  - Mailchimp - Optional
  - Kit.com (ConvertKit) - Optional
- Documentation:
  - README.md with quick start guide and examples
  - LICENSE (MIT)
  - This CHANGELOG

### Technical Details
- Follows Agent Skills open standard (SKILL.md with YAML frontmatter)
- 3-layer architecture: Directives (SKILL.md) + Orchestration (Claude) + Execution (scripts)
- Progressive disclosure: Metadata always loaded, instructions on activation, resources on demand
- Tier 4 ecosystem: Main orchestrator + sub-skills + agents + references + templates
- kebab-case naming convention for all skill directories
- JSON output format for all Python scripts

### Requirements
- Claude Code CLI (latest version)
- Python 3.10+ (for deliverability scripts)
- Gmail MCP or Outlook MCP (for inbox triage features)
- Optional: `checkdmarc` Python package for advanced DNS validation

---

## [Unreleased]

### Planned
- Zapier integration for automation workflows
- A/B testing framework for email campaigns
- Advanced analytics dashboard
- Bulk email validation tool
- Email template library (50+ pre-built templates)
- Multi-language support for international campaigns
- Integration with additional ESPs (ActiveCampaign, Brevo, HubSpot)
- Advanced spam score prediction using machine learning
- Email accessibility checker (WCAG compliance)
- Interactive email builder with drag-and-drop interface

---

[1.0.0]: https://github.com/AgriciDaniel/claude-email/releases/tag/v1.0.0
