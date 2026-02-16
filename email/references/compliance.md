# Email Compliance Rules

This reference covers CAN-SPAM, GDPR, CCPA, and RFC 8058 compliance requirements for email marketing.

---

## CAN-SPAM Act (United States)

**Jurisdiction**: United States
**Applies To**: Commercial email messages
**Enforced By**: Federal Trade Commission (FTC)

### Core Requirements

1. **Accurate Header Information**
   - From/To/Reply-To must accurately identify sender
   - Routing information must be accurate
   - Domain name must belong to sender

2. **Non-Deceptive Subject Lines**
   - Subject must reflect email content
   - No misleading or false subject lines
   - Examples of violations:
     - "Re: Your order" (when no prior order exists)
     - "Your account suspended" (when not true)
     - Subject completely unrelated to content

3. **Identify as Advertisement**
   - Must clearly identify commercial messages
   - Disclosure can be in subject or body
   - Not required for transactional/relationship messages

4. **Physical Postal Address**
   - Valid physical postal address required
   - Can be street address, PO box, or private mailbox (PMB) registered with a commercial mail receiving agency (per USPS regulations)
   - Must be current and accurate
   - Location: Typically in email footer

5. **Unsubscribe Mechanism**
   - Clear and conspicuous opt-out method
   - Must work for at least 30 days after email sent
   - Process opt-out within 10 business days
   - Cannot charge fee or require additional information beyond email address
   - Cannot require login to unsubscribe

6. **Third-Party Responsibility**
   - Sender responsible even if hired third party
   - Both advertiser and sender can be held liable

### Exemptions (Transactional/Relationship Emails)
- Order confirmations
- Account updates
- Warranty information
- Product recall notices
- Security alerts
- Transaction facilitation

### Penalties
- **Civil**: $51,744 per violation (adjusted for inflation)
- **Criminal**: Aggravated violations (harvesting, spoofing) can result in imprisonment
- **No Cap**: Each separate email can be a separate violation

### Validation Checklist
- ✅ Accurate From/Reply-To headers
- ✅ Subject line matches content
- ✅ Physical postal address in footer
- ✅ Unsubscribe link present and functional
- ✅ Unsubscribe honored within 10 business days
- ❌ Deceptive subject line
- ❌ Missing physical address
- ❌ No unsubscribe mechanism
- ❌ Unsubscribe requires login/payment

---

## GDPR (European Union / UK)

**Jurisdiction**: EU/EEA member states, UK
**Applies To**: Processing of personal data of EU/UK residents
**Enforced By**: Data Protection Authorities (DPAs)

### Legal Bases for Email Marketing

1. **Consent** (Most Common for B2C)
   - Must be freely given, specific, informed, unambiguous
   - Affirmative action required (no pre-checked boxes)
   - Easy to withdraw as it was to give
   - Must keep records of consent (who, when, what they consented to)
   - Granular consent for different purposes

2. **Legitimate Interest** (Common for B2B)
   - Must document legitimate interest assessment (LIA)
   - Balance sender's interest vs. recipient's rights
   - Must offer opt-out
   - Appropriate for:
     - Existing customer relationships
     - B2B cold outreach (soft opt-in)
     - Similar products/services to existing customers

3. **Contract** (Transactional Emails Only)
   - Order confirmations
   - Shipping notifications
   - Account-related messages

### Core Requirements

1. **Data Minimization**
   - Only collect necessary personal data
   - Don't ask for more than needed
   - Delete when no longer needed

2. **Transparency**
   - Privacy notice before/at collection
   - Clear explanation of data use
   - Identity of data controller

3. **Individual Rights**
   - **Right to Access**: Provide copy of data on request
   - **Right to Erasure**: Delete data ("right to be forgotten")
   - **Right to Rectification**: Correct inaccurate data
   - **Right to Portability**: Provide data in machine-readable format
   - **Right to Object**: Stop processing for marketing
   - **Right to Restrict**: Limit processing in certain cases

4. **Data Security**
   - Appropriate technical and organizational measures
   - Encryption of sensitive data
   - Regular security assessments

5. **Breach Notification**
   - Notify DPA within 72 hours of breach
   - Notify affected individuals if high risk

6. **Data Processing Agreements (DPAs)**
   - Required with email service providers (ESPs)
   - Must specify data processing terms

### Consent Requirements

**Valid Consent Must Be:**
- **Freely given**: No bundled consent, genuine choice
- **Specific**: Separate consent for different purposes
- **Informed**: User understands what they consent to
- **Unambiguous**: Clear affirmative action
- **Withdrawable**: Easy to withdraw consent

