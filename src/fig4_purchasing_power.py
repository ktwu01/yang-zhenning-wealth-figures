"""Figure 4: $20,177 in 1957 → 2025 equivalent under four different deflators.

The horizontal bars span several orders of magnitude, so we use log scale.
The point is that "inflation factor selection is itself a value judgment".
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from style import DATA_DIR, PALETTE, apply_style, save_figure, add_source_note, tr, pick_col


COLORS = [
    PALETTE["accent_blue"],
    PALETTE["accent_orange"],
    PALETTE["accent_green"],
    PALETTE["accent_purple"],
]


def fmt_money(v):
    if v >= 1e6:
        return f"${v/1e6:,.1f}M"
    if v >= 1e3:
        return f"${v/1e3:,.0f}K"
    return f"${v:,.0f}"


def main() -> None:
    apply_style()
    df = pd.read_csv(DATA_DIR / "purchasing_power_1957.csv", comment="#")

    fig, ax = plt.subplots(figsize=(12.5, 6.5))

    y = np.arange(len(df))[::-1]   # display top-down in CSV order
    bars = ax.barh(
        y, df["equiv_2025_usd"], color=COLORS[: len(df)],
        height=0.6, edgecolor="white", linewidth=1.5, alpha=0.9,
    )

    deflator_labels = pick_col(df, "deflator").tolist()
    note_labels = pick_col(df, "notes").tolist()

    # Label inside or after the bar
    for i, row in df.iterrows():
        yi = y[i]
        val = row["equiv_2025_usd"]
        ax.text(val * 1.15, yi,
                f"{fmt_money(val)}  ({row['multiplier']:g}×)",
                va="center", ha="left", fontsize=10,
                color=PALETTE["ink"], fontweight="bold")
        ax.text(val * 1.15, yi - 0.32, note_labels[i],
                va="center", ha="left", fontsize=8,
                color=PALETTE["muted"], style="italic")

    ax.set_yticks(y)
    ax.set_yticklabels(deflator_labels, fontsize=11)
    ax.set_xscale("log")
    ax.set_xlim(1e4, 2e8)
    ax.xaxis.set_major_formatter(FuncFormatter(
        lambda v, _: f"${v/1000:,.0f}K" if v < 1e6 else
                     (f"${v/1e6:,.0f}M" if v < 1e9 else f"${v/1e9:,.1f}B")
    ))
    ax.set_xlabel(tr("折算到 2025 年的等价美元（对数刻度）",
                     "Equivalent 2025 USD (log scale)"))
    ax.set_title(
        tr(
            "1957 年杨振宁分得的 $20,177 诺奖份额：用不同膨胀因子折算到 2025 年",
            "Yang's 1957 Nobel share ($20,177) projected to 2025 under four different deflators",
        ),
        pad=14,
    )

    # Anchor: the original 1957 amount
    ax.axvline(20177, color=PALETTE["ink"], lw=0.8, ls="--", alpha=0.6)
    ax.text(20177 * 0.9, 0.3,
            tr("1957 年原值\n$20,177", "1957 face value\n$20,177"),
            ha="right", va="bottom", fontsize=9,
            color=PALETTE["ink"], style="italic")

    ax.grid(axis="y", visible=False)

    add_source_note(
        fig,
        tr(
            "来源：BLS CPI（1957=28.1，2025≈322）；伦敦金现长期价格；Robert Shiller 标普 500 长期数据；"
            "上海房价指数为定性外推（1990 年代后房地产私有化指数级跃升）。"
            " 不同膨胀因子的选择本身就是一种价值判断。",
            "Sources: BLS CPI (1957=28.1, 2025≈322); London gold long-run price; Robert Shiller's S&P 500 dataset; "
            "Shanghai housing index extrapolated qualitatively from the post-1990 privatization-era curve. "
            "Choice of deflator is itself a value judgment.",
        ),
    )

    save_figure(fig, "fig4_purchasing_power")


if __name__ == "__main__":
    main()
