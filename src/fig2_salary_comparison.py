"""Figure 2: Academic vs industry vs AI-industry salary ladder (2024 USD).

Horizontal bar chart with three color groups:
  - Academic (blue)
  - Industry biotech/pharma (orange)
  - Industry AI/ML at FAANG-tier (red)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from style import DATA_DIR, PALETTE, apply_style, save_figure, add_source_note


GROUP_COLORS = {
    "academic":    PALETTE["accent_blue"],
    "industry":    PALETTE["accent_orange"],
    "industry_ai": PALETTE["accent_red"],
}
GROUP_LABELS = {
    "academic":    "学术界",
    "industry":    "工业界（生物医药）",
    "industry_ai": "工业界（AI/ML 顶尖）",
}


def fmt_money(v):
    if v >= 1_000_000:
        return f"${v/1_000_000:.1f}M"
    return f"${v/1000:.0f}K"


def main() -> None:
    apply_style()
    df = pd.read_csv(DATA_DIR / "salary_comparison.csv", comment="#")

    # Plot from bottom to top: academic first (low), AI last (high)
    order = ["academic", "industry", "industry_ai"]
    df["__group_order"] = df["group"].map({g: i for i, g in enumerate(order)})
    df = df.sort_values(["__group_order", "low"]).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(12, 7))

    y_positions = np.arange(len(df))
    for i, row in df.iterrows():
        color = GROUP_COLORS[row["group"]]
        ax.barh(
            i,
            row["high"] - row["low"],
            left=row["low"],
            color=color,
            alpha=0.85,
            height=0.62,
            edgecolor="white",
            linewidth=1.2,
        )
        # Range label on the right of each bar
        ax.text(
            row["high"] + (df["high"].max() * 0.012),
            i,
            f"{fmt_money(row['low'])} – {fmt_money(row['high'])}",
            va="center",
            ha="left",
            fontsize=9,
            color=PALETTE["ink"],
        )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(df["role_cn"], fontsize=10)
    ax.set_xscale("log")
    ax.set_xlim(3e4, 5e6)
    ax.xaxis.set_major_formatter(FuncFormatter(
        lambda v, _: f"${v/1000:.0f}K" if v < 1e6 else f"${v/1e6:.0f}M"
    ))
    ax.set_xlabel("年总薪酬（2024 年美元，对数刻度）")
    ax.set_title("学术界、工业界、AI 行业的薪酬梯度（2024 年）", pad=14)
    ax.grid(axis="y", visible=False)

    # Group legend (custom)
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=GROUP_COLORS[g]) for g in order
    ]
    labels = [GROUP_LABELS[g] for g in order]
    ax.legend(handles, labels, loc="lower right", framealpha=0.9)

    # Annotation: Yang's effective Stony Brook chair compensation after inflation
    ax.annotate(
        "杨振宁的石溪 Einstein Professor 席位\n按通胀调整后大致落在该区间",
        xy=(350_000, 4),
        xytext=(280_000, 1.4),
        textcoords="data",
        fontsize=9, color=PALETTE["accent_blue"], style="italic",
        arrowprops=dict(arrowstyle="->", color=PALETTE["accent_blue"], lw=0.7),
    )

    add_source_note(
        fig,
        "来源：NIH 博士后标准 2024；AAUP 2023-24 教职薪酬调查；Stanford 2024 教职薪资报告；Nature 2021 全球科研人员薪资调查；levels.fyi 2024 大厂 RS L6-L7 总包。",
    )

    save_figure(fig, "fig2_salary_comparison")


if __name__ == "__main__":
    main()