**Invalid Consent Examples:**
- Pre-checked boxes
- "By using our site, you consent to marketing emails"
- Bundled with terms and conditions
- Unclear language about data use

### Documentation Requirements
- What data is collected
- Why it's collected (purpose)
- Legal basis (consent, legitimate interest, etc.)
- How long it's retained
- Who it's shared with
- Date and method of consent

### Penalties
- **Tier 1**: Up to €10M or 2% of global annual revenue (whichever is higher)
- **Tier 2**: Up to €20M or 4% of global annual revenue
- Based on: Severity, duration, intent, cooperation, prior violations

### Validation Checklist
- ✅ Explicit opt-in consent (or documented legitimate interest for B2B)
- ✅ Privacy notice provided before data collection
- ✅ Consent records documented (who, when, what)
- ✅ Easy unsubscribe mechanism
- ✅ Data processing agreement with ESP
- ✅ Breach notification procedures in place
- ❌ Pre-checked consent boxes
- ❌ No privacy notice
- ❌ Cannot provide consent records
- ❌ Difficult to withdraw consent

---

## CCPA/CPRA (California)

**Jurisdiction**: California, USA
**Applies To**: Businesses meeting thresholds (see below)
**Enforced By**: California Privacy Protection Agency (CPPA)

### Applicability Thresholds (Any One)
- Annual gross revenues >$25 million
- Buy/sell personal info of 100,000+ California consumers/households/year
- Derive 50%+ of annual revenue from selling/sharing personal info

### Core Consumer Rights

1. **Right to Know**
   - What personal information is collected
   - Sources of information
   - Purpose of collection/use
   - Third parties data is shared with
   - Specific pieces of data collected

2. **Right to Delete**
   - Request deletion of personal information
   - Exceptions: Complete transaction, detect fraud, comply with legal obligations

3. **Right to Opt-Out**
   - Opt out of sale/sharing of personal information
   - "Do Not Sell or Share My Personal Info" link required
   - Apply opt-out universally (honor GPC - Global Privacy Control)

4. **Right to Correct**
   - Request correction of inaccurate personal information
   - Added by CPRA (2023)

5. **Right to Limit Sensitive Data Use**
   - Limit use/disclosure of sensitive personal information
   - Added by CPRA (2023)

6. **Right to Non-Discrimination**
   - Cannot discriminate for exercising rights
   - No denial of service, different pricing, lower quality
   - Exception: Can offer financial incentive for providing data

### Email Marketing Implications

1. **Privacy Notice Requirements**
   - Provide notice at or before data collection
   - Explain what data is collected and why
   - How long data is retained
   - If data is sold/shared

2. **Do Not Sell Link**
   - Required on website if selling/sharing data
   - Must honor request within 15 business days
   - Apply to all browsers/devices for that consumer

3. **Sensitive Personal Information**
   - Email content may contain sensitive data
   - Must allow opt-out of sensitive data use

4. **Data Sale Definition**
   - Sharing data with third parties for consideration
   - Includes some ESP integrations (ad networks, data brokers)
   - Retargeting pixels may constitute "sale"

### Verification Requirements
- Reasonable method to verify consumer identity
- Match data points provided to data on file
- Can request additional information if needed

### Response Timeframes
- **Right to Know**: 45 days (extendable to 90)
- **Right to Delete**: 45 days (extendable to 90)
- **Right to Opt-Out**: 15 business days

### Penalties
- **Civil**: $2,500 per violation
- **Intentional**: $7,500 per violation
- **Data Breach**: $100-$750 per consumer per incident

### Validation Checklist
- ✅ Privacy notice provided before data collection
- ✅ "Do Not Sell" link on website (if selling data)
- ✅ Honor opt-out requests within 15 business days
- ✅ Verify consumer identity for requests
- ✅ Data inventory and mapping complete
- ❌ No privacy notice
- ❌ Discriminate against consumers exercising rights
- ❌ Cannot verify data deletion

---

## CASL (Canada's Anti-Spam Legislation)

**Jurisdiction**: Canada
**Applies To**: Commercial electronic messages (CEMs) sent to or from Canada
**Enforced By**: Canadian Radio-television and Telecommunications Commission (CRTC)

### Core Requirements

1. **Express Consent Required (Opt-In)**
   - Must obtain explicit consent before sending commercial emails
   - Pre-checked boxes are NOT valid consent
   - Must clearly identify the sender and purpose at time of consent
   - Consent records must be kept (who, when, how)

2. **Implied Consent (Limited Duration)**
   - Valid for existing business relationships: 2 years from last purchase/transaction
   - Valid for existing non-business relationships: 2 years from membership/donation
   - Valid for inquiries: 6 months from inquiry
   - Must convert to express consent before implied consent expires

