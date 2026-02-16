#!/usr/bin/env python3
"""
Email Deliverability Checker

Analyzes DNS records (SPF, DKIM, DMARC, MX) to assess email deliverability health.
Uses DNS lookups via subprocess and provides a comprehensive health score.

Usage:
    python check_deliverability.py example.com
    python check_deliverability.py example.com --json
    python check_deliverability.py example.com --verbose
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Any


# Common DKIM selectors to check
COMMON_DKIM_SELECTORS = [
    "google", "default", "selector1", "selector2", "k1",
    "mandrill", "dkim", "s1", "s2", "mail", "email"
]

# MX hostname patterns to identify mail providers
MX_PROVIDER_PATTERNS = {
    "aspmx.l.google.com": "Google Workspace",
    "googlemail.com": "Google Workspace",
    "mail.protection.outlook.com": "Microsoft 365",
    "pphosted.com": "Proofpoint",
    "mimecast.com": "Mimecast",
    "messagelabs.com": "Symantec",
}


def run_dig_command(query: str, record_type: str = "TXT") -> List[str]:
    """
    Execute dig command and return cleaned results.

    Args:
        query: DNS query string
        record_type: DNS record type (TXT, MX, etc.)

    Returns:
        List of result strings
    """
    try:
        cmd = ["dig", "+short", record_type.lower(), query]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return []

        # Clean and filter results
        lines = [line.strip().strip('"') for line in result.stdout.strip().split('\n')]
        return [line for line in lines if line]

    except subprocess.TimeoutExpired:
        return []
    except FileNotFoundError:
        print("ERROR: 'dig' command not found. Please install dnsutils package.", file=sys.stderr)
        sys.exit(1)
    except Exception:
        return []


def check_spf(domain: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Check SPF record for domain.

    Returns:
        Dict with SPF analysis results
    """
    results = run_dig_command(domain, "TXT")
    spf_record = None

    # Find SPF record
    for record in results:
        if record.startswith("v=spf1"):
            spf_record = record
            break

    if not spf_record:
        return {
            "valid": False,
            "record": None,
            "enforcement": None,
            "lookup_count": 0,
            "issues": ["No SPF record found"]
        }

    # Determine enforcement level
    enforcement = "none"
    if spf_record.endswith("-all"):
        enforcement = "hard_fail"
    elif spf_record.endswith("~all"):
        enforcement = "soft_fail"
    elif spf_record.endswith("?all"):
        enforcement = "neutral"
    elif spf_record.endswith("+all"):
        enforcement = "pass_all"  # Very bad practice

    # Count DNS lookups (include, a, mx, redirect mechanisms)
    lookup_count = (
        spf_record.count("include:") +
        spf_record.count("a:") +
        spf_record.count("mx:") +
        spf_record.count("redirect=")
    )

    # Check for "a" or "mx" without colon (counts current domain)
    if " a " in f" {spf_record} " or spf_record.startswith("a "):
        lookup_count += 1
    if " mx " in f" {spf_record} " or spf_record.startswith("mx "):
        lookup_count += 1

    issues = []
    if lookup_count > 10:
        issues.append(f"SPF lookup count ({lookup_count}) exceeds limit of 10")
    if enforcement in ["neutral", "pass_all"]:
        issues.append(f"Weak enforcement level: {enforcement}")

    if verbose:
        print(f"  SPF Record: {spf_record}")
        print(f"  Enforcement: {enforcement}")
        print(f"  DNS Lookups: {lookup_count}")

    return {
        "valid": True,
        "record": spf_record,
        "enforcement": enforcement,
        "lookup_count": lookup_count,
        "issues": issues
    }


