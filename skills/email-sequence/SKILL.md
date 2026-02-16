---
name: email-sequence
description: Designs complete email automation sequences with timing, subject lines, copy, and conditional logic. Supports welcome series, nurture campaigns, re-engagement, abandoned cart, post-purchase, review requests, and custom sequences. Adapts sequence type, cadence, frameworks, and conditional branching to business context. Use when user wants to create an automated email series triggered by subscriber actions or time intervals.
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
---

# Email Sequence Designer

Designs complete email automation sequences with strategic timing, persuasive copy, and conditional logic.

## Quick Reference

| Sequence Type | Emails | Duration | Best For |
|---------------|--------|----------|----------|
| Welcome Series | 4-6 | 14 days | New subscribers |
| Nurture | 6-10 | 6-10 weeks | Education, engagement |
| Re-engagement | 3-5 | 28 days | Inactive subscribers |
| Abandoned Cart | 3 | 3 days | E-commerce recovery |
| Post-Purchase | 4-6 | 30 days | Customer experience |
| Review Request | 1-2 | 1-24 hours | Social proof |
| Custom | Variable | Variable | Specific goals |

## Execution Protocol

### Step 1: Load Context
Read the business profile for context:
- `email-profile.md` (project root)

Load reference files for frameworks and benchmarks:
- `references/copy-frameworks.md`
- `references/benchmarks.md`

### Step 2: Gather Sequence Requirements

Ask the user:
1. **Sequence type**: welcome, nurture, re-engagement, abandoned-cart, post-purchase, review-request, or custom
2. **If custom**: goal, trigger event, desired email count, preferred cadence, tone

Confirm business context from profile:
- Industry
- Target audience
- Brand voice
- Primary offer/product

### Step 3: Design Sequence Architecture

Based on sequence type, define:
- Total number of emails
- Timing between emails
- Framework assignment per email
- Conditional logic rules
- KPI targets

### Step 4: Generate Each Email

For each email in sequence, create:
1. **Position and timing**: Email X, Day Y or Hours after trigger
2. **Subject lines**: 3 variants with scores (60-100)
3. **Preheader text**: 30-80 characters
4. **Email body**: Full copy following assigned framework
5. **CTA**: Button text and link placeholder
6. **Conditional logic**: What happens based on engagement

### Step 5: Add Implementation Guidance

Include:
- Platform setup notes
- A/B test recommendations
- KPI benchmarks for this sequence type
- Segment considerations

## Sequence Type Templates

### 1. Welcome Series (4-6 emails, 14 days)

**Standard Timeline:**
- Email 1: Immediate (welcome + deliver lead magnet)
- Email 2: Day 1 (brand story)
- Email 3: Day 2 (best content/resource)
- Email 4: Day 4 (social proof)
- Email 5: Day 7 (soft offer)
- Email 6: Day 14 (stronger CTA or segmentation)

**Framework Assignment:**
- Email 1: BAB (Before-After-Bridge)
- Email 2: BAB (Before-After-Bridge)
- Email 3: FAB (Features-Advantages-Benefits)
- Email 4: 4Ps (Picture-Promise-Prove-Push)
- Email 5: AIDA (Attention-Interest-Desire-Action)
- Email 6: PAS (Problem-Agitate-Solution)

**KPI Targets:**
- Average open rate: 40-60%
- Average click rate: 3-8%
- Conversion rate: 2-5%

### 2. Nurture Sequence (6-10 emails, 6-10 weeks)

**Cadence**: 1-2 emails per week

**Content Mix**:
- 80% value (education, tips, resources)
- 20% promotion (offers, CTAs)

**Framework Rotation**: PAS -> FAB -> BAB -> 4Ps -> AIDA -> repeat

**Progressive Profiling**: Gather data over time through link clicks, survey questions

**KPI Targets:**
- Average open rate: 25-35%
- Average click rate: 2-5%
- Conversion rate: 1-3%

### 3. Re-engagement / Win-Back (3-5 emails, 28 days)

**Trigger**: 90 days no click engagement (not opens, due to Apple MPP)

