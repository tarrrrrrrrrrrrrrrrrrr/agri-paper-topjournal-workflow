from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_PALETTE = [
    "#274753",
    "#297270",
    "#299D8F",
    "#8AB07C",
    "#E7C66B",
    "#F3A361",
    "#E66D50",
]


def _load_pyplot():
    try:
        import matplotlib as mpl
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "matplotlib is required. Install it with: python -m pip install matplotlib"
        ) from exc

    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "font.size": 8,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.facecolor": "white",
        }
    )
    return plt


def read_bar_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    required = {"label", "mean", "error", "letter"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    data = data.copy()
    if "block" not in data.columns:
        data["block"] = ""
    data["block"] = data["block"].fillna("").astype(str)
    data["label"] = data["label"].astype(str)
    data["letter"] = data["letter"].fillna("").astype(str).str.strip()
    data["mean"] = pd.to_numeric(data["mean"], errors="raise")
    data["error"] = pd.to_numeric(data["error"], errors="raise")

    if not np.isfinite(data[["mean", "error"]].to_numpy()).all():
        raise ValueError("Mean and error values must be finite.")
    if (data["error"] < 0).any():
        raise ValueError("Error values cannot be negative.")
    if (data["letter"] == "").any():
        raise ValueError(
            "Every bar must have a model-supported compact-letter label; "
            "use a separate non-significance plot when letters are unavailable."
        )

    if "order" in data.columns:
        data["order"] = pd.to_numeric(data["order"], errors="raise")
        data = data.sort_values(["block", "order"], kind="stable")
    return data.reset_index(drop=True)


def _x_layout(
    data: pd.DataFrame, block_gap: float
) -> tuple[np.ndarray, list[tuple[str, float, float]]]:
    positions: list[float] = []
    blocks: list[tuple[str, float, float]] = []
    cursor = 0.0
    for block, part in data.groupby("block", sort=False):
        start = cursor
        for _ in range(len(part)):
            positions.append(cursor)
            cursor += 1.0
        end = cursor - 1.0
        blocks.append((block, start, end))
        cursor += block_gap
    return np.asarray(positions), blocks


def plot_significance_bars(
    data: pd.DataFrame,
    output_base: Path,
    *,
    ylabel: str,
    palette: list[str] | None = None,
    width_mm: float = 89,
    height_mm: float = 72,
    block_gap: float = 1.1,
    show_values: bool = False,
    panel_label: str | None = None,
) -> tuple[Path, Path]:
    plt = _load_pyplot()
    palette = palette or DEFAULT_PALETTE
    x, blocks = _x_layout(data, block_gap)
    if "color" in data.columns:
        colors = data["color"].fillna("").tolist()
    else:
        colors = [palette[i % len(palette)] for i in range(len(data))]
    colors = [c if c else palette[i % len(palette)] for i, c in enumerate(colors)]

    fig, ax = plt.subplots(figsize=(width_mm / 25.4, height_mm / 25.4))
    bars = ax.bar(
        x,
        data["mean"],
        yerr=data["error"],
        width=0.72,
        color=colors,
        edgecolor="black",
        linewidth=0.85,
        error_kw={
            "ecolor": "black",
            "elinewidth": 0.85,
            "capsize": 3,
            "capthick": 0.85,
        },
        zorder=2,
    )

    top = (data["mean"] + data["error"]).to_numpy()
    bottom = min(0.0, float((data["mean"] - data["error"]).min()))
    span = max(float(top.max() - bottom), abs(float(top.max())) * 0.2, 1e-9)
    letter_pad = span * 0.045
    value_pad = span * 0.012

    for bar, mean, error, letter in zip(
        bars, data["mean"], data["error"], data["letter"], strict=True
    ):
        center = bar.get_x() + bar.get_width() / 2
        ax.text(
            center,
            mean + error + letter_pad,
            letter,
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            clip_on=False,
        )
        if show_values:
            ax.text(
                center,
                mean + value_pad,
                f"{mean:.3g}",
                ha="center",
                va="bottom",
                fontsize=7,
                color="#333333",
            )

    ax.set_ylabel(ylabel)
    ax.set_xticks(x, data["label"])
    ax.tick_params(direction="out", length=3, width=0.8)
    ax.set_ylim(bottom, float(top.max() + span * 0.16))
    ax.grid(False)

    visible_blocks = [(name, start, end) for name, start, end in blocks if name]
    for idx, (name, start, end) in enumerate(visible_blocks):
        center = (start + end) / 2
        ax.text(
            center,
            -0.18,
            name,
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="top",
            fontsize=8,
        )
        if idx < len(visible_blocks) - 1:
            next_start = visible_blocks[idx + 1][1]
            ax.axvline(
                (end + next_start) / 2,
                color="#B8B8B8",
                lw=0.7,
                ls="--",
                zorder=0,
            )

    if panel_label:
        ax.text(
            -0.12,
            1.03,
            panel_label,
            transform=ax.transAxes,
            fontsize=10,
            fontweight="bold",
            ha="left",
            va="bottom",
        )

    fig.subplots_adjust(
        left=0.18,
        right=0.98,
        top=0.92,
        bottom=0.27 if visible_blocks else 0.20,
    )
    output_base = output_base.resolve()
    output_base.parent.mkdir(parents=True, exist_ok=True)
    pdf_path = output_base.with_suffix(".pdf")
    png_path = output_base.with_suffix(".png")
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, dpi=600, bbox_inches="tight")
    plt.close(fig)
    return pdf_path, png_path


def parse_palette(value: str | None) -> list[str] | None:
    if not value:
        return None
    colors = [item.strip() for item in value.split(",") if item.strip()]
    if not colors:
        raise ValueError("Palette must contain at least one color.")
    return colors


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Draw journal-ready significance bars from a validated summary CSV. "
            "Required columns: label, mean, error, letter. Optional: block, order, color."
        )
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-base", required=True, type=Path)
    parser.add_argument("--ylabel", required=True)
    parser.add_argument("--palette", help="Comma-separated hexadecimal colors.")
    parser.add_argument("--width-mm", type=float, default=89)
    parser.add_argument("--height-mm", type=float, default=72)
    parser.add_argument("--block-gap", type=float, default=1.1)
    parser.add_argument("--show-values", action="store_true")
    parser.add_argument("--panel-label")
    args = parser.parse_args()

    data = read_bar_data(args.input)
    pdf_path, png_path = plot_significance_bars(
        data,
        args.output_base,
        ylabel=args.ylabel,
        palette=parse_palette(args.palette),
        width_mm=args.width_mm,
        height_mm=args.height_mm,
        block_gap=args.block_gap,
        show_values=args.show_values,
        panel_label=args.panel_label,
    )
    print(pdf_path)
    print(png_path)


if __name__ == "__main__":
    main()