3. **Required Message Elements**
   - Sender identification (name, business name)
   - Contact information (mailing address, phone/email/web)
   - Unsubscribe mechanism (must work for 60 days after sending)
   - Process unsubscribe within 10 business days

4. **Unsubscribe Mechanism**
   - Must be functional for at least 60 days after email is sent
   - Must be processed within 10 business days
   - Cannot require any action beyond sending a reply or visiting a single webpage
   - Cannot charge a fee

### Penalties
- **Individuals**: Up to $1M CAD per violation
- **Organizations**: Up to $10M CAD per violation
- **Private Right of Action**: Individuals can sue for damages (up to $200 per violation, max $1M per day)

### Key Differences from CAN-SPAM
- CASL requires **opt-in** (CAN-SPAM is opt-out)
- CASL applies to messages sent **to** Canada (not just from)
- Implied consent has a **2-year expiry** (CAN-SPAM has none)
- Higher penalties per violation than CAN-SPAM

### Validation Checklist
- ✅ Express consent obtained and documented (or valid implied consent)
- ✅ Sender identification in message (name, address, contact info)
- ✅ Functional unsubscribe mechanism (works 60 days)
- ✅ Unsubscribe honored within 10 business days
- ✅ Consent records maintained (who, when, how)
- ❌ No consent obtained before sending
- ❌ Pre-checked consent boxes
- ❌ Implied consent expired (>2 years since last transaction)
- ❌ Unsubscribe mechanism non-functional

---

## RFC 8058: One-Click Unsubscribe

**Status**: IETF Standard (May 2017)
**Required By**: Google, Yahoo, Microsoft (for bulk senders as of 2024)
**Applies To**: Marketing/promotional emails from bulk senders (5,000+ emails/day)

### Required Email Headers

```
List-Unsubscribe: <https://example.com/unsubscribe?id=UNIQUE_ID>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

### Technical Requirements

1. **HTTPS URI Required**
   - Must use HTTPS (not HTTP)
   - Cannot use mailto: URIs for one-click
   - URI must be unique per recipient

2. **POST Request Support**
   - Endpoint must accept POST requests
   - POST body: `List-Unsubscribe=One-Click`
   - Must return 2xx status code on success

3. **DKIM Coverage**
   - DKIM signature must cover both headers:
     - `List-Unsubscribe`
     - `List-Unsubscribe-Post`
   - Prevents header forgery

4. **Processing Requirements**
   - Process unsubscribe within 2 business days
   - No additional confirmation required from user
   - Cannot require login/authentication
   - Must unsubscribe from sender, not just list

### Example Headers

```
List-Unsubscribe: <https://example.com/unsub?id=a8b3f2c1>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

DKIM signature must cover both `list-unsubscribe` and `list-unsubscribe-post` headers. Server endpoint must accept POST with body `List-Unsubscribe=One-Click` and return 2xx.

### Gmail/Yahoo Enforcement
- Bulk senders (5,000+ emails/day) must implement
- Non-compliance results in:
  - Temporary deferral (4xx codes)
  - Permanent rejection (5xx codes)
  - Lower sender reputation
  - Reduced inbox placement

### Validation Checklist
- ✅ Both headers present (List-Unsubscribe + List-Unsubscribe-Post)
- ✅ HTTPS URI (not HTTP or mailto)
- ✅ Endpoint accepts POST requests
- ✅ Returns 2xx status code
- ✅ DKIM signature covers both headers
- ✅ Processes unsubscribe within 2 business days
- ❌ Missing List-Unsubscribe-Post header
- ❌ HTTP URI (must be HTTPS)
- ❌ Endpoint returns errors (4xx/5xx)
- ❌ DKIM doesn't cover headers
- ❌ Requires user login/confirmation

---

## Compliance Comparison Table

| Requirement | CAN-SPAM (US) | GDPR (EU/UK) | CCPA (CA) | CASL (Canada) | RFC 8058 |
|-------------|---------------|--------------|-----------|---------------|----------|
| **Opt-in required** | No (opt-out) | Yes (consent) | No (opt-out) | Yes (express consent) | N/A |
| **Physical address** | Yes (required) | Recommended | No | Yes (required) | No |
| **Unsubscribe link** | Yes (10 biz days) | Yes (immediate) | Yes (15 biz days) | Yes (10 biz days) | Yes (2 biz days) |
| **One-click unsub** | No | No | No | No | Yes (bulk senders) |
| **Data deletion** | No | Yes (right to erasure) | Yes (right to delete) | No | No |
| **Consent records** | No | Yes (documentation) | Recommended | Yes (required) | No |
| **Privacy notice** | No | Yes (before collection) | Yes (at/before collection) | At consent | No |
| **Implied consent** | N/A (opt-out) | No | N/A | Yes (2-year expiry) | N/A |
| **Breach notification** | Varies | 72 hours to DPA | Without delay | N/A | N/A |
| **Penalties (max)** | $51,744/violation | €20M or 4% revenue | $7,500/violation | $10M CAD/violation | Delivery failure |

