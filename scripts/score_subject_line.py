#!/usr/bin/env python3
"""
Subject Line Scorer

Analyzes email subject lines and provides a deliverability/engagement score.
Checks length, spam triggers, formatting, power words, personalization, and engagement.

Usage:
    python score_subject_line.py "Your subject line here"
    python score_subject_line.py "Your subject line here" --json
    python score_subject_line.py --batch subjects.txt
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Tuple, Any


# Spam trigger words/phrases (case-insensitive)
SPAM_TRIGGERS = [
    "free", "act now", "limited time", "guaranteed", "no obligation",
    "winner", "congratulations", "urgent", "click here", "buy now",
    "order now", "don't delete", "not spam", "as seen on", "double your",
    "earn money", "no cost", "risk free", "satisfaction guaranteed",
    "call now", "order today", "what are you waiting for", "supplies are limited",
    "while supplies last", "exclusive deal", "promise you", "this isn't spam",
    "dear friend", "for instant access", "get it now", "get started now"
]

# Power words (positive engagement)
POWER_WORDS = [
    "new", "exclusive", "proven", "secret", "discover", "unlock",
    "essential", "breakthrough", "insider", "limited", "instant", "save",
    "transform", "boost", "master", "ultimate", "complete", "guide",
    "strategy", "tips", "hacks", "results", "effective", "powerful",
    "simple", "easy", "fast", "quick", "step-by-step"
]

# Merge tag patterns
MERGE_TAG_PATTERNS = [
    r'\{first_name\}', r'\{\{name\}\}', r'\{name\}', r'\{\{first_name\}\}',
    r'\{email\}', r'\{\{email\}\}', r'\[first_name\]', r'\[name\]'
]


def count_words_and_chars(subject: str) -> Tuple[int, int]:
    """Count words and characters in subject line."""
    words = subject.split()
    word_count = len(words)
    char_count = len(subject)
    return word_count, char_count


def calculate_length_score(word_count: int, char_count: int) -> Tuple[int, str]:
    """
    Calculate length score (0-30 points).

    Optimal: 6-10 words AND 30-50 characters = 30 points
    Good: 4-5 or 11-12 words = 20 points
    Acceptable: 3 or 13-15 words = 10 points
    Poor: <3 or >15 words = 0 points
    """
    score = 0
    note = ""

    if 6 <= word_count <= 10 and 30 <= char_count <= 50:
        score = 30
        note = "Optimal length"
    elif 6 <= word_count <= 10:
        score = 25
        note = "Good word count, but character count could be optimized"
    elif 30 <= char_count <= 50:
        score = 25
        note = "Good character count, but word count could be optimized"
    elif 4 <= word_count <= 5 or 11 <= word_count <= 12:
        score = 20
        note = f"{word_count} words - slightly {'short' if word_count < 6 else 'long'}"
    elif word_count == 3 or 13 <= word_count <= 15:
        score = 10
        note = f"{word_count} words - too {'short' if word_count < 6 else 'long'}"
    else:
        score = 0
        note = f"{word_count} words - {'very short' if word_count < 3 else 'way too long'}"

    return score, note


def check_spam_triggers(subject: str) -> Tuple[int, List[str]]:
    """
    Check for spam trigger words.
    Returns: (penalty, list of triggers found)

    -5 points per trigger, max -25
    """
    subject_lower = subject.lower()
    triggers_found = []

    for trigger in SPAM_TRIGGERS:
        # Special case for "free" - only flag if it's emphasized
        if trigger == "free":
            if re.search(r'\bFREE\b', subject) or 'free!' in subject_lower:
                triggers_found.append(trigger)
        elif trigger in subject_lower:
            triggers_found.append(trigger)

    penalty = max(len(triggers_found) * -5, -25)
    return penalty, triggers_found


def check_formatting(subject: str) -> Tuple[int, List[str]]:
    """
    Check formatting issues.
    Returns: (penalty, list of issues)

    - ALL CAPS (entire subject): -15
    - Excessive exclamation marks (2+): -10 per extra
    - Excessive question marks (2+): -5
    - Multiple emoji (3+): -5
    """
    penalty = 0
    issues = []

    # Check for ALL CAPS (ignore merge tags and common acronyms)
    text_without_tags = re.sub(r'\{[^}]+\}|\[[^\]]+\]', '', subject)
    if text_without_tags.isupper() and len(text_without_tags) > 5:
        penalty -= 15
        issues.append("ALL CAPS detected")

    # Check exclamation marks
    exclamation_count = subject.count('!')
    if exclamation_count >= 2:
        penalty -= (exclamation_count - 1) * 10
        issues.append(f"{exclamation_count} exclamation marks - excessive")

    # Check question marks
    question_count = subject.count('?')
    if question_count >= 2:
        penalty -= 5
        issues.append(f"{question_count} question marks - excessive")

    # Check emoji (rough heuristic - non-ASCII characters)
    emoji_count = sum(1 for char in subject if ord(char) > 127)
    if emoji_count >= 3:
        penalty -= 5
        issues.append(f"Multiple emoji detected ({emoji_count})")

    return penalty, issues


def check_power_words(subject: str) -> Tuple[int, List[str]]:
    """
    Check for power words.
    Returns: (bonus, list of power words found)

    +3 points per word, max +15
    """
    subject_lower = subject.lower()
    words_found = []

    for word in POWER_WORDS:
        if re.search(rf'\b{word}\b', subject_lower):
            words_found.append(word)

    bonus = min(len(words_found) * 3, 15)
    return bonus, words_found


def check_personalization(subject: str) -> Tuple[int, List[str]]:
    """
    Check for personalization.
    Returns: (bonus, list of features)

    - Merge tags: +10
    - Numbers/statistics: +5
    """
    bonus = 0
    features = []

    # Check for merge tags
    has_merge_tags = any(re.search(pattern, subject) for pattern in MERGE_TAG_PATTERNS)
    if has_merge_tags:
        bonus += 10
        features.append("merge tags")

    # Check for numbers (statistics are engaging)
    if re.search(r'\b\d+\b', subject):
        bonus += 5
        features.append("numbers/statistics")

    return bonus, features


def check_engagement(subject: str) -> Tuple[int, List[str]]:
    """
    Check for engagement techniques.
    Returns: (bonus, list of features)

    - Starts with question: +5
    - Contains colon (Topic: Detail): +3
    - Contains brackets [Like This]: +3
    """
    bonus = 0
    features = []

    # Starts with question
    if subject.strip().startswith(('How', 'What', 'Why', 'When', 'Where', 'Who', 'Which')):
        bonus += 5
        features.append("starts with question")

    # Contains colon
    if ':' in subject and not subject.endswith(':'):
        bonus += 3
        features.append("colon format")

    # Contains brackets
    if '[' in subject and ']' in subject:
        bonus += 3
        features.append("brackets")

    return bonus, features


def generate_recommendations(breakdown: Dict[str, Any], subject: str) -> List[str]:
    """Generate actionable recommendations based on analysis."""
    recommendations = []
    word_count = breakdown['length']['word_count']
    char_count = breakdown['length']['char_count']

    # Length recommendations
    if word_count < 6:
        recommendations.append(f"Add {6 - word_count}-{10 - word_count} more words for optimal length (6-10 words)")
    elif word_count > 10:
        recommendations.append(f"Remove {word_count - 10} words to reach optimal length (6-10 words)")

    if char_count < 30:
        recommendations.append(f"Consider adding more detail to reach 30-50 characters")
    elif char_count > 50:
        recommendations.append(f"Consider shortening to 30-50 characters for better mobile display")

    # Spam triggers
    if breakdown['spam_triggers']['triggers_found']:
        recommendations.append(f"Remove spam triggers: {', '.join(breakdown['spam_triggers']['triggers_found'])}")

    # Formatting
    if breakdown['formatting']['issues']:
        recommendations.append("Fix formatting issues to avoid spam filters")

    # Power words
    if not breakdown['power_words']['words_found']:
        recommendations.append("Add power words to increase engagement (e.g., 'new', 'exclusive', 'proven')")

    # Personalization
    if not breakdown['personalization']['has_merge_tags']:
        recommendations.append("Consider adding personalization with merge tags like {first_name}")

    # Engagement
    if not breakdown['engagement']['features']:
        recommendations.append("Try starting with a question to boost curiosity")

    return recommendations[:5]  # Limit to top 5


def generate_alternatives(subject: str) -> List[str]:
    """Generate 3 alternative subject line suggestions."""
    # Extract any existing merge tags
    merge_tag = None
    for pattern in MERGE_TAG_PATTERNS:
        match = re.search(pattern, subject)
        if match:
            merge_tag = match.group(0)
            break

    # Extract topic from subject (use core nouns, skip common words)
    skip_words = {
        'the', 'a', 'an', 'your', 'our', 'my', 'this', 'that', 'these',
        'how', 'why', 'what', 'when', 'where', 'is', 'are', 'was', 'were',
        'to', 'for', 'in', 'on', 'at', 'of', 'and', 'or', 'but', 'not',
        'do', "don't", 'get', 'here', "here's", 'new', 'top', 'best',
        'discover', 'unlock', 'boost', 'master', 'proven', 'secret',
        'personalized', 'exclusive', 'limited', 'amazing', 'incredible',
        'ultimate', 'free', 'guaranteed', 'instantly', 'urgent', 'important',
    }
    words = subject.split()
    topic_words = []
    for word in words:
        clean = word.strip('[](){}:,!?."\'').lower()
        if clean not in skip_words and len(clean) > 2 and not clean.isdigit():
            topic_words.append(word.strip('[](){}:,!?."\''))
            if len(topic_words) >= 2:
                break
    topic = ' '.join(topic_words) if topic_words else "Email"

    alternatives = [
        f"Your {topic} Guide: What Top Businesses Know",
        f"Stop Guessing: A Proven {topic} Framework",
        f"{merge_tag or '{first_name}'}, Your {topic} Roadmap Is Ready"
    ]

    return alternatives


def score_subject_line(subject: str) -> Dict[str, Any]:
    """
    Score a subject line and provide breakdown.

    Base score: 50
    Length: 0-30
    Spam triggers: -25 to 0
    Formatting: -X to 0
    Power words: 0-15
    Personalization: 0-15
    Engagement: 0-5

    Final: Clamped to 0-100
    """
    word_count, char_count = count_words_and_chars(subject)

    # Calculate components
    length_score, length_note = calculate_length_score(word_count, char_count)
    spam_penalty, spam_triggers_found = check_spam_triggers(subject)
    format_penalty, format_issues = check_formatting(subject)
    power_bonus, power_words_found = check_power_words(subject)
    personal_bonus, personal_features = check_personalization(subject)
    engagement_bonus, engagement_features = check_engagement(subject)

    # Calculate final score
    base_score = 50
    final_score = (
        base_score +
        length_score +
        spam_penalty +
        format_penalty +
        power_bonus +
        personal_bonus +
        engagement_bonus
    )
    final_score = max(0, min(100, final_score))

    # Build breakdown
    breakdown = {
        "length": {
            "score": length_score,
            "note": length_note,
            "word_count": word_count,
            "char_count": char_count
        },
        "spam_triggers": {
            "score": spam_penalty,
            "triggers_found": spam_triggers_found
        },
        "formatting": {
            "score": format_penalty,
            "issues": format_issues
        },
        "power_words": {
            "score": power_bonus,
            "words_found": power_words_found
        },
        "personalization": {
            "score": personal_bonus,
            "has_merge_tags": "merge tags" in personal_features,
            "features": personal_features
        },
        "engagement": {
            "score": engagement_bonus,
            "features": engagement_features
        }
    }

    recommendations = generate_recommendations(breakdown, subject)
    alternatives = generate_alternatives(subject)

    return {
        "subject": subject,
        "score": final_score,
        "word_count": word_count,
        "char_count": char_count,
        "breakdown": breakdown,
        "recommendations": recommendations,
        "alternatives": alternatives
    }


def format_human_readable(result: Dict[str, Any]) -> str:
    """Format result as human-readable scorecard."""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    score = result['score']
    if score >= 80:
        score_color = GREEN
        grade = "A"
    elif score >= 70:
        score_color = GREEN
        grade = "B"
    elif score >= 60:
        score_color = YELLOW
        grade = "C"
    elif score >= 50:
        score_color = YELLOW
        grade = "D"
    else:
        score_color = RED
        grade = "F"

    output = []
    output.append(f"\n{BOLD}Subject Line Scorecard{RESET}")
    output.append(f"\nSubject: \"{result['subject']}\"")
    output.append(f"\n{BOLD}Score: {score_color}{score}/100 (Grade: {grade}){RESET}")
    output.append(f"Length: {result['word_count']} words, {result['char_count']} characters")

    # Breakdown
    output.append(f"\n{BOLD}Breakdown:{RESET}")
    bd = result['breakdown']

    # Length
    length_score = bd['length']['score']
    length_color = GREEN if length_score >= 25 else YELLOW if length_score >= 15 else RED
    output.append(f"  Length: {length_color}{length_score}/30{RESET} - {bd['length']['note']}")

    # Spam triggers
    spam_score = bd['spam_triggers']['score']
    if spam_score < 0:
        output.append(f"  Spam Triggers: {RED}{spam_score}{RESET} - Found: {', '.join(bd['spam_triggers']['triggers_found'])}")
    else:
        output.append(f"  Spam Triggers: {GREEN}0{RESET} - None detected")

    # Formatting
    format_score = bd['formatting']['score']
    if format_score < 0:
        output.append(f"  Formatting: {RED}{format_score}{RESET} - Issues: {', '.join(bd['formatting']['issues'])}")
    else:
        output.append(f"  Formatting: {GREEN}0{RESET} - No issues")

    # Power words
    power_score = bd['power_words']['score']
    power_color = GREEN if power_score >= 9 else YELLOW
    if bd['power_words']['words_found']:
        output.append(f"  Power Words: {power_color}+{power_score}{RESET} - Found: {', '.join(bd['power_words']['words_found'])}")
    else:
        output.append(f"  Power Words: {YELLOW}0{RESET} - None found")

    # Personalization
    personal_score = bd['personalization']['score']
    personal_color = GREEN if personal_score >= 10 else YELLOW
    if bd['personalization']['features']:
        output.append(f"  Personalization: {personal_color}+{personal_score}{RESET} - Has: {', '.join(bd['personalization']['features'])}")
    else:
        output.append(f"  Personalization: {YELLOW}0{RESET} - No personalization")

    # Engagement
    engagement_score = bd['engagement']['score']
    engagement_color = GREEN if engagement_score >= 5 else YELLOW
    if bd['engagement']['features']:
        output.append(f"  Engagement: {engagement_color}+{engagement_score}{RESET} - Uses: {', '.join(bd['engagement']['features'])}")
    else:
        output.append(f"  Engagement: {YELLOW}0{RESET} - No engagement techniques")

    # Recommendations
    if result['recommendations']:
        output.append(f"\n{BOLD}Recommendations:{RESET}")
        for i, rec in enumerate(result['recommendations'], 1):
            output.append(f"  {i}. {rec}")

    # Alternatives
    output.append(f"\n{BOLD}Alternative Suggestions:{RESET}")
    for i, alt in enumerate(result['alternatives'], 1):
        output.append(f"  {i}. \"{alt}\"")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Score email subject lines for deliverability and engagement"
    )
    parser.add_argument(
        "subject",
        nargs="?",
        help="Subject line to score"
    )
    parser.add_argument(
        "--batch",
        help="File with one subject line per line"
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

    # Batch mode
    if args.batch:
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                subjects = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"ERROR: File not found: {args.batch}", file=sys.stderr)
            sys.exit(1)

        results = [score_subject_line(subject) for subject in subjects]

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for i, result in enumerate(results, 1):
                print(f"\n{'='*60}")
                print(f"Subject Line #{i}")
                print('='*60)
                print(format_human_readable(result))

    # Single subject mode
    elif args.subject:
        result = score_subject_line(args.subject)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_human_readable(result))

        # Exit code based on score
        if result['score'] < 60:
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
