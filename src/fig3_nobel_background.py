"""Figure 3: Nobel laureate socioeconomic background distribution.

Two subplots side by side:
  Left:  parental income percentile distribution
  Right: parental education percentile distribution

In each, we compare laureate share (bars) vs uniform population share (line at 20% per quintile).
Annotated to show "top 5% accounts for ~50-60% of laureates".

Data stylized from Novosad et al. (2024).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from style import DATA_DIR, PALETTE, apply_style, save_figure, add_source_note


def _plot_panel(ax, df_panel, title_cn, accent_color):
    bins = df_panel["bin_label"].tolist()
    laur = df_panel["laureate_share"].to_numpy(dtype=float)
    pop = df_panel["population_share"].to_numpy(dtype=float)

    x = np.arange(len(bins))
    width = 0.4

    ax.bar(x - width / 2, pop, width, color=PALETTE["muted"], alpha=0.55,
           label="一般人口分布", edgecolor="white", linewidth=0.8)
    ax.bar(x + width / 2, laur, width, color=accent_color,
           label="诺奖得主分布", edgecolor="white", linewidth=0.8)

    # Top-5 shading: bins covering P95-P99 and P99-P100
    top5_indices = [i for i, b in enumerate(bins) if b in ("P95-P99", "P99-P100")]
    top5_share = laur[top5_indices].sum()
    if top5_indices:
        ax.axvspan(min(top5_indices) - 0.5, max(top5_indices) + 0.5,
                   color=PALETTE["fill_red"], alpha=0.25, zorder=0)
        ax.text(
            np.mean(top5_indices), max(laur) * 1.05,
            f"前 5%：约 {top5_share:.0f}%\n的诺奖得主出身于此",
            ha="center", va="bottom", fontsize=9,
            color=PALETTE["accent_red"], fontweight="bold",
        )

    ax.set_xticks(x)
    ax.set_xticklabels(bins, fontsize=9, rotation=20)
    ax.set_ylabel("分布占比（%）")
    ax.set_ylim(0, max(laur) * 1.30)
    ax.set_title(title_cn, pad=10)
    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)


def main() -> None:
    apply_style()
    df = pd.read_csv(DATA_DIR / "nobel_socioeconomic.csv", comment="#")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.2))

    df_income = df[df["dimension"] == "income"].reset_index(drop=True)
    df_edu = df[df["dimension"] == "education"].reset_index(drop=True)

    _plot_panel(ax1, df_income, "父辈收入百分位分布", PALETTE["accent_blue"])
    _plot_panel(ax2, df_edu,    "父辈教育水平百分位分布", PALETTE["accent_orange"])

    # Median markers
    ax1.axvline(6.0, color=PALETTE["accent_red"], lw=1.2, ls="--", alpha=0.8)
    ax1.text(6.05, ax1.get_ylim()[1] * 0.45,
             "诺奖得主中位\n第 87 百分位", color=PALETTE["accent_red"],
             fontsize=8.5, ha="left", va="center")
    ax2.axvline(6.3, color=PALETTE["accent_red"], lw=1.2, ls="--", alpha=0.8)
    ax2.text(6.35, ax2.get_ylim()[1] * 0.45,
             "诺奖得主中位\n第 90 百分位", color=PALETTE["accent_red"],
             fontsize=8.5, ha="left", va="center")

    fig.suptitle(
        "诺贝尔奖得主父辈社经背景分布（物理 / 化学 / 医学 / 经济学，1901 – 2023）",
        fontsize=14, fontweight="bold", y=0.995,
    )

    add_source_note(
        fig,
        "数据基于 Novosad, Asher, Farquharson, Iljazi (2024) 对 739 位诺奖得主的研究；分位数边界按百分位标注。"
        " 普通人口分布在每个分位段近似均匀分布（20%/20%/20%/20%/10%/5%/4%/1%）。",
    )

    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    save_figure(fig, "fig3_nobel_background")


if __name__ == "__main__":
    main()
