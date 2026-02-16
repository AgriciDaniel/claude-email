---
name: email-audit
description: Audits email domain deliverability setup (SPF, DKIM, DMARC, MX records, blacklists, TLS) and generates health score (0-100) with prioritized fix list. Checks bulk sender compliance against Google/Yahoo/Microsoft 2024-2026 requirements. Provides DNS records to add/update. Use when user asks to audit, check, or analyze email deliverability, domain health, or inbox placement.
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Email Audit Sub-Skill

## Purpose

Performs comprehensive email deliverability auditing for a domain. Checks DNS authentication records (SPF, DKIM, DMARC), infrastructure (MX, PTR, TLS), reputation (blacklists), and bulk sender compliance. Generates a health score (0-100) with prioritized fixes.

## Input

- **Domain name**: e.g., `rankenstein.cloud`, `example.com`
- **Optional**: Email volume (triggers bulk sender compliance checks if 5,000+ emails/day)

## Audit Categories

### 1. SPF Record (Weight: 10%)

**What to check:**
- SPF record exists at `TXT <domain>`
- Valid syntax: starts with `v=spf1`
- DNS lookup count (max 10, warn at 8+)
- Enforcement level: `-all` (pass), `~all` (softfail), `?all` (neutral), `+all` (fail)
- No multiple SPF records (causes validation failure)
- Includes are efficient and necessary

**Commands:**
```bash
dig txt <domain> +short | grep "v=spf1"
# or
python scripts/check_deliverability.py <domain> --spf
```

**Scoring:**
- Valid + hard fail (`-all`): 100 points
- Valid + soft fail (`~all`): 70 points
- Valid + neutral/pass all: 40 points
- Invalid syntax or 10+ lookups: 20 points
- Missing: 0 points

### 2. DKIM Record (Weight: 15%)

**What to check:**
- At least one valid DKIM record exists
- Key length: 2048-bit (required minimum per NIST), 1024-bit (legacy, upgrade recommended)
- Common selectors: `google`, `default`, `selector1`, `selector2`, `k1`, `mandrill`, `dkim`

**Commands:**
```bash
dig txt google._domainkey.<domain> +short
dig txt default._domainkey.<domain> +short
dig txt selector1._domainkey.<domain> +short
# Check common selectors
```

**Note:** DKIM selectors are not discoverable without prior knowledge. Check common ones and ask user if their email provider uses a specific selector.

**Scoring:**
- 2048-bit key found: 100 points
- 1024-bit key found: 70 points
- Invalid/weak key: 30 points
- Missing: 0 points

### 3. DMARC Policy (Weight: 15%)

**What to check:**
- DMARC record exists at `TXT _dmarc.<domain>`
- Policy level: `p=reject` (excellent), `p=quarantine` (good), `p=none` (monitoring)
- Aggregate reporting (`rua=`) tag present
- Forensic reporting (`ruf=`) tag present (optional)
- Alignment mode: `aspf=` (SPF) and `adkim=` (DKIM) - relaxed vs strict
- Percentage (`pct=`) should be 100 for full enforcement

**Commands:**
```bash
dig txt _dmarc.<domain> +short
```

**Scoring:**
- `p=reject` + `rua` + `pct=100`: 100 points
- `p=quarantine` + `rua`: 80 points
- `p=none` + `rua`: 40 points
- `p=none` without reporting: 20 points
- Missing: 0 points

### 4. MX Records (Weight: 10%)

**What to check:**
- Valid MX records exist
- MX hosts resolve to IP addresses
- Priority ordering is logical
- Mail provider identification (Google Workspace, Microsoft 365, custom)

**Commands:**
```bash
dig mx <domain> +short
dig a <mx-hostname> +short
```

**Scoring:**
- Valid + all hosts resolve + known provider: 100 points
- Valid + all hosts resolve: 80 points
- Valid but some hosts don't resolve: 40 points
- Missing or invalid: 0 points

### 5. Reverse DNS / PTR (Weight: 5%)

**What to check:**
- PTR records exist for MX server IPs
- PTR records match forward DNS (hostname matches)

**Commands:**
```bash
dig -x <mx-ip> +short
```

**Scoring:**
- All MX IPs have matching PTR: 100 points
- Partial PTR coverage: 50 points
- Missing PTR: 0 points

### 6. TLS/STARTTLS (Weight: 10%)

