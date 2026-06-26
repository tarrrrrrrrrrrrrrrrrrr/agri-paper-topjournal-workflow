from __future__ import annotations

import argparse
import csv
import html
import re
from pathlib import Path
from zipfile import ZipFile

try:
    from scripts.common import write_csv, write_json
except ModuleNotFoundError:
    from common import write_csv, write_json


NUMBER_RE = re.compile(r"(?<![-A-Za-z])[-+]?\d+(?:\.\d+)?(?![-A-Za-z])")


def extract_docx_text(path: Path) -> str:
    chunks = []
    with ZipFile(path) as zf:
        bad = zf.testzip()
        if bad:
            raise ValueError(f"Corrupt DOCX member: {bad}")
        for name in zf.namelist():
            if name.startswith("word/") and name.endswith(".xml"):
                xml = zf.read(name).decode("utf-8", errors="ignore")
                xml = re.sub(r"</w:p>", "\n", xml)
                chunks.append(html.unescape(re.sub(r"<[^>]+>", " ", xml)))
    return "\n".join(chunks)


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return extract_docx_text(path)
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_numbers_from_text(text: str) -> set[float]:
    values = set()
    for match in NUMBER_RE.finditer(text):
        try:
            values.add(float(match.group(0)))
        except ValueError:
            continue
    return values


def extract_csv_numbers(path: Path) -> list[dict]:
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row_index, row in enumerate(reader, start=2):
            label = row.get("metric") or row.get("response") or row.get("variable") or row.get("trait") or ""
            for column, raw in row.items():
                if raw is None:
                    continue
                value = str(raw).strip()
                if not value or not NUMBER_RE.fullmatch(value):
                    continue
                rows.append({"source": str(path), "row": row_index, "column": column, "label": label, "value": float(value)})
    return rows


def has_close_value(value: float, candidates: set[float], tolerance: float) -> bool:
    return any(abs(value - candidate) <= tolerance for candidate in candidates)


def audit_numeric_consistency(result_tables: list[Path], manuscript_files: list[Path], tolerance: float = 0.001) -> dict:
    result_values = []
    for table in result_tables:
        result_values.extend(extract_csv_numbers(table))

    manuscript_numbers: set[float] = set()
    for manuscript in manuscript_files:
        manuscript_numbers.update(extract_numbers_from_text(read_text(manuscript)))

    result_number_set = {item["value"] for item in result_values}
    issues = []

    for item in result_values:
        if not has_close_value(item["value"], manuscript_numbers, tolerance):
            issues.append(
                {
                    "code": "result_value_not_mentioned",
                    "source": item["source"],
                    "row": item["row"],
                    "column": item["column"],
                    "value": item["value"],
                    "message": "A numeric result value is not mentioned in the manuscript files.",
                }
            )

    for value in sorted(manuscript_numbers):
        if not has_close_value(value, result_number_set, tolerance):
            issues.append(
                {
                    "code": "manuscript_number_not_in_results",
                    "source": "",
                    "row": "",
                    "column": "",
                    "value": value,
                    "message": "A manuscript number was not found in the supplied result tables.",
                }
            )

    return {
        "result_tables": [str(path) for path in result_tables],
        "manuscript_files": [str(path) for path in manuscript_files],
        "tolerance": tolerance,
        "result_value_count": len(result_values),
        "manuscript_number_count": len(manuscript_numbers),
        "issues": issues,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit numeric consistency between result CSV tables and manuscript text/DOCX files.")
    parser.add_argument("--results", nargs="+", required=True, type=Path)
    parser.add_argument("--manuscripts", nargs="+", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--tolerance", type=float, default=0.001)
    args = parser.parse_args()

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = audit_numeric_consistency(args.results, args.manuscripts, args.tolerance)
    write_json(output / "numeric_consistency_audit.json", report)
    write_csv(
        output / "numeric_consistency_issues.csv",
        report["issues"],
        ["code", "source", "row", "column", "value", "message"],
    )
    print(output)


if __name__ == "__main__":
    main()