---

## Compliance by Email Type

### Transactional/Relationship Emails
- **CAN-SPAM**: Exempt from most requirements (still need accurate headers, address)
- **GDPR**: Allowed under "contract" legal basis (no consent needed)
- **CCPA**: Allowed for transaction fulfillment
- **CASL**: Exempt (transactional messages are not CEMs)
- **RFC 8058**: Not required (marketing only)

### Marketing/Promotional Emails
- **CAN-SPAM**: All requirements apply
- **GDPR**: Requires consent or legitimate interest (documented)
- **CCPA**: Subject to all privacy rights
- **CASL**: Express consent required (or valid implied consent within 2-year window)
- **RFC 8058**: Required for bulk senders (5,000+/day)

### B2B Cold Outreach
- **CAN-SPAM**: Allowed (must have opt-out)
- **GDPR**: Allowed under "legitimate interest" (must document LIA)
- **CCPA**: Subject to privacy rights if California business contacts
- **CASL**: Requires consent (implied consent for existing business relationships only)
- **RFC 8058**: Required if bulk volume

---

## Geographic Compliance Strategy

### US-Only Audience
- Comply with CAN-SPAM (minimum)
- Add RFC 8058 if bulk sender
- California users: Add CCPA disclosures

### Canadian Audience
- CASL compliance required (opt-in, not just opt-out)
- Track implied consent expiry dates (2 years from last transaction)
- Keep consent records (who, when, how)
- Include sender identification and contact info in every email

### EU/UK Audience
- GDPR compliance required
- Must obtain explicit consent
- Keep consent records
- Data processing agreement with ESP

### North American Audience (US + Canada)
- Apply CASL standards (stricter than CAN-SPAM due to opt-in requirement)
- Segment US vs Canada contacts for consent tracking
- RFC 8058 for bulk senders

### Global Audience
- Apply GDPR standards (strictest overall)
- Segment by region for consent/opt-in rules
- Unified privacy policy covering all jurisdictions
- RFC 8058 for bulk senders

---

## Common Compliance Violations

### High-Risk Violations
1. **No unsubscribe link** - Violates all regulations
2. **Deceptive subject lines** - CAN-SPAM violation, FTC enforcement
3. **No physical address** - CAN-SPAM violation
4. **Pre-checked consent boxes** - GDPR and CASL violation
5. **Purchased email lists** - GDPR and CASL violation (no valid consent)
6. **No privacy notice** - GDPR/CCPA violation
7. **Sending to Canada without express consent** - CASL violation ($10M CAD penalty)

### Medium-Risk Violations
1. **Slow unsubscribe processing** - >10 days CAN-SPAM, >2 days RFC 8058
2. **Unsubscribe requires login** - CAN-SPAM violation
3. **No consent documentation** - GDPR enforcement risk
4. **Missing RFC 8058 headers** - Delivery issues with Google/Yahoo

### Low-Risk Issues
1. **Unsubscribe link hard to find** - Not illegal but bad practice
2. **Vague privacy notice** - Legal but not best practice
3. **No data processing agreement** - GDPR risk if audited

---

## Compliance Monitoring Checklist

### Pre-Send Validation
- [ ] Physical address in footer (CAN-SPAM)
- [ ] Unsubscribe link present and functional
- [ ] Subject line matches content
- [ ] List-Unsubscribe headers (bulk senders)
- [ ] DKIM covers RFC 8058 headers
- [ ] Consent records available (GDPR)
- [ ] Privacy notice provided (GDPR/CCPA)

### Post-Send Monitoring
- [ ] Unsubscribe requests honored within SLA
- [ ] Consent withdrawal processed
- [ ] Data deletion requests fulfilled
- [ ] Complaint rate under 0.1%
- [ ] No spam trap hits

### Quarterly Audits
- [ ] Review consent documentation
- [ ] Update privacy notices if practices change
- [ ] Verify ESP data processing agreements
- [ ] Test all unsubscribe mechanisms
- [ ] Review list hygiene practices

<!-- Updated: 2026-02-16 -->
