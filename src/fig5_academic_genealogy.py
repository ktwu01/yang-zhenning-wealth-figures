"""Figure 5: Academic genealogy converging at Yang Zhenning.

Two parallel ancestral lines (physics via Sommerfeld/Fermi, math via Dickson/Yang Wuzhi)
merge at Yang Zhenning, then branch out to his descendants.

We use a custom hierarchical layout (year on x, line on y) rather than spring
layout, so the temporal & thematic structure stays legible.
"""

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

from style import DATA_DIR, PALETTE, apply_style, save_figure, add_source_note, tr, LANG


# Edges: (parent, child). Curated from biographical sources.
EDGES = [
    # Deep root
    ("stupanus", "hoffmann"),
    ("hoffmann", "sommerfeld"),
    # Physics line
    ("sommerfeld", "born"),
    ("sommerfeld", "heisenberg"),
    ("heisenberg", "fermi"),    # not direct PhD; ideational lineage
    ("fermi", "teller"),         # Teller worked closely with Fermi
    ("fermi", "yang"),           # Fermi as key informal mentor at Chicago
    ("teller", "yang"),          # Yang's official PhD advisor
    # Math line
    ("dickson", "yang_wuzhi"),
    ("yang_wuzhi", "chen_xingshen"),
    ("yang_wuzhi", "yang"),       # father-son, intellectual transmission
    ("dickson", "yang"),          # via father's library
    # SWU mentors
    ("wu_ta_you", "yang"),
    ("wang_zhuxi", "yang"),
    ("chen_xingshen", "yang"),
    # Co-laureate
    ("yang", "lee"),
    ("lee", "yang"),
    # Descendants
    ("yang", "sutherland"),
    ("yang", "zhang_shoucheng"),
]


# Hand-tuned positions: (x_year, y_lane).
# We override the CSV `year_active` for layout so the right cluster spreads out.
POS = {
    # Root chain (deep ancestral)
    "stupanus":      (1640, 0.0),
    "hoffmann":      (1720, 0.0),
    # Physics line — top half, staggered horizontally
    "sommerfeld":    (1895, 2.3),
    "born":          (1918, 3.2),
    "heisenberg":    (1934, 2.4),
    "fermi":         (1948, 3.1),
    "teller":        (1953, 1.7),
    # Math line — bottom half
    "dickson":       (1915, -2.6),
    "yang_wuzhi":    (1935, -2.0),
    "chen_xingshen": (1948, -1.0),
    # SWU mentors — near Yang horizontally
    "wu_ta_you":     (1942, 0.9),
    "wang_zhuxi":    (1948, 0.2),
    # Yang — anchor
    "yang":          (1965, 0.0),
    "lee":           (1965, -1.5),
    # Descendants
    "sutherland":      (1990, 1.4),
    "zhang_shoucheng": (2008, -1.4),
}