**What to check:**
- STARTTLS support on MX servers (port 25)
- TLS version (1.2+ recommended)

**Commands:**
```bash
openssl s_client -starttls smtp -connect <mx-hostname>:25 -brief
```

**Note:** This may require network access. If not available, note as "Unable to verify".

**Scoring:**
- TLS 1.2+ with STARTTLS: 100 points
- TLS 1.0/1.1 with STARTTLS: 60 points
- No STARTTLS: 0 points

### 7. Blacklist Check (Weight: 20%)

**What to check:**
- Domain and MX IP addresses against major blacklists:
  - Spamhaus (SBL, XBL, PBL)
  - Barracuda
  - SORBS
  - SpamCop
  - URIBL
  - Invaluement

**Commands:**
```bash
# Use checkdmarc library if available
python -c "import checkdmarc; print(checkdmarc.check_domains(['<domain>']))"

# Or manual checks
dig <ip>.zen.spamhaus.org +short
dig <ip>.b.barracudacentral.org +short
```

**Scoring:**
- Clean on all lists: 100 points
- Listed on 1 minor list: 50 points
- Listed on 1 major list (Spamhaus, Barracuda): 30 points
- Listed on 2+ major lists: 0 points

**Critical:** Any listing on major blacklists severely impacts deliverability.

### 8. Bulk Sender Compliance (Weight: 10%)

**Applies to:** Domains sending 5,000+ emails/day to Gmail, Yahoo, Microsoft recipients.

**Requirements (Google/Yahoo/Microsoft 2024-2026 rules):**
1. **Both SPF AND DKIM** must pass (not just one)
2. **DMARC** policy at minimum `p=none` with alignment
3. **One-click unsubscribe** header (RFC 8058: `List-Unsubscribe-Post: One-Click`)
4. **Spam complaint rate** under 0.3% (target under 0.1%)
5. **Valid forward and reverse DNS** (PTR records)
6. **Honor unsubscribe** within 2 business days
7. **No impersonation** of Gmail/Yahoo/Microsoft from headers
8. **TLS** connection for message transmission

**Scoring:**
- All 8 requirements met: 100 points
- 6-7 requirements met: 70 points
- 4-5 requirements met: 50 points
- Less than 4 met: 0 points

### 9. Additional Checks (Weight: 5%)

**Bonus points for:**
- **BIMI** record (Brand Indicators for Message Identification) at `TXT default._bimi.<domain>`
- **MTA-STS** policy at `https://mta-sts.<domain>/.well-known/mta-sts.txt`
- **TLSRPT** record at `TXT _smtp._tls.<domain>` (TLS reporting)
- **Mail-from domain alignment** (DKIM/SPF align with From: domain)

**Commands:**
```bash
dig txt default._bimi.<domain> +short
curl https://mta-sts.<domain>/.well-known/mta-sts.txt
dig txt _smtp._tls.<domain> +short
```

**Scoring:**
- Each bonus feature: +25 points (max 100)

## Health Score Calculation

**Formula:**
```
Total Score = (SPF × 0.10) + (DKIM × 0.15) + (DMARC × 0.15) + (MX × 0.10) +
              (PTR × 0.05) + (TLS × 0.10) + (Blacklists × 0.20) +
              (Bulk Compliance × 0.10) + (Extras × 0.05)
```

**Score Interpretation:**

| Score | Rating | Status | Action |
|-------|--------|--------|--------|
| 90-100 | Excellent | All critical checks pass, fully compliant | Monitor regularly |
| 75-89 | Good | Minor issues, generally deliverable | Fix medium priority items |
| 60-74 | Fair | Issues that could impact inbox placement | Fix high priority items within 1 week |
| 40-59 | Poor | Significant deliverability risks | Fix critical items immediately |
| 0-39 | Critical | Major issues, emails likely going to spam | Emergency fixes required |

## Workflow

### Step 1: Gather Domain Information
Ask user for:
- Domain name to audit
- Approximate email volume (to trigger bulk sender checks)
- Known DKIM selector (if not using common ones)

### Step 2: Parallel Delegation
Spawn these agents in parallel for faster auditing:

**Agent 1: email-deliverability**
```
Check DNS authentication records for <domain>:
- SPF record validation
- DKIM record discovery (selectors: google, default, selector1, selector2, k1)
- DMARC policy analysis
- MX record validation
- PTR/reverse DNS check

Return JSON with pass/fail status and raw records.
```

