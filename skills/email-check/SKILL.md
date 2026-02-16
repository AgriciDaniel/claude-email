---
name: email-check
description: Intelligent inbox triage that connects to Gmail or Outlook, scores emails by importance (0-100) using sender recognition, urgency keywords, thread depth, time sensitivity, and business relevance, categorizes into Urgent/Important/Routine/Archive, and generates reply suggestions for top priority items. Use when the user wants to check email, review inbox, triage messages, see what's urgent, or get reply suggestions. Triggers on check email, inbox triage, what's important, email summary, unread emails, priority inbox.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Email Check Sub-Skill

## Purpose

This sub-skill handles intelligent inbox triage by connecting to Gmail or Outlook via MCP, analyzing unread emails, scoring them by importance, categorizing them, and generating reply suggestions for high-priority items.

## Workflow

### 1. Detect Available Email Provider

Check which MCP tools are available:
- **Gmail**: `search_gmail_messages`, `get_gmail_messages_content_batch`, `get_gmail_thread_content`, `list_gmail_labels`
- **Outlook**: `list-mail-messages`, `list-mail-folder-messages`, `get-mail-message`

Prefer Gmail if both are available (better batch operations).

### 2. Fetch Unread Emails

**For Gmail:**
```
search_gmail_messages(query="is:unread", max_results=50)
```

**For Outlook:**
```
list-mail-messages (defaults to recent messages, filter for unread)
```

### 3. Batch Fetch Email Content

**For Gmail:**
```
get_gmail_messages_content_batch(message_ids=[...])  # Up to 25 at a time
```

If more than 25 unread, prioritize most recent first.

**For Outlook:**
```
get-mail-message for each message (sequential)
```

Limit to 25 emails maximum to avoid overwhelming analysis.

### 4. Score Each Email (0-100)

Apply the following scoring algorithm:

#### Base Score: 50

