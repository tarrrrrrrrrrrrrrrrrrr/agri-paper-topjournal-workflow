from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


FAIL = "FAIL"
WARN = "WARN"
INFO = "INFO"

AI_WORDS_EN = {
    "crucial",
    "delve",
    "delves",
    "groundbreaking",
    "landscape",
    "leverage",
    "leverages",
    "myriad",
    "pivotal",
    "robust",
    "showcase",
    "showcasing",
    "underscore",
    "underscores",
    "underscoring",
    "unprecedented",
}

AI_PHRASES_EN = [
    r"in\s+the\s+(?:ever[- ]evolving|rapidly\s+evolving)\s+landscape",
    r"it\s+is\s+worth\s+noting\s+that",
    r"paving\s+the\s+way\s+for",
    r"plays?\s+an?\s+(?:crucial|pivotal|vital|important)\s+role",
    r"not\s+only\b.{1,80}\bbut\s+also",
]

MECH_CONNECTIVES_EN = {
    "moreover",
    "furthermore",
    "additionally",
    "notably",
    "importantly",
    "consequently",
}

AI_WORDS_ZH = [
    "值得注意的是",
    "毋庸置疑",
    "众所周知",
    "具有重要意义",
    "提供理论依据",
    "奠定基础",
    "赋能",
]


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    line: int = 0
    count: int = 1
    examples: list[str] = field(default_factory=list)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8", errors="replace")


def split_sentences(text: str, lang: str) -> list[str]:
    if lang == "zh":
        parts = re.split(r"(?<=[。！？；])", text)
    else:
        protected = re.sub(r"\b(e\.g|i\.e|et al|Fig|Eq|vs)\.", r"\1<DOT>", text)
        parts = re.split(r"(?<=[.!?])\s+", protected)
        parts = [part.replace("<DOT>", ".") for part in parts]
    return [part.strip() for part in parts if part.strip()]


def word_count(sentence: str, lang: str) -> int:
    if lang == "zh":
        return len(re.findall(r"[\u4e00-\u9fff]", sentence)) + len(re.findall(r"[A-Za-z]+", sentence))
    return len(re.findall(r"[A-Za-z][A-Za-z'-]*", sentence))


def check_latex(text: str) -> list[Issue]:
    issues: list[Issue] = []
    for char, label in [("%", r"\%"), ("&", r"\&"), ("#", r"\#")]:
        matches = [m for m in re.finditer(re.escape(char), text) if m.start() == 0 or text[m.start() - 1] != "\\"]
        if matches:
            issues.append(
                Issue(
                    FAIL,
                    "LATEX_UNESCAPED",
                    f"Unescaped '{char}' x{len(matches)}; use '{label}' outside math.",
                    line=line_of(text, matches[0].start()),
                    count=len(matches),
                )
            )
    if text.count("$") % 2:
        issues.append(Issue(FAIL, "LATEX_UNBALANCED_MATH", "Unbalanced '$' math delimiter.", count=1))
    if re.search(r"\*\*[^*]+\*\*|(?<!\w)__[^_]+__", text):
        issues.append(Issue(FAIL, "LATEX_MARKDOWN_RESIDUE", "Markdown bold markers found in LaTeX text.", count=1))
    return issues


def check_word_markdown(text: str, lang: str) -> list[Issue]:
    issues: list[Issue] = []
    markdown_hits = list(re.finditer(r"\*\*[^*]+\*\*|(?<!\w)__[^_]+__|^\s{0,3}#{1,6}\s", text, re.MULTILINE))
    if markdown_hits:
        issues.append(
            Issue(
                FAIL,
                "WORD_MARKDOWN_RESIDUE",
                "Markdown markup remains in Word/plain manuscript text.",
                line=line_of(text, markdown_hits[0].start()),
                count=len(markdown_hits),
            )
        )
    if lang == "zh":
        half_width = list(re.finditer(r"[\u4e00-\u9fff][,;:!?][\u4e00-\u9fff]", text))
        if half_width:
            issues.append(
                Issue(
                    WARN,
                    "ZH_HALF_WIDTH_PUNCT",
                    "Half-width punctuation appears between Chinese characters.",
                    line=line_of(text, half_width[0].start()),
                    count=len(half_width),
                )
            )
    return issues


