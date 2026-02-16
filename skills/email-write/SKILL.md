---
name: email-write
description: Compose high-converting emails using proven copy frameworks (PAS, AIDA, BAB, FAB, 4Ps). Generates subject line variants with scores, responsive HTML templates with dark mode support, plain-text fallback, and preheader recommendations. Optimized for cold outreach, newsletters, product launches, promotions, and transactional emails. Adapts to user context from email-profile.md.
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
---

# Email Write Sub-Skill

## Purpose

Generate professional, high-converting email copy using proven copywriting frameworks. Produces subject line variants with scoring, responsive HTML templates with dark mode support, plain-text fallback, and preheader recommendations.

## Activation

This sub-skill is invoked by the main `/email` skill when the user needs to compose a new email.

## Workflow

### 1. Gather Context

First, check if `email-profile.md` exists in the project directory. If yes, load business type, tone preferences, and target audience from the profile.

If no profile exists or user provides new context, ask for:

- **Email Purpose**: cold outreach, newsletter, product launch, promotional, re-engagement, welcome, feature announcement, etc.
- **Recipient**: name, role, relationship (new lead, existing customer, subscriber, team member)
- **Tone**: professional, friendly, casual, authoritative, empathetic, enthusiastic
- **Business Type**: (from profile or ask) SaaS, e-commerce, service business, agency, creator, B2B, B2C
- **Key Message**: what action should the recipient take?
- **Additional Context**: product details, promotion details, deadline, personalization data

### 2. Select Copy Framework

Based on the email purpose, choose the appropriate framework from `references/copy-frameworks.md`:

| Email Purpose | Recommended Framework | Why |
|--------------|----------------------|-----|
| Cold outreach | PAS | Empathy-driven, addresses pain points |
| Product launch | AIDA | Builds excitement, drives action |
| Newsletter | BAB or AIDA | Aspirational or engaging storytelling |
| Feature announcement | FAB | Clear value proposition for features |
| Promotional/sale | AIDA | Creates desire and urgency |
| Re-engagement | PAS | Identifies problem of disengagement |
| Welcome email | BAB | Shows transformation journey |
| Case study | 4Ps | Proof-heavy, testimonial-driven |
| Review request | PAS | Empathetic ask for feedback |
| Appointment reminder | Direct | No framework needed |

If uncertain, default to **AIDA** for marketing emails or **PAS** for relationship emails.

### 3. Generate Subject Lines

Create **3 subject line variants** using these strategies:

1. **Curiosity-Driven**: Creates intrigue, open loop, question, teaser
2. **Benefit-Driven**: Clear value proposition, outcome, result
3. **Urgency-Driven**: Time-sensitive, scarcity, FOMO (but not spammy)

**Subject Line Rules:**
- Optimal length: 6-10 words / 30-50 characters
- Never use ALL CAPS
- Maximum 1 exclamation mark per subject line
- Avoid spam triggers: "FREE!!!", "Act Now", "Limited Time Only", "Guaranteed", "Cash", "No obligation"
- Include personalization where possible (beyond first name: behavior, location, purchase history)
- Use power words: exclusive, secret, insider, proven, breakthrough, transform, discover

**Scoring Methodology (0-100):**

| Criteria | Weight | Scoring |
|----------|--------|---------|
| Length | 20 | 100 if 30-50 chars, -10 per 5 chars over/under |
| Power Words | 20 | +20 per power word (max 2) |
| Personalization | 25 | +25 if personalized beyond first name |
| Spam Triggers | -50 | -50 if contains spam word |
| Clarity | 20 | 100 if benefit/topic is clear |
| Curiosity | 15 | +15 if creates open loop |

Minimum passing score: 70

### 4. Write Preheader Text

Generate preheader recommendation (30-80 characters):

- Must complement (not repeat) the subject line
- Include secondary value proposition or CTA preview
- Avoid generic text like "View this email in your browser"

**Example:**
- Subject: "Your personalized SEO roadmap is ready"
- Preheader: "3 quick wins to boost your rankings this week"

### 5. Compose Email Body

Apply the chosen framework structure. Load full framework details from `references/copy-frameworks.md` before writing.

**General Email Writing Rules:**

- **Opening**: Hook in first sentence, address recipient by name if available
- **Body**: Use short paragraphs (2-3 sentences max), bullet points for scannability
- **Tone**: Match requested tone from profile or user input
- **Personalization**: Use merge tags like `{{firstName}}`, `{{company}}`, `{{productName}}`
- **CTA**: One primary CTA, clear and action-oriented ("Get Your Free Audit", "Claim Your Spot", "Start Your Trial")
- **Social Proof**: Include if available (testimonial, stat, case study result)
- **Signature**: Professional sign-off with name, title, company

**Framework-Specific Structure:**

Load the full structure from `references/copy-frameworks.md` and apply. Each framework has:
- Section breakdown (e.g., PAS: Problem → Agitate → Solve)
- Transition phrases
- Example templates

### 6. Generate HTML Version

Create a responsive, dark-mode compatible HTML email using these specifications:

