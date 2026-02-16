#!/usr/bin/env bash
# pre-send-check.sh — Quality gate before sending emails
# Hook type: PreToolUse (Bash)
# Exit 0 = allow, Exit 2 = block with message

set -euo pipefail

# Read email content from arguments or stdin
EMAIL_SUBJECT="${1:-}"
EMAIL_BODY="${2:-}"

if [[ -z "$EMAIL_SUBJECT" && -z "$EMAIL_BODY" ]]; then
    # If no args, try stdin
    EMAIL_CONTENT=$(cat)
    EMAIL_SUBJECT=$(echo "$EMAIL_CONTENT" | grep -i "^Subject:" | head -1 | sed 's/^Subject: *//i' || true)
    EMAIL_BODY=$(echo "$EMAIL_CONTENT" | sed '1,/^$/d')
fi

WARNINGS=()
WORD_COUNT=$(echo "$EMAIL_BODY" | wc -w | tr -d ' ')

# Check 1: Spam trigger words in subject
SPAM_WORDS=("FREE!!!" "ACT NOW" "LIMITED TIME" "CLICK HERE" "BUY NOW" "URGENT" "WINNER" "CONGRATULATIONS!!!")
for word in "${SPAM_WORDS[@]}"; do
    if echo "$EMAIL_SUBJECT" | grep -qi "$word"; then
        WARNINGS+=("⚠️  Subject contains spam trigger word: '$word'")
    fi
done

# Check 2: All caps subject
if [[ "$EMAIL_SUBJECT" =~ ^[A-Z0-9[:space:][:punct:]]+$ ]] && [[ ${#EMAIL_SUBJECT} -gt 5 ]]; then
    WARNINGS+=("⚠️  Subject is all caps — may trigger spam filters")
fi

# Check 3: Email body too short
if [[ $WORD_COUNT -lt 20 ]]; then
    WARNINGS+=("⚠️  Email body very short ($WORD_COUNT words) — consider adding more context")
fi

# Check 4: Missing unsubscribe link in marketing emails (block if detected as marketing)
MARKETING_KEYWORDS=("newsletter" "unsubscribe" "marketing" "promotion" "offer" "discount")
IS_MARKETING=false
for keyword in "${MARKETING_KEYWORDS[@]}"; do
    if echo "$EMAIL_BODY" | grep -qi "$keyword"; then
        IS_MARKETING=true
        break
    fi
done

if $IS_MARKETING && ! echo "$EMAIL_BODY" | grep -qi "unsubscribe"; then
    echo "❌ BLOCKED: Marketing email missing unsubscribe link"
    echo "Add an unsubscribe mechanism to comply with CAN-SPAM and GDPR."
    exit 2
fi

# Print warnings but allow send
if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    echo "Pre-send quality checks:"
    for warning in "${WARNINGS[@]}"; do
        echo "$warning"
    done
    echo ""
    echo "✓ Checks passed (warnings above are advisory)"
fi

exit 0
