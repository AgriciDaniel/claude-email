# Email Deliverability Rules & Thresholds

This reference provides validation rules, thresholds, and best practices for email deliverability.

---

## SPF (Sender Policy Framework) Validation

### Core Rules
- **DNS Lookup Limit**: Maximum 10 DNS lookups per SPF record (RFC 7208)
- **Warning Threshold**: 8+ lookups (approaching limit, flattening recommended)
- **Record Limit**: Only 1 SPF record allowed per domain (multiple = invalid)
- **Syntax**: `v=spf1 [mechanisms] [qualifiers]`

### Qualifiers
| Qualifier | Meaning | Usage |
|-----------|---------|-------|
| `-all` | Hard fail | Recommended for production (reject unauthorized) |
| `~all` | Soft fail | Testing phase (flag as suspicious) |
| `?all` | Neutral | Not recommended (no policy) |
| `+all` | Pass all | Never use (allows anyone to spoof) |

### Common Includes
- `_spf.google.com` - Google Workspace (3 lookups)
- `spf.protection.outlook.com` - Microsoft 365 (1 lookup)
- `_spf.salesforce.com` - Salesforce (2 lookups)
- `sendgrid.net` - SendGrid (1 lookup)
- `_spf.mlsend.com` - MailerLite (2 lookups)
- `servers.mcsv.net` - Mailchimp (1 lookup)

### SPF Flattening
When approaching the 10-lookup limit:
1. Replace `include:` mechanisms with direct IP ranges (`ip4:` / `ip6:`)
2. Use SPF flattening services (automated IP range updates)
3. Example: Replace `include:_spf.google.com` with `ip4:35.190.247.0/24 ip4:64.233.160.0/19`
4. Warning: Manual flattening requires periodic updates when providers change IPs

### Validation Checks
- ✅ Single SPF record exists
- ✅ DNS lookup count ≤ 10
- ✅ Uses `-all` qualifier (production domains)
- ✅ Includes all authorized sending sources
- ⚠️ 8-9 lookups (consider flattening)
- ❌ Multiple SPF records
- ❌ 10+ lookups (invalid, will fail)

---

## DKIM (DomainKeys Identified Mail) Validation

### Key Requirements
- **Minimum Key Size**: 2048-bit (NIST recommended minimum as of 2024)
- **Legacy Key Size**: 1024-bit (deprecated; still accepted by most providers but upgrade strongly recommended)
- **Key Rotation**: Every 6-12 months
- **Selector Naming**: Use descriptive selectors (e.g., `google`, `k1`, `selector1`)

### Common Selectors by Provider
| Provider | Selector(s) | Notes |
|----------|-------------|-------|
| Google Workspace | `google` | Single selector |
| Microsoft 365 | `selector1`, `selector2` | Dual selector rotation |
| Mailchimp | `k1`, `k2`, `k3` | Multiple selectors |
| Mandrill | `mandrill` | Single selector |
| SendGrid | `s1`, `s2` | Dual selector |
| Brevo (Sendinblue) | `mail`, `mail2` | Dual selector |

### Required Header Coverage
DKIM signature MUST cover these headers for bulk senders:
- `From`
- `To`
- `Subject`
- `Date`
- `List-Unsubscribe`
- `List-Unsubscribe-Post`

### DKIM Discovery Process
1. Check common selectors: `google`, `default`, `selector1`, `selector2`, `k1`, `mandrill`, `dkim`
2. Query DNS: `dig TXT <selector>._domainkey.<domain>`
3. Validate key format: `v=DKIM1; k=rsa; p=<public-key>`
4. Check key length from public key string

### Validation Checks
- ✅ DKIM record exists for active selector
- ✅ Key size ≥ 2048-bit
- ✅ Covers List-Unsubscribe headers (bulk senders)
- ⚠️ Key size 1024-bit (upgrade recommended)
- ⚠️ Key age > 12 months (rotate recommended)
- ❌ Key size < 1024-bit (insecure)
- ❌ Invalid record syntax

---

## ARC (Authenticated Received Chain) - RFC 8617

ARC preserves authentication results across mail forwarding hops. When a mailing list or forwarding service relays a message, SPF and DKIM can break. ARC allows the final receiver to validate the chain of custody.

**Relevance:** Google, Microsoft, and Yahoo use ARC results when SPF/DKIM fail due to forwarding. Not directly configurable by senders — handled by intermediaries (mailing lists, forwarding services). Awareness is important when diagnosing "SPF pass but DMARC fail" scenarios caused by mail forwarding.