#### Sender Recognition (+20 to -20)
- **+20**: VIP/known contact (domain matches user's company, appears in sent folder frequently)
- **+10**: Recognized sender (has prior thread history)
- **0**: Unknown sender with legitimate domain
- **-15**: Newsletter/automated sender (bulk email headers, unsubscribe links)
- **-20**: Notification sender (no-reply@, noreply@, automated@)

#### Direct Address (+15 to -10)
- **+15**: Primary recipient (To: field)
- **0**: CC'd (CC: field)
- **-10**: BCC'd or mass email (many recipients)

#### Thread Depth (+10)
- **+10**: Reply in active thread (Re: subject, multiple messages in thread)
- **0**: New email (no thread history)

#### Urgency Keywords (+15)
Check subject and first 200 characters for:
- urgent, ASAP, deadline, action required, immediate, time-sensitive, expiring, expires, due
- **+15** if any urgency keyword found

#### Calendar/Meeting (+20)
- **+20**: Calendar invite, meeting request, event notification
- Detect via attachments (ics file) or subject patterns (Invitation:, Meeting:)

#### Deadline Detection (+25)
Parse email body for dates/deadlines:
- **+25**: Deadline within 48 hours
- **+10**: Deadline within 7 days
- **0**: No deadline or deadline > 7 days

#### Business Relevance (+15 to -10)
If `email-profile.md` exists in parent directory:
- **+15**: Mentions user's key topics, clients, projects
- **+5**: Industry-relevant keywords
- **-10**: Off-topic or personal (if business inbox)

#### Final Score Calculation
Sum all adjustments to base score of 50.
Clamp to 0-100 range.

### 5. Categorize Emails

Based on final score:

| Score Range | Category | Action |
|-------------|----------|--------|
| 85-100 | **Urgent** | Immediate attention, generate reply suggestions |
| 65-84 | **Important** | Review soon, may need action |
| 40-64 | **Routine** | Normal priority, review when available |
| 20-39 | **Low Priority** | Skim or defer |
| 0-19 | **Archive** | Likely noise or automated |

### 6. Generate Reply Suggestions

For emails scored 85+ (Urgent category):

1. **Read full thread context** using `get_gmail_thread_content` or equivalent
2. **Check for email-profile.md** in parent directory for user's:
   - Brand voice (professional, casual, direct, warm)
   - Common sign-off
   - Industry/role context
3. **Draft two reply options:**
   - **Brief**: 1-2 sentences, direct answer
   - **Detailed**: 1 paragraph with context

**Do NOT draft replies if:**
- Email requires research beyond available context
- Email needs user decision (approve/decline, choose option)
- Email is FYI/informational only
- Email is calendar invite (suggest accept/decline/tentative instead)

In these cases, output: **"This email requires your personal attention: [reason]"**

### 7. Output Format

```markdown
## Inbox Summary

**X unread emails** | Y Urgent | Z Important | W Routine | V Low Priority

### Urgent (Action Required)

| # | From | Subject | Score | Suggested Action |
|---|------|---------|-------|------------------|
| 1 | sender@domain.com | Subject line | 95 | [Reply/Review/Respond] |
| 2 | ... | ... | 88 | ... |

---

### Important

| # | From | Subject | Score | Category |
|---|------|---------|-------|----------|
| 3 | ... | ... | 78 | Meeting follow-up |
| 4 | ... | ... | 70 | Client inquiry |

---

### Routine & Low Priority

- **Routine (40-64)**: X emails - [grouped summary by sender/topic]
- **Low Priority (20-39)**: Y emails - newsletters, notifications
- **Archive (<20)**: Z emails - automated/noise

---

### Suggested Replies

#### 1. Re: [Subject] (to: sender@domain.com)

**Context:** [Why this email scored high, key points]

**Brief Option:**
> [1-2 sentence reply]
>
> [Sign-off]

**Detailed Option:**
> [Paragraph with more context/explanation]
>
> [Sign-off]

#### 2. Re: [Next urgent email]

[Repeat format]

---

### Emails Requiring Personal Attention

- **#X - [Subject]**: Needs decision on [topic]
- **#Y - [Subject]**: Requires research before responding
```

## Scoring Signal Reference

| Signal | Score Impact | Detection |
|--------|-------------|-----------|
| Direct To: address | +15 | Check To: field |
| VIP/known sender | +20 | Domain match, sent folder history |
| Active thread | +10 | Thread ID, Re: in subject |
| Urgency keywords | +15 | Subject/body scan |
| Calendar invite | +20 | .ics attachment, invite headers |
| Deadline <48h | +25 | Date parsing in body |
| Deadline <7d | +10 | Date parsing in body |
| Business relevance | +15 | Match email-profile.md topics |
| CC'd (not primary) | -10 | CC: field |
| Newsletter | -20 | Unsubscribe link, bulk headers |
| Notification | -15 | no-reply@ sender |
| Unknown sender | -10 | No thread history |

## Reply Suggestion Guidelines

### Tone Adaptation
If `email-profile.md` exists, adapt replies to match:
- **Professional**: Formal, structured, clear
- **Casual**: Friendly, conversational
- **Direct**: Brief, action-oriented
- **Warm**: Personable, relationship-focused

Default to professional-friendly if no profile exists.

### Reply Structure

**Brief Option:**
- Answer the core question/request
- 1-2 sentences maximum
- Clear next step if needed

**Detailed Option:**
- Address all points raised
- Provide context or explanation
- 1 paragraph (3-5 sentences)
- Suggest next steps or timeline

### When NOT to Draft
- Email asks for approval/decision → Suggest: "Review and approve/decline X"
- Email requires data you don't have → "This email requires your personal attention: needs [data/info]"
- Email is complex multi-part → "This email requires your personal attention: multiple decisions needed"
- Email is FYI only → Suggested Action: "Review (no response needed)"

## Error Handling

### No MCP Connection
If neither Gmail nor Outlook MCP is available:
```
Error: No email provider connected. Please ensure Gmail MCP or Outlook MCP is configured.
```

### Empty Inbox
```
## Inbox Summary
**0 unread emails** - Your inbox is clear!
```

### MCP Rate Limits
If batch fetch fails, fall back to individual message retrieval (slower but reliable).

### Thread Context Unavailable
If `get_gmail_thread_content` fails, draft replies based on single message only (note: "Limited context - single message view").

## Integration Points

### email-profile.md (optional)
If exists in parent directory (`../email-profile.md`), use for:
- Brand voice detection
- Business relevance scoring
- Reply tone/style matching
- Common topics/clients list

### Gmail-Specific Features
- Use labels to refine categorization (e.g., skip "Promotions" labeled emails)
- Check sent folder for sender recognition

### Outlook-Specific Features
- Use folder structure for context (Inbox vs Focused)
- Leverage categories if available

## Performance Optimization

- Batch fetch 25 emails at a time (Gmail)
- Limit analysis to 50 most recent unread
- Cache sender recognition data during session
- Prioritize most recent emails if >50 unread

## Output Constraints

- Keep total output under 2000 lines
- Group routine/low priority emails by topic/sender
- Only show full details for Urgent and Important categories
- Collapse archived emails into summary count

## Quality Gates

Before outputting digest:
1. Verify all urgency scores are justified with signal breakdown
2. Ensure reply suggestions are actionable (not generic)
3. Check that "personal attention" notes explain why
4. Confirm categories align with score ranges
5. Validate that batch operations completed successfully

## Success Criteria

A successful email check session should:
- Identify all truly urgent emails (no false negatives)
- Minimize false positives in Urgent category (precision > 80%)
- Provide actionable reply drafts for top 3-5 emails
- Complete analysis in <30 seconds for 25 emails
- Output clear next actions for each category
