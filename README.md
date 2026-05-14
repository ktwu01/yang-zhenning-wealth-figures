# Yang Zhenning Wealth Figures

Configuration-driven matplotlib scripts that generate the 6 data figures accompanying the blog post:

> 《杨振宁先生到底有多少财富？》<br>
> https://ktwu01.github.io/zh/posts/2026/05/yang-zhenning-wealth-questions/

Each figure is reproducible from a CSV in `data/` plus a single Python file in `src/`. The output `output/*.png` files are regenerated on every run and are not tracked in git — run `make all` to recreate them.

## Quick start

```bash
pip install -r requirements.txt
make all        # generate all 6 figures into output/
make fig1       # or generate one at a time
```

Outputs land in `output/` as PNG (300 dpi, for embedding) and SVG (vector backup).

## The 6 figures

| # | File | What it shows |
|---|---|---|
| 1 | `fig1_wealth_timeline.py` | Yang Zhenning's estimated wealth trajectory from 1922 birth to 2025 death. Counterfactual compound-growth model: Nobel principal + Stony Brook salary deposits + later prizes, grown at 8% / 10% / 10.5% CAGR, with major charitable gifts deducted. |
| 2 | `fig2_salary_comparison.py` | 2024 USD salary ladder across 8 tiers: postdoc → assistant prof → ... → endowed chair → biotech industry → FAANG AI Research Scientist. Shows the order-of-magnitude gap between academia and AI industry. |
| 3 | `fig3_nobel_background.py` | Distribution of Nobel laureates' parental income and education percentiles vs general population (Novosad et al. 2024). Top-5% families produce ~50–60% of laureates. |
| 4 | `fig4_purchasing_power.py` | Yang's $20,177 1957 Nobel share, projected to 2025 USD under four different deflators (CPI, gold, S&P 500 total return, Shanghai real estate). Spans 130× — illustrating that deflator choice is itself a value judgment. |
| 5 | `fig5_academic_genealogy.py` | Two parallel mentorship chains (Sommerfeld → Fermi → Yang; Dickson → Yang Wuzhi → Yang) converging at Yang Zhenning, with descendants. Drawn from biographical sources; some edges (e.g., Fermi → Yang) are ideational rather than formal PhD advising relationships. |
| 6 | `fig6_lost_einsteins.py` | Recreation of the central plot from Bell, Chetty et al. 2019 *QJE*: inventor rate vs parental income percentile, with and without controlling for early math ability. ~10× gap persists after controls. |

## Repository layout

```
.
├── data/                       # CSVs with source notes in comments
├── src/
│   ├── style.py                # shared matplotlib styling
│   └── fig{1..6}_*.py          # one script per figure
├── output/                     # generated PNG + SVG (gitignored)
├── Makefile
├── requirements.txt
└── LICENSE                     # MIT
```

## Data provenance and honesty

Every CSV starts with a comment block citing the underlying source. A few important caveats:

- **Figure 1 is a model, not a measurement.** Yang Zhenning never published audited net-worth figures. The trajectory is built from public biographical anchors (salaries by tier, prize amounts, documented charitable gifts) compounded forward under three CAGR scenarios. The 2025 endpoint of $10M–$50M is a range, not a point estimate, and it represents accumulated principal minus known major gifts.
- **Figure 3** uses stylized bins consistent with the numerical findings reported by Novosad, Asher, Farquharson, and Iljazi (2024). The exact within-bin shares are illustrative; the medians (P87 income, P90 education) and top-5% share (~50–60%) are the verified takeaways.
- **Figure 4** uses CPI and gold prices that are public record. The S&P 500 multiplier (~700×) is the Shiller long-run total return; the Shanghai housing multiplier (~1500×) is directional, extrapolating from the post-1990 privatization-era price index.
- **Figure 5** is a curated subset of a large genealogy. Some links (Fermi → Yang) reflect documented intellectual influence rather than the official PhD-advisor relation (which was Edward Teller).
- **Figure 6** reproduces the qualitative shape of Bell et al. 2019. The bin-level numbers are stylized to match the published curve.

If you spot an error in a CSV or a script, please open an issue or PR.

## License

MIT — see `LICENSE`. Use the figures freely, with attribution to the blog post.