**Standard Timeline:**
- Email 1: Day 0 (friendly check-in)
- Email 2: Day 5-7 (value reminder)
- Email 3: Day 10-14 (incentive offer)
- Email 4: Day 21 (last chance)
- Email 5: Day 28 (final goodbye)

**Framework Assignment:**
- Email 1: BAB (Before-After-Bridge)
- Email 2: 4Ps (Picture-Promise-Prove-Push)
- Email 3: AIDA (Attention-Interest-Desire-Action)
- Email 4: PAS (Problem-Agitate-Solution)
- Email 5: Direct

**After sequence**: Remove non-responders from active list to protect sender reputation

**KPI Targets:**
- Average open rate: 15-25%
- Average click rate: 1-3%
- Re-engagement rate: 5-10%

### 4. Abandoned Cart (3 emails, 3 days)

**Standard Timeline:**
- Email 1: 1 hour (reminder, no discount)
- Email 2: 24 hours (address objections, social proof)
- Email 3: 48-72 hours (incentive offer)

**Framework Assignment:**
- Email 1: Direct
- Email 2: PAS (Problem-Agitate-Solution)
- Email 3: AIDA (Attention-Interest-Desire-Action)

**Show cart items**: Include product images, names, prices in email body

**Target recovery rate**: 5-15%

**KPI Targets:**
- Email 1 open rate: 40-50%
- Email 2 open rate: 30-40%
- Email 3 open rate: 25-35%
- Total recovery rate: 10-18%

### 5. Post-Purchase (4-6 emails, 30 days)

**Standard Timeline:**
- Email 1: Immediate (order confirmation)
- Email 2: Shipped (shipping notification)
- Email 3: Delivered (delivery confirmation + tips)
- Email 4: Day 7 (value-add content)
- Email 5: Day 14 (review request)
- Email 6: Day 30 (cross-sell/upsell)

**Framework Assignment:**
- Email 1: Direct
- Email 2: Direct
- Email 3: FAB (Features-Advantages-Benefits)
- Email 4: BAB (Before-After-Bridge)
- Email 5: PAS (Problem-Agitate-Solution)
- Email 6: AIDA (Attention-Interest-Desire-Action)

**KPI Targets:**
- Average open rate: 50-70%
- Average click rate: 5-12%
- Review request response: 5-15%
- Cross-sell conversion: 3-8%

### 6. Review Request (1-2 emails)

**Timing varies by business type:**
- Restaurant/food: within 24 hours
- Salon/spa/service: same day or next day
- Home services: 24-48 hours
- Retail (simple products): 1-2 days
- Shoes/clothing: 1-2 weeks
- Courses/coaching: 1+ week
- Medical/dental: 24 hours

**Framework**: PAS (Problem-Agitate-Solution) - position review as helping others

**Include**:
- Direct link to review platform
- Multiple platform options if applicable
- Incentive (optional): discount on next purchase

**KPI Targets:**
- Open rate: 50-70%
- Review completion: 10-25%

### 7. Custom Sequence

For custom sequences, ask user:
1. **Goal**: What should this sequence accomplish?
2. **Trigger event**: What starts this sequence?
3. **Email count**: How many emails?
4. **Cadence**: How often should emails send?
5. **Tone**: Formal, casual, urgent, educational?

Design sequence architecture based on responses.

## Conditional Logic Rules

Apply these rules to every sequence:

### Engagement-Based Branching

**If opened previous email but didn't click:**
- Emphasize CTA more strongly
- Add social proof elements
- Simplify the ask

**If clicked previous email:**
- Move faster in sequence
- Skip reminder emails
- Advance to stronger offer

**If no engagement on 2+ consecutive emails:**
- Slow down cadence
- Change subject line approach
- Test different framework

**If unsubscribed:**
- Stop sequence immediately
- Remove from all active lists

### Time-Based Branching

**If cart value is high (e.g., over $200):**
- Extend abandoned cart sequence
- Add personal outreach email

**If first purchase:**
- Trigger post-purchase sequence
- Add to VIP nurture track

**If repeat customer:**
- Skip welcome emails
- Go straight to loyalty sequence

