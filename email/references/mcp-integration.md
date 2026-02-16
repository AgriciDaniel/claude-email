# MCP Integration Setup Guide

This guide covers setup for all supported email MCP servers. The email skill auto-detects available tools and adapts functionality accordingly.

## Gmail MCP (Primary — Recommended)

**Server:** taylorwilsdon/google_workspace_mcp
**Install:** `uvx workspace-mcp` or `pip install workspace-mcp`

### Configuration

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "uvx",
      "args": ["workspace-mcp"],
      "env": {
        "GOOGLE_OAUTH_CREDENTIALS": "/path/to/credentials.json",
        "GOOGLE_OAUTH_TOKEN": "/path/to/token.json"
      }
    }
  }
}
```

### Setup Steps

1. **Google Cloud Console** → Create new project
2. **APIs & Services** → Enable Gmail API
3. **OAuth consent screen** → Configure (External, test users)
4. **Credentials** → Create OAuth 2.0 Client ID (Desktop app)
5. Download `credentials.json` to secure location
6. Run `uvx workspace-mcp` first time to authorize → generates `token.json`
7. Update paths in settings.json

### Key Tools

| Tool | Purpose |
|------|---------|
| search_gmail_messages | Search with query syntax |
| get_gmail_messages_content_batch | Fetch multiple emails |
| send_gmail_message | Send email |
| draft_gmail_message | Create draft |
| get_gmail_thread_content | Get conversation thread |
| list_gmail_labels | List labels/folders |
| manage_gmail_label | Add/remove labels |
| create_gmail_filter | Create filter rules |

## Microsoft 365 MCP (Optional)

**Server:** Softeria/ms-365-mcp-server
**Install:** npm-based

### Configuration

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "ms-365": {
      "command": "npx",
      "args": ["-y", "ms-365-mcp-server"],
      "env": {
        "AZURE_CLIENT_ID": "your-client-id",
        "AZURE_TENANT_ID": "your-tenant-id",
        "AZURE_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

### Setup Steps

1. **Azure Portal** → App registrations → New registration
2. **API permissions** → Add permissions:
   - Mail.Read
   - Mail.Send
   - Mail.ReadWrite
   - Calendars.Read (optional)
3. **Certificates & secrets** → New client secret
4. Copy Client ID, Tenant ID, Secret to config

### Key Tools

| Tool | Purpose |
|------|---------|
| list-mail-messages | List inbox/folder messages |
| get-mail-message | Get single message |
| send-mail | Send email |
| create-draft-email | Create draft |

## SendGrid MCP (Optional — Marketing/Transactional)

**Server:** Garoth/sendgrid-mcp
**Install:** Clone repo + `npm install`

### Configuration

```json
{
  "mcpServers": {
    "sendgrid": {
      "command": "node",
      "args": ["/path/to/sendgrid-mcp/index.js"],
      "env": {
        "SENDGRID_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Setup Steps

1. **SendGrid Dashboard** → Settings → API Keys
2. Create API key with Full Access (or Mail Send + Stats permissions)
3. Copy key to config

### Key Tools

| Tool | Purpose |
|------|---------|
| send_single_email | Send transactional email |
| list_all_contacts | List contacts |
| create_template | Create email template |
| get_stats | Get sending statistics |

**Free Tier:** 100 emails/day forever

## Mailchimp MCP (Optional — Marketing)

**Server:** mattcoatsworth/mailchip-mcp-server
**Install:** npm-based

### Configuration

```json
{
  "mcpServers": {
    "mailchimp": {
      "command": "npx",
      "args": ["-y", "mailchimp-mcp-server"],
      "env": {
        "MAILCHIMP_API_KEY": "your-api-key",
        "MAILCHIMP_SERVER_PREFIX": "us1"
      }
    }
  }
}
```

### Key Tools

| Tool | Purpose |
|------|---------|
| get_campaigns | List campaigns |
| create_campaign | Create new campaign |
| send_campaign | Send campaign |
| get_lists | Get audience lists |
| add_list_member | Add subscriber |
| get_campaign_reports | Campaign analytics |

**Free Tier:** 500 contacts, 1000 sends/month

## Kit.com / ConvertKit MCP (Optional — Creator)

**Server:** aplaceforallmystuff/mcp-kit
**Install:** npm-based, requires Node.js 18+

### Configuration

```json
{
  "mcpServers": {
    "kit": {
      "command": "npx",
      "args": ["-y", "mcp-kit"],
      "env": {
        "KIT_API_SECRET": "your-api-secret"
      }
    }
  }
}
```

### Key Tools

Subscribers, tags, sequences, broadcasts, webhooks management

**Free Tier:** Up to 10,000 subscribers

## CLI Tools (No MCP Required)

### checkdmarc (Deliverability Checks)

```bash
pip install checkdmarc
checkdmarc example.com
```

Returns SPF, DMARC, DKIM validation results

### dig (DNS Lookups — Pre-installed)

```bash
dig txt example.com                              # SPF record
dig txt _dmarc.example.com                       # DMARC record
dig txt selector._domainkey.example.com          # DKIM record
dig mx example.com                               # MX records
```

## Tool Detection

The email skill auto-detects available platforms by checking for these tool patterns:

| Tool Pattern | Detected Platform |
|-------------|-------------------|
| search_gmail_messages | Gmail |
| list-mail-messages | Outlook 365 |
| send_single_email (SendGrid context) | SendGrid |
| get_campaigns (Mailchimp context) | Mailchimp |
| kit_list_subscribers | Kit.com |

## Offline Mode

If no email MCP server is detected, the skill operates in **offline mode**:

**Available:**
- Email composition and review
- Template creation
- Copy auditing
- Deliverability analysis (via checkdmarc/dig)

**Requires MCP:**
- Inbox checking
- Sending emails
- Draft creation
- Thread management
- Analytics/reporting

## Troubleshooting

### MCP Server Not Connecting

```bash
# Check Claude Code logs
tail -f ~/.claude/logs/mcp.log

# Test MCP server manually
uvx workspace-mcp  # Should start without errors
```

### Gmail OAuth Expired

Delete `token.json` and re-run authorization flow:

```bash
rm /path/to/token.json
uvx workspace-mcp  # Opens browser for re-auth
```

### Tool Not Found

Use `ListMcpResourcesTool` to verify available tools:
- Email skill will list detected tools on first run
- Check server name matches expected tool patterns

<!-- Updated: 2026-02-16 -->
