"""Shared matplotlib styling for the Yang Zhenning wealth figures.

Imports configure global rcParams so individual figure scripts only need
to call `apply_style()` once at the top.
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
OUTPUT_DIR = REPO_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


# Economist / FT-inspired palette, but warmer.
PALETTE = {
    "ink": "#1a1a1a",
    "muted": "#6b6b6b",
    "grid": "#e6e6e6",
    "accent_blue": "#1f4e79",
    "accent_orange": "#d97706",
    "accent_red": "#b91c1c",
    "accent_green": "#15803d",
    "accent_purple": "#6b21a8",
    "fill_blue": "#dbeafe",
    "fill_orange": "#fed7aa",
    "fill_red": "#fecaca",
    "fill_green": "#bbf7d0",
    "fill_purple": "#e9d5ff",
    "bg": "#fafaf7",
}


CN_FONT_CANDIDATES = [
    "Hiragino Sans GB",
    "PingFang HK",
    "PingFang SC",
    "Heiti TC",
    "STHeiti",
    "Source Han Sans SC",
    "Noto Sans CJK SC",
    "Arial Unicode MS",
]


def _pick_cn_font() -> str:
    available = {f.name for f in mpl.font_manager.fontManager.ttflist}
    for name in CN_FONT_CANDIDATES:
        if name in available:
            return name
    return "Arial Unicode MS"


def apply_style() -> None:
    """Apply repo-wide matplotlib styling. Call once per script."""
    cn_font = _pick_cn_font()
    mpl.rcParams.update(
        {
            "font.family": [cn_font, "Helvetica", "Arial", "DejaVu Sans"],
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "axes.edgecolor": PALETTE["ink"],
            "axes.labelcolor": PALETTE["ink"],
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": PALETTE["grid"],
            "grid.linewidth": 0.6,
            "grid.linestyle": "-",
            "xtick.color": PALETTE["ink"],
            "ytick.color": PALETTE["ink"],
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.frameon": False,
            "legend.fontsize": 10,
            "figure.facecolor": PALETTE["bg"],
            "axes.facecolor": PALETTE["bg"],
            "savefig.facecolor": PALETTE["bg"],
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "pdf.fonttype": 42,
            "axes.unicode_minus": False,
        }
    )


def save_figure(fig, stem: str) -> None:
    """Save figure as PNG + SVG into output/."""
    png_path = OUTPUT_DIR / f"{stem}.png"
    svg_path = OUTPUT_DIR / f"{stem}.svg"
    fig.savefig(png_path, dpi=300)
    fig.savefig(svg_path)
    print(f"  wrote {png_path.relative_to(REPO_ROOT)}")
    print(f"  wrote {svg_path.relative_to(REPO_ROOT)}")


def add_source_note(fig, text: str) -> None:
    """Add a small italic source/caveat note at the bottom of the figure."""
    fig.text(
        0.01,
        0.005,
        text,
        ha="left",
        va="bottom",
        fontsize=8,
        color=PALETTE["muted"],
        style="italic",
    )
