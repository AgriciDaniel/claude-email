---
name: email-review
description: Pre-send email quality review and scoring across 5 dimensions (subject line, copy quality, technical/HTML, deliverability, compliance). Analyzes subject lines, body copy, HTML structure, spam triggers, and CAN-SPAM compliance. Scores 0-100 with detailed recommendations for improvement. Use when user wants to review an email before sending, check email quality, or validate marketing email best practices.
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Email Review Sub-Skill

## Purpose

Reviews email content before sending and provides a comprehensive quality score (0-100) across 5 weighted dimensions. Identifies critical issues, suggests improvements, and provides a rewritten version for low-scoring emails.

## When to Activate

- User asks to "review this email"
- User provides email content (subject + body) for feedback
- User requests email quality check or score
- User wants to validate email before sending
- User provides Gmail draft ID for review
- User asks about email deliverability or spam risk

## Input Formats

Accept email content in any of these formats:

1. **Pasted text** - Subject line + body in conversation
2. **File path** - Path to HTML email file
3. **Gmail draft ID** - Fetch via `gmail_get_draft` MCP tool
4. **Raw HTML** - HTML email source code

## Scoring Framework

### Overall Score Calculation

Total score = weighted sum of 5 categories:

| Category | Weight | Focus |
|----------|--------|-------|
| Subject Line | 25% | Length, power words, spam triggers, personalization |
| Copy Quality | 25% | Word count, CTA clarity, framework structure, readability |
| Technical/HTML | 20% | Size, responsiveness, dark mode, alt text, preheader |
| Deliverability | 15% | Spam signals, link count, sender reputation factors |
| Compliance | 15% | CAN-SPAM, unsubscribe, physical address, RFC 8058 |

---

## 1. Subject Line Scoring (25% weight)

**Base Score: 0-100, then weighted at 25%**

### Length Check (0-25 points)
- **Optimal**: 6-10 words OR 30-50 characters = 25 points
- **Acceptable**: 5 or 11 words = 20 points
- **Marginal**: 4 or 12 words = 10 points
- **Poor**: <4 or >12 words = 0 points

### Spam Trigger Detection (-5 points each)
Penalize for each occurrence:
- ALL CAPS words
- Multiple exclamation marks (!!!)
- Phrases: "FREE", "Act Now", "Limited Time", "Guaranteed", "Winner", "Click Here", "Buy Now", "Order Now"
- Excessive punctuation ($$$, ???)

### Power Words (+5 points each, max +15)
Bonus for strategic use of:
- "New", "Exclusive", "Proven", "Secret", "Discover"
- "Ultimate", "Essential", "Complete", "Breakthrough"
- Industry-specific power words

### Personalization (+10 points)
- Contains merge tags like `{{first_name}}` or `{{company}}`
- Behavioral personalization indicators

### Emoji Usage (+5 or -5)
- **1 emoji** = +5 points (increases open rates)
- **2+ emojis** = -5 points (reduces professionalism)
- **No emoji** = 0 points (neutral)

---

## 2. Copy Quality Scoring (25% weight)

**Base Score: 0-100, then weighted at 25%**

### Word Count (0-20 points)
- **150-300 words** = 20 points (optimal)
- **100-149 or 301-400** = 15 points
- **50-99 or 401-500** = 10 points
- **<50 or >500** = 0 points

### CTA Count (0-25 points)
- **1 primary CTA** = 25 points (best conversion)
- **2 CTAs** = 15 points (acceptable)
- **3+ CTAs** = 5 points (diluted focus)
- **0 CTAs** = 0 points (no action path)

### CTA Clarity (0-15 points)
Score based on:
- **15 points**: Action verb + benefit ("Get My Free Guide", "Start Your Trial")
- **10 points**: Generic action ("Learn More", "Download")
- **5 points**: Vague ("Submit", "Click Here")
- **0 points**: No CTA or unclear

### Framework Structure (0-15 points)
Check if email follows proven framework:
- **PAS (Problem-Agitate-Solution)**: 15 points
- **AIDA (Attention-Interest-Desire-Action)**: 15 points
- **BAB (Before-After-Bridge)**: 15 points
- **FAB (Features-Advantages-Benefits)**: 15 points
- **4Ps (Picture-Promise-Proof-Push)**: 15 points
- **No clear structure**: 0 points

### Readability (0-15 points)
- Short paragraphs (2-3 lines max): +5
- Bullet points or numbered lists: +5
- Scannable with subheadings: +5
- No walls of text: +5
- Deduct -5 for each readability issue

