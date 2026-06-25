from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from PIL import Image


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "plot_significance_bars.py"
SPEC = importlib.util.spec_from_file_location("plot_significance_bars", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SignificanceBarTests(unittest.TestCase):
    def test_rejects_missing_letters(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "bad.csv"
            pd.DataFrame(
                {"label": ["A"], "mean": [1.0], "error": [0.1], "letter": [""]}
            ).to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "compact-letter"):
                MODULE.read_bar_data(path)

    def test_exports_pdf_and_600_dpi_png(self):
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            data = pd.DataFrame(
                {
                    "block": ["Factor A", "Factor A", "Factor B", "Factor B"],
                    "label": ["A1", "A2", "B1", "B2"],
                    "mean": [1.0, 1.4, 0.9, 1.2],
                    "error": [0.10, 0.12, 0.08, 0.09],
                    "letter": ["b", "a", "b", "a"],
                }
            )
            pdf, png = MODULE.plot_significance_bars(
                data,
                temp_path / "figure",
                ylabel="Response",
                width_mm=89,
                height_mm=72,
            )
            self.assertTrue(pdf.exists())
            self.assertTrue(png.exists())
            self.assertGreater(pdf.stat().st_size, 1000)
            with Image.open(png) as image:
                self.assertGreaterEqual(image.info["dpi"][0], 599)
                self.assertGreater(image.width, 1000)


if __name__ == "__main__":
    unittest.main()