def check_ai_tells(text: str, lang: str) -> list[Issue]:
    issues: list[Issue] = []
    if lang == "en":
        lower = text.lower()
        for word in sorted(AI_WORDS_EN):
            matches = re.findall(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", lower)
            if matches:
                issues.append(Issue(WARN, "AI_WORD", f"Possible AI-tell word: '{word}' x{len(matches)}.", count=len(matches), examples=[word]))
        for pattern in AI_PHRASES_EN:
            matches = list(re.finditer(pattern, lower))
            if matches:
                issues.append(Issue(WARN, "AI_PHRASE", f"Template-like phrase x{len(matches)}: {pattern}", line=line_of(text, matches[0].start()), count=len(matches)))
        sentences = split_sentences(text, lang)
        starts = []
        for sentence in sentences:
            first = re.match(r"\s*([A-Za-z]+)", sentence)
            if first and first.group(1).lower() in MECH_CONNECTIVES_EN:
                starts.append(first.group(1))
        if len(starts) >= 3:
            issues.append(Issue(WARN, "MECHANICAL_CONNECTIVES", f"Mechanical connective overuse x{len(starts)}.", count=len(starts), examples=starts[:5]))
        ing_hits = list(re.finditer(r",\s+(?:highlighting|showcasing|underscoring|demonstrating)\b", lower))
        if ing_hits:
            issues.append(Issue(WARN, "DANGLING_ING", f"Superficial comma-ing ending x{len(ing_hits)}.", line=line_of(text, ing_hits[0].start()), count=len(ing_hits)))
    else:
        for word in AI_WORDS_ZH:
            count = text.count(word)
            if count:
                issues.append(Issue(WARN, "AI_WORD_ZH", f"Possible Chinese AI-tell phrase: '{word}' x{count}.", count=count, examples=[word]))
    return issues


def check_style_stats(text: str, lang: str) -> list[Issue]:
    issues: list[Issue] = []
    sentences = split_sentences(text, lang)
    if not sentences:
        return issues
    lengths = [word_count(sentence, lang) for sentence in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((length - mean) ** 2 for length in lengths) / len(lengths)
    sd = variance ** 0.5
    cv = sd / mean if mean else 0.0
    issues.append(Issue(INFO, "SENTENCE_LENGTH", f"Sentence length mean={mean:.1f}, sd={sd:.1f}, cv={cv:.2f}, min={min(lengths)}, max={max(lengths)}."))
    if lang == "en" and cv < 0.25 and len(sentences) >= 4:
        issues.append(Issue(WARN, "MONOTONE_RHYTHM", "Sentence lengths are unusually uniform; check for mechanical rhythm."))
    if lang == "en":
        passive = re.findall(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(?:\w+ed|shown|found|given|taken|seen|known|made|built)\b", text, flags=re.I)
        ratio = len(passive) / len(sentences)
        issues.append(Issue(INFO, "PASSIVE_RATIO", f"Approximate passive structures: {len(passive)} / {len(sentences)} sentences ({ratio:.0%})."))
        if ratio > 0.45:
            issues.append(Issue(WARN, "HIGH_PASSIVE_RATIO", "Passive voice ratio is high; check whether agency is hidden."))
    return issues


def lint_text(text: str, mode: str, lang: str) -> dict:
    issues: list[Issue] = []
    if mode == "latex":
        issues.extend(check_latex(text))
    if mode in {"word", "docx", "plain"}:
        issues.extend(check_word_markdown(text, lang))
    issues.extend(check_ai_tells(text, lang))
    issues.extend(check_style_stats(text, lang))
    fail = sum(1 for issue in issues if issue.severity == FAIL)
    warn = sum(1 for issue in issues if issue.severity == WARN)
    info = sum(1 for issue in issues if issue.severity == INFO)
    verdict = FAIL if fail else WARN if warn else "PASS"
    return {
        "summary": {"verdict": verdict, "fail": fail, "warn": warn, "info": info, "total": len(issues)},
        "mode": mode,
        "lang": lang,
        "issues": [asdict(issue) for issue in issues],
    }


def print_report(report: dict, quiet: bool) -> None:
    summary = report["summary"]
    if quiet:
        print(f"{summary['verdict']} (FAIL {summary['fail']} / WARN {summary['warn']} / INFO {summary['info']})")
        return
    print(f"==== writing_lint (mode={report['mode']}, lang={report['lang']}) ====")
    for issue in report["issues"]:
        print(f"[{issue['severity']}] {issue['code']}: {issue['message']}")
    print(f"---- {summary['verdict']} (FAIL {summary['fail']} / WARN {summary['warn']} / INFO {summary['info']}) ----")


def main() -> None:
    parser = argparse.ArgumentParser(description="Agricultural manuscript writing-quality linter.")
    parser.add_argument("path", help="Text path, or '-' for stdin.")
    parser.add_argument("--mode", choices=["latex", "word", "docx", "markdown", "plain"], default="plain")
    parser.add_argument("--lang", choices=["en", "zh"], default="en")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    text = read_input(args.path)
    report = lint_text(text, args.mode, args.lang)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print_report(report, args.quiet)
    summary = report["summary"]
    raise SystemExit(2 if summary["fail"] else 1 if summary["warn"] else 0)


if __name__ == "__main__":
    main()
