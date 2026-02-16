---
name: email
description: >
  Comprehensive email management and marketing for any business type. Inbox
  triage with importance scoring and AI reply suggestions via Gmail or Outlook
  MCP. Email composition using proven copy frameworks (PAS, AIDA, BAB, FAB).
  Pre-send quality review scoring subject lines, copy, HTML rendering, dark
  mode compatibility, and compliance. Domain deliverability auditing with
  SPF/DKIM/DMARC validation, blacklist checks, and bulk sender compliance
  (Google/Yahoo/Microsoft 2024-2026 rules). Automation sequence design for
  welcome series, nurture, re-engagement, abandoned cart, and post-purchase
  flows. Email marketing strategy with industry-specific templates for local
  businesses, SaaS, e-commerce, creators, and agencies. Triggers on: "email",
  "inbox", "check email", "write email", "compose", "email audit",
  "deliverability", "SPF", "DKIM", "DMARC", "email sequence", "welcome
  series", "email plan", "email marketing", "subject line", "email review".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
---

# Email -- Universal Email Management & Marketing Skill

Comprehensive email management across all business types (local services,
SaaS, e-commerce, creators, agencies). Orchestrates 6 specialized sub-skills
and 4 subagents.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/email` | Interactive mode: detect context, show inbox summary or menu |
| `/email check` | Inbox triage: scan, score importance, categorize, suggest replies |
| `/email write` | Compose email: choose framework, generate subject + body + HTML |
| `/email review <email>` | Pre-send quality check: score subject, copy, HTML, compliance |
| `/email audit <domain>` | Deliverability audit: SPF/DKIM/DMARC, blacklists, compliance |
| `/email sequence <type>` | Design automation: welcome, nurture, win-back, cart, custom |
| `/email plan <business>` | Email marketing strategy with industry template |

## Orchestration Logic

### Interactive Mode (`/email`)

When invoked without arguments:
1. Check for `email-profile.md` in project root
2. If missing, run first-time onboarding (see User Profile System below)
3. If profile exists, detect available MCP servers (Gmail, Outlook, SendGrid)
4. Show interactive menu with inbox summary if email MCP is available

### Command Routing

For specific commands, load the relevant sub-skill directly:
- `/email check` -> `skills/email-check/SKILL.md`
- `/email write` -> `skills/email-write/SKILL.md`
- `/email review` -> `skills/email-review/SKILL.md`
- `/email audit` -> `skills/email-audit/SKILL.md`
- `/email sequence` -> `skills/email-sequence/SKILL.md`
- `/email plan` -> `skills/email-plan/SKILL.md`

### Audit Delegation

When the user invokes `/email audit`, delegate to subagents in parallel:
1. Run `scripts/check_deliverability.py` for DNS-based checks
2. Spawn subagents: email-deliverability, email-compliance
3. Collect results and generate unified Email Health Score (0-100)
4. Create prioritized fix list (Critical -> High -> Medium -> Low)

## User Profile System

On first run, generate `email-profile.md` in the project root:

1. Detect existing MCP configurations:
   - Check for Gmail MCP tools (search_gmail_messages, send_gmail_message)
   - Check for Outlook MCP tools (list-mail-messages, send-mail)
   - Check for marketing MCPs (SendGrid, Mailchimp, Kit.com)
2. Ask 4 setup questions:
   - **Business type**: local business, SaaS, ecommerce, creator, agency, personal
   - **Primary email platform**: Gmail, Outlook, other
   - **Compliance regions**: US only, EU/GDPR, both
   - **Brand voice**: professional, friendly, casual, authoritative
3. Generate `email-profile.md` with these settings
4. All sub-skills reference this profile to adapt recommendations

### Profile-Driven Behavior

| Business Type | Emphasis |
|---------------|----------|
| Local business | Review requests, appointment reminders, loyalty, seasonal promos |
| SaaS | Onboarding sequences, feature announcements, churn prevention, NPS |
| Ecommerce | Abandoned cart, post-purchase, promotional, cross-sell/upsell |
| Creator | Newsletter, community engagement, monetization, content teasers |
| Agency | Client communication, project updates, case studies, proposals |
| Personal | Inbox management, reply drafts, organization |

## Quality Gates

Hard rules enforced across all sub-skills:
- Subject lines: 6-10 words / 30-50 characters
- Spam complaint rate must stay under 0.1% (hard limit: 0.3%)
- Bounce rate must stay under 2% (ideal: under 1%)
- HTML email total size under 102 KB (Gmail clips larger emails)
- Image-to-text ratio: minimum 60% text / 40% images
- Every marketing email must include unsubscribe mechanism
- Every marketing email must include physical postal address (CAN-SPAM)
- One-click unsubscribe headers required (RFC 8058) for bulk senders
- Honor unsubscribe requests within 2 business days
- Never send more than 20 emails per session without explicit approval
- Always show email draft for approval before sending

## Reference Files

Load these on-demand as needed -- do NOT load all at startup:
- `references/deliverability-rules.md` -- SPF/DKIM/DMARC validation, bulk sender rules
- `references/benchmarks.md` -- KPI benchmarks by industry, scoring thresholds
- `references/compliance.md` -- CAN-SPAM, GDPR, CCPA, RFC 8058 requirements
- `references/copy-frameworks.md` -- PAS, AIDA, BAB, FAB, 4Ps with templates
- `references/technical-standards.md` -- HTML rendering, dark mode, responsive design
- `references/mcp-integration.md` -- Setup guides for Gmail, Outlook, SendGrid, etc.

## Scoring Methodology

### Email Health Score (0-100) -- for `/email audit`

| Category | Weight |
|----------|--------|
| Authentication (SPF+DKIM+DMARC) | 40% |
| Blacklist Status | 20% |
| DNS Configuration | 15% |
| Compliance | 15% |
| TLS/Security | 10% |

### Email Quality Score (0-100) -- for `/email review`

| Category | Weight |
|----------|--------|
| Subject Line | 25% |
| Copy Quality | 25% |
| Technical (HTML) | 20% |
| Deliverability Signals | 15% |
| Compliance | 15% |

### Priority Levels
- **Critical**: Blocks delivery or causes blacklisting (immediate fix)
- **High**: Significantly impacts inbox placement (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

## Sub-Skills

This skill orchestrates 6 specialized sub-skills:

1. **email-check** -- Inbox triage, importance scoring, reply suggestions
2. **email-write** -- Email composition with copy frameworks and templates
3. **email-review** -- Pre-send quality scoring (0-100)
4. **email-audit** -- Domain deliverability audit (SPF/DKIM/DMARC, blacklists)
5. **email-sequence** -- Automation sequence design (welcome, nurture, win-back)
6. **email-plan** -- Email marketing strategy with industry templates

## Subagents

For parallel analysis during audits:
- `email-deliverability` -- SPF/DKIM/DMARC + blacklist + reputation checks
- `email-compliance` -- CAN-SPAM/GDPR/CCPA compliance scanning
- `email-content` -- Copy quality and framework adherence scoring
- `email-inbox` -- Inbox categorization and importance scoring

## MCP Integration

### Detecting Available MCP Tools

Check for these tool patterns to determine available platforms:
- **Gmail**: `search_gmail_messages`, `send_gmail_message`, `get_gmail_message_content`
- **Outlook**: `list-mail-messages`, `send-mail`, `get-mail-message`
- **SendGrid**: `send_single_email`, `list_all_contacts`, `get_stats`
- **Mailchimp**: `get_campaigns`, `create_campaign`, `send_campaign`
- **Kit.com**: `kit_list_subscribers`, `kit_create_broadcast`

If no email MCP is detected, inform the user and offer setup guidance
from `references/mcp-integration.md`.