def main() -> None:
    apply_style()
    df = pd.read_csv(DATA_DIR / "academic_genealogy.csv", comment="#")
    nodes = {row["id"]: row for _, row in df.iterrows()}

    G = nx.DiGraph()
    for nid, row in nodes.items():
        G.add_node(nid, **row.to_dict())
    G.add_edges_from(EDGES)

    pos = POS

    fig, ax = plt.subplots(figsize=(15, 7.5))

    # Background lane shading
    ax.axhspan( 1.2,  3.5, color=PALETTE["fill_blue"],   alpha=0.25, zorder=0)
    ax.axhspan(-3.5, -1.2, color=PALETTE["fill_orange"], alpha=0.25, zorder=0)
    ax.text(1605, 3.2,
            tr("物理线（Sommerfeld → Fermi → 杨振宁）",
               "Physics line (Sommerfeld → Fermi → Yang)"),
            fontsize=10, color=PALETTE["accent_blue"], fontweight="bold")
    ax.text(1605, -3.3,
            tr("数学/数论线（Dickson → 杨武之 → 杨振宁）",
               "Math / number-theory line (Dickson → Yang Wuzhi → Yang)"),
            fontsize=10, color=PALETTE["accent_orange"], fontweight="bold")

    # Edges
    for u, v in G.edges():
        x0, y0 = pos[u]; x1, y1 = pos[v]
        ax.annotate(
            "", xy=(x1, y1), xytext=(x0, y0),
            arrowprops=dict(
                arrowstyle="->", color=PALETTE["muted"],
                lw=0.8, alpha=0.6,
                connectionstyle="arc3,rad=0.15",
            ),
            zorder=2,
        )

    # Per-node label placement overrides (dx, dy in data coords, plus ha/va)
    LABEL_PLACEMENT = {
        "stupanus":      ( 0.0, -0.30, "center", "top"),
        "hoffmann":      ( 0.0, -0.30, "center", "top"),
        "sommerfeld":    ( 0.0,  0.32, "center", "bottom"),
        "born":          ( 0.0,  0.32, "center", "bottom"),
        "heisenberg":    ( 0.0,  0.32, "center", "bottom"),
        "fermi":         ( 0.0,  0.32, "center", "bottom"),
        "teller":        ( 0.0,  0.32, "center", "bottom"),
        "dickson":       ( 0.0, -0.32, "center", "top"),
        "yang_wuzhi":    ( 0.0, -0.32, "center", "top"),
        "chen_xingshen": ( 0.0, -0.32, "center", "top"),
        "wu_ta_you":     (-3.0,  0.0, "right", "center"),
        "wang_zhuxi":    (-3.0,  0.0, "right", "center"),
        "yang":          ( 3.0, -0.30, "left", "top"),
        "lee":           ( 0.0, -0.32, "center", "top"),
        "sutherland":    ( 0.0,  0.32, "center", "bottom"),
        "zhang_shoucheng": ( 0.0, -0.32, "center", "top"),
    }

    # Nodes
    for nid, row in nodes.items():
        x, y = pos[nid]
        is_yang = (nid == "yang")
        is_laureate = bool(row["nobel"])

        if is_yang:
            color = PALETTE["accent_red"]
            size = 340
        elif is_laureate:
            color = PALETTE["accent_purple"]
            size = 190
        else:
            color = PALETTE["accent_blue"] if row["line"] == "physics" else (
                PALETTE["accent_orange"] if row["line"] == "math" else PALETTE["muted"]
            )
            size = 130

        ax.scatter([x], [y], s=size, color=color,
                   edgecolors="white", linewidths=1.5, zorder=4)

        dx, dy, ha, va = LABEL_PLACEMENT[nid]
        weight = "bold" if is_yang else "normal"
        name_field = "name_en" if (LANG == "en" and "name_en" in row) else "name_cn"
        ax.text(x + dx, y + dy, row[name_field],
                ha=ha, va=va, fontsize=9.5,
                color=PALETTE["ink"], fontweight=weight, zorder=5)

    # Center label for Yang
    ax.annotate(
        tr("1957 年诺奖\n两条线在此交汇",
           "1957 Nobel\nthe two lines converge here"),
        xy=(1965, 0.0), xytext=(1980, 0.9),
        textcoords="data",
        fontsize=10, color=PALETTE["accent_red"], fontweight="bold",
        ha="left", va="center",
        arrowprops=dict(arrowstyle="->", color=PALETTE["accent_red"], lw=0.9),
    )

    # Legend
    legend_handles = [
        mpatches.Patch(color=PALETTE["accent_red"],    label=tr("杨振宁", "Chen Ning Yang")),
        mpatches.Patch(color=PALETTE["accent_purple"], label=tr("诺奖得主", "Nobel laureate")),
        mpatches.Patch(color=PALETTE["accent_blue"],   label=tr("物理线导师", "Physics-line mentor")),
        mpatches.Patch(color=PALETTE["accent_orange"], label=tr("数学线导师", "Math-line mentor")),
        mpatches.Patch(color=PALETTE["muted"],         label=tr("共同祖先", "Common ancestor")),
    ]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=9, framealpha=0.9)

    ax.set_xlim(1600, 2030)
    ax.set_ylim(-3.6, 3.6)
    ax.set_xlabel(tr("年份（按各位学者主要活跃年份定位）",
                     "Year (placed by each scholar's main active period)"))
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_title(
        tr("杨振宁的学术家谱：两条独立的师承链如何在他这里交汇",
           "Yang's academic genealogy: two independent mentor chains converge on one person"),
        pad=14,
    )
    ax.grid(axis="y", visible=False)

    add_source_note(
        fig,
        tr(
            "来源：Math Genealogy Project；American Physical Society 资料；Tol (2024) Scientometrics —— 727 位诺奖得主中 696 位属同一棵学术家族树。"
            " 部分关系（如 Fermi → 杨振宁）为思想传承而非正式博士导师关系。",
            "Sources: Mathematics Genealogy Project; American Physical Society records; Tol (2024) Scientometrics "
            "(696 of 727 Nobel laureates lie on a single academic family tree). "
            "Some edges (e.g. Fermi → Yang) reflect intellectual influence rather than the official PhD-advisor relation.",
        ),
    )

    save_figure(fig, "fig5_academic_genealogy")


if __name__ == "__main__":
    main()
