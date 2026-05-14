"""Figure 1: Yang Zhenning estimated wealth trajectory, 1922-2025.

This is a counterfactual reconstruction, not a measurement.
We model three regimes:
  - lower (conservative): Stony Brook salary savings + Nobel principal at 8% CAGR
  - middle  (baseline):    same + S&P 500 total return ~10.3% CAGR
  - upper  (optimistic):  same + 10.5% CAGR and later prize money invested

Each scenario is a piecewise-compound curve with key events as deposits.
Values are in 2025 USD (no further inflation adjustment after deposit year).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, LogLocator

from style import (
    DATA_DIR,
    PALETTE,
    apply_style,
    save_figure,
    add_source_note,
    tr,
)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

# CPI inflation 1957 -> 2025 ≈ 11.5x; CPI 1948 -> 2025 ≈ 13.3x; CPI 1966 -> 2025 ≈ 9.7x.
# We deposit each cashflow as 2025-USD-equivalent, then grow it forward at the
# scenario CAGR. This abstracts away which year the dollar was actually earned.

# Cashflow deposits: (year, amount_in_2025_USD, label)
DEPOSITS = [
    (1948, 8_000,    "博士起薪（约同当代博士后年存款）"),
    (1957, 230_000,  "诺贝尔奖金（CPI 调整后）"),
    (1966, 60_000,   "石溪起始年储蓄"),
    (1975, 120_000,  "石溪中期年储蓄峰值"),
    (1985, 180_000,  "石溪后期年储蓄"),
    (1994, 250_000,  "鲍威尔奖"),
    (2001, 200_000,  "费萨尔国王奖"),
]

# Net annual savings flow during Stony Brook 1966-1999 (per year, 2025 USD).
# Kept modest because Yang was known to live frugally and donate.
ANNUAL_SAVINGS_1966_1999 = 40_000

# Withdrawals: large charitable gifts in 2025 USD.
WITHDRAWALS = [
    (2003, -4_000_000, "捐清华建高研院"),
    (2008, -75_000,    "汶川地震捐款"),
]

YEAR_START = 1922
YEAR_END = 2025


def simulate(cagr: float) -> np.ndarray:
    years = np.arange(YEAR_START, YEAR_END + 1)
    wealth = np.zeros_like(years, dtype=float)

    for i, yr in enumerate(years):
        prev = wealth[i - 1] if i > 0 else 0.0
        # Compound from previous year
        cur = prev * (1 + cagr)
        # Apply lump-sum deposits
        for d_yr, d_amt, _ in DEPOSITS:
            if d_yr == yr:
                cur += d_amt
        # Apply annual Stony Brook savings flow
        if 1966 <= yr <= 1999:
            cur += ANNUAL_SAVINGS_1966_1999
        # Apply withdrawals
        for w_yr, w_amt, _ in WITHDRAWALS:
            if w_yr == yr:
                cur += w_amt  # w_amt is negative
        wealth[i] = max(cur, 1.0)  # floor at $1 to keep log scale sane

    return years, wealth


def main() -> None:
    apply_style()

    events = pd.read_csv(DATA_DIR / "yang_wealth_timeline.csv", comment="#")

    years, w_low = simulate(0.080)
    _,     w_mid = simulate(0.100)
    _,     w_hi  = simulate(0.105)

    fig, ax = plt.subplots(figsize=(13, 7.2))

    # Shaded band between low and high
    ax.fill_between(years, w_low, w_hi, color=PALETTE["fill_blue"], alpha=0.55,
                    label=tr("估算区间（8% 至 10.5% 年化）",
                            "Estimated range (8% to 10.5% CAGR)"))
    ax.plot(years, w_mid, color=PALETTE["accent_blue"], lw=2.4,
            label=tr("中位估算（10% 年化复合增长）",
                     "Median scenario (10% CAGR)"))
    ax.plot(years, w_low, color=PALETTE["accent_blue"], lw=0.9, ls="--", alpha=0.7)
    ax.plot(years, w_hi,  color=PALETTE["accent_blue"], lw=0.9, ls="--", alpha=0.7)

    # Event markers
    kind_color = {
        "birth":   PALETTE["muted"],
        "milestone": PALETTE["accent_orange"],
        "prize":   PALETTE["accent_red"],
        "death":   PALETTE["ink"],
    }
    for _, row in events.iterrows():
        yr = int(row["year"])
        col = kind_color.get(row["kind"], PALETTE["muted"])
        ax.axvline(yr, color=col, lw=0.6, alpha=0.45, ls=":")
        # Find the wealth value at that year for annotation
        idx = np.searchsorted(years, yr)
        if 0 <= idx < len(years):
            y_val = w_mid[idx]
            ax.scatter([yr], [y_val], color=col, s=28, zorder=5,
                       edgecolor="white", linewidth=0.8)

    # Manual label placement (avoid auto-overlap nightmare)
    label_positions = {
        1922: (1922, 5,        tr("出生（合肥）", "Born (Hefei)"), "left"),
        1938: (1938, 60,       tr("考入西南联大", "Enters SW Associated Univ."), "left"),
        1948: (1948, 12_000,   tr("芝加哥博士", "Chicago PhD"), "left"),
        1957: (1957, 320_000,  tr("诺贝尔奖", "Nobel Prize"), "left"),
        1965: (1965, 900_000,  tr("石溪 Einstein Professor", "Stony Brook (Einstein Prof.)"), "left"),
        1994: (1994, 9_000_000,tr("Bower 奖", "Bower Award"), "left"),
        2003: (2003, 4_500_000,tr("回清华 / 捐建高研院", "Returns to Tsinghua / endows IAS"), "right"),
        2025: (2025, 35_000_000,tr("逝世", "Death"), "right"),
    }
    for yr, (xx, yy, txt, ha) in label_positions.items():
        ax.annotate(
            txt, xy=(xx, yy),
            xytext=(8 if ha == "left" else -8, 0),
            textcoords="offset points",
            fontsize=9, color=PALETTE["ink"], ha=ha, va="center",
        )

    # Final-year value annotation
    final_low = w_low[-1]
    final_mid = w_mid[-1]
    final_hi  = w_hi[-1]
    ax.annotate(
        tr(
            f"2025 年估算区间\n约 ${final_low/1e6:.0f}M – ${final_hi/1e6:.0f}M\n中位 ${final_mid/1e6:.0f}M",
            f"2025 estimated range\n~${final_low/1e6:.0f}M – ${final_hi/1e6:.0f}M\nmedian ${final_mid/1e6:.0f}M",
        ),
        xy=(2025, final_mid),
        xytext=(-160, 40),
        textcoords="offset points",
        fontsize=10, color=PALETTE["accent_blue"], fontweight="bold",
        ha="left", va="center",
        arrowprops=dict(arrowstyle="-", color=PALETTE["accent_blue"], lw=0.8),
    )

    ax.set_yscale("log")
    ax.set_xlim(YEAR_START - 2, YEAR_END + 2)
    ax.set_ylim(1, 2e8)
    ax.yaxis.set_major_locator(LogLocator(base=10, numticks=10))
    ax.yaxis.set_major_formatter(FuncFormatter(
        lambda v, _: ("$%g" % v) if v < 1000 else (
            "$%dK" % (v / 1000) if v < 1_000_000 else "$%dM" % (v / 1_000_000)
        )
    ))
    ax.set_xlabel(tr("年份", "Year"))
    ax.set_ylabel(tr("累计净资产（2025 年美元，对数刻度）",
                     "Cumulative net worth (2025 USD, log scale)"))
    ax.set_title(tr("杨振宁估算财富轨迹（1922 – 2025）",
                    "Estimated wealth trajectory of Chen Ning Yang (1922 – 2025)"),
                 pad=14)

    ax.legend(loc="upper left", framealpha=0.9)

    add_source_note(
        fig,
        tr(
            "反事实模型：诺奖份额 + 石溪薪资节余 + 后续奖金，按 8%/10%/10.5% 年化复合到 2025 年，扣除已知大额捐赠。\n"
            "并非实测净资产，仅用于说明复利在百年尺度上的量级。",
            "Counterfactual model: Nobel share + Stony Brook salary savings + later prizes, "
            "compounded at 8% / 10% / 10.5% CAGR to 2025, net of documented major gifts.\n"
            "Not a measurement — an illustration of compounding over a century.",
        ),
    )

    save_figure(fig, "fig1_wealth_timeline")


if __name__ == "__main__":
    main()