**HTML Template Structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <title>{{emailSubject}}</title>
  <style>
    /* Inline critical CSS */
    body { margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; }
    table { border-collapse: collapse; }
    .email-container { max-width: 600px; margin: 0 auto; }
    .body-text { font-size: 16px; line-height: 1.6; color: #333333; }
    .cta-button {
      display: inline-block;
      padding: 14px 28px;
      background-color: #0066cc;
      color: #ffffff;
      text-decoration: none;
      border-radius: 4px;
      font-weight: bold;
      min-height: 44px;
      min-width: 44px;
    }

    /* Dark mode styles */
    @media (prefers-color-scheme: dark) {
      body { background-color: #1a1a1a !important; }
      .body-text { color: #e0e0e0 !important; }
      .email-container { background-color: #2a2a2a !important; }
    }

    /* Mobile responsive */
    @media only screen and (max-width: 600px) {
      .body-text { font-size: 14px !important; }
      .headline { font-size: 22px !important; }
      .cta-button { display: block !important; width: 100% !important; }
    }
  </style>
</head>
<body>
  <!-- Email content goes here -->
</body>
</html>
```

**HTML Rules:**
- Use table-based layout (not CSS Grid/Flexbox for email client compatibility)
- Max width: 600px
- Inline critical CSS (some clients strip `<style>` tags)
- Web-safe fonts with fallbacks: Arial, Helvetica, Georgia, Times New Roman
- Minimum 14px body text, 22px headlines on mobile
- CTA button: minimum 44x44px touch target, high contrast ratio (4.5:1)
- Include `color-scheme: light dark` meta tag
- Dark mode CSS using `@media (prefers-color-scheme: dark)`
- Alt text on all images (describe content, not "image" or "photo")
- Always include plain-text MIME part for accessibility

**CTA Button Best Practices:**
- One primary CTA per email (secondary CTAs okay as text links)
- Use `<a>` tag with `role="button"` for accessibility
- Padding: 14px vertical, 28px horizontal minimum
- Background color with 4.5:1 contrast ratio against text
- Include fallback for dark mode (lighter background or inverted colors)

### 7. Generate Plain-Text Version

Create a plain-text fallback with:
- No HTML tags
- Line breaks for readability (max 70 characters per line)
- CTA as full URL on separate line
- Signature block with contact info

### 8. Output Format

Present the final email composition in this structure:

```markdown
## Email Composition

**Framework**: [chosen framework name]
**Purpose**: [email purpose]
**Tone**: [tone]
**Recipient Type**: [recipient type]

---

### Subject Line Options

| # | Subject | Score | Type | Notes |
|---|---------|-------|------|-------|
| 1 | [subject line 1] | 87 | Curiosity | [why this works] |
| 2 | [subject line 2] | 82 | Benefit | [why this works] |
| 3 | [subject line 3] | 79 | Urgency | [why this works] |

**Recommended**: #1 (highest score)

**Preheader Text**: [30-80 char preheader recommendation]

---

### Email Body (Plain Text)

[Full email body using framework structure]

[Include merge tags like {{firstName}}, {{company}}]

[CTA]

[Signature]

---

### HTML Version

```html
[Complete HTML email code with inline CSS, dark mode support, responsive design]
```

---

### Plain Text Version

```
[Plain text fallback with line breaks, CTA as full URL]
```

---

### Email Metadata

- **Word Count**: [body word count]
- **Reading Time**: [estimated reading time]
- **Character Count** (with spaces): [count]
- **CTA Count**: [number of CTAs]

---

### Next Steps

- [ ] Review and edit copy
- [ ] Choose subject line variant
- [ ] Test HTML rendering in email client preview tool
- [ ] Send as draft via MCP (if available) or copy to email platform
- [ ] A/B test subject lines if sending to large list
```

## Quality Gates

Before delivering the email, verify:

1. **Subject line scores**: At least one variant scores 70+
2. **Preheader length**: 30-80 characters
3. **Framework alignment**: Body follows chosen framework structure
4. **CTA clarity**: Primary CTA is clear and action-oriented
5. **Mobile readability**: Paragraphs are 2-3 sentences max
6. **HTML validity**: Table-based layout, inline CSS, dark mode support
7. **Accessibility**: Alt text on images, plain-text fallback included
8. **Spam check**: No spam trigger words in subject or body
9. **Personalization**: Merge tags used where appropriate
10. **Tone match**: Email tone matches requested tone from profile

If any gate fails, revise before output.

## Error Handling

- If `references/copy-frameworks.md` is missing, warn user and use basic AIDA structure
- If `email-profile.md` is missing, prompt user for context (don't fail)
- If subject line scores are all below 70, generate new variants
- If HTML template fails validation, fall back to plain-text only and warn user

## Resources

- `references/copy-frameworks.md` - Full framework structures and examples
- `email-profile.md` - User's business context and preferences (optional)

## Example Invocation

User: "Write a cold outreach email to a SaaS founder about my SEO audit service"

Agent:
1. Loads email-profile.md (if exists)
2. Selects PAS framework (cold outreach)
3. Generates 3 subject line variants with scores
4. Writes email body following PAS structure
5. Creates HTML template with dark mode
6. Creates plain-text fallback
7. Outputs full email composition with metadata and next steps

## Notes

- This sub-skill focuses on composition only (no sending/scheduling)
- For sending emails, use `email-send` sub-skill or MCP email tools
- For A/B testing, generate multiple variants using different frameworks
- Always adapt tone and complexity to recipient type (B2B vs B2C, technical vs non-technical)
