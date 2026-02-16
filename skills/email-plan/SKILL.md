---
name: email-plan
description: Generate comprehensive email marketing strategy with 90-day implementation roadmap. Analyzes business type (local-business, saas, ecommerce, creator, agency) to deliver industry-specific segmentation plans, automation sequences, content calendars, KPI targets, platform recommendations, and week-by-week rollout schedule. Use when building email program from scratch or restructuring existing strategy.
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
---

# Email Plan -- Email Marketing Strategy Generator

## Overview

This sub-skill generates a complete email marketing strategy tailored to your business type, including:

- Email platform recommendations
- Domain authentication checklist
- List building strategy
- Segmentation plan
- Automation sequence priorities
- Content calendar template
- KPI targets and benchmarks
- 90-day implementation roadmap

## Usage

Invoked by `/email plan` from the main email skill.

## Workflow

### 1. Detect Business Type

First, check if `email-profile.md` exists and contains business type. If not, analyze context signals:

**Business Type Detection:**
- **Local Business**: Physical location, appointments, service area, reviews, foot traffic
- **SaaS**: Software product, trials, subscriptions, feature usage, onboarding
- **E-commerce**: Product catalog, shopping cart, inventory, shipping, order fulfillment
- **Creator/Newsletter**: Content creation, audience building, paid subscriptions, courses
- **Agency**: Client services, proposals, case studies, retainers, project-based

If unclear, ask: "What type of business is this strategy for? (local-business, saas, ecommerce, creator, agency)"

### 2. Load Industry Template

Based on business type, load the appropriate template from:
- `assets/local-business.md`
- `assets/saas.md`
- `assets/ecommerce.md`
- `assets/creator.md`
- `assets/agency.md`
- `assets/generic.md` (fallback)

### 3. Generate Strategy

Create a comprehensive strategy document with these sections:

## Strategy Sections

### Executive Summary

2-3 sentence overview of the strategy, highlighting:
- Business type and primary email marketing goal
- Key strategic focus areas
- Expected timeline to see results

### 1. Email Program Foundation

**Platform Recommendation:**

Based on business size, budget, and needs:

| Business Size | Recommended Platform | Monthly Cost | Best For |
|---------------|---------------------|--------------|----------|
| Solo/startup (<1K subscribers) | Kit.com or MailerLite | $0-29 | Creators, solopreneurs |
| Small (1-5 staff, 1K-10K) | Mailchimp or MailerLite | $13-45 | Local businesses, agencies |
| Medium (5-50 staff, 10K-50K) | ActiveCampaign or Klaviyo | $49-150 | SaaS, ecommerce |
| Large (50+ staff, 50K+) | HubSpot or Salesforce | $800+ | Enterprise SaaS, large ecommerce |

**Industry-Specific Platforms:**
- **E-commerce**: Klaviyo (product recommendations, revenue attribution)
- **SaaS**: Customer.io or Intercom (behavioral triggers, in-app messaging)
- **Creators**: Kit.com/ConvertKit or Beehiiv (monetization tools, referral programs)
- **Agencies**: HubSpot (CRM integration, sales pipeline)

**Domain Authentication Checklist:**

Before sending any emails, verify these DNS records are configured:

- [ ] **SPF Record**: Authorizes sending servers
- [ ] **DKIM Record**: Cryptographic email signature
- [ ] **DMARC Record**: Enforcement policy for SPF/DKIM failures
- [ ] **Custom Sending Domain**: Use mail.yourdomain.com instead of platform domain
- [ ] **Verification**: Run `/email audit <domain>` to confirm setup

**List Building Strategy:**

3-5 methods specific to business type (from industry template):

Example for local business:
1. QR code on receipts → signup landing page
2. Sign-up prompt at checkout (iPad/tablet)
3. WiFi login portal → email capture
4. Google Business Profile → newsletter CTA
5. In-store signage with incentive (10% off next visit)

Example for SaaS:
1. Free trial signup (automatic list add)
2. Content marketing lead magnets (guides, templates)
3. Webinar registrations
4. Product updates blog → email subscription
5. Referral program

**Consent and Compliance:**

- **US**: CAN-SPAM compliant (physical address, unsubscribe link)
- **EU/UK**: GDPR compliant (explicit opt-in, data processing agreement)
- **Canada**: CASL compliant (express consent, unsubscribe)
- **Australia**: Spam Act compliant (consent, identify, unsubscribe)