---

## DMARC (Domain-based Message Authentication) Validation

### Rollout Sequence
Progressive enforcement recommended:
1. **p=none** - Monitor mode (collect reports, no enforcement)
2. **p=quarantine** - Flag as spam (after monitoring 30+ days)
3. **p=reject** - Block at SMTP (after quarantine 30+ days)

### Required Tags
- `p=` - Policy for domain (none/quarantine/reject)
- `rua=` - Aggregate report email (required for monitoring)

### Optional Tags
| Tag | Purpose | Recommended Value |
|-----|---------|-------------------|
| `pct=` | Percentage of messages to enforce | `100` (full enforcement) |
| `sp=` | Subdomain policy | Match `p=` value |
| `adkim=` | DKIM alignment mode | `r` (relaxed) or `s` (strict) |
| `aspf=` | SPF alignment mode | `r` (relaxed) or `s` (strict) |
| `fo=` | Failure reporting options | `1` (any failure) |
| `ruf=` | Forensic report email | Optional (privacy concerns) |

### Alignment Modes
- **Relaxed (r)**: Organizational domain match (mail.example.com passes for example.com)
- **Strict (s)**: Exact domain match required

### Example DMARC Records
```
# Monitoring phase
v=DMARC1; p=none; rua=mailto:dmarc@example.com; pct=100; adkim=r; aspf=r

# Quarantine phase
v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com; pct=100; fo=1

# Reject phase (full enforcement)
v=DMARC1; p=reject; rua=mailto:dmarc@example.com; pct=100; sp=reject
```

### Industry Statistics
- **18%** of top domains have valid DMARC policies
- **7-8%** enforce quarantine or reject
- **2.7x** higher inbox placement with full SPF+DKIM+DMARC

### Validation Checks
- ✅ DMARC record exists
- ✅ `rua=` tag present (reporting enabled)
- ✅ `p=reject` or `p=quarantine` (enforcing)
- ✅ `pct=100` (full coverage)
- ⚠️ `p=none` (monitoring only, no enforcement)
- ⚠️ `pct=` < 100 (partial enforcement)
- ❌ No DMARC record
- ❌ Invalid syntax

---

## IP Warmup Schedule

For new sending IPs or domains with no sending history:

| Day Range | Volume (% of target) | Notes |
|-----------|---------------------|-------|
| 1-3 | 5-10% | Start with highly engaged recipients |
| 4-7 | 15-25% | Monitor complaint rates closely |
| 8-14 | 30-50% | Gradual increase if metrics healthy |
| 15-21 | 60-75% | Check sender reputation scores |
| 22-30 | 80-100% | Full volume if all metrics green |

### Warmup Best Practices
- Start with most engaged subscribers (opened last 30 days)
- Maintain consistent daily volume (avoid spikes)
- Monitor complaint rates (<0.1% target)
- Pause warmup if bounce rate >2% or complaint rate >0.2%
- Use dedicated IP for high-volume senders (50K+ emails/month)

---

## Sender Reputation Factors

### Impact Ranking (Most to Least Critical)

| Factor | Impact Level | Target Metric |
|--------|--------------|---------------|
| Spam complaint rate | **Critical** | <0.1% (hard limit: 0.3%) |
| Bounce rate | **High** | <1% ideal, <2% acceptable |
| Engagement rate | **High** | Opens, clicks, replies boost score |
| Volume consistency | **Medium** | Avoid sudden spikes (>20% change) |
| Domain age | **Medium** | 6+ months for full reputation |
| Authentication | **High** | SPF+DKIM+DMARC all passing |
| List hygiene | **High** | Remove inactive >6 months |
| Spam trap hits | **Critical** | Zero tolerance |

### Reputation Score Impact
- **Full authentication** (SPF+DKIM+DMARC): 2.7x higher inbox placement
- **Domain age** <30 days: 40-50% lower initial reputation
- **Complaint rate** >0.3%: Automatic filtering/blocking
- **Bounce rate** >5%: IP/domain reputation decline
- **Engagement** decline >30%: Lower priority inbox placement

---

## Google/Yahoo/Microsoft Bulk Sender Requirements (2024-2026)

Applies to senders of **5,000+ emails/day** to personal accounts (Gmail, Yahoo, Outlook.com).

