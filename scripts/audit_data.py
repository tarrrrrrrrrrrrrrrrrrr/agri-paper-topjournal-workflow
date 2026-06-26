from __future__ import annotations

import argparse
import math
from itertools import product
from pathlib import Path

import pandas as pd

try:
    from scripts.common import write_csv, write_json
except ModuleNotFoundError:
    from common import write_csv, write_json


FACTOR_ALIASES = {
    "season": ("season", "year", "年份", "季节"),
    "cultivar": ("cultivar", "variety", "genotype", "material", "品种", "品系", "材料", "栽培模式"),
    "treatment": ("treatment", "shade", "shading", "nitrogen", "light", "处理", "遮光", "氮素", "光质"),
    "replicate": ("replicate", "rep", "block", "重复", "区组"),
}

SUMMARY_COLUMN_HINTS = ("mean", "se", "sem", "sd", "ci", "letter", "lsmean", "emmean", "平均", "显著")


def normalize(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_")


def infer_column(columns: list[str], aliases: tuple[str, ...]) -> str | None:
    normalized = {normalize(c): c for c in columns}
    for alias in aliases:
        target = normalize(alias)
        if target in normalized:
            return normalized[target]
    return None


def clean_level(value: object) -> object:
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def read_frames(path: Path) -> dict[str, pd.DataFrame]:
    if path.suffix.lower() in {".csv", ".tsv"}:
        return {path.stem: pd.read_csv(path, sep="\t" if path.suffix.lower() == ".tsv" else ",")}
    with pd.ExcelFile(path) as book:
        return {name: pd.read_excel(book, sheet_name=name) for name in book.sheet_names}


def build_replicate_balance(data: pd.DataFrame, factor_columns: list[str], replicate_column: str | None) -> list[dict]:
    if not factor_columns or not replicate_column or replicate_column not in data.columns:
        return []

    observed_reps = sorted(clean_level(x) for x in data[replicate_column].dropna().unique().tolist())
    levels = [sorted(data[col].dropna().unique().tolist()) for col in factor_columns]
    rows = []

    for combo in product(*levels):
        mask = pd.Series(True, index=data.index)
        for col, value in zip(factor_columns, combo, strict=True):
            mask &= data[col] == value
        part = data.loc[mask]
        present = sorted(clean_level(x) for x in part[replicate_column].dropna().unique().tolist())
        missing = [rep for rep in observed_reps if rep not in present]
        duplicate_count = int(part.duplicated(subset=factor_columns + [replicate_column]).sum())
        row = {col: value for col, value in zip(factor_columns, combo, strict=True)}
        row.update(
            {
                "observed_units": int(part.shape[0]),
                "unique_replicates": len(present),
                "expected_replicates": len(observed_reps),
                "present_replicates": ";".join(map(str, present)),
                "missing_replicates": ";".join(map(str, missing)),
                "duplicate_replicate_rows": duplicate_count,
                "status": "ok" if len(missing) == 0 and duplicate_count == 0 and int(part.shape[0]) == len(observed_reps) else "check",
            }
        )
        rows.append(row)

    return rows


def audit_workbook(path: Path, factor_columns: list[str] | None = None, replicate_column: str | None = None) -> dict:
    path = path.resolve()
    frames = read_frames(path)
    inventory = [
        {
            "sheet": name,
            "rows": int(frame.shape[0]),
            "columns": int(frame.shape[1]),
            "summary_only_candidate": bool(frame.shape[0] <= 10),
        }
        for name, frame in frames.items()
    ]

    data_name, data = max(frames.items(), key=lambda item: item[1].shape[0] * max(item[1].shape[1], 1))
    columns = [str(c) for c in data.columns]
    if factor_columns is None:
        factor_columns = [c for key in ("season", "cultivar", "treatment") if (c := infer_column(columns, FACTOR_ALIASES[key]))]
    if replicate_column is None:
        replicate_column = infer_column(columns, FACTOR_ALIASES["replicate"])

    issues = []
    missingness = {str(c): int(data[c].isna().sum()) for c in data.columns}
    duplicate_count = int(data.duplicated().sum())
    factor_levels = {c: sorted(data[c].dropna().astype(str).unique().tolist()) for c in factor_columns if c in data.columns}
    replicate_levels = []
    if replicate_column and replicate_column in data.columns:
        replicate_levels = sorted(clean_level(x) for x in data[replicate_column].dropna().unique().tolist())

    expected_combinations = math.prod(len(v) for v in factor_levels.values()) if factor_levels else 0
    expected_units = expected_combinations * len(replicate_levels) if replicate_levels else expected_combinations
    observed_combinations = int(data[factor_columns].drop_duplicates().shape[0]) if factor_columns else 0
    balance = build_replicate_balance(data, factor_columns, replicate_column)
    unbalanced = [row for row in balance if row["status"] != "ok"]

    if not factor_columns:
        issues.append({"code": "missing_factor_columns", "message": "No treatment, cultivar, season or equivalent factor columns were inferred."})
    if not replicate_column:
        issues.append({"code": "missing_replicate_column", "message": "No plot/block/replicate column was inferred; inferential statistics cannot be checked from means alone."})
    if len(frames) == 1 and data.shape[0] <= 10 and not replicate_column:
        issues.append({"code": "summary_only_candidate", "message": "The primary table is small and lacks replicate identifiers; it may contain treatment summaries rather than raw experimental units."})
    summary_like_columns = [c for c in columns if any(hint in normalize(c) for hint in SUMMARY_COLUMN_HINTS)]
    if summary_like_columns and not replicate_column:
        issues.append({"code": "summary_statistics_without_units", "message": f"Summary-statistic columns without raw replicate identifiers: {summary_like_columns}"})
    if unbalanced:
        issues.append({"code": "unbalanced_replicates", "message": f"{len(unbalanced)} factor combination(s) have missing, duplicated or unexpected replicate rows."})

    numeric = data.select_dtypes(include="number")
    numeric_summary = []
    for col in numeric.columns:
        series = numeric[col].dropna()
        numeric_summary.append(
            {
                "variable": str(col),
                "n": int(series.size),
                "min": float(series.min()) if len(series) else None,
                "max": float(series.max()) if len(series) else None,
                "mean": float(series.mean()) if len(series) else None,
            }
        )

    variables = [
        {"original_name": str(c), "normalized_name": normalize(c), "dtype": str(data[c].dtype), "missing": missingness[str(c)]}
        for c in data.columns
    ]

    return {
        "input": str(path),
        "primary_sheet": data_name,
        "sheets": inventory,
        "design": {
            "factor_columns": factor_columns,
            "factor_levels": factor_levels,
            "replicate_column": replicate_column,
            "replicate_levels": replicate_levels,
        },
        "duplicates": {"exact_rows": duplicate_count},
        "missingness": missingness,
        "coverage": {
            "expected_combinations": expected_combinations,
            "observed_combinations": observed_combinations,
            "expected_experimental_units": expected_units,
            "observed_rows": int(data.shape[0]),
            "unbalanced_combinations": len(unbalanced),
        },
        "replicate_balance": balance,
        "issues": issues,
        "variables": variables,
        "numeric_summary": numeric_summary,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit agricultural spreadsheet structure and replicate balance.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--factors", nargs="*")
    parser.add_argument("--replicate")
    args = parser.parse_args()

    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = audit_workbook(Path(args.input), args.factors, args.replicate)
    write_json(output / "data_audit.json", report)
    write_csv(output / "sheet_inventory.csv", report["sheets"], ["sheet", "rows", "columns", "summary_only_candidate"])
    write_csv(output / "variable_dictionary.csv", report["variables"], ["original_name", "normalized_name", "dtype", "missing"])
    write_csv(output / "missingness.csv", [{"variable": k, "missing": v} for k, v in report["missingness"].items()], ["variable", "missing"])
    write_csv(output / "design_coverage.csv", [report["coverage"]], list(report["coverage"].keys()))
    balance_fields = list(report["replicate_balance"][0].keys()) if report["replicate_balance"] else ["status"]
    write_csv(output / "replicate_balance.csv", report["replicate_balance"], balance_fields)
    write_csv(output / "data_issues.csv", report["issues"], ["code", "message"])
    print(output)


if __name__ == "__main__":
    main()