Load compliance requirements from `../../references/compliance.md` based on region.

### 2. Segmentation Plan

Define 3-5 core segments with:
- **Segment Name**
- **Criteria** (behavioral, demographic, engagement)
- **Estimated Size** (% of list)
- **Email Frequency** (emails per week/month)
- **Content Type** (educational, promotional, transactional)

**Example Segmentation Table:**

| Segment | Criteria | Est. Size | Frequency | Content Type |
|---------|----------|-----------|-----------|--------------|
| New Customers | First 30 days after signup | 15% | 3/week | Onboarding, educational |
| Repeat Customers | 2+ purchases | 25% | 2/week | Loyalty, cross-sell |
| VIP | Top 20% by spend | 20% | 2/week | Exclusive offers, early access |
| At-risk | 60-90 days no activity | 20% | 1/week | Win-back, incentives |
| Lapsed | 90+ days no activity | 20% | 1/month | Re-engagement, surveys |

Load industry-specific segments from template.

### 3. Automation Sequence Priorities

Rank automation sequences to build, based on business type and impact.

**Format:**

| Priority | Sequence Name | Trigger | # Emails | Purpose |
|----------|---------------|---------|----------|---------|
| 1 | Welcome Series | List signup | 3-5 | Introduce brand, set expectations |
| 2 | [Industry-specific] | [Trigger] | [Count] | [Goal] |
| 3 | [Industry-specific] | [Trigger] | [Count] | [Goal] |

**Industry-Specific Priorities:**

**Local Business:**
1. Welcome Series → introduce business, set expectations
2. Review Request → post-visit review ask (timing varies by industry)
3. Appointment Reminder → reduce no-shows
4. Birthday/Loyalty → reward program, special offers
5. Re-engagement → win back lapsed customers

**SaaS:**
1. Onboarding/Feature Adoption → drive activation, reduce time-to-value
2. Trial-to-Paid → convert trials with education + urgency
3. Feature Announcement → drive usage of new capabilities
4. NPS/Feedback → gather insights, reduce churn risk
5. Churn Prevention → detect at-risk users, intervention

**E-commerce:**
1. Abandoned Cart → recover lost revenue (3-email series)
2. Welcome + First Purchase → convert new subscribers
3. Post-Purchase → build loyalty, request review
4. Win-Back → re-engage dormant customers
5. Cross-Sell/Upsell → product recommendations

**Creator/Newsletter:**
1. Welcome → introduce yourself, set content expectations
2. Content Drip → best-of archive, value demonstration
3. Monetization → product/course launch sequence
4. Re-engagement → win back dormant subscribers
5. Referral → incentivize word-of-mouth growth

**Agency:**
1. Welcome/Credibility → establish expertise, showcase work
2. Case Study Drip → demonstrate results over time
3. Proposal Follow-up → nurture leads post-proposal
4. Client Onboarding → set expectations, gather info
5. Quarterly Business Review → retain clients, upsell

### 4. Content Calendar

Monthly email cadence template based on industry best practices.

**Standard Cadence:**

| Frequency | Email Type | Purpose |
|-----------|----------|---------|
| Weekly | Value Email | Educational, tips, insights (80/20 rule) |
| Weekly | Promotional Email | Offers, announcements, product updates |
| Monthly | Newsletter Roundup | Month recap, top content, community highlights |
| Quarterly | Survey/Feedback | NPS, product feedback, preferences |
| Seasonal | Holiday Campaigns | Holiday-specific promotions, greetings |

**Industry-Specific Adjustments:**

- **E-commerce**: 3-4 emails/week (higher tolerance for promotional content)
- **SaaS**: 1-2 emails/week (focus on feature adoption, education)
- **Local Business**: 1-2 emails/week max (avoid overwhelming small local audience)
- **Creator**: 1-3 emails/week (consistency is key, content-driven)
- **Agency**: 1 email/week (thought leadership, case studies)

**Content Mix by Business Type:**

Load from industry template (e.g., local business: 40% tips, 30% promotions, 20% news, 10% community).

### 5. KPI Targets

Set realistic benchmarks based on business type and industry averages.

Load benchmarks from `../../references/benchmarks.md` and customize:

| Metric | Industry Benchmark | Your Target | Notes |
|--------|-------------------|-------------|-------|
| Open Rate | 15-25% | 20% | Varies by industry, list health |
| Click Rate | 2-5% | 3.5% | Engagement quality indicator |
| Conversion Rate | 1-3% | 2% | Purchase, signup, download |
| Unsubscribe Rate | <0.5% | <0.3% | High = content/frequency issue |
| Bounce Rate | <2% | <1% | High = list hygiene problem |
| Revenue per Email | Varies | $X | E-commerce specific |

**KPI Tracking Schedule:**
- Weekly: Open rate, click rate, unsubscribe rate
- Monthly: Conversion rate, revenue per email, list growth rate
- Quarterly: Deliverability audit, segment performance review

### 6. Platform Setup Guide

Step-by-step platform configuration based on recommendation:

1. **Account Creation**
   - Choose plan tier based on list size
   - Enable two-factor authentication
   - Configure sender name and reply-to address

2. **Domain Authentication**
   - Add custom sending domain (mail.yourdomain.com)
   - Configure SPF, DKIM, DMARC records
   - Verify authentication in platform settings

3. **List Import**
   - Clean list before import (remove bounces, duplicates)
   - Tag import source for segmentation
   - Send re-permission email if list is old (6+ months)

4. **Compliance Settings**
   - Add physical mailing address to footer
   - Configure unsubscribe preferences
   - Set up preference center (frequency, content type)

5. **Integration Setup**
   - Connect website forms
   - Integrate CRM/e-commerce platform
   - Set up analytics tracking (UTM parameters)

### 7. 90-Day Implementation Roadmap

Week-by-week plan to launch a complete email program.

| Week | Milestone | Tasks | Success Criteria |
|------|-----------|-------|------------------|
| 1-2 | Foundation | Domain auth (SPF/DKIM/DMARC), platform setup, list import, compliance config | Authentication verified, list imported, first test email sent |
| 3-4 | First Sends | Welcome sequence live (3-5 emails), first newsletter sent, analytics connected | Welcome series activated, first newsletter delivered, open rate >15% |
| 5-6 | Automation #2 | Second automation built (industry-specific), segment creation, A/B test setup | Second sequence live, 3-5 segments created, first A/B test running |
| 7-8 | Optimization | A/B testing program started, deliverability review, content calendar established | 2+ A/B tests completed, deliverability >95%, 4-week content calendar drafted |
| 9-10 | Automation #3 | Third automation built, behavioral triggers added, dynamic content tested | Third sequence live, trigger rules configured, personalization active |
| 11-12 | Review & Plan | Performance review, optimization pass, identify gaps, plan Q2 roadmap | KPI dashboard created, underperforming emails identified, Q2 plan drafted |

**Week 1-2: Foundation**
- Set up email platform account
- Configure domain authentication (SPF, DKIM, DMARC)
- Import and clean existing list
- Design email template (mobile-responsive)
- Run `/email audit <domain>` to verify setup

**Week 3-4: First Sends**
- Build welcome sequence (3-5 emails)
- Send first newsletter to test deliverability
- Monitor metrics (opens, clicks, bounces)
- Set up analytics tracking

**Week 5-6: Automation #2**
- Build second priority sequence (from industry template)
- Create core segments (3-5)
- Set up A/B testing framework
- Optimize welcome series based on data

**Week 7-8: Optimization**
- Run 2+ A/B tests (subject lines, send times, CTAs)
- Conduct deliverability audit
- Establish 4-week rolling content calendar
- Review and adjust frequency based on engagement

**Week 9-10: Automation #3**
- Build third priority sequence
- Add behavioral triggers (clicks, purchases, inactivity)
- Test dynamic content and personalization
- Expand segmentation based on learnings

**Week 11-12: Review & Plan Q2**
- Generate performance report (all KPIs)
- Identify underperforming emails and sequences
- Optimize low-performing content
- Draft Q2 roadmap with new sequences, segments, campaigns

## Output Format