def check_dkim(domain: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Check DKIM records for common selectors.

    Returns:
        Dict with DKIM analysis results
    """
    found_selectors = []

    for selector in COMMON_DKIM_SELECTORS:
        query = f"{selector}._domainkey.{domain}"
        results = run_dig_command(query, "TXT")

        for record in results:
            if "v=DKIM1" in record or "k=rsa" in record or "p=" in record:
                found_selectors.append(selector)
                if verbose:
                    print(f"  DKIM Selector '{selector}' found")
                break

    issues = []
    if not found_selectors:
        issues.append("No DKIM records found for common selectors")
    elif len(found_selectors) == 1:
        issues.append("Only one DKIM selector found - consider adding backup")

    return {
        "found": len(found_selectors) > 0,
        "selectors": found_selectors,
        "issues": issues
    }


def check_dmarc(domain: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Check DMARC record for domain.

    Returns:
        Dict with DMARC analysis results
    """
    query = f"_dmarc.{domain}"
    results = run_dig_command(query, "TXT")
    dmarc_record = None

    # Find DMARC record
    for record in results:
        if record.startswith("v=DMARC1"):
            dmarc_record = record
            break

    if not dmarc_record:
        return {
            "valid": False,
            "policy": None,
            "reporting": False,
            "rua": None,
            "ruf": None,
            "issues": ["No DMARC record found"]
        }

    # Parse DMARC tags
    tags = {}
    for part in dmarc_record.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            tags[key.strip()] = value.strip()

    policy = tags.get("p", "none")
    rua = tags.get("rua")
    ruf = tags.get("ruf")
    reporting = bool(rua or ruf)

    issues = []
    if policy == "none":
        issues.append("DMARC policy is 'none' - no enforcement")
    if not reporting:
        issues.append("No DMARC reporting configured (rua/ruf)")

    if verbose:
        print(f"  DMARC Record: {dmarc_record}")
        print(f"  Policy: {policy}")
        if rua:
            print(f"  Aggregate Reports: {rua}")
        if ruf:
            print(f"  Forensic Reports: {ruf}")

    return {
        "valid": True,
        "policy": policy,
        "reporting": reporting,
        "rua": rua,
        "ruf": ruf,
        "issues": issues
    }


def check_mx(domain: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Check MX records for domain.

    Returns:
        Dict with MX analysis results
    """
    results = run_dig_command(domain, "MX")

    if not results:
        return {
            "valid": False,
            "records": [],
            "provider": None,
            "issues": ["No MX records found"]
        }

    # Parse MX records
    mx_records = []
    provider = None

    for record in results:
        parts = record.split()
        if len(parts) >= 2:
            try:
                priority = int(parts[0])
                host = parts[1].rstrip(".")
                mx_records.append({"priority": priority, "host": host})

                # Detect provider
                if not provider:
                    for pattern, provider_name in MX_PROVIDER_PATTERNS.items():
                        if pattern in host:
                            provider = provider_name
                            break
            except ValueError:
                continue

    # Sort by priority
    mx_records.sort(key=lambda x: x["priority"])

    issues = []
    if len(mx_records) == 1:
        issues.append("Only one MX record - consider adding backup")

    if verbose:
        print(f"  MX Records: {len(mx_records)}")
        for mx in mx_records:
            print(f"    Priority {mx['priority']}: {mx['host']}")
        if provider:
            print(f"  Detected Provider: {provider}")

    return {
        "valid": True,
        "records": mx_records,
        "provider": provider,
        "issues": issues
    }


def calculate_health_score(spf: Dict, dkim: Dict, dmarc: Dict, mx: Dict) -> int:
    """
    Calculate DNS-only deliverability health score (0-100).

    This is a partial score covering DNS-accessible components only.
    The full Email Health Score (from email-audit sub-skill) includes
    blacklist, TLS, and compliance checks via subagents.

    Weights aligned with main SKILL.md source of truth:
        - SPF: 0-10 points (10% of full score)
        - DKIM: 0-15 points (15% of full score)
        - DMARC: 0-15 points (15% of full score)
        - MX: 0-10 points (10% of full score)
    Total: 50 points max, scaled to 100
    """
    score = 0

    # SPF scoring (10% of full score)
    if spf["valid"]:
        if spf["enforcement"] == "hard_fail":
            score += 10
        elif spf["enforcement"] == "soft_fail":
            score += 7
        else:
            score += 3

    # DKIM scoring (15% of full score)
    if dkim["found"]:
        score += 15

    # DMARC scoring (15% of full score)
    if dmarc["valid"]:
        policy = dmarc["policy"]
        if policy == "reject":
            score += 15
        elif policy == "quarantine":
            score += 11
        elif policy == "none":
            score += 5

    # MX scoring (10% of full score)
    if mx["valid"]:
        score += 10

    # Scale to 0-100
    return int((score / 50) * 100)


def format_human_readable(domain: str, results: Dict) -> str:
    """
    Format results as human-readable report with ANSI colors.
    """
    # ANSI color codes
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def status(valid: bool, issues: List[str]) -> str:
        if valid and not issues:
            return f"{GREEN}✓ PASS{RESET}"
        elif valid and issues:
            return f"{YELLOW}⚠ WARN{RESET}"
        else:
            return f"{RED}✗ FAIL{RESET}"

    output = []
    output.append(f"\n{BOLD}Email Deliverability Report: {domain}{RESET}")
    output.append(f"Timestamp: {results['timestamp']}")
    output.append(f"\n{BOLD}Health Score: {results['health_score']}/100{RESET}")

    # Color code the score
    score = results['health_score']
    if score >= 80:
        score_color = GREEN
    elif score >= 60:
        score_color = YELLOW
    else:
        score_color = RED
    output[-1] = f"\n{BOLD}Health Score: {score_color}{score}/100{RESET}"

    # SPF
    output.append(f"\n{BOLD}SPF Record:{RESET} {status(results['spf']['valid'], results['spf']['issues'])}")
    if results['spf']['valid']:
        output.append(f"  Record: {results['spf']['record']}")
        output.append(f"  Enforcement: {results['spf']['enforcement']}")
        output.append(f"  DNS Lookups: {results['spf']['lookup_count']}/10")
    for issue in results['spf']['issues']:
        output.append(f"  {YELLOW}⚠{RESET} {issue}")

    # DKIM
    output.append(f"\n{BOLD}DKIM:{RESET} {status(results['dkim']['found'], results['dkim']['issues'])}")
    if results['dkim']['found']:
        output.append(f"  Selectors: {', '.join(results['dkim']['selectors'])}")
    for issue in results['dkim']['issues']:
        output.append(f"  {YELLOW}⚠{RESET} {issue}")

    # DMARC
    output.append(f"\n{BOLD}DMARC:{RESET} {status(results['dmarc']['valid'], results['dmarc']['issues'])}")
    if results['dmarc']['valid']:
        output.append(f"  Policy: {results['dmarc']['policy']}")
        if results['dmarc']['rua']:
            output.append(f"  Reporting (rua): {results['dmarc']['rua']}")
        if results['dmarc']['ruf']:
            output.append(f"  Reporting (ruf): {results['dmarc']['ruf']}")
    for issue in results['dmarc']['issues']:
        output.append(f"  {YELLOW}⚠{RESET} {issue}")

    # MX
    output.append(f"\n{BOLD}MX Records:{RESET} {status(results['mx']['valid'], results['mx']['issues'])}")
    if results['mx']['valid']:
        for record in results['mx']['records']:
            output.append(f"  Priority {record['priority']}: {record['host']}")
        if results['mx']['provider']:
            output.append(f"  Provider: {results['mx']['provider']}")
    for issue in results['mx']['issues']:
        output.append(f"  {YELLOW}⚠{RESET} {issue}")

    # Overall issues
    if results['issues']:
        output.append(f"\n{BOLD}Critical Issues:{RESET}")
        for issue in results['issues']:
            severity_color = RED if issue['severity'] == 'high' else YELLOW
            output.append(f"  {severity_color}[{issue['severity'].upper()}]{RESET} {issue['check']}: {issue['message']}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Check email deliverability health via DNS records"
    )
    parser.add_argument(
        "domain",
        help="Domain to check (e.g., example.com)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed progress"
    )

    args = parser.parse_args()
    domain = args.domain.lower().strip()

    if args.verbose and not args.json:
        print(f"Checking deliverability for: {domain}\n")

    # Run all checks
    if args.verbose and not args.json:
        print("Checking SPF...")
    spf_results = check_spf(domain, args.verbose and not args.json)

    if args.verbose and not args.json:
        print("\nChecking DKIM...")
    dkim_results = check_dkim(domain, args.verbose and not args.json)

    if args.verbose and not args.json:
        print("\nChecking DMARC...")
    dmarc_results = check_dmarc(domain, args.verbose and not args.json)

    if args.verbose and not args.json:
        print("\nChecking MX records...")
    mx_results = check_mx(domain, args.verbose and not args.json)

    # Calculate health score
    health_score = calculate_health_score(spf_results, dkim_results, dmarc_results, mx_results)

    # Collect critical issues
    critical_issues = []
    for check_name, check_results in [("spf", spf_results), ("dkim", dkim_results),
                                       ("dmarc", dmarc_results), ("mx", mx_results)]:
        for issue in check_results.get("issues", []):
            # Determine severity
            severity = "medium"
            if "No" in issue and "found" in issue:
                severity = "high"
            elif check_name == "dkim" and "Only one" in issue:
                severity = "low"

            critical_issues.append({
                "severity": severity,
                "check": check_name,
                "message": issue
            })

    # Build final results
    results = {
        "domain": domain,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "health_score": health_score,
        "spf": spf_results,
        "dkim": dkim_results,
        "dmarc": dmarc_results,
        "mx": mx_results,
        "issues": critical_issues
    }

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_human_readable(domain, results))

    # Exit code based on health score
    if health_score < 60:
        sys.exit(1)


if __name__ == "__main__":
    main()
