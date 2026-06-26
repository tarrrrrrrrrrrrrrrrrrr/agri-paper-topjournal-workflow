from __future__ import annotations

import tempfile
import subprocess
import sys
from pathlib import Path

from audit_data import audit_workbook
from audit_numeric_consistency import audit_numeric_consistency
from plot_significance_bars import plot_significance_bars, read_bar_data


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
REFERENCES = ROOT / "references"


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_balanced_three_replicates() -> None:
    report = audit_workbook(EXAMPLES / "balanced_three_replicates.csv")
    coverage = report["coverage"]
    assert_true(coverage["expected_experimental_units"] == 12, "expected 12 plot units")
    assert_true(coverage["observed_rows"] == 12, "expected 12 observed rows")
    assert_true(coverage["unbalanced_combinations"] == 0, "balanced file should have no unbalanced combinations")
    assert_true(not report["issues"], "balanced file should not raise audit issues")


def test_missing_replicate_is_flagged() -> None:
    report = audit_workbook(EXAMPLES / "missing_replicate.csv")
    codes = {issue["code"] for issue in report["issues"]}
    assert_true("unbalanced_replicates" in codes, "missing replicate should be flagged")
    assert_true(report["coverage"]["unbalanced_combinations"] == 1, "one combination should be unbalanced")


def test_summary_only_table_is_blocker() -> None:
    report = audit_workbook(EXAMPLES / "summary_only_means.csv")
    codes = {issue["code"] for issue in report["issues"]}
    assert_true("missing_replicate_column" in codes, "summary table should lack replicate column")
    assert_true("summary_only_candidate" in codes, "summary table should be flagged")


def test_significance_plot_exports() -> None:
    data = read_bar_data(EXAMPLES / "significance_bar_example.csv")
    with tempfile.TemporaryDirectory() as tmp:
        pdf, png = plot_significance_bars(data, Path(tmp) / "figure_main_effects", ylabel="Mean response")
        assert_true(pdf.exists() and pdf.stat().st_size > 1000, "PDF export should exist")
        assert_true(png.exists() and png.stat().st_size > 1000, "PNG export should exist")


def test_workflow_reference_modules_exist_and_are_clean() -> None:
    required = [
        "manuscript-draft-template.md",
        "results-discussion-framework.md",
        "nature-polishing-flow.md",
        "writing-quality-gate.md",
        "citation-workflow.md",
        "journal-variants.md",
        "mixed-model-python-templates.md",
    ]
    for name in required:
        path = REFERENCES / name
        assert_true(path.exists(), f"missing reference module: {name}")
        text = path.read_text(encoding="utf-8")
        assert_true(len(text.strip()) > 500, f"reference module is too thin: {name}")
    text_files = [
        *ROOT.glob("*.md"),
        *REFERENCES.glob("*.md"),
        *ROOT.glob("evals/*.json"),
        *ROOT.glob("examples/*.csv"),
        *[path for path in ROOT.glob("scripts/*.py") if path.name != "test_agri_skill.py"],
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in text_files)
    for token in ["鍞", "鈹", "脳", "虏", "卤", "鈥", "渭", "掳"]:
        assert_true(token not in combined, f"encoding residue remains: {token}")
    nature_flow = (REFERENCES / "nature-polishing-flow.md").read_text(encoding="utf-8")
    for phrase in [
        "paper type",
        "reader path",
        "hourglass",
        "diagnose the failure mode",
        "claim-evidence-boundary",
        "sentence control",
    ]:
        assert_true(phrase in nature_flow, f"Nature polishing flow missing phrase: {phrase}")


def test_numeric_consistency_audit_detects_missing_claims() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        table = tmp_path / "results.csv"
        manuscript = tmp_path / "draft.md"
        table.write_text("metric,value\nYield,7.2\n2-AP,68.2\n", encoding="utf-8")
        manuscript.write_text("Yield increased to 7.2 t ha-1, while 2-AP reached 60.0 ng g-1.", encoding="utf-8")
        report = audit_numeric_consistency([table], [manuscript], tolerance=0.001)
        codes = {issue["code"] for issue in report["issues"]}
        assert_true("result_value_not_mentioned" in codes, "missing table value should be reported")
        assert_true("manuscript_number_not_in_results" in codes, "unsupported manuscript number should be reported")


def test_writing_lint_gate_detects_bad_and_good_latex() -> None:
    lint = ROOT / "scripts" / "writing_lint.py"
    bad = EXAMPLES / "writing_lint_bad.tex"
    good = EXAMPLES / "writing_lint_good.tex"
    assert_true(lint.exists(), "writing_lint.py should be bundled")
    assert_true(bad.exists(), "bad writing-lint example should exist")
    assert_true(good.exists(), "good writing-lint example should exist")

    bad_run = subprocess.run(
        [sys.executable, "-B", str(lint), str(bad), "--mode", "latex", "--lang", "en", "--quiet"],
        text=True,
        capture_output=True,
    )
    good_run = subprocess.run(
        [sys.executable, "-B", str(lint), str(good), "--mode", "latex", "--lang", "en", "--quiet"],
        text=True,
        capture_output=True,
    )
    assert_true(bad_run.returncode == 2, f"bad LaTeX example should fail, got {bad_run.returncode}: {bad_run.stdout} {bad_run.stderr}")
    assert_true(good_run.returncode == 0, f"good LaTeX example should pass, got {good_run.returncode}: {good_run.stdout} {good_run.stderr}")

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    gate_text = (REFERENCES / "writing-quality-gate.md").read_text(encoding="utf-8")
    for phrase in ["task type", "medium", "target journal", "language direction", "revision conservativeness", "processing scope"]:
        assert_true(phrase in gate_text, f"writing gate missing Stage 0 field: {phrase}")
    for phrase in ["revised text", "back-translation", "change log", "writing_lint.py"]:
        assert_true(phrase in gate_text, f"writing gate missing delivery or lint requirement: {phrase}")
    assert_true("writing-quality-gate.md" in skill_text, "SKILL.md should route manuscript writing through writing-quality-gate.md")


def main() -> None:
    test_balanced_three_replicates()
    test_missing_replicate_is_flagged()
    test_summary_only_table_is_blocker()
    test_significance_plot_exports()
    test_workflow_reference_modules_exist_and_are_clean()
    test_numeric_consistency_audit_detects_missing_claims()
    test_writing_lint_gate_detects_bad_and_good_latex()
    print("agri skill tests passed")


if __name__ == "__main__":
    main()
