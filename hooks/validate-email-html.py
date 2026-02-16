#!/usr/bin/env python3
"""Validate HTML email after editing.

Hook type: PostToolUse (Edit, Write)
Exit 0 = allow, Exit 2 = block with message
"""

import sys
import re
from pathlib import Path

def validate_html_email(file_path: str) -> tuple[bool, list[str]]:
    """Validate HTML email file.

    Returns:
        (is_valid, messages) where messages are warnings/errors
    """
    path = Path(file_path)

    # Only check .html files
    if path.suffix.lower() != '.html':
        return True, []

    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"❌ Cannot read file: {e}"]

    errors = []
    warnings = []

    # Check 1: File size (Gmail clips at 102KB)
    file_size = len(content.encode('utf-8'))
    if file_size > 102 * 1024:
        errors.append(f"❌ BLOCKED: File size {file_size // 1024}KB exceeds 102KB Gmail limit")
        errors.append("   Gmail will clip your email. Reduce content or move to plain text.")
    elif file_size > 80 * 1024:
        warnings.append(f"⚠️  File size {file_size // 1024}KB approaching 102KB limit")

    # Check 2: Contains at least one <table> (email layout best practice)
    if not re.search(r'<table[^>]*>', content, re.IGNORECASE):
        warnings.append("⚠️  No <table> elements found — consider using table-based layout for email")

    # Check 3: No CSS Grid or Flexbox (poor email client support)
    if re.search(r'display:\s*grid', content, re.IGNORECASE):
        errors.append("❌ BLOCKED: CSS Grid detected — not supported in most email clients")
    if re.search(r'display:\s*flex', content, re.IGNORECASE):
        errors.append("❌ BLOCKED: CSS Flexbox detected — not supported in most email clients")

    # Check 4: Has viewport meta tag
    if not re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE):
        warnings.append("⚠️  Missing viewport meta tag — may not render properly on mobile")

    # Check 5: Inline styles preferred over <style> tags
    if re.search(r'<style[^>]*>', content, re.IGNORECASE):
        style_count = len(re.findall(r'<style[^>]*>', content, re.IGNORECASE))
        warnings.append(f"⚠️  {style_count} <style> tag(s) found — inline styles have better email client support")

    is_valid = len(errors) == 0
    messages = errors + warnings

    return is_valid, messages


def main():
    if len(sys.argv) < 2:
        print("Usage: validate-email-html.py <file_path>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    is_valid, messages = validate_html_email(file_path)

    if messages:
        print("HTML email validation results:")
        for msg in messages:
            print(msg)
        print()

    if is_valid:
        if messages:
            print("✓ Validation passed (warnings above are advisory)")
        sys.exit(0)
    else:
        print("✗ Validation failed — see errors above")
        sys.exit(2)


if __name__ == '__main__':
    main()