```markdown
## Email Marketing Strategy: [Business Name/Type]

### Executive Summary
[2-3 sentence overview: business type, primary goal, strategic focus, expected timeline]

### 1. Email Program Foundation

**Platform Recommendation:** [Platform name] ($X/month)
**Why:** [1-2 sentence rationale based on business needs]

**Domain Authentication Checklist:**
- [ ] SPF Record configured
- [ ] DKIM Record configured
- [ ] DMARC Record configured
- [ ] Custom sending domain verified
- [ ] Run `/email audit <domain>` to confirm

**List Building Strategy:**
1. [Method 1 with details]
2. [Method 2 with details]
3. [Method 3 with details]
4. [Method 4 with details]
5. [Method 5 with details]

**Compliance:** [Region-specific requirements]

### 2. Segmentation Plan

| Segment | Criteria | Est. Size | Frequency | Content Type |
|---------|----------|-----------|-----------|--------------|
| [Segment 1] | [Criteria] | [%] | [X/week] | [Type] |
| [Segment 2] | [Criteria] | [%] | [X/week] | [Type] |
| [Segment 3] | [Criteria] | [%] | [X/week] | [Type] |
| [Segment 4] | [Criteria] | [%] | [X/week] | [Type] |
| [Segment 5] | [Criteria] | [%] | [X/week] | [Type] |

### 3. Automation Sequence Priorities

| Priority | Sequence Name | Trigger | # Emails | Purpose |
|----------|---------------|---------|----------|---------|
| 1 | [Sequence 1] | [Trigger] | [Count] | [Goal] |
| 2 | [Sequence 2] | [Trigger] | [Count] | [Goal] |
| 3 | [Sequence 3] | [Trigger] | [Count] | [Goal] |
| 4 | [Sequence 4] | [Trigger] | [Count] | [Goal] |
| 5 | [Sequence 5] | [Trigger] | [Count] | [Goal] |

### 4. Content Calendar

**Email Frequency:** [X emails per week/month]

**Content Mix:**
- [Content Type 1]: [%]
- [Content Type 2]: [%]
- [Content Type 3]: [%]
- [Content Type 4]: [%]

**Monthly Template:**
| Week | Value Email | Promotional Email | Other |
|------|-------------|-------------------|-------|
| Week 1 | [Topic] | [Offer] | - |
| Week 2 | [Topic] | [Offer] | Newsletter |
| Week 3 | [Topic] | [Offer] | - |
| Week 4 | [Topic] | [Offer] | - |

### 5. KPI Targets

| Metric | Industry Benchmark | Your Target | Review Frequency |
|--------|-------------------|-------------|------------------|
| Open Rate | 15-25% | 20% | Weekly |
| Click Rate | 2-5% | 3.5% | Weekly |
| Conversion Rate | 1-3% | 2% | Monthly |
| Unsubscribe Rate | <0.5% | <0.3% | Weekly |
| Bounce Rate | <2% | <1% | Monthly |
| [Industry-specific metric] | [Benchmark] | [Target] | [Frequency] |

### 6. Platform Setup Guide

[5-step setup guide specific to recommended platform]

### 7. 90-Day Implementation Roadmap

| Week | Milestone | Success Criteria |
|------|-----------|------------------|
| 1-2 | Foundation | Authentication verified, list imported, test email sent |
| 3-4 | First Sends | Welcome series live, first newsletter sent, open rate >15% |
| 5-6 | Automation #2 | Second sequence live, segments created, A/B test running |
| 7-8 | Optimization | Tests completed, deliverability >95%, content calendar set |
| 9-10 | Automation #3 | Third sequence live, triggers configured, personalization active |
| 11-12 | Review & Plan | KPI dashboard created, gaps identified, Q2 plan drafted |

### Next Steps

**Immediate Actions:**
1. Run `/email audit <domain>` to verify domain authentication
2. Run `/email sequence welcome` to design the welcome series
3. Set up platform account and complete domain configuration

**Week 1 Priority:**
- [ ] Configure SPF, DKIM, DMARC records
- [ ] Import and clean email list
- [ ] Design email template
- [ ] Send test email to verify deliverability

**Resources:**
- Platform setup guides in `references/mcp-integration.md`
- Compliance requirements in `/references/compliance.md`
- Benchmarks in `/references/benchmarks.md`
```

## Quality Checks

Before delivering strategy:

1. **Business type detected or confirmed** (not assumed)
2. **Industry template loaded and customized** (not generic copy-paste)
3. **Platform recommendation justified** based on size, budget, needs
4. **All 7 sections present** with complete information
5. **90-day roadmap has specific, actionable milestones**
6. **KPI targets are realistic** based on industry benchmarks
7. **Next steps are clear and prioritized**

## Error Handling

- If business type unclear and no email-profile.md exists, ask user to specify
- If industry template doesn't match business perfectly, use closest match + customize
- If budget constraints mentioned, adjust platform recommendation
- If compliance region unknown, default to strictest (GDPR) and note assumption