### Mandatory Requirements
1. ✅ **SPF authentication** passing
2. ✅ **DKIM authentication** passing (both SPF AND DKIM required)
3. ✅ **DMARC policy** p=none minimum (must align with SPF or DKIM)
4. ✅ **One-click unsubscribe** (RFC 8058) for marketing emails
5. ✅ **Spam complaint rate** under 0.3%
6. ✅ **Valid forward DNS** (A/AAAA record for sending domain)
7. ✅ **Valid reverse DNS** (PTR record matching forward DNS)
8. ✅ **Honor unsubscribe** within 2 business days

### RFC 8058 One-Click Unsubscribe
Required headers for bulk marketing emails:
```
List-Unsubscribe: <https://example.com/unsub?id=UNIQUE_ID>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

Requirements:
- HTTPS endpoint (not HTTP)
- Must accept POST requests (not just GET)
- DKIM signature must cover both headers
- Must process unsubscribe within 2 business days
- Endpoint must return 2xx status code

### Enforcement Timeline
- **Google**: Soft enforcement February 2024; hard enforcement (5xx rejections) November 2025
- **Yahoo**: Enforced February 2024
- **Microsoft**: Enforcement began May 5, 2025 (junk foldering, then rejection for non-compliant senders)

### Non-Compliance Consequences
- Temporary deferral (4xx codes)
- Permanent rejection (5xx codes)
- Sender reputation decline
- Inbox placement reduction

---

## Blacklist Checking

### Major Blacklists to Monitor
- **Spamhaus ZEN** (most impactful)
- **Spamhaus DBL** (domain-based)
- **Barracuda** (spam filtering)
- **Spamcop** (user-reported spam)
- **SURBL** (URI-based)
- **URIBL** (URI-based)

### Checking Process
```bash
# Check IP blacklist
dig +short <reversed-ip>.zen.spamhaus.org

# Check domain blacklist
dig +short <domain>.dbl.spamhaus.org

# Return code 127.0.0.x means listed
```

### Delisting Process
1. Identify root cause (spam complaints, compromised account, etc.)
2. Fix underlying issue
3. Request delisting through blacklist provider
4. Monitor to prevent re-listing

---

## MX Record Validation

### Requirements
- At least 1 MX record (recommended: 2+ for redundancy)
- Priority values: Lower = higher priority (0-65535)
- MX hostname must resolve to A/AAAA record (not CNAME)
- TLS support required for modern deliverability

### Example Validation
```bash
dig MX example.com +short
# Expected output:
# 10 mail1.example.com.
# 20 mail2.example.com.

dig A mail1.example.com +short
# Expected: Valid IP address
```

### Checks
- ✅ 2+ MX records (redundancy)
- ✅ All MX hostnames resolve to IPs
- ✅ TLS certificates valid (not expired)
- ⚠️ Single MX record (no redundancy)
- ❌ No MX records
- ❌ MX points to CNAME (invalid)
- ❌ TLS certificate expired/invalid

---

## Reverse DNS (PTR) Validation

### Requirements
- Sending IP must have PTR record
- PTR must match forward DNS (A/AAAA record)
- Hostname should match mail server identity

### Validation Example
```bash
# Check PTR for IP 192.0.2.1
dig -x 192.0.2.1 +short
# Expected: mail.example.com.

# Verify forward match
dig A mail.example.com +short
# Expected: 192.0.2.1
```

### Checks
- ✅ PTR record exists
- ✅ Forward/reverse DNS match
- ✅ Hostname matches sending identity
- ❌ No PTR record
- ❌ PTR/forward mismatch

---

## Scoring Methodology

### Deliverability Health Score (0-100)

| Component | Weight | Criteria |
|-----------|--------|----------|
| **Authentication** | 40% | SPF (10%), DKIM (15%), DMARC (15%) |
| **Blacklists** | 20% | Listed on any = -20 points |
| **DNS Configuration** | 15% | MX (10%), PTR (5%) |
| **Compliance** | 15% | Bulk sender rules (10%), RFC 8058/CAN-SPAM (5%) |
| **TLS/Security** | 10% | STARTTLS support, TLS version |

### Score Ranges
- **90-100**: Excellent (all systems green)
- **75-89**: Good (minor issues, monitor)
- **60-74**: Fair (fix recommended issues)
- **40-59**: Poor (deliverability at risk)
- **0-39**: Critical (immediate action required)

### Priority Levels for Fixes
- **Critical**: Blocking deliverability (blacklisted, no DKIM, SPF fail)
- **High**: Reducing inbox placement (DMARC p=none, complaint rate >0.2%)
- **Medium**: Best practice gaps (single MX, 1024-bit DKIM)
- **Low**: Optimization opportunities (SPF flattening, key rotation)

<!-- Updated: 2026-02-16 -->