### Personalization Beyond Name (0-10 points)
- Behavioral triggers (past purchase, browsing): +5
- Location/timezone awareness: +3
- Industry/role customization: +2

---

## 3. Technical/HTML Scoring (20% weight)

**Base Score: 100, deduct points for violations**

### Total Size (-20 if fail)
- **Must be under 102 KB** (Gmail clips emails over this)
- Check HTML + embedded images (if data URIs)

### Text-to-Image Ratio (-15 if fail)
- **Minimum 60% text / 40% images**
- Image-heavy emails trigger spam filters

### Responsive Design (-10 if fail)
Check for:
- Viewport meta tag: `<meta name="viewport" content="width=device-width">`
- Media queries for mobile breakpoints
- Fluid tables or container widths

### Dark Mode Support (-5 if fail)
Check for:
- `<meta name="color-scheme" content="light dark">`
- CSS with `@media (prefers-color-scheme: dark)`
- Dark mode color overrides

### Alt Text on Images (-5 per missing)
- All `<img>` tags must have `alt` attribute
- Alt text should be descriptive, not just filename

### Table-Based Layout (-5 if fail)
- Email should use `<table>` for layout (HTML email best practice)
- Deduct if using CSS Grid/Flexbox (poor email client support)

### Font Safety (-5 if fail)
- Must use web-safe fonts with fallbacks
- Example: `font-family: Arial, Helvetica, sans-serif;`
- Avoid custom web fonts without fallbacks

### CTA Button Size (-5 if fail)
- Minimum **44x44 pixels** (mobile touch target)
- Check all `<a>` styled as buttons

### Plain-Text Version (-10 if fail)
- Must have plain-text MIME part OR
- Text-only fallback within HTML

### Preheader Text (-5 if missing)
- **30-80 character** preview text
- Located immediately after `<body>` tag
- Often hidden with CSS for HTML view

---

## 4. Deliverability Signals (15% weight)

**Base Score: 100, deduct points for red flags**

### Spam Word Density (-5 per word)
Count occurrences of spam triggers in body:
- "Free", "Winner", "Guarantee", "Risk-free", "Act now"
- "Cash", "Bonus", "Extra income", "Work from home"
- "Unsecured credit", "Viagra", "Pharmacy"

### Link Count (warn at 5+)
- **0-3 links** = 0 penalty
- **4-5 links** = -5 points (warning threshold)
- **6+ links** = -15 points (spam signal)

### Image-Only Email (-20 if fail)
- Emails with **only images and no text** are spam signals
- Must have substantive text content

### Unsubscribe Link (-25 if missing)
- **Required for marketing emails**
- Must be clearly visible and functional
- Check for `<a>` with "unsubscribe" keyword

### Sender Name (-10 if generic)
- Deduct for: "info@", "noreply@", "admin@", "support@"
- Personal or company name preferred

### Link Shorteners (-10 if detected)
- Penalize use of: bit.ly, tinyurl, goo.gl, ow.ly
- Spam filters distrust shortened URLs

---

## 5. Compliance Scoring (15% weight)

**Base Score: 100, deduct points for violations**

### Physical Address (-20 if missing)
- **CAN-SPAM requires postal address**
- Check footer for street address or P.O. Box

### Unsubscribe Mechanism (-25 if missing)
- Must have working unsubscribe link
- Should process within 10 business days (CAN-SPAM)

### Honest Subject Line (-15 if misleading)
- Subject must accurately reflect email content
- No deceptive "Re:" or "Fwd:" if not a reply

### RFC 8058 Headers (-10 if missing for bulk)
For bulk/marketing emails, check for:
```
List-Unsubscribe: <mailto:unsub@example.com>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

### Sender Identification (-10 if missing)
- Must clearly state who is sending the email
- Check for "From" name and footer company info

---

## Score Interpretation

| Score | Rating | Status | Recommendation |
|-------|--------|--------|----------------|
| 90-100 | Excellent | ✅ Ready to send | Minor tweaks optional |
| 75-89 | Good | ⚠️ Review suggested | Address medium-priority issues |
| 60-74 | Fair | ⚠️ Fix before sending | Resolve high-priority issues |
| 40-59 | Poor | ❌ Needs rework | Significant changes required |
| 0-39 | Critical | ❌ DO NOT SEND | Major compliance/deliverability issues |

---

## Output Format

Structure the review report as:

1. **Header**: `## Email Quality Review` with overall score, rating, status
2. **Score table**: 5 categories with raw score, weight, and weighted score
3. **Issues Found**: Grouped by severity (Critical/High/Medium/Low) with specific fixes
4. **Detailed Breakdown**: Per-category analysis (subject length/triggers/power words, word count/CTA/framework, HTML size/responsive/dark mode, spam words/links, address/unsubscribe/RFC 8058)
5. **Improved Version** (if score < 75): Rewritten subject line, copy fix recommendations, HTML fixes