**Agent 2: email-compliance**
```
Check bulk sender compliance for <domain>:
- Verify both SPF and DKIM pass
- Check DMARC alignment
- Note TLS support
- Check for List-Unsubscribe headers (if sample email provided)

Return compliance checklist with met/not met status.
```

**Agent 3: email-reputation** (if tools available)
```
Check reputation for <domain>:
- Blacklist status (Spamhaus, Barracuda, SORBS, SpamCop)
- Historical deliverability issues
- Spam complaint rate (if available)

Return list of blacklist hits and reputation score.
```

### Step 3: Aggregate Results
Collect results from all agents and calculate weighted health score.

### Step 4: Generate Prioritized Fix List
Categorize issues by priority:

**Critical (Fix Immediately):**
- Blacklist listings
- Missing SPF/DKIM/DMARC
- Invalid DNS records
- MX records not resolving

**High (Fix Within 1 Week):**
- Weak SPF enforcement (`~all` instead of `-all`)
- 1024-bit DKIM keys (upgrade to 2048-bit)
- DMARC policy `p=none` (upgrade to `p=quarantine` or `p=reject`)
- Missing PTR records

**Medium (Fix Within 1 Month):**
- Missing aggregate reporting (`rua` tag)
- No TLS/STARTTLS support
- SPF approaching 10 DNS lookup limit
- Missing bonus features (BIMI, MTA-STS, TLSRPT)

### Step 5: Generate DNS Record Recommendations
Provide exact DNS records to add/update with copy-paste ready values.

## Output Format

Structure the audit report as:

1. **Header**: `## Email Deliverability Audit: [domain]` with date, health score, rating
2. **Authentication table**: SPF/DKIM/DMARC with status, score, raw records
3. **Infrastructure table**: MX/PTR/TLS with status, score, provider detection
4. **Reputation**: Blacklist status across Spamhaus, Barracuda, SORBS, SpamCop
5. **Bulk Sender Compliance**: 8-requirement checklist (Google/Yahoo/Microsoft rules)
6. **Bonus Features**: BIMI, MTA-STS, TLSRPT, Mail-from alignment
7. **Prioritized Fix List**: Critical/High/Medium with impact, fix steps, DNS records
8. **DNS Records to Add**: Copy-paste ready TXT/MX records
9. **Next Steps**: Immediate, this week, this month, monitoring, re-audit

Use score weights from Health Score Calculation section. Use status badges: ✅ PASS, ⚠️ WARN, ❌ FAIL.

## Tools

Run `python scripts/check_deliverability.py <domain> --json` for automated DNS checks.

Manual DNS commands (used in audit categories above):
- SPF: `dig txt <domain> +short`
- DKIM: `dig txt <selector>._domainkey.<domain> +short`
- DMARC: `dig txt _dmarc.<domain> +short`
- MX: `dig mx <domain> +short`
- PTR: `dig -x <ip> +short`
- TLS: `openssl s_client -starttls smtp -connect <mx-hostname>:25 -brief`

## Quality Gates

Before delivering audit results:
1. **All critical checks completed** (SPF, DKIM, DMARC, MX, Blacklists)
2. **Health score calculated** with breakdown by category
3. **Prioritized fix list generated** with specific action steps
4. **DNS records provided** in copy-paste ready format
5. **Score interpretation explained** with next steps

## Error Handling

**If DNS queries fail:**
- Note as "Unable to verify" in audit report
- Provide manual check instructions
- Suggest alternative DNS servers (8.8.8.8, 1.1.1.1)

**If DKIM selector unknown:**
- Check common selectors (google, default, selector1, selector2)
- Ask user for their email provider's DKIM selector
- Note as "DKIM selector not found - requires manual verification"

**If no MX records found:**
- Critical failure - domain cannot receive email
- Check if domain uses mail forwarding (Cloudflare, etc.)
- Provide setup instructions for email hosting

## References

Load on demand:
- `references/deliverability-rules.md` - Scoring thresholds and compliance rules
- `references/mcp-integration.md` - Provider-specific setup and DNS configuration
- `references/compliance.md` - Compliance rules and regulatory requirements

## Success Criteria

Audit is successful when:
- Health score accurately reflects deliverability state
- All critical issues identified with clear severity levels
- User receives actionable DNS records to implement
- Fix priority aligns with business impact
- Re-audit timeframe provided based on score