## Output Format Template

```
## Email Sequence: [Sequence Type]

**Business**: [from email-profile.md]
**Industry**: [from profile]
**Trigger**: [what starts this sequence]
**Total Emails**: X
**Duration**: X days/weeks
**Goal**: [primary objective]

### Sequence Timeline

Day 0 -> Email 1 (immediate)
Day 1 -> Email 2
Day 4 -> Email 3
Day 7 -> Email 4
[visual timeline]

---

### Email 1: [Descriptive Title] (Day 0 / Immediate)

**Purpose**: [what this email accomplishes]

**Subject Lines:**
| # | Subject | Score | Reason |
|---|---------|-------|--------|
| 1 | [subject line] | 85 | [why this scores high] |
| 2 | [subject line] | 80 | [why this scores high] |
| 3 | [subject line] | 78 | [why this scores high] |

**Preheader**: [30-80 character preview text]

**Framework**: [PAS/AIDA/BAB/FAB/4Ps/Direct]

**Body:**

[Full email copy with proper formatting, following the selected framework structure]

**CTA**: [Button text] -> [link placeholder or description]

**Conditional Logic:**
- **If opened**: Proceed to Email 2 at scheduled time
- **If not opened**: Wait 24h, resend with subject line variant #2
- **If clicked CTA**: [action - skip email, advance sequence, tag subscriber]
- **If no engagement**: [fallback action]

**A/B Test Recommendation**: [specific element to test for this email]

---

[Repeat full structure for each email in sequence]

---

### Implementation Notes

**Platform Setup:**
- [Automation trigger setup instructions]
- [Segmentation requirements]
- [Tag/field requirements]

**Recommended A/B Tests:**
1. [Test for Email 1]
2. [Test for Email 3]
3. [Overall sequence test]

**KPI Targets:**
| Metric | Target | Industry Benchmark |
|--------|--------|-------------------|
| Average Open Rate | X% | X% |
| Average Click Rate | X% | X% |
| Conversion Rate | X% | X% |
| Unsubscribe Rate | <0.5% | <0.5% |

**Monitoring:**
- Check performance after 50 subscribers complete sequence
- Adjust timing if open rates drop >20% between emails
- Test new subject lines if Email 1 opens <30%

**Segment Considerations:**
- [How to adapt for different audience segments]
- [Mobile vs desktop considerations]
- [Geographic/timezone notes if applicable]
```

## Quality Checklist

Before delivering sequence, verify:

- [ ] Each email has 3 subject line variants
- [ ] Preheaders are 30-80 characters
- [ ] Each email follows assigned framework structure
- [ ] CTAs are clear and actionable
- [ ] Conditional logic is defined for each email
- [ ] Timing makes sense for business type
- [ ] KPI targets are realistic
- [ ] A/B test recommendations are specific
- [ ] Implementation notes include platform setup

## Framework Quick Reference

Load `../../references/copy-frameworks.md` for detailed structures:

- **PAS**: Problem -> Agitate -> Solution
- **AIDA**: Attention -> Interest -> Desire -> Action
- **BAB**: Before -> After -> Bridge
- **FAB**: Features -> Advantages -> Benefits
- **4Ps**: Picture -> Promise -> Prove -> Push
- **Direct**: Straightforward, no persuasion layer (transactional emails)

## Notes

- Always adapt sequence length and cadence to business context
- B2B sequences should be longer (nurture over 8-12 weeks)
- E-commerce can be more aggressive (faster cadence)
- Service businesses benefit from educational content
- Always include easy unsubscribe option
- Test sequences with small segment before full deployment
- Monitor sender reputation metrics (bounce rate, complaint rate)
- Apple Mail Privacy Protection makes open tracking unreliable - focus on clicks
- Use sunset policies: remove non-engaged subscribers after 6-12 months

## Integration with Other Skills

- Use `/email audit` to verify domain deliverability before launching sequences
- Use `/email write` for individual email drafts or rewrites
- Use `/email review` to score and optimize each email in the sequence
- Use `/email plan` to align sequences with overall marketing strategy