Use status badges: ✅ Ready to send (90+), ⚠️ Review suggested (75-89), ⚠️ Fix before sending (60-74), ❌ Needs rework (40-59), ❌ DO NOT SEND (0-39).

---

## Workflow

### Step 1: Intake
Identify input format and extract:
- Subject line
- Body copy (text or HTML)
- HTML source (if applicable)

### Step 2: Run Analysis Scripts (if available)

Check for and execute:
```bash
# Subject line scoring
python scripts/score_subject_line.py --subject "[subject]"

# HTML email analysis
python scripts/analyze_email_html.py --file [path]
```

### Step 3: Manual Scoring

For each category:
1. Start with base score
2. Apply positive adjustments
3. Apply penalties
4. Calculate weighted score

### Step 4: Reference Checks

Consult knowledge files for edge cases:
- `references/technical-standards.md` - HTML/CSS email rules
- `references/compliance.md` - CAN-SPAM, GDPR, CASL requirements
- `references/deliverability-rules.md` - Deliverability scoring and spam signal reference

### Step 5: Generate Report

Format output per template above, ensuring:
- Clear categorization of issues by severity
- Actionable fix recommendations
- Improved version if score < 75

### Step 6: User Confirmation

Ask user if they want to:
- Apply suggested improvements
- Re-review after manual edits
- Send as-is (if score >= 75)

---

## Quality Gates

### Hard Rules (Automatic Failure)

These issues result in "DO NOT SEND" status regardless of total score:

1. **Missing unsubscribe link** (for marketing emails)
2. **Missing physical address** (CAN-SPAM violation)
3. **Email size > 102 KB** (Gmail will clip)
4. **Image-only email** (no text content)
5. **Deceptive subject line** (FTC violation)

---

## Edge Cases

### Gmail Drafts
If user provides draft ID:
1. Use `gmail_get_draft` MCP tool to fetch
2. Extract subject from `payload.headers`
3. Extract HTML body from `payload.parts` (mimeType = text/html)
4. Proceed with normal review

### Plain-Text Emails
If email has no HTML:
1. Skip technical/HTML scoring (default to 80/100)
2. Focus on copy quality, subject line, compliance
3. Adjust weighting: Subject 30%, Copy 35%, Deliverability 20%, Compliance 15%

### Non-English Emails
1. Note language in report
2. Skip spam word detection (English-specific)
3. Focus on structural/technical issues
4. Provide caveats about readability scoring

### Transactional Emails
If email is transactional (receipts, confirmations):
1. Relax compliance rules (unsubscribe not required)
2. Focus on technical delivery and clarity
3. Note in report: "Transactional email - relaxed marketing rules"

---

## Tools Integration

### Available Scripts

Run these scripts from the `scripts/` directory:

**score_subject_line.py**
- Input: `python scripts/score_subject_line.py --subject "Subject line text" --json`
- Output: JSON with length, spam triggers, power words, score
- Use: Auto-score subject line component

**analyze_email_html.py**
- Input: `python scripts/analyze_email_html.py --file path/to/email.html --json`
- Output: JSON with size, responsiveness, alt text, preheader, issues
- Use: Auto-score technical/HTML component

### MCP Tools

**gmail_get_draft**
- Fetch draft email from Gmail by ID
- Extract subject and HTML body

**gmail_send_message**
- Send reviewed email (after user approval)

---

## Examples

**High-scoring email** (92/100): Subject "New guide: 5 proven SEO tactics for 2026" -- 8 words, power word, no spam triggers, 280 words, 1 CTA, responsive HTML, all compliance elements present. Status: Ready to send.

**Low-scoring email** (23/100): Subject "FREE MONEY!!! ACT NOW GUARANTEED WINNER!!!" -- all caps, 4 spam triggers, 50 words, 5 CTAs, missing unsubscribe and address. Status: DO NOT SEND (CAN-SPAM violations).

---

## Notes

- Always run available scripts before manual scoring
- Reference knowledge files for edge cases
- Provide specific, actionable recommendations
- Never approve emails with compliance violations
- Weight user industry context (B2B vs B2C vs transactional)
- Update scoring criteria based on evolving best practices
