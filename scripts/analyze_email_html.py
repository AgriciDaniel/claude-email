#!/usr/bin/env python3
"""
HTML Email Analyzer

Analyzes HTML email files for best practices, deliverability, and rendering issues.
Checks size, images, responsive design, dark mode, layout, links, and compliance.

Usage:
    python analyze_email_html.py email.html
    python analyze_email_html.py email.html --json
    python analyze_email_html.py --stdin < email.html
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Try to import BeautifulSoup with graceful fallback
try:
    from bs4 import BeautifulSoup
    PARSER = "lxml"
    try:
        # Test if lxml is available
        BeautifulSoup("<html></html>", "lxml")
    except:
        PARSER = "html.parser"
except ImportError:
    print("WARNING: BeautifulSoup not installed. Install with: pip install beautifulsoup4 lxml", file=sys.stderr)
    print("Falling back to basic HTML parsing (limited functionality)", file=sys.stderr)
    BeautifulSoup = None
    PARSER = None


# Link shortener domains to flag
LINK_SHORTENERS = [
    "bit.ly", "tinyurl.com", "goo.gl", "ow.ly", "t.co", "buff.ly",
    "is.gd", "tiny.cc", "shorturl.at", "rebrand.ly"
]

# Pure white color variations
PURE_WHITE_VARIANTS = [
    "#ffffff", "#fff", "white", "rgb(255,255,255)", "rgb(255, 255, 255)",
    "rgba(255,255,255,1)", "rgba(255, 255, 255, 1)"
]


def analyze_size(html: str, filepath: str) -> Dict[str, Any]:
    """Analyze HTML file size and Gmail clip risk."""
    size_bytes = len(html.encode('utf-8'))
    size_kb = size_bytes / 1024

    gmail_clip_risk = size_kb > 80
    gmail_clip_critical = size_kb > 102

    issues = []
    if gmail_clip_critical:
        issues.append({"severity": "high", "check": "size", "message": f"HTML exceeds 102KB - Gmail will clip this email"})
    elif gmail_clip_risk:
        issues.append({"severity": "medium", "check": "size", "message": f"HTML exceeds 80KB - approaching Gmail clip limit"})

    return {
        "size_bytes": size_bytes,
        "size_kb": round(size_kb, 1),
        "gmail_clip_risk": gmail_clip_risk,
        "gmail_clip_critical": gmail_clip_critical,
        "issues": issues
    }


def analyze_images(soup: BeautifulSoup, html: str) -> Dict[str, Any]:
    """Analyze image usage and alt text."""
    if not soup:
        return {"count": 0, "missing_alt": 0, "text_image_ratio": "unknown", "issues": []}

    img_tags = soup.find_all('img')
    img_count = len(img_tags)
    missing_alt = sum(1 for img in img_tags if not img.get('alt'))

    # Calculate text to image ratio
    text_content = soup.get_text(separator=' ', strip=True)
    text_length = len(text_content)

    # Rough estimate: assume average image is 50KB encoded as base64
    # For external images, we can't know size, so use conservative estimate
    estimated_image_size = img_count * 50 * 1024  # 50KB per image

    if text_length > 0:
        # Text ratio = text_chars / (text_chars + estimated_image_chars)
        # Using file size as proxy for visual weight
        text_ratio = (text_length / (text_length + estimated_image_size / 10)) * 100
        image_ratio = 100 - text_ratio
        ratio_str = f"{int(text_ratio)}/{int(image_ratio)}"
    else:
        ratio_str = "0/100"
        text_ratio = 0

    issues = []
    if missing_alt > 0:
        issues.append({
            "severity": "medium",
            "check": "images",
            "message": f"{missing_alt} image(s) missing alt text"
        })

    if img_count > 0 and text_ratio < 60:
        issues.append({
            "severity": "medium",
            "check": "images",
            "message": f"Low text-to-image ratio ({ratio_str}) - aim for 60/40 minimum"
        })

    if img_count > 0 and text_length < 100:
        issues.append({
            "severity": "high",
            "check": "images",
            "message": "Image-only email detected - will fail with images disabled"
        })

    return {
        "count": img_count,
        "missing_alt": missing_alt,
        "text_image_ratio": ratio_str,
        "issues": issues
    }


def analyze_responsive(soup: BeautifulSoup, html: str) -> Dict[str, Any]:
    """Check responsive design implementation."""
    if not soup:
        return {"viewport_meta": False, "media_queries": False, "max_width": None, "issues": []}

    # Check for viewport meta tag
    viewport_meta = soup.find('meta', attrs={'name': 'viewport'}) is not None

    # Check for media queries
    media_queries = '@media' in html

    # Check for max-width on main container
    max_width = None
    style_tags = soup.find_all('style')
    for style in style_tags:
        if style.string and 'max-width' in style.string:
            # Try to extract max-width value
            match = re.search(r'max-width:\s*(\d+)px', style.string)
            if match:
                max_width = f"{match.group(1)}px"
                break

    # Also check inline styles
    if not max_width:
        for tag in soup.find_all(style=True):
            if 'max-width' in tag['style']:
                match = re.search(r'max-width:\s*(\d+)px', tag['style'])
                if match:
                    max_width = f"{match.group(1)}px"
                    break

    issues = []
    if not viewport_meta:
        issues.append({
            "severity": "medium",
            "check": "responsive",
            "message": "Missing viewport meta tag"
        })

    if not media_queries:
        issues.append({
            "severity": "low",
            "check": "responsive",
            "message": "No @media queries found - email may not be responsive"
        })

    if max_width:
        width_val = int(re.search(r'\d+', max_width).group())
        if width_val > 640:
            issues.append({
                "severity": "low",
                "check": "responsive",
                "message": f"Max-width ({max_width}) exceeds recommended 600-640px"
            })

    return {
        "viewport_meta": viewport_meta,
        "media_queries": media_queries,
        "max_width": max_width,
        "issues": issues
    }


def analyze_dark_mode(soup: BeautifulSoup, html: str) -> Dict[str, Any]:
    """Check dark mode implementation."""
    if not soup:
        return {
            "prefers_color_scheme": False,
            "color_scheme_meta": False,
            "outlook_data_attrs": False,
            "pure_white_bg": False,
            "issues": []
        }

    # Check for prefers-color-scheme media query
    prefers_color_scheme = 'prefers-color-scheme' in html and 'dark' in html

    # Check for color-scheme meta tag or CSS property
    color_scheme_meta = (
        soup.find('meta', attrs={'name': 'color-scheme'}) is not None or
        'color-scheme:' in html
    )

    # Check for Outlook dark mode data attributes
    outlook_data_attrs = '[data-ogsc]' in html or '[data-ogsb]' in html

    # Check for pure white backgrounds
    pure_white_bg = False
    for variant in PURE_WHITE_VARIANTS:
        if variant in html.lower():
            pure_white_bg = True
            break

    issues = []
    if not prefers_color_scheme:
        issues.append({
            "severity": "low",
            "check": "dark_mode",
            "message": "No dark mode support via prefers-color-scheme"
        })

    if pure_white_bg:
        issues.append({
            "severity": "medium",
            "check": "dark_mode",
            "message": "Pure white backgrounds detected - will blind users in dark mode"
        })

    return {
        "prefers_color_scheme": prefers_color_scheme,
        "color_scheme_meta": color_scheme_meta,
        "outlook_data_attrs": outlook_data_attrs,
        "pure_white_bg": pure_white_bg,
        "issues": issues
    }


def analyze_layout(soup: BeautifulSoup, html: str) -> Dict[str, Any]:
    """Analyze email layout structure."""
    if not soup:
        return {
            "table_based": False,
            "css_grid": False,
            "flexbox": False,
            "issues": []
        }

    # Check if table-based layout (good for email)
    tables = soup.find_all('table')
    table_based = len(tables) > 0

    # Check for CSS Grid (bad for email)
    css_grid = 'display:grid' in html or 'display: grid' in html

    # Check for Flexbox (bad for email)
    flexbox = 'display:flex' in html or 'display: flex' in html

    issues = []
    if not table_based:
        issues.append({
            "severity": "high",
            "check": "layout",
            "message": "Not using table-based layout - may break in email clients"
        })

    if css_grid:
        issues.append({
            "severity": "high",
            "check": "layout",
            "message": "CSS Grid detected - not supported in most email clients"
        })

    if flexbox:
        issues.append({
            "severity": "high",
            "check": "layout",
            "message": "Flexbox detected - limited support in email clients"
        })

    return {
        "table_based": table_based,
        "css_grid": css_grid,
        "flexbox": flexbox,
        "issues": issues
    }


def analyze_links(soup: BeautifulSoup, html: str) -> Dict[str, Any]:
    """Analyze links and CTAs."""
    if not soup:
        return {
            "count": 0,
            "has_unsubscribe": False,
            "shorteners_found": False,
            "issues": []
        }

    links = soup.find_all('a')
    link_count = len(links)

    # Check for unsubscribe link
    has_unsubscribe = False
    for link in links:
        href = link.get('href', '').lower()
        text = link.get_text().lower()
        if 'unsubscribe' in href or 'unsubscribe' in text:
            has_unsubscribe = True
            break

    # Check for link shorteners
    shorteners_found = False
    for link in links:
        href = link.get('href', '')
        for shortener in LINK_SHORTENERS:
            if shortener in href:
                shorteners_found = True
                break

    issues = []
    if link_count > 5:
        issues.append({
            "severity": "medium",
            "check": "links",
            "message": f"{link_count} links found - high link count may trigger spam filters"
        })

    if shorteners_found:
        issues.append({
            "severity": "high",
            "check": "links",
            "message": "Link shorteners detected - may trigger spam filters"
        })

    if not has_unsubscribe:
        issues.append({
            "severity": "high",
            "check": "links",
            "message": "No unsubscribe link found - required by CAN-SPAM"
        })

    return {
        "count": link_count,
        "has_unsubscribe": has_unsubscribe,
        "shorteners_found": shorteners_found,
        "issues": issues
    }


def analyze_preheader(soup: BeautifulSoup, html: str) -> Dict[str, Any]:
    """Check for preheader text."""
    if not soup:
        return {"found": False, "length": 0, "issues": []}

    # Look for common preheader patterns
    preheader = None

    # Check for elements with "preheader" in class or id
    for tag in soup.find_all(['div', 'span', 'td']):
        class_list = tag.get('class', [])
        id_attr = tag.get('id', '')

        if 'preheader' in str(class_list).lower() or 'preheader' in id_attr.lower():
            preheader = tag.get_text(strip=True)
            break

    if not preheader:
        # Check for hidden text at the beginning (common preheader pattern)
        body = soup.find('body')
        if body:
            first_element = body.find(['div', 'span'])
            if first_element:
                style = first_element.get('style', '')
                if 'display:none' in style or 'display: none' in style:
                    preheader = first_element.get_text(strip=True)

    length = len(preheader) if preheader else 0

    issues = []
    if not preheader:
        issues.append({
            "severity": "medium",
            "check": "preheader",
            "message": "No preheader text found"
        })
    elif length < 30:
        issues.append({
            "severity": "low",
            "check": "preheader",
            "message": f"Preheader too short ({length} chars) - aim for 30-80 characters"
        })
    elif length > 80:
        issues.append({
            "severity": "low",
            "check": "preheader",
            "message": f"Preheader too long ({length} chars) - will be truncated"
        })

    return {
        "found": preheader is not None,
        "length": length,
        "issues": issues
    }


def analyze_compliance(soup: BeautifulSoup, html: str) -> Dict[str, Any]:
    """Check CAN-SPAM compliance."""
    if not soup:
        return {
            "physical_address": False,
            "unsubscribe": False,
            "sender_id": False,
            "issues": []
        }

    text_content = soup.get_text().lower()

    # Check for physical address (rough heuristic)
    # Look for patterns like street address, city, state, zip
    physical_address = bool(re.search(r'\d+\s+\w+\s+(street|st|avenue|ave|road|rd|drive|dr|lane|ln)', text_content))

    # Check for unsubscribe
    unsubscribe = 'unsubscribe' in text_content

    # Check for sender identification (company name, from address)
    # This is hard to verify automatically, so we'll check if there's a from/sender element
    sender_id = soup.find('meta', attrs={'name': 'from'}) is not None or 'from:' in text_content

    issues = []
    if not physical_address:
        issues.append({
            "severity": "high",
            "check": "compliance",
            "message": "No physical address found - required by CAN-SPAM"
        })

    if not unsubscribe:
        issues.append({
            "severity": "high",
            "check": "compliance",
            "message": "No unsubscribe mechanism found - required by CAN-SPAM"
        })

    return {
        "physical_address": physical_address,
        "unsubscribe": unsubscribe,
        "sender_id": sender_id,
        "issues": issues
    }


def calculate_score(results: Dict[str, Any]) -> int:
    """Calculate overall email quality score (0-100)."""
    score = 100

    # Deduct points for issues
    for category in results.values():
        if isinstance(category, dict) and 'issues' in category:
            for issue in category['issues']:
                severity = issue.get('severity', 'medium')
                if severity == 'high':
                    score -= 15
                elif severity == 'medium':
                    score -= 8
                elif severity == 'low':
                    score -= 3

    return max(0, score)


def format_human_readable(filepath: str, results: Dict) -> str:
    """Format results as human-readable report."""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def status(has_issues: bool, critical: bool = False) -> str:
        if not has_issues:
            return f"{GREEN}✓ PASS{RESET}"
        elif critical:
            return f"{RED}✗ FAIL{RESET}"
        else:
            return f"{YELLOW}⚠ WARN{RESET}"

    output = []
    output.append(f"\n{BOLD}HTML Email Analysis: {filepath}{RESET}")
    output.append(f"\n{BOLD}Overall Score: {results['score']}/100{RESET}")

    # Size
    output.append(f"\n{BOLD}Size:{RESET} {status(results['gmail_clip_risk'])}")
    output.append(f"  File size: {results['size_kb']} KB")
    if results['gmail_clip_critical']:
        output.append(f"  {RED}✗ Exceeds Gmail 102KB limit - will be clipped!{RESET}")
    elif results['gmail_clip_risk']:
        output.append(f"  {YELLOW}⚠ Approaching Gmail 80KB limit{RESET}")

    # Images
    img = results['images']
    output.append(f"\n{BOLD}Images:{RESET} {status(len(img['issues']) > 0)}")
    output.append(f"  Count: {img['count']}")
    output.append(f"  Missing alt text: {img['missing_alt']}")
    output.append(f"  Text/Image ratio: {img['text_image_ratio']}")

    # Responsive
    resp = results['responsive']
    output.append(f"\n{BOLD}Responsive Design:{RESET} {status(len(resp['issues']) > 0)}")
    output.append(f"  Viewport meta: {resp['viewport_meta']}")
    output.append(f"  Media queries: {resp['media_queries']}")
    output.append(f"  Max width: {resp['max_width'] or 'Not set'}")

    # Dark Mode
    dark = results['dark_mode']
    output.append(f"\n{BOLD}Dark Mode:{RESET} {status(len(dark['issues']) > 0)}")
    output.append(f"  Prefers-color-scheme: {dark['prefers_color_scheme']}")
    output.append(f"  Color-scheme meta: {dark['color_scheme_meta']}")
    output.append(f"  Pure white backgrounds: {dark['pure_white_bg']}")

    # Layout
    layout = results['layout']
    output.append(f"\n{BOLD}Layout:{RESET} {status(len(layout['issues']) > 0, layout['css_grid'] or layout['flexbox'])}")
    output.append(f"  Table-based: {layout['table_based']}")
    output.append(f"  CSS Grid: {layout['css_grid']}")
    output.append(f"  Flexbox: {layout['flexbox']}")

    # Links
    links = results['links']
    output.append(f"\n{BOLD}Links:{RESET} {status(len(links['issues']) > 0)}")
    output.append(f"  Count: {links['count']}")
    output.append(f"  Unsubscribe link: {links['has_unsubscribe']}")
    output.append(f"  Link shorteners: {links['shorteners_found']}")

    # Preheader
    pre = results['preheader']
    output.append(f"\n{BOLD}Preheader:{RESET} {status(len(pre['issues']) > 0)}")
    output.append(f"  Found: {pre['found']}")
    if pre['found']:
        output.append(f"  Length: {pre['length']} chars")

    # Compliance
    comp = results['compliance']
    output.append(f"\n{BOLD}CAN-SPAM Compliance:{RESET} {status(len(comp['issues']) > 0, True)}")
    output.append(f"  Physical address: {comp['physical_address']}")
    output.append(f"  Unsubscribe: {comp['unsubscribe']}")

    # All issues
    all_issues = []
    for category in results.values():
        if isinstance(category, dict) and 'issues' in category:
            all_issues.extend(category['issues'])

    if all_issues:
        output.append(f"\n{BOLD}Issues Found:{RESET}")
        for issue in sorted(all_issues, key=lambda x: {'high': 0, 'medium': 1, 'low': 2}[x['severity']]):
            color = RED if issue['severity'] == 'high' else YELLOW if issue['severity'] == 'medium' else ""
            output.append(f"  {color}[{issue['severity'].upper()}]{RESET} {issue['message']}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze HTML email for best practices and deliverability"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to HTML email file"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read HTML from stdin"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed analysis"
    )

    args = parser.parse_args()

    # Read HTML
    if args.stdin:
        html = sys.stdin.read()
        filepath = "<stdin>"
    elif args.file:
        filepath = args.file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
        except FileNotFoundError:
            print(f"ERROR: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    # Parse HTML
    soup = None
    if BeautifulSoup:
        soup = BeautifulSoup(html, PARSER)

    # Run all checks
    size_results = analyze_size(html, filepath)
    image_results = analyze_images(soup, html)
    responsive_results = analyze_responsive(soup, html)
    dark_mode_results = analyze_dark_mode(soup, html)
    layout_results = analyze_layout(soup, html)
    links_results = analyze_links(soup, html)
    preheader_results = analyze_preheader(soup, html)
    compliance_results = analyze_compliance(soup, html)

    # Compile results
    results = {
        "file": filepath,
        "size_bytes": size_results["size_bytes"],
        "size_kb": size_results["size_kb"],
        "gmail_clip_risk": size_results["gmail_clip_risk"],
        "gmail_clip_critical": size_results.get("gmail_clip_critical", False),
        "images": {
            "count": image_results["count"],
            "missing_alt": image_results["missing_alt"],
            "text_image_ratio": image_results["text_image_ratio"]
        },
        "responsive": responsive_results,
        "dark_mode": dark_mode_results,
        "layout": layout_results,
        "links": links_results,
        "preheader": preheader_results,
        "compliance": compliance_results
    }

    # Collect all issues
    all_issues = []
    for category in [size_results, image_results, responsive_results, dark_mode_results,
                     layout_results, links_results, preheader_results, compliance_results]:
        all_issues.extend(category.get("issues", []))

    # Calculate score
    results["score"] = calculate_score(results)
    results["issues"] = all_issues

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_human_readable(filepath, results))

    # Exit code based on critical issues
    critical_count = sum(1 for issue in all_issues if issue['severity'] == 'high')
    if critical_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
