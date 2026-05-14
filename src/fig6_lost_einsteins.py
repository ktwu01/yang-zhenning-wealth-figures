"""Figure 6: Lost Einsteins — inventor rate vs parental income percentile.

Recreates the central plot from Bell, Chetty, Jaravel, Petkova, Van Reenen (2019),
"Who Becomes an Inventor in America?" (QJE).

Two series:
  - Raw rate (all children)
  - Conditional on top-quintile 3rd-grade math (showing gap persists)

Highlights:
  - 10x gap between top 1% and median
  - Yang Zhenning's position annotated (top 0.1% in 1930s China)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from style import DATA_DIR, PALETTE, apply_style, save_figure, add_source_note, tr


def main() -> None:
    apply_style()
    df = pd.read_csv(DATA_DIR / "chetty_inventor_rates.csv", comment="#")

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.plot(
        df["parental_income_percentile"], df["inventors_per_1000_raw"],
        marker="o", color=PALETTE["accent_blue"], lw=2.2, markersize=7,
        label=tr("所有儿童", "All children"),
    )
    ax.plot(
        df["parental_income_percentile"], df["inventors_per_1000_top_math"],
        marker="s", color=PALETTE["accent_orange"], lw=2.0, markersize=7, ls="--",
        label=tr("三年级数学测试前 20% 的儿童",
                 "Children in top 20% of 3rd-grade math scores"),
    )

    # Highlight 10x gap: median (~50th) vs top 1% (99th)
    median_rate = float(df.loc[df["parental_income_percentile"] == 55,
                               "inventors_per_1000_raw"].iloc[0])
    top1_rate   = float(df.loc[df["parental_income_percentile"] == 99,
                               "inventors_per_1000_raw"].iloc[0])
    ratio = top1_rate / median_rate

    ax.axhline(median_rate, color=PALETTE["muted"], lw=0.7, ls=":")
    ax.axhline(top1_rate,   color=PALETTE["accent_red"], lw=0.7, ls=":")
    ax.annotate(
        "",
        xy=(102, top1_rate), xytext=(102, median_rate),
        arrowprops=dict(arrowstyle="<->", color=PALETTE["accent_red"], lw=1.2),
        annotation_clip=False,
    )
    ax.text(
        103, (median_rate + top1_rate) / 2,
        tr(f"约 {ratio:.0f} 倍差距", f"~{ratio:.0f}× gap"),
        va="center", ha="left",
        fontsize=11, color=PALETTE["accent_red"], fontweight="bold",
    )

    # Yang Zhenning marker: at the extreme right (top 0.1%, ~99.9 percentile)
    yang_x = 99.5
    yang_y = 13.5  # extrapolated
    ax.scatter([yang_x], [yang_y], marker="*", s=400,
               color=PALETTE["accent_red"], edgecolors="white", linewidths=1.5,
               zorder=6)
    ax.annotate(
        tr(
            "杨振宁（1922 年合肥出生）\n清华教授之子，约处中国前 0.1%",
            "Chen Ning Yang (born 1922, Hefei)\nson of a Tsinghua professor, ~top 0.1% of China",
        ),
        xy=(yang_x, yang_y), xytext=(70, 16),
        textcoords="data",
        fontsize=10, color=PALETTE["accent_red"], fontweight="bold",
        ha="left", va="center",
        arrowprops=dict(arrowstyle="->", color=PALETTE["accent_red"], lw=0.9),
    )

    ax.set_xlim(0, 105)
    ax.set_ylim(0, 22)
    ax.set_xlabel(tr("父母收入百分位", "Parental income percentile"))
    ax.set_ylabel(tr("每 1,000 名儿童中成为发明者的人数",
                     "Inventors per 1,000 children"))
    ax.set_title(
        tr(
            '"Lost Einsteins"：父母收入百分位 vs 子代成为发明者的概率',
            '"Lost Einsteins": inventor rate by parental income percentile',
        ),
        pad=14,
    )

    ax.legend(loc="upper left", framealpha=0.9)

    # Sub-annotation: even after controlling for math ability
    ax.annotate(
        tr(
            "即使控制了三年级数学测试成绩\n富裕家庭孩子的发明者率仍显著更高",
            "Even controlling for 3rd-grade math scores,\nchildren of wealthy families still invent at a much higher rate",
        ),
        xy=(85, df["inventors_per_1000_top_math"].iloc[-3]),
        xytext=(30, 10.5),
        textcoords="data",
        fontsize=9.5, color=PALETTE["accent_orange"], style="italic",
        ha="left", va="center",
        arrowprops=dict(arrowstyle="->", color=PALETTE["accent_orange"], lw=0.7),
    )

    add_source_note(
        fig,
        tr(
            "数据基于 Bell, Chetty, Jaravel, Petkova, Van Reenen (2019), Who Becomes an Inventor in America?, QJE。"
            " Chetty 团队估算：仅美国一国，每年约 6 万名「潜在发明家」因出生在错误的邮政编码而未提出第一份专利。",
            "Data: Bell, Chetty, Jaravel, Petkova, Van Reenen (2019), Who Becomes an Inventor in America?, QJE. "
            "Chetty et al. estimate that in the US alone roughly 60,000 \"lost Einsteins\" per year never file a first patent "
            "because they were born in the wrong zip code.",
        ),
    )

    save_figure(fig, "fig6_lost_einsteins")


if __name__ == "__main__":
    main()
